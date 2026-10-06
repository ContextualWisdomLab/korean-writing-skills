"""Focused successor contracts; frozen evaluations and packaging tests are not run."""
from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("skill_structure", ROOT / "tests/skill_structure_test.py")
structure = importlib.util.module_from_spec(spec)
spec.loader.exec_module(structure)


class StructureFollowupTests(unittest.TestCase):
    def check(self, frontmatter, body="", files=()):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / "SKILL.md"
            skill.write_text("---\n" + frontmatter + "\n---\n" + body, encoding="utf-8")
            for name in files:
                p = root / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text("evidence\n", encoding="utf-8")
            return structure.validate_skill(skill)

    def test_incomplete_yaml_is_rejected(self):
        self.assertTrue(self.check("name: sample\ndescription: ["))

    def test_non_string_description_is_rejected(self):
        self.assertTrue(self.check("name: sample\ndescription: [one, two]"))

    def test_whitespace_description_is_rejected(self):
        self.assertTrue(self.check('name: sample\ndescription: " "'))

    def test_yaml_mapping_and_both_string_fields_are_required(self):
        for frontmatter in ("- item", "name: 123\ndescription: valid", "name: sample\ndescription: null", "name: false\ndescription: valid"):
            with self.subTest(frontmatter=frontmatter):
                self.assertTrue(self.check(frontmatter))

    def test_block_scalar_description_is_allowed(self):
        self.assertEqual([], self.check("name: sample\ndescription: |\n  A valid description."))

    def test_missing_reference_link_is_rejected(self):
        self.assertTrue(self.check("name: sample\ndescription: valid", "[근거][source]\n\n[source]: references/missing.md\n"))

    def test_reference_image_outside_package_is_rejected(self):
        self.assertTrue(self.check("name: sample\ndescription: valid", "![근거][source]\n\n[source]: ../outside.md\n"))

    def test_defined_reference_and_inline_positive(self):
        self.assertEqual([], self.check("name: sample\ndescription: valid", "[근거][source] and [same](references/existing.md#anchor)\n\n[source]: references/existing.md\n", ("references/existing.md",)))

    def test_encoded_reference_destination_is_checked(self):
        self.assertEqual([], self.check("name: sample\ndescription: valid", "[근거][source]\n\n[source]: references/a%20b.md\n", ("references/a b.md",)))

    def test_code_not_link_and_external_positive(self):
        self.assertEqual([], self.check("name: sample\ndescription: valid", "`[literal](missing.md)`\n\n[web](https://example.org)\n"))


class HygieneFollowupTests(unittest.TestCase):
    def invoke(self, filename, content):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tests").mkdir()
            shutil.copyfile(ROOT / "tests/public_hygiene_test.sh", root / "tests/public_hygiene_test.sh")
            names = ("ARCHITECTURE.md", "CHANGELOG.md", "CLAUDE.md", "SECURITY.md", "docs/adr/0001-skill-product-boundary.md", "docs/product-technical-gap-baseline.md")
            for name in names:
                p = root / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text("public fixture\n", encoding="utf-8")
            (root / filename).write_text(content, encoding="utf-8")
            env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
            env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
            subprocess.run(["git", "init", "-q", str(root)], env=env, check=True, capture_output=True)
            subprocess.run(["git", "-C", str(root), "add", "--", "."], env=env, check=True, capture_output=True)
            return subprocess.run(["bash", "tests/public_hygiene_test.sh"], cwd=root, env=env, capture_output=True, text=True, timeout=10)

    def test_korean_filename_is_scanned_without_quoting(self):
        result = self.invoke("한국어 예문.md", "public fixture\n")
        self.assertEqual(0, result.returncode, result.stderr)

    def test_newline_filename_is_scanned_as_one_path(self):
        result = self.invoke("two\nlines.md", "public fixture\n")
        self.assertEqual(0, result.returncode, result.stderr)

    def test_unsafe_content_in_korean_filename_is_rejected(self):
        result = self.invoke("한국어.md", "/" + "Users/example/private.md\n")
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertIn("public tree contains", result.stderr)


if __name__ == "__main__":
    unittest.main()
