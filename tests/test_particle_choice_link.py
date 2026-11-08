#!/usr/bin/env python3
"""Regression contract for the particle-choice entry point in korean-editing."""
from __future__ import annotations

import unittest

from skill_structure_test import REPOSITORY_ROOT, markdown_destinations


class ParticleChoiceLinkContract(unittest.TestCase):
    """Keep the detailed particle-choice guidance discoverable from SKILL.md."""

    def test_entry_point_links_directly_to_particle_choice(self) -> None:
        skill_path = REPOSITORY_ROOT / "skills" / "korean-editing" / "SKILL.md"
        content = skill_path.read_text(encoding="utf-8")
        heading = "### ‘이/가’와 ‘은/는’의 선택"
        self.assertIn(heading, content)
        section = content.split(heading, 1)[1].split("\n### ", 1)[0]
        self.assertIn(
            "references/particle-choice.md",
            markdown_destinations(section),
            "The particle-choice section must link directly to its guidance.",
        )
        target = skill_path.parent / "references" / "particle-choice.md"
        self.assertTrue(target.is_file(), "The linked guidance must exist.")


if __name__ == "__main__":
    unittest.main()
