#!/usr/bin/env python3
"""Offline acceptance tests for the dependency-locked preview packager."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPOSITORY_ROOT / "scripts" / "package_skills.py"
NAMES = ("korean-editing", "apa7-manuscript-writing")
REFERENCES = {
    "korean-editing": ("examples.md", "source-ledger.md", "validation.md"),
    "apa7-manuscript-writing": (
        "document-format-checklist.md", "jars-quant-table1.md",
        "reporting-workflow.md", "source-ledger.md", "validation.md",
        "verified-scope.md",
    ),
}


class PackageSkillsTests(unittest.TestCase):
    def setUp(self):
        scratch = Path.home() / ".hermes" / "cache" / "scratch"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="package-test-", dir=scratch)
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / "repository"
        for name in NAMES:
            skill = self.root / "skills" / name
            (skill / "references").mkdir(parents=True)
            links = "\n".join(
                "[reference](references/{})".format(filename)
                for filename in REFERENCES[name]
            )
            (skill / "SKILL.md").write_text(
                "---\nname: {}\ndescription: Preview fixture.\n---\n\n{}\n".format(name, links),
                encoding="utf-8",
            )
            for filename in REFERENCES[name]:
                (skill / "references" / filename).write_text("# 합성 근거\n", encoding="utf-8")
        self.output = self.base / "output"

    def module(self):
        self.assertTrue(SCRIPT.is_file(), "preview packager is not implemented")
        spec = importlib.util.spec_from_file_location("package_skills", SCRIPT)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertTrue(hasattr(module, "PackagingError"), "fail-closed validation is missing")
        return module

    def test_packages_only_allowlisted_markdown_with_verified_manifest(self):
        (self.root / "private.md").write_text("not shipped", encoding="utf-8")
        (self.root / "skills" / "other").mkdir()
        (self.root / "skills" / "other" / "SKILL.md").write_text("not shipped", encoding="utf-8")
        (self.root / "skills" / NAMES[0] / "secret.json").write_text("not shipped", encoding="utf-8")
        manifest = self.module().package_skills(self.root, self.output)
        self.assertEqual(manifest, json.loads((self.output / "manifest.json").read_text(encoding="utf-8")))
        self.assertEqual(manifest["status"], "preview")
        self.assertIn("not an official release", manifest["limitations"])
        self.assertIn("not APA 7 certification", manifest["limitations"])
        self.assertEqual([item["skill"] for item in manifest["packages"]], sorted(NAMES))
        self.assertEqual(
            {path.name for path in self.output.iterdir()},
            {"manifest.json"} | {name + "-preview.zip" for name in NAMES},
        )
        for package in manifest["packages"]:
            archive = self.output / package["artifact"]
            self.assertEqual(package["sha256"], hashlib.sha256(archive.read_bytes()).hexdigest())
            with zipfile.ZipFile(archive) as zipped:
                expected = sorted(
                    [package["skill"] + "/SKILL.md"] +
                    [package["skill"] + "/references/" + filename for filename in REFERENCES[package["skill"]]]
                )
                self.assertEqual(zipped.namelist(), expected)
                self.assertEqual([entry["path"] for entry in package["files"]], expected)
                for entry in package["files"]:
                    data = zipped.read(entry["path"])
                    self.assertEqual(entry["sha256"], hashlib.sha256(data).hexdigest())
                    self.assertEqual(entry["size"], len(data))
                    self.assertEqual(data, (self.root / "skills" / entry["path"]).read_bytes())
                for info in zipped.infolist():
                    self.assertEqual(info.date_time, (1980, 1, 1, 0, 0, 0))
                    self.assertEqual(info.create_system, 3)
                    self.assertEqual(info.external_attr >> 16, 0o100644)
                    self.assertEqual(info.compress_type, zipfile.ZIP_STORED)
                    self.assertEqual(info.extra, b"")
                    self.assertEqual(info.comment, b"")
    def assert_rejected(self):
        module = self.module()
        with self.assertRaises(module.PackagingError):
            module.package_skills(self.root, self.output)
        self.assertFalse(self.output.exists(), "validation must finish before any output")

    def test_missing_evidence_in_either_skill_is_fail_closed(self):
        module = self.module()
        for name in NAMES:
            for filename in REFERENCES[name]:
                with self.subTest(skill=name, evidence=filename):
                    path = self.root / "skills" / name / "references" / filename
                    data = path.read_bytes()
                    path.unlink()
                    with self.assertRaises(module.PackagingError):
                        module.package_skills(self.root, self.output)
                    self.assertFalse(self.output.exists())
                    path.write_bytes(data)

    def test_missing_skill_document_is_fail_closed(self):
        (self.root / "skills" / NAMES[1] / "SKILL.md").unlink()
        self.assert_rejected()

    def test_invalid_frontmatter_is_fail_closed(self):
        for text in ("# no frontmatter", "---\nname: wrong\n---\nbody", "---\nname: korean-editing\n---\nbody"):
            with self.subTest(text=text):
                (self.root / "skills" / NAMES[0] / "SKILL.md").write_text(text, encoding="utf-8")
                self.assert_rejected()
    def test_malicious_or_missing_links_are_fail_closed(self):
        document = self.root / "skills" / NAMES[1] / "references" / "source-ledger.md"
        payloads = (
            "[bad](../../outside.md)", "[bad](%2e%2e/%2e%2e/outside.md)",
            "[bad](%252e%252e/outside.md)", "[bad](/outside.md)",
            "[bad](file:///outside.md)", "[bad](javascript:alert(1))",
            "[bad](data:text/plain,bad)", "[bad](//example.invalid/a)",
            "[bad](C:/outside.md)", "[bad](..\\outside.md)",
            "[bad](missing.md)", "[bad](secret.json)",
            "[bad](<../../outside.md>)", "![bad](../../outside.md)",
            "[bad][evidence]\n[evidence]: ../../outside.md",
            "[bad][]\n[bad]: missing.md", "[bad][undefined]",
            '<a href="../../outside.md">bad</a>',
            '<img src="file:///outside.md">',
            "<file:///outside.md>",
            "[nested [label]](../../outside.md)",
            '[nested [deeper [label]]](../../outside.md)',
            '<img srcset="../../outside.md 1x">',
            "[bad](missing.md?download=1#scope)",
            "[multiline\nlabel](../../outside.md)",
        )
        for index, text in enumerate(payloads):
            with self.subTest(payload=text):
                self.output = self.base / ("denied-" + str(index))
                document.write_text(text, encoding="utf-8")
                self.assert_rejected()

    def test_code_span_and_html_label_destinations_are_fail_closed(self):
        document = self.root / "skills" / NAMES[0] / "references" / "validation.md"
        templates = (
            "[bad `]` label]({target})",
            "[bad <span title=']'>label</span>]({target})",
        )
        for index, template in enumerate(templates):
            for target in ("../../outside.md", "file:///outside.md", "javascript:alert(1)"):
                with self.subTest(variant=index, target=target):
                    document.write_text(template.format(target=target), encoding="utf-8")
                    self.output = self.base / ("precedence-denied-" + str(index) + "-" + target.split(":", 1)[0].replace("/", "_"))
                    self.assert_rejected()

    def test_rendered_label_precedence_has_collected_safe_archive_bytes(self):
        from markdown_it import MarkdownIt
        module = self.module()
        document = self.root / "skills" / NAMES[0] / "references" / "validation.md"
        templates = (
            "[good `]` label]({target})",
            "[good <span title=']'>label</span>]({target})",
            r"[good\]label]({target})",
            r"[good\[label]({target})",
            "[good]\n\n> [good]: {target}",
            "[good]\n\n- [good]: {target}",
            "[good label]\n\n[good\nlabel]: {target}",
            "[good]\n\n> [good]: {target}",
        )
        reference = MarkdownIt("commonmark", {"html": True})
        reference.validateLink = lambda target: True
        for index, template in enumerate(templates):
            safe = template.format(target="source-ledger.md")
            with self.subTest(variant=index):
                rendered = reference.render(safe)
                self.assertIn('href="source-ledger.md"', rendered)
                collector = module._HTMLLinks()
                collector.feed(rendered)
                collector.close()
                self.assertEqual(set(collector.targets), {"source-ledger.md"})
                self.assertEqual(set(module._link_targets(safe)), set(collector.targets))
                document.write_text(safe, encoding="utf-8")
                output = self.base / ("precedence-safe-" + str(index))
                module.package_skills(self.root, output)
                with zipfile.ZipFile(output / (NAMES[0] + "-preview.zip")) as archive:
                    self.assertEqual(archive.read(NAMES[0] + "/references/validation.md"), safe.encode("utf-8"))

    def test_conservative_code_examples_and_unsafe_html_are_fail_closed(self):
        document = self.root / "skills" / NAMES[0] / "references" / "validation.md"
        payloads = (
            "`[bad](../../outside.md)`",
            "```md\n[bad](../../outside.md)\n```",
            "    [bad](file:///outside.md)\n",
            "```md\n[bad](source-ledger.md\n```",
            "`[bad][undefined]`",
            '<script src="https://example.invalid/code.js"></script>',
            '<span onclick="alert(1)">label</span>',
            '<span style="background:url(../../outside.md)">label</span>',
            '<a href="source-ledger.md" ping="../../outside.md">label</a>',
            '<button formaction="../../outside.md">label</button>',
            '<iframe srcdoc="&lt;img src=../../outside.md&gt;"></iframe>',
            '<svg><a xlink:href="../../outside.md">label</a></svg>',
        )
        for index, text in enumerate(payloads):
            with self.subTest(payload=text):
                document.write_text(text, encoding="utf-8")
                self.output = self.base / ("policy-denied-" + str(index))
                self.assert_rejected()

    def test_unused_duplicate_and_undefined_reference_admission_policy(self):
        document = self.root / "skills" / NAMES[0] / "references" / "validation.md"
        payloads = (
            "[unused]: ../../outside.md",
            "[same]: source-ledger.md\n[same]: ../../outside.md",
            "[same]: source-ledger.md\n[SAME]: validation.md",
            "[bad][undefined]", "[bad](source-ledger.md", "[bad][unfinished",
        )
        for index, text in enumerate(payloads):
            with self.subTest(payload=text):
                document.write_text(text, encoding="utf-8")
                self.output = self.base / ("reference-policy-denied-" + str(index))
                self.assert_rejected()

    def test_code_and_escaped_nonlinks_have_declared_conservative_scope(self):
        module = self.module()
        document = self.root / "skills" / NAMES[0] / "references" / "validation.md"
        payloads = (
            "`[safe](source-ledger.md)`",
            "```md\n[safe](source-ledger.md)\n```",
            "    [safe](source-ledger.md)\n",
            "```md\n[unused]: source-ledger.md\n```",
            "`[safe](source-ledger.md) preview_<commit>/`",
        )
        for index, text in enumerate(payloads):
            with self.subTest(payload=text):
                self.assertEqual(set(module._link_targets(text)), {"source-ledger.md"})
                document.write_text(text, encoding="utf-8")
                output = self.base / ("code-safe-" + str(index))
                module.package_skills(self.root, output)
                with zipfile.ZipFile(output / (NAMES[0] + "-preview.zip")) as archive:
                    self.assertEqual(archive.read(NAMES[0] + "/references/validation.md"), text.encode("utf-8"))
        from markdown_it import MarkdownIt
        for text in (r"\[label](../../outside.md)", "&lt;a href='../../outside.md'&gt;label&lt;/a&gt;"):
            self.assertEqual(module._link_targets(text), [])
            self.assertNotIn('href="', MarkdownIt("commonmark", {"html": True}).render(text))

    def test_escaped_bracket_inline_links_validate_every_destination(self):
        document = self.root / "skills" / NAMES[0] / "references" / "validation.md"
        templates = (
            r"[bad\]label]({target})",
            r"[bad\[label]({target})",
            r"[bad\[label\]tail]({target})",
            r"[outer [bad\]label]]({target})",
            r"[outer [deeper [bad\]label]]]({target})",
            r"![bad\]label]({target})",
            r"![outer [bad\]label]]({target})",
            r"[bad\\]({target})",
            r"[bad\\\]label]({target})",
            r"[first](#scope) [bad\]label]({target}) [last](#end)",
        )
        module = self.module()
        for index, template in enumerate(templates):
            for target in ("../../outside.md", "file:///outside.md"):
                with self.subTest(variant=index, target=target):
                    document.write_text(template.format(target=target), encoding="utf-8")
                    self.output = self.base / ("inline-denied-" + str(index) + "-" + target.split(":", 1)[0].replace("/", "_"))
                    self.assert_rejected()
            safe = template.format(target="source-ledger.md")
            with self.subTest(variant=index, safety="safe"):
                self.assertIn("source-ledger.md", module._link_targets(safe),
                              "safe inline destination was not collected")
                document.write_text(safe, encoding="utf-8")
                output = self.base / ("inline-safe-" + str(index))
                module.package_skills(self.root, output)
                with zipfile.ZipFile(output / (NAMES[0] + "-preview.zip")) as archive:
                    self.assertEqual(archive.read(NAMES[0] + "/references/validation.md"), safe.encode("utf-8"))

    def test_container_and_multiline_reference_bypasses_are_fail_closed(self):
        document = self.root / "skills" / NAMES[1] / "references" / "source-ledger.md"
        payloads = (
            "[bad]\n\n> [bad]: ../../outside.md",
            "[bad]\n\n- [bad]: ../../outside.md",
            "[bad label]\n\n[bad\nlabel]: ../../outside.md",
            "[bad]\n\n> [bad]: file:///outside.md",
        )
        for index, text in enumerate(payloads):
            with self.subTest(payload=text):
                self.output = self.base / ("reference-denied-" + str(index))
                document.write_text(text, encoding="utf-8")
                self.assert_rejected()

    def test_safe_container_and_multiline_references_are_preserved(self):
        document = self.root / "skills" / NAMES[0] / "references" / "validation.md"
        payloads = (
            "[good]\n\n> [good]: source-ledger.md",
            "[good]\n\n- [good]: source-ledger.md",
            "[good label]\n\n[good\nlabel]: source-ledger.md",
            "[good]\n\n> [good]: https://example.invalid/source",
        )
        module = self.module()
        for index, text in enumerate(payloads):
            with self.subTest(payload=text):
                self.output = self.base / ("reference-safe-" + str(index))
                document.write_text(text, encoding="utf-8")
                # Require collection as well as admission: a missing scanner also
                # accepts safe inputs, but cannot prove the paired denial gate.
                targets = module._link_targets(text)
                self.assertTrue(targets, "safe reference destinations were not collected")
                self.assertEqual(set(targets), {text.rsplit(": ", 1)[1]})
                module.package_skills(self.root, self.output)
                with zipfile.ZipFile(self.output / (NAMES[0] + "-preview.zip")) as archive:
                    self.assertEqual(archive.read(NAMES[0] + "/references/validation.md"), text.encode("utf-8"))

    def test_reference_definition_siblings_validate_every_destination(self):
        document = self.root / "skills" / NAMES[0] / "references" / "validation.md"
        templates = (
            "[good]\n\n+ [good]: {target}",
            "[good]\n\n* [good]: {target}",
            "[good]\n\n1. [good]: {target}",
            "[good]\n\n2) [good]: {target}",
            "[good]\n\n> - > 1. [good]: {target}",
            "[good label]\n\n> [good\n> label]: {target}",
            "[good label]\n\n- [good\n  label]: {target}",
            "[good]\n\n> [good]:\n>   {target}",
            "[good]\n\n- [good]:\n  {target}",
            '[good]\n\n[good]: <{target}> "title"',
            "[good]\n\n[\ngood\n]: {target}",
            "[unused]: {target}",
            "[good]\r\n\r\n> [good]: {target}",
            "[good]\r\r> [good]: {target}",
            r"[go\[od]" + "\n\n" + r"[go\[od]: {target}",
            r"[go\]od]" + "\n\n" + r"[go\]od]: {target}",
            r"[good\\]" + "\n\n" + r"[good\\]: {target}",
            "[good\\\nlabel]\n\n[good\\\nlabel]: {target}",
        )
        module = self.module()
        for index, template in enumerate(templates):
            safe = template.format(target="source-ledger.md")
            with self.subTest(variant=index, safety="safe"):
                document.write_text(safe, encoding="utf-8")
                targets = module._link_targets(safe)
                self.assertTrue(targets, "definition destination was not collected")
                self.assertEqual(set(targets), {"source-ledger.md"})
                module.package_skills(self.root, self.base / ("sibling-safe-" + str(index)))
            for target in ("../../outside.md", "file:///outside.md", "missing.md"):
                with self.subTest(variant=index, target=target):
                    document.write_text(template.format(target=target), encoding="utf-8")
                    self.output = self.base / ("sibling-denied-" + str(index) + "-" + target.split(":", 1)[0].replace("/", "_"))
                    self.assert_rejected()

    def test_bracketed_prose_without_definitions_is_not_a_link(self):
        document = self.root / "skills" / NAMES[0] / "references" / "validation.md"
        text = "\n".join((
            "[확인 필요]", "> [확인 필요]", "- [확인 필요]", "[여러 줄\n확인 필요]",
            "문장 속 [확인 필요]: 설명이지 참조 정의가 아니다.",
        ))
        module = self.module()
        self.assertEqual(module._link_targets(text), [])
        document.write_text(text, encoding="utf-8")
        module.package_skills(self.root, self.output)

    def test_safe_inline_reference_html_and_external_links_are_preserved(self):
        document = self.root / "skills" / NAMES[0] / "references" / "validation.md"
        text = '\n'.join((
            '[local](../SKILL.md#scope "title")', '[local](<source-ledger.md>)',
            '[source][ledger]', '[ledger]: source-ledger.md', '[ledger]',
            '<a href="source-ledger.md">source</a>',
            '[official](https://example.invalid/a_(b))',
            '[mail](mailto:editor@example.invalid)', '[anchor](#scope)',
            'This is not a link: [확인 필요].',
        ))
        document.write_text(text, encoding="utf-8")
        self.module().package_skills(self.root, self.output)
        with zipfile.ZipFile(self.output / (NAMES[0] + "-preview.zip")) as archive:
            self.assertEqual(archive.read(NAMES[0] + "/references/validation.md"), text.encode("utf-8"))
    def test_symlink_files_directories_and_ignored_entries_are_rejected(self):
        skill = self.root / "skills" / NAMES[1]
        for relative, target in (("linked.md", "SKILL.md"), ("linked-dir", "references"),
                                 ("ignored.json", "SKILL.md"), ("broken", "absent")):
            with self.subTest(relative=relative):
                link = skill / relative
                link.symlink_to(target)
                self.assert_rejected()
                link.unlink()

    def test_symlink_skill_root_or_skills_parent_is_rejected(self):
        for path in (self.root / "skills" / NAMES[1], self.root / "skills"):
            with self.subTest(component=path.name):
                moved = path.with_name(path.name + "-saved")
                path.rename(moved)
                path.symlink_to(moved, target_is_directory=True)
                self.assert_rejected()
                path.unlink()
                moved.rename(path)

    def test_source_fifo_is_rejected_without_reading(self):
        import os
        import subprocess
        import sys
        os.mkfifo(self.root / "skills" / NAMES[1] / "pipe.md")
        code = (
            "import importlib.util,sys; from pathlib import Path; "
            "s=importlib.util.spec_from_file_location('packager',sys.argv[1]); "
            "m=importlib.util.module_from_spec(s); s.loader.exec_module(m); "
            "m.package_skills(Path(sys.argv[2]),Path(sys.argv[3]))"
        )
        try:
            result = subprocess.run([sys.executable, "-B", "-c", code, str(SCRIPT), str(self.root), str(self.output)],
                                    capture_output=True, text=True, timeout=2)
        except subprocess.TimeoutExpired:
            self.fail("packager blocks reading a FIFO instead of rejecting it")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("PackagingError", result.stderr)
        self.assertFalse(self.output.exists())

    def test_validation_uses_the_same_bytes_as_the_archive(self):
        from unittest.mock import patch
        module = self.module()
        document = self.root / "skills" / NAMES[0] / "references" / "validation.md"
        original = document.read_bytes()
        original_read_bytes = Path.read_bytes
        reads = []

        def read_once(path):
            data = original_read_bytes(path)
            if path == document:
                reads.append(data)
                document.write_text("[bad](../../outside.md)", encoding="utf-8")
            return data

        with patch.object(Path, "read_bytes", read_once), patch.object(
            Path, "read_text", side_effect=AssertionError("validation must decode the byte snapshot")
        ):
            module.package_skills(self.root, self.output)
        self.assertEqual(reads, [original], "source must be snapshotted once, before validation")
        with zipfile.ZipFile(self.output / (NAMES[0] + "-preview.zip")) as archive:
            self.assertEqual(archive.read(NAMES[0] + "/references/validation.md"), original)
    def test_output_inside_repository_or_ancestor_is_rejected(self):
        module = self.module()
        for output in (self.root, self.root / "build", self.root / "skills" / NAMES[0] / "output", self.base):
            with self.subTest(component=output.name):
                with self.assertRaises(module.PackagingError):
                    module.package_skills(self.root, output)
                self.assertFalse((output / "manifest.json").exists())

    def test_existing_output_is_never_overwritten_even_if_empty(self):
        self.output.mkdir()
        module = self.module()
        with self.assertRaises(module.PackagingError):
            module.package_skills(self.root, self.output)
        self.assertEqual(list(self.output.iterdir()), [])
        sentinel = self.output / "manifest.json"
        sentinel.write_bytes(b"original")
        with self.assertRaises(module.PackagingError):
            module.package_skills(self.root, self.output)
        self.assertEqual(sentinel.read_bytes(), b"original")
        self.assertEqual(list(self.output.iterdir()), [sentinel])

    def test_symlink_output_and_parent_are_rejected(self):
        module = self.module()
        target = self.base / "destination"
        target.mkdir()
        alias = self.base / "alias"
        alias.symlink_to(target, target_is_directory=True)
        for output in (alias, alias / "new-output"):
            with self.subTest(component=output.name):
                with self.assertRaises(module.PackagingError):
                    module.package_skills(self.root, output)
                self.assertEqual(list(target.iterdir()), [])
    def test_repeated_builds_ignore_mtime_mode_and_creation_order(self):
        import os
        import shutil
        module = self.module()
        first = self.base / "first"
        module.package_skills(self.root, first)
        second_root = self.base / "second-repository"
        for path in reversed(sorted(self.root.rglob("*.md"))):
            destination = second_root / path.relative_to(self.root)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, destination)
            destination.chmod(0o600)
            os.utime(destination, (1_234_567_890, 1_234_567_890))
        second = self.base / "second"
        module.package_skills(second_root, second)
        first_digests = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in first.iterdir()}
        second_digests = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in second.iterdir()}
        self.assertEqual(first_digests, second_digests)

    def test_cli_builds_real_skills_from_any_working_directory(self):
        import subprocess
        import sys
        result = subprocess.run([sys.executable, "-B", str(SCRIPT), "--output", str(self.output)],
                                cwd=self.base, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.output / "manifest.json").is_file(), "CLI did not publish a manifest")
        manifest = json.loads((self.output / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(len(manifest["packages"]), 2)
        for package in manifest["packages"]:
            with zipfile.ZipFile(self.output / package["artifact"]) as archive:
                for info in archive.infolist():
                    self.assertEqual(archive.read(info.filename), (REPOSITORY_ROOT / "skills" / info.filename).read_bytes())
        failed = subprocess.run([sys.executable, "-B", str(SCRIPT), "--output", str(self.output)],
                                cwd=self.base, capture_output=True, text=True, timeout=10)
        self.assertEqual(failed.returncode, 1)
        self.assertIn("output already exists", failed.stderr)
        self.assertNotIn(str(self.base), failed.stderr)

    def test_io_failure_removes_only_newly_owned_partial_output(self):
        from unittest.mock import patch
        module = self.module()
        original_write = Path.write_bytes

        def fail_manifest(path, data):
            if path.name == "manifest.json":
                raise OSError("synthetic write failure")
            return original_write(path, data)

        with patch.object(Path, "write_bytes", fail_manifest):
            with self.assertRaises(OSError):
                module.package_skills(self.root, self.output)
        self.assertFalse(self.output.exists(), "partial previews must not survive a failed write")
    def test_member_order_is_lexical_for_nested_documents(self):
        skill = self.root / "skills" / NAMES[0]
        (skill / "a").mkdir()
        (skill / "a" / "notes.md").write_text("# notes\n", encoding="utf-8")
        (skill / "a.md").write_text("# overview\n", encoding="utf-8")
        self.module().package_skills(self.root, self.output)
        with zipfile.ZipFile(self.output / (NAMES[0] + "-preview.zip")) as archive:
            self.assertEqual(archive.namelist(), sorted(archive.namelist()))

    def test_unsafe_archive_filenames_are_rejected(self):
        skill = self.root / "skills" / NAMES[0]
        for index, filename in enumerate(("bad\\name.md", "bad\nname.md", "bad:name.md")):
            with self.subTest(filename=filename):
                self.output = self.base / ("filename-denied-" + str(index))
                path = skill / filename
                path.write_text("# fixture\n", encoding="utf-8")
                self.assert_rejected()
                path.unlink()

    def test_empty_required_evidence_is_rejected(self):
        (self.root / "skills" / NAMES[1] / "references" / "source-ledger.md").write_bytes(b"")
        self.assert_rejected()


if __name__ == "__main__":
    unittest.main()
