"""Offline integration tests: never contact the official upstream."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/auto_update_skills.py'


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AutoUpdateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='updater-test-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.repo = self.base / 'upstream'
        self.repo.mkdir()
        shutil.copytree(ROOT / 'skills', self.repo / 'skills')
        self.git('init', '-b', 'main')
        self.git('add', '.')
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'initial')
        self.home = self.base / 'home'
        self.home.mkdir()
        self.cache = self.base / 'cache'
        self.installer = load(ROOT / 'scripts/install_skills.py', 'fixture_installer')
        self.installer.install(ROOT, ['claude', 'cursor'], ['korean-editing'], home=self.home, environ={})
        self.mod = load(SCRIPT, 'auto_updater')

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.repo), *args], stderr=subprocess.DEVNULL).decode().strip()

    def newer(self):
        path = self.repo / 'skills/korean-editing/SKILL.md'
        path.write_text(path.read_text() + '\n새 버전 문장.\n')
        self.git('add', '.')
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'new')
        return self.git('rev-parse', 'HEAD')

    def run_update(self, **kwargs):
        return self.mod.update_once(['claude', 'cursor', 'gemini'], home=self.home, environ={}, cache_dir=self.cache, source_url=str(self.repo), **kwargs)

    def test_new_commit_and_modified_install_preserved(self):
        revision = self.newer()
        edited = self.home / '.cursor/skills/korean-editing/SKILL.md'
        edited.write_text(edited.read_text() + '\nLocal edit\n')
        report = self.run_update()
        self.assertEqual(report['source_revision'], revision)
        self.assertEqual([x['action'] for x in report['installations']], ['replaced', 'skipped-modified', 'not-installed'])
        self.assertIn('Local edit', edited.read_text())
        self.assertIn('새 버전', (self.home / '.claude/skills/korean-editing/SKILL.md').read_text())
        self.assertFalse((self.home / '.gemini').exists())
        receipt = self.home / '.claude/.korean-writing-skills/receipts/korean-editing.json'
        self.assertEqual(json.loads(receipt.read_text())['source'], revision)
        self.assertEqual(list(self.cache.iterdir()), [])

    def test_fetched_python_is_never_executed(self):
        scripts = self.repo / 'scripts'
        scripts.mkdir()
        (scripts / 'package_skills.py').write_text("raise RuntimeError('fetched code ran')")
        self.git('add', '.')
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'untrusted script')
        self.assertEqual(self.run_update()['status'], 'ok')

    def test_symlink_destination_refused(self):
        dest = self.home / '.claude/skills/korean-editing/SKILL.md'
        dest.unlink()
        private = self.base / 'private.md'
        private.write_text('preserve')
        dest.symlink_to(private)
        with self.assertRaises(self.mod.UpdateError):
            self.run_update()
        self.assertEqual(private.read_text(), 'preserve')

    def test_dry_run(self):
        self.newer()
        dest = self.home / '.claude/skills/korean-editing/SKILL.md'
        before = dest.read_bytes()
        report = self.run_update(dry_run=True)
        self.assertTrue(report['dry_run'])
        self.assertEqual(dest.read_bytes(), before)

    def test_unsafe_upstream_symlink(self):
        (self.repo / 'skills/korean-editing/unsafe.md').symlink_to('/etc/passwd')
        self.git('add', '.')
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'link')
        with self.assertRaises(self.mod.UpdateError):
            self.run_update()
        self.assertEqual(list(self.cache.iterdir()), [])

    def test_failed_fetch(self):
        shutil.rmtree(self.repo)
        with self.assertRaises(self.mod.UpdateError):
            self.run_update()
        self.assertEqual(list(self.cache.iterdir()), [])

    def test_invalid_interval_and_arbitrary_source_cli(self):
        for args in (['--interval-seconds', '59'], ['--repository', 'secret'], ['--ref', 'other']):
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as caught:
                self.mod.main(['--agent', 'claude', *args])
            self.assertEqual(caught.exception.code, 2)

    def test_watch_retries_and_is_foreground(self):
        out, err = io.StringIO(), io.StringIO()
        with patch.object(self.mod, 'update_once', side_effect=[self.mod.UpdateError('fetch failed'), {'installations': []}]) as cycle, patch.object(self.mod.time, 'sleep', side_effect=[None, KeyboardInterrupt]) as sleep, contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            self.assertEqual(self.mod.main(['--agent', 'claude', '--watch', '--interval-seconds', '60']), 130)
        self.assertEqual(cycle.call_count, 2)
        self.assertEqual(sleep.call_count, 2)
        self.assertEqual([json.loads(line)['status'] for line in out.getvalue().splitlines()], ['error', 'ok'])
        self.assertIn('failed', err.getvalue())

    def test_lock_excludes_second_cycle(self):
        self.cache.mkdir()
        (self.cache / 'update.lock').write_text('occupied')
        with self.assertRaises(self.mod.UpdateError):
            self.run_update()
        self.assertEqual((self.cache / 'update.lock').read_text(), 'occupied')


if __name__ == '__main__':
    unittest.main()
