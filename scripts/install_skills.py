#!/usr/bin/env python3
"""Install validated preview skills into explicit agent skill directories.

Offline, copy-only installer. Does not change rules, auto-load settings, accounts,
remote workers or running sessions. Use on quiescent, user-controlled trees.
Each install records file hashes in a receipt so --update can tell an unmodified
earlier install from local edits.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile
import uuid
import zipfile


AGENTS = ("hermes", "claude", "codex", "opencode", "cursor", "gemini", "antigravity", "agents")
SKILLS = ("apa7-manuscript-writing", "korean-editing")
USER_PATHS = {
    "claude": ".claude/skills", "codex": ".agents/skills",
    "opencode": ".config/opencode/skills", "cursor": ".cursor/skills",
    "gemini": ".gemini/skills", "antigravity": ".gemini/config/skills",
    "agents": ".agents/skills",
}
PROJECT_PATHS = {
    "hermes": ".hermes/skills", "claude": ".claude/skills", "codex": ".agents/skills",
    "opencode": ".opencode/skills", "cursor": ".cursor/skills",
    "gemini": ".gemini/skills", "antigravity": ".agents/skills",
    "agents": ".agents/skills",
}


class InstallError(ValueError):
    """Invalid or unsafe installation request."""


def target_root(agent, scope, *, home=None, project=None, environ=None):
    """Resolve documented paths without touching disk or guessing an agent."""
    if agent not in AGENTS or scope not in ("user", "project"):
        raise InstallError("unsupported agent or scope")
    home = Path.home() if home is None else Path(home)
    env = os.environ if environ is None else environ
    if scope == "project":
        if project is None:
            raise InstallError("project scope requires --project")
        base = Path(project).absolute()
        if not base.is_dir():
            raise InstallError("project must be an existing directory")
        return base / PROJECT_PATHS[agent]
    if agent == "hermes":
        base = Path(env.get("HERMES_HOME") or home / ".hermes").expanduser()
        if not base.is_absolute():
            raise InstallError("HERMES_HOME must be absolute")
        return base / "skills"
    return home / USER_PATHS[agent]


def reject_links(path):
    for component in (path,) + tuple(path.parents):
        if component.is_symlink():
            raise InstallError("symlinked installation paths are refused")


def inventory(root):
    """Exact file-byte map; include extras, refuse links and special files."""
    reject_links(root)
    if not root.exists():
        return None
    if not root.is_dir():
        raise InstallError("existing destination is not a directory")
    found = {}
    pending = [root]
    while pending:
        for item in sorted(pending.pop().iterdir()):
            mode = item.lstat().st_mode
            if stat.S_ISLNK(mode):
                raise InstallError("symlinked installed files are refused")
            if stat.S_ISDIR(mode):
                pending.append(item)
            elif stat.S_ISREG(mode):
                found[item.relative_to(root).as_posix()] = item.read_bytes()
            else:
                raise InstallError("nonregular installed files are refused")
    return found


def validated_payloads(repository, temporary):
    """Reuse the existing packager's metadata and link checks, then ZIP bytes."""
    spec = importlib.util.spec_from_file_location("korean_preview_packager", repository / "scripts" / "package_skills.py")
    if spec is None or spec.loader is None:
        raise InstallError("preview packager is unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        manifest = module.package_skills(repository, temporary / "packages")
    except module.PackagingError as error:
        raise InstallError("source preview validation failed: " + str(error)) from None
    result = {}
    for package in manifest["packages"]:
        name = package["skill"]
        archive = temporary / "packages" / package["artifact"]
        if hashlib.sha256(archive.read_bytes()).hexdigest() != package["sha256"]:
            raise InstallError("preview archive hash mismatch")
        files = {}
        with zipfile.ZipFile(archive) as zipped:
            if len(zipped.namelist()) != len(set(zipped.namelist())):
                raise InstallError("duplicate archive member")
            if set(zipped.namelist()) != {entry["path"] for entry in package["files"]}:
                raise InstallError("archive inventory mismatch")
            for entry in package["files"]:
                relative = Path(entry["path"])
                if relative.is_absolute() or relative.parts[0] != name or ".." in relative.parts:
                    raise InstallError("unsafe archive member")
                data = zipped.read(entry["path"])
                if len(data) != entry["size"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
                    raise InstallError("preview member hash mismatch")
                files[Path(*relative.parts[1:]).as_posix()] = data
        result[name] = files
    return result


RECEIPT_DIR = ".korean-writing-skills"


def receipt_path(dest):
    """Keep receipts beside, not inside, the discoverable skills directory."""
    return dest.parent.parent / RECEIPT_DIR / "receipts" / (dest.name + ".json")


def file_hashes(files):
    return {relative: hashlib.sha256(data).hexdigest() for relative, data in sorted(files.items())}


def read_receipt(dest):
    """Return recorded installed hashes, or None when absent or not trustworthy."""
    path = receipt_path(dest)
    reject_links(path)
    if not path.exists():
        return None
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError, RecursionError):
        return None
    if not isinstance(data, dict):
        return None
    files = data.get("files")
    if (data.get("schema_version") != 1 or data.get("skill") != dest.name
            or not isinstance(files, dict) or not files):
        return None
    for relative, value in files.items():
        if (not isinstance(relative, str) or not isinstance(value, str) or len(value) != 64
                or any(char not in "0123456789abcdef" for char in value)):
            return None
    return files


def write_receipt(dest, files, source):
    path = receipt_path(dest)
    reject_links(path)
    reject_links(path.parent)
    path.parent.mkdir(parents=True, exist_ok=True)
    body = {
        "schema_version": 1, "skill": dest.name, "source": source,
        "files": file_hashes(files),
    }
    handle, temporary = tempfile.mkstemp(prefix=".receipt-", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            json.dump(body, stream, ensure_ascii=False, indent=2, sort_keys=True)
            stream.write("\n")
        os.replace(temporary, path)
    except BaseException:
        if os.path.exists(temporary):
            os.unlink(temporary)
        raise


def source_revision(repository):
    """Best-effort Git commit for receipts; absence does not block installation."""
    head = repository / ".git"
    try:
        import subprocess
        result = subprocess.run(
            ["git", "-C", str(repository), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=False, timeout=10,
        )
    except (OSError, ValueError, subprocess.SubprocessError):
        return None
    value = result.stdout.strip()
    if result.returncode != 0 or len(value) != 40 or not head.exists():
        return None
    return value


def install(repository, agents, skills, *, scope="user", project=None, dry_run=False,
            replace=False, update=False, home=None, environ=None,
            source_revision_override=None):
    """Preflight all destinations, then install each skill with backup/readback.

    update=True touches only existing installations. It replaces an installed
    skill only when its exact files still match the receipt recorded by this
    installer, so local edits and unknown copies are preserved and reported.

    Multi-destination writes are not a transaction. A later filesystem failure
    can leave earlier successful installations; completed results are returned
    on success only. Retained backups allow manual recovery. No runtime lock is
    implied: callers must stop concurrent writers before invoking replacement.

    source_revision_override records a revision already verified by the caller
    (for example a fetched snapshot without a .git directory).
    """
    if update and replace:
        raise InstallError("--update preserves local edits; use --replace separately")
    repository = Path(repository).absolute()
    reject_links(repository)
    if not agents or any(agent not in AGENTS for agent in agents):
        raise InstallError("select at least one supported agent")
    if not skills or any(skill not in SKILLS for skill in skills):
        raise InstallError("select at least one supported skill")
    source = source_revision_override or source_revision(repository)
    with tempfile.TemporaryDirectory(prefix="korean-skill-install-") as temp:
        payloads = validated_payloads(repository, Path(temp).resolve())
        plans = {}
        baselines = {}
        for agent in agents:
            root = target_root(agent, scope, home=home, project=project, environ=environ)
            reject_links(root)
            root = root.absolute()
            for name in skills:
                dest = root / name
                resolved = dest.resolve()
                repo = repository.resolve()
                if resolved == repo or repo in resolved.parents or resolved in repo.parents:
                    raise InstallError("installation cannot overlap its source repository")
                key = str(dest)
                if key in plans:
                    if agent not in plans[key]["agents"]:
                        plans[key]["agents"].append(agent)
                    continue
                baseline = inventory(dest)
                if baseline == payloads[name]:
                    action = "unchanged"
                elif baseline is None:
                    action = "not-installed" if update else "install"
                elif update:
                    recorded = read_receipt(dest)
                    action = "replaced" if recorded == file_hashes(baseline) else "skipped-modified"
                else:
                    action = "replaced"
                    if not replace:
                        raise InstallError("different installed skill exists; inspect it, then use --replace for backup and replacement")
                baselines[key] = baseline
                plans[key] = {
                    "agent": agent, "agents": [agent], "skill": name,
                    "destination": str(dest), "action": action,
                    "files": len(payloads[name]), "backup": None,
                }
        if not dry_run:
            for key, plan in plans.items():
                dest = Path(key)
                reject_links(dest)
                if inventory(dest) != baselines[key]:
                    raise InstallError("destination changed after preflight")
                if plan["action"] in ("not-installed", "skipped-modified"):
                    continue
                if plan["action"] == "unchanged":
                    if read_receipt(dest) != file_hashes(payloads[plan["skill"]]):
                        write_receipt(dest, payloads[plan["skill"]], source)
                    continue
                reject_links(dest.parent.parent)
                dest.parent.parent.mkdir(parents=True, exist_ok=True)
                stage = Path(tempfile.mkdtemp(prefix=".korean-skill-stage-", dir=dest.parent.parent))
                backup = None
                try:
                    for relative, data in payloads[plan["skill"]].items():
                        path = stage / relative
                        path.parent.mkdir(parents=True, exist_ok=True)
                        path.write_bytes(data)
                    if inventory(stage) != payloads[plan["skill"]]:
                        raise InstallError("staged file readback mismatch")
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    reject_links(dest)
                    if inventory(dest) != baselines[key]:
                        raise InstallError("destination changed before publication")
                    if plan["action"] == "replaced":
                        backup_root = dest.parent.parent / ".korean-writing-skill-backups"
                        reject_links(backup_root)
                        backup_root.mkdir(exist_ok=True)
                        backup = backup_root / (plan["skill"] + "-" + uuid.uuid4().hex)
                        dest.rename(backup)
                        plan["backup"] = str(backup)
                    if dest.exists() or dest.is_symlink():
                        raise InstallError("destination appeared before publication")
                    stage.rename(dest)
                    if inventory(dest) != payloads[plan["skill"]]:
                        raise InstallError("installed file readback mismatch")
                except BaseException:
                    if backup is not None and backup.exists() and not dest.exists() and not dest.is_symlink():
                        backup.rename(dest)
                    raise
                finally:
                    if stage.exists():
                        shutil.rmtree(stage)
                write_receipt(dest, payloads[plan["skill"]], source)
        return {
            "status": "preview", "dry_run": dry_run, "scope": scope, "update": update,
            "source_revision": source,
            "installations": list(plans.values()),
            "notes": [
                "Skill files only; no configuration or always-on rules were changed.",
                "Shared/compatible directories can be discovered by other agents too.",
                "Check discovery in a new agent session; file hashes do not prove activation.",
            ],
        }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", action="append", choices=AGENTS, required=True, help="Repeat for multiple agents; agents is the shared .agents directory.")
    parser.add_argument("--skill", action="append", choices=SKILLS + ("all",), help="Default: korean-editing; repeat or select all for both skills.")
    parser.add_argument("--scope", choices=("user", "project"), default="user")
    parser.add_argument("--project", type=Path, help="Existing project directory; required for project scope.")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print the plan without writing agent directories.")
    parser.add_argument("--replace", action="store_true", help="Back up a different existing skill before replacing it.")
    parser.add_argument("--update", action="store_true", help="Update existing installations only; skip locally edited copies.")
    args = parser.parse_args(argv)
    if args.project is not None and args.scope != "project":
        parser.error("--project requires --scope project")
    if args.update and args.replace:
        parser.error("--update and --replace cannot be combined")
    requested = args.skill or ["korean-editing"]
    skills = list(SKILLS) if "all" in requested else list(dict.fromkeys(requested))
    try:
        result = install(Path(__file__).resolve().parents[1], args.agent, skills,
                         scope=args.scope, project=args.project, dry_run=args.dry_run,
                         replace=args.replace, update=args.update)
    except (InstallError, OSError, UnicodeError, ValueError):
        print("skill installation failed; check source, destination, links and --replace requirements", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if any(item["action"] == "skipped-modified" for item in result["installations"]):
        print("some installations have local edits and were not updated; inspect them, then use --replace", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
