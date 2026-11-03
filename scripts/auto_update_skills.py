#!/usr/bin/env python3
"""Opt-in foreground updater for existing, receipt-tracked skill installations.

CLI always fetches official main. --watch stays in the foreground; it does not
install a scheduler or alter any agent configuration. Stop concurrent local
writers before updating. A leftover update.lock after an uncatchable kill must
be inspected and removed manually, never automatically stolen.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import importlib.util
import io
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import signal
import subprocess
import sys
import tarfile
import tempfile
import time

OFFICIAL_URL = 'https://github.com/ContextualWisdomLab/korean-writing-skills.git'
BRANCH = 'refs/heads/main'
GIT_TIMEOUT = 90
LOCAL_SCRIPTS = Path(__file__).resolve().parent


def _installer():
    spec = importlib.util.spec_from_file_location('local_skill_installer', LOCAL_SCRIPTS / 'install_skills.py')
    if spec is None or spec.loader is None:
        raise UpdateError('local installer unavailable')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class UpdateError(ValueError):
    """Sanitized cycle failure; never includes Git stderr or credentials."""


def _git(args, *, cwd, network=False, allow_file=False):
    # Ignore global/system config, credential helpers, URL rewrites, prompts,
    # hooks and environment-injected Git config. No shell, checkout or worktree.
    env = {key: value for key, value in os.environ.items()
           if not key.startswith('GIT_') and key not in ('SSH_ASKPASS',)}
    env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
               GIT_TERMINAL_PROMPT='0', GIT_ASKPASS='/usr/bin/false')
    command = ['git', '-c', 'credential.helper=', '-c', 'core.hooksPath=/dev/null',
               '-c', 'protocol.allow=never', '-c', 'protocol.https.allow=always',
               '-c', 'protocol.file.allow=' + ('always' if allow_file else 'never'),
               '-c', 'http.followRedirects=false', '-c', 'http.lowSpeedLimit=1',
               '-c', 'http.lowSpeedTime=30', *args]
    try:
        with subprocess.Popen(command, cwd=cwd, env=env, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, start_new_session=True) as process:
            try:
                output, _ = process.communicate(timeout=GIT_TIMEOUT if network else 30)
            finally:
                # Git may spawn an HTTPS helper; kill the whole owned group,
                # including on timeout, Ctrl-C and SIGTERM, then reap git.
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except (ProcessLookupError, PermissionError):
                    pass
                process.wait()
            returncode = process.returncode
    except (OSError, subprocess.SubprocessError):
        raise UpdateError('git fetch failed or timed out' if network else 'git snapshot failed') from None
    if returncode:
        raise UpdateError('git fetch failed' if network else 'git snapshot failed')
    return output


@contextmanager
def _cache_lock(cache, installer):
    installer.reject_links(cache)
    cache.mkdir(parents=True, exist_ok=True)
    lock = cache / 'update.lock'
    try:
        descriptor = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        raise UpdateError('another update holds the cache lock') from None
    try:
        os.close(descriptor)
        yield
    finally:
        lock.unlink()


def _snapshot(repository, snapshot, installer):
    revision = _git(['rev-parse', '--verify', 'FETCH_HEAD^{commit}'], cwd=repository).decode('ascii').strip()
    if len(revision) not in (40, 64) or any(c not in '0123456789abcdef' for c in revision):
        raise UpdateError('invalid upstream revision')
    archive = _git(['archive', '--format=tar', revision, '--', *['skills/' + name for name in installer.SKILLS]], cwd=repository)
    snapshot.mkdir()
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:') as tar:
        for member in tar:
            relative = PurePosixPath(member.name)
            if (relative.is_absolute() or '..' in relative.parts or len(relative.parts) < 2
                    or relative.parts[0] != 'skills' or relative.parts[1] not in installer.SKILLS):
                # git archive emits the common skills/ directory too.
                if member.isdir() and member.name.rstrip('/') == 'skills':
                    continue
                raise UpdateError('unsafe upstream path')
            if member.isdir():
                continue
            if not member.isfile():
                raise UpdateError('unsafe upstream link or special file')
            if relative.suffix != '.md':
                continue
            destination = snapshot.joinpath(*relative.parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            stream = tar.extractfile(member)
            if stream is None:
                raise UpdateError('unreadable upstream document')
            destination.write_bytes(stream.read())
    (snapshot / 'scripts').mkdir()
    # Never load fetched Python: the installer expects this trusted local file.
    shutil.copyfile(LOCAL_SCRIPTS / 'package_skills.py', snapshot / 'scripts/package_skills.py')
    return revision


def update_once(agents, skills=None, *, scope='user', project=None, dry_run=False,
                home=None, environ=None, cache_dir=None, source_url=OFFICIAL_URL):
    """One locked cycle; source_url is an offline-test seam, not a CLI option.

    Only official main is supported in production. Temporary bare objects and
    Markdown snapshots are deleted on success and failure. No worktrees exist.
    """
    installer = _installer()
    env = os.environ if environ is None else environ
    home = Path.home() if home is None else Path(home)
    base = Path(env.get('XDG_CACHE_HOME') or home / '.cache')
    cache = Path(cache_dir) if cache_dir is not None else base / 'korean-writing-skills'
    if not cache.is_absolute():
        raise UpdateError('cache path must be absolute')
    skills = ['korean-editing'] if skills is None else skills
    # Reject invalid destinations before network activity.
    try:
        if not agents or any(a not in installer.AGENTS for a in agents):
            raise UpdateError('unsupported agent')
        if not skills or any(s not in installer.SKILLS for s in skills):
            raise UpdateError('unsupported skill')
        for agent in agents:
            installer.reject_links(installer.target_root(agent, scope, home=home, project=project, environ=env))
        with _cache_lock(cache, installer):
            with tempfile.TemporaryDirectory(prefix='cycle-', dir=cache) as temporary:
                directory = Path(temporary)
                bare = directory / 'objects.git'
                _git(['init', '--bare', str(bare)], cwd=directory)
                _git(['fetch', '--no-tags', '--depth=1', '--', source_url, BRANCH], cwd=bare,
                     network=True, allow_file=source_url != OFFICIAL_URL)
                snapshot = directory / 'snapshot'
                revision = _snapshot(bare, snapshot, installer)
                report = installer.install(snapshot, agents, skills, scope=scope,
                    project=project, dry_run=dry_run, update=True, home=home, environ=env,
                    source_revision_override=revision)
                report['upstream'] = OFFICIAL_URL
                report['source_revision'] = revision
                report['status'] = 'partial' if any(i['action'] == 'skipped-modified' for i in report['installations']) else 'ok'
                return report
    except UpdateError:
        raise
    except (installer.InstallError, OSError, UnicodeError, ValueError, RecursionError, tarfile.TarError):
        raise UpdateError('update validation or destination check failed') from None


def _interval(value):
    try:
        seconds = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError('interval must be an integer') from None
    if seconds < 60:
        raise argparse.ArgumentTypeError('interval must be at least 60 seconds')
    return seconds


def main(argv=None):
    installer = _installer()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--agent', choices=installer.AGENTS, action='append', required=True)
    parser.add_argument('--skill', choices=installer.SKILLS + ('all',), action='append')
    parser.add_argument('--scope', choices=('user', 'project'), default='user')
    parser.add_argument('--project', type=Path)
    parser.add_argument('--dry-run', action='store_true')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--once', action='store_true', help='One cycle (default).')
    mode.add_argument('--watch', action='store_true', help='Explicit foreground periodic loop.')
    parser.add_argument('--interval-seconds', type=_interval, default=86400)
    args = parser.parse_args(argv)
    if (args.project is None) != (args.scope == 'user'):
        parser.error('--project is required only for --scope project')
    requested = args.skill or ['korean-editing']
    skills = list(installer.SKILLS) if 'all' in requested else list(dict.fromkeys(requested))

    def stop(signum, frame):
        raise KeyboardInterrupt
    # SIGTERM unwinds like Ctrl-C: _git kills its process group and the
    # lock/temporary directory context managers clean up.
    previous = signal.signal(signal.SIGTERM, stop)
    try:
        while True:
            try:
                report = update_once(args.agent, skills, scope=args.scope, project=args.project, dry_run=args.dry_run)
                report.setdefault('status', 'ok')
                code = 1 if report['status'] != 'ok' else 0
                if code:
                    print('locally modified installations skipped', file=sys.stderr, flush=True)
            except UpdateError as error:
                report = {'status': 'error', 'error': str(error)}
                print('skill update failed: ' + str(error), file=sys.stderr, flush=True)
                code = 1
            print(json.dumps(report, ensure_ascii=False, sort_keys=True), flush=True)
            if not args.watch:
                return code
            time.sleep(args.interval_seconds)
    except KeyboardInterrupt:
        return 130
    finally:
        signal.signal(signal.SIGTERM, previous)


if __name__ == '__main__':
    raise SystemExit(main())
