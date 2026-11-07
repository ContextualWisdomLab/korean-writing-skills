#!/usr/bin/env python3
"""Offline tests for agent-specific skill installation."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "install_skills.py"


def digest(path: Path) -> dict[str, str]:
    return {
        item.relative_to(path).as_posix(): hashlib.sha256(item.read_bytes()).hexdigest()
        for item in sorted(path.rglob("*")) if item.is_file()
    }


class InstallSkillsTests(unittest.TestCase):
    def setUp(self):
        scratch = Path.home() / ".hermes" / "cache" / "scratch"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="install-skills-", dir=scratch)
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.home = self.base / "home"
        self.project = self.base / "project"
        self.home.mkdir()
        self.project.mkdir()

    def module(self):
        self.assertTrue(SCRIPT.is_file(), "agent installer is not implemented")
        spec = importlib.util.spec_from_file_location("install_skills", SCRIPT)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def run_cli(self, *args, env=None):
        merged = dict(os.environ, HOME=str(self.home))
        merged.pop("HERMES_HOME", None)
        merged.pop("CODEX_HOME", None)
        if env:
            merged.update(env)
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args], cwd=ROOT, env=merged,
            text=True, capture_output=True, check=False,
        )

    def test_user_targets_follow_agent_specific_paths(self):
        module = self.module()
        expected = {
            "hermes": self.home / ".hermes" / "skills",
            "claude": self.home / ".claude" / "skills",
            "codex": self.home / ".agents" / "skills",
            "opencode": self.home / ".config" / "opencode" / "skills",
            "cursor": self.home / ".cursor" / "skills",
            "gemini": self.home / ".gemini" / "skills",
            "antigravity": self.home / ".gemini" / "config" / "skills",
            "agents": self.home / ".agents" / "skills",
        }
        for agent, path in expected.items():
            with self.subTest(agent=agent):
                self.assertEqual(module.target_root(agent, "user", home=self.home, environ={}), path)

    def test_project_targets_follow_agent_specific_paths(self):
        module = self.module()
        expected = {
            "hermes": ".hermes/skills", "claude": ".claude/skills", "codex": ".agents/skills",
            "opencode": ".opencode/skills", "cursor": ".cursor/skills",
            "gemini": ".gemini/skills", "antigravity": ".agents/skills",
            "agents": ".agents/skills",
        }
        for agent, relative in expected.items():
            with self.subTest(agent=agent):
                self.assertEqual(
                    module.target_root(agent, "project", home=self.home, project=self.project, environ={}),
                    self.project / relative,
                )
        with self.assertRaises(module.InstallError):
            module.target_root("claude", "project", home=self.home, project=None, environ={})

    def test_hermes_home_is_respected(self):
        module = self.module()
        profile = self.base / "profile"
        self.assertEqual(module.target_root("hermes", "user", home=self.home, environ={"HERMES_HOME": str(profile)}), profile / "skills")

    def test_dry_run_reports_plan_without_writing(self):
        result = self.run_cli("--agent", "claude", "--agent", "codex", "--skill", "korean-editing", "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        plan = json.loads(result.stdout)
        self.assertEqual([item["agent"] for item in plan["installations"]], ["claude", "codex"])
        self.assertTrue(all(item["action"] == "install" for item in plan["installations"]))
        self.assertFalse((self.home / ".claude").exists())
        self.assertFalse((self.home / ".agents").exists())

    def test_install_copies_complete_skill_and_is_idempotent(self):
        first = self.run_cli("--agent", "claude", "--skill", "korean-editing")
        self.assertEqual(first.returncode, 0, first.stderr)
        installed = self.home / ".claude" / "skills" / "korean-editing"
        self.assertEqual(digest(installed), digest(ROOT / "skills" / "korean-editing"))
        second = self.run_cli("--agent", "claude", "--skill", "korean-editing")
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(json.loads(second.stdout)["installations"][0]["action"], "unchanged")

    def test_different_existing_skill_requires_explicit_replace_and_backs_up(self):
        installed = self.home / ".cursor" / "skills" / "korean-editing"
        installed.mkdir(parents=True)
        (installed / "SKILL.md").write_text("local customization\n", encoding="utf-8")
        refused = self.run_cli("--agent", "cursor", "--skill", "korean-editing")
        self.assertEqual(refused.returncode, 1)
        self.assertEqual((installed / "SKILL.md").read_text(encoding="utf-8"), "local customization\n")
        replaced = self.run_cli("--agent", "cursor", "--skill", "korean-editing", "--replace")
        self.assertEqual(replaced.returncode, 0, replaced.stderr)
        report = json.loads(replaced.stdout)["installations"][0]
        self.assertEqual(report["action"], "replaced")
        backup = Path(report["backup"])
        self.assertEqual((backup / "SKILL.md").read_text(encoding="utf-8"), "local customization\n")
        self.assertNotEqual(backup.parent, installed.parent, "backups must not become discoverable skills")
        self.assertEqual(digest(installed), digest(ROOT / "skills" / "korean-editing"))

    def test_symlinked_destination_is_refused(self):
        real = self.base / "real-skills"
        real.mkdir()
        (self.home / ".claude").mkdir()
        (self.home / ".claude" / "skills").symlink_to(real, target_is_directory=True)
        result = self.run_cli("--agent", "claude", "--skill", "korean-editing")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(list(real.iterdir()), [])

    def test_shared_agents_path_is_installed_once(self):
        result = self.run_cli("--agent", "codex", "--agent", "agents", "--skill", "korean-editing", "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        plan = json.loads(result.stdout)["installations"]
        self.assertEqual(len(plan), 1)
        self.assertEqual(plan[0]["agents"], ["codex", "agents"])

    def test_all_installs_both_skills_for_named_agent(self):
        result = self.run_cli("--agent", "opencode", "--skill", "all", "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        skills = [item["skill"] for item in json.loads(result.stdout)["installations"]]
        self.assertEqual(skills, ["apa7-manuscript-writing", "korean-editing"])

    def test_real_copy_for_every_agent_and_scope(self):
        module = self.module()
        for scope in ("user", "project"):
            for agent in module.AGENTS:
                with self.subTest(scope=scope, agent=agent):
                    args = ["--agent", agent, "--skill", "all", "--scope", scope]
                    if scope == "project":
                        args.extend(["--project", str(self.project)])
                    result = self.run_cli(*args)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    plan = json.loads(result.stdout)["installations"]
                    self.assertEqual(len(plan), 2)
                    for item in plan:
                        self.assertEqual(digest(Path(item["destination"])), digest(ROOT / "skills" / item["skill"]))

    def test_preflight_conflict_does_not_install_earlier_agent(self):
        occupied = self.home / ".cursor" / "skills" / "korean-editing"
        occupied.mkdir(parents=True)
        (occupied / "SKILL.md").write_text("keep this", encoding="utf-8")
        result = self.run_cli("--agent", "claude", "--agent", "cursor")
        self.assertEqual(result.returncode, 1)
        self.assertFalse((self.home / ".claude").exists())
        self.assertEqual((occupied / "SKILL.md").read_text(encoding="utf-8"), "keep this")

    def test_hermes_relative_home_is_rejected(self):
        result = self.run_cli("--agent", "hermes", env={"HERMES_HOME": "relative"})
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("Traceback", result.stderr)

    def test_source_overlap_is_rejected_without_writing(self):
        result = self.run_cli("--agent", "hermes", "--scope", "project", "--project", str(ROOT))
        self.assertEqual(result.returncode, 1)
        self.assertFalse((ROOT / ".hermes").exists())

    def test_symlink_within_existing_skill_is_refused_even_with_replace(self):
        installed = self.home / ".claude" / "skills" / "korean-editing"
        installed.mkdir(parents=True)
        target = self.base / "private.md"
        target.write_text("preserve", encoding="utf-8")
        (installed / "SKILL.md").symlink_to(target)
        result = self.run_cli("--agent", "claude", "--replace")
        self.assertEqual(result.returncode, 1)
        self.assertTrue((installed / "SKILL.md").is_symlink())
        self.assertEqual(target.read_text(encoding="utf-8"), "preserve")

    def receipt(self, agent_dir, skill="korean-editing"):
        return self.home / agent_dir / ".korean-writing-skills" / "receipts" / (skill + ".json")

    def old_install(self, agent_dir, text="old version\n", receipt=True):
        installed = self.home / agent_dir / "skills" / "korean-editing"
        installed.mkdir(parents=True)
        (installed / "SKILL.md").write_text(text, encoding="utf-8")
        if receipt:
            path = self.receipt(agent_dir)
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps({
                "schema_version": 1, "skill": "korean-editing",
                "files": {"SKILL.md": hashlib.sha256(text.encode()).hexdigest()},
            }), encoding="utf-8")
        return installed

    def test_install_records_receipt_of_installed_hashes(self):
        result = self.run_cli("--agent", "claude")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(self.receipt(".claude").read_text(encoding="utf-8"))
        self.assertEqual(data["skill"], "korean-editing")
        self.assertEqual(data["files"], digest(ROOT / "skills" / "korean-editing"))

    def test_update_replaces_unmodified_previous_install(self):
        installed = self.old_install(".claude")
        result = self.run_cli("--agent", "claude", "--update")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)["installations"][0]
        self.assertEqual(report["action"], "replaced")
        self.assertEqual((Path(report["backup"]) / "SKILL.md").read_text(encoding="utf-8"), "old version\n")
        self.assertEqual(digest(installed), digest(ROOT / "skills" / "korean-editing"))
        receipt = json.loads(self.receipt(".claude").read_text(encoding="utf-8"))
        self.assertEqual(receipt["files"], digest(ROOT / "skills" / "korean-editing"))

    def test_update_keeps_local_edits_and_updates_other_agents(self):
        edited = self.old_install(".cursor")
        (edited / "SKILL.md").write_text("old version\nlocal note\n", encoding="utf-8")
        clean = self.old_install(".claude")
        result = self.run_cli("--agent", "cursor", "--agent", "claude", "--update")
        self.assertEqual(result.returncode, 1)
        actions = {item["agent"]: item["action"] for item in json.loads(result.stdout)["installations"]}
        self.assertEqual(actions, {"cursor": "skipped-modified", "claude": "replaced"})
        self.assertEqual((edited / "SKILL.md").read_text(encoding="utf-8"), "old version\nlocal note\n")
        self.assertEqual(digest(clean), digest(ROOT / "skills" / "korean-editing"))

    def test_update_without_receipt_does_not_replace_different_skill(self):
        installed = self.old_install(".claude", receipt=False)
        result = self.run_cli("--agent", "claude", "--update")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["installations"][0]["action"], "skipped-modified")
        self.assertEqual((installed / "SKILL.md").read_text(encoding="utf-8"), "old version\n")

    def test_update_skips_agents_without_installation(self):
        result = self.run_cli("--agent", "gemini", "--update")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["installations"][0]["action"], "not-installed")
        self.assertFalse((self.home / ".gemini").exists())

    def test_identical_install_without_receipt_is_adopted(self):
        installed = self.home / ".claude" / "skills" / "korean-editing"
        installed.parent.mkdir(parents=True)
        import shutil
        shutil.copytree(ROOT / "skills" / "korean-editing", installed)
        result = self.run_cli("--agent", "claude", "--update")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["installations"][0]["action"], "unchanged")
        self.assertTrue(self.receipt(".claude").is_file())

    def test_update_malformed_receipt_preserves_installation(self):
        installed = self.old_install(".claude")
        self.receipt(".claude").write_text("[]", encoding="utf-8")
        result = self.run_cli("--agent", "claude", "--update")
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(json.loads(result.stdout)["installations"][0]["action"], "skipped-modified")
        self.assertEqual((installed / "SKILL.md").read_text(encoding="utf-8"), "old version\n")

    def test_update_deeply_nested_receipt_is_treated_as_modified(self):
        installed = self.old_install(".claude")
        self.receipt(".claude").write_text("[" * 200000, encoding="utf-8")
        result = self.run_cli("--agent", "claude", "--update")
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(json.loads(result.stdout)["installations"][0]["action"], "skipped-modified")
        self.assertEqual((installed / "SKILL.md").read_text(encoding="utf-8"), "old version\n")

    def test_update_dry_run_writes_nothing(self):
        installed = self.old_install(".claude")
        before = self.receipt(".claude").read_bytes()
        result = self.run_cli("--agent", "claude", "--update", "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["installations"][0]["action"], "replaced")
        self.assertEqual((installed / "SKILL.md").read_text(encoding="utf-8"), "old version\n")
        self.assertEqual(self.receipt(".claude").read_bytes(), before)

    def test_invalid_agent_fails_without_traceback(self):
        result = self.run_cli("--agent", "unknown", "--skill", "korean-editing")
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
