#!/usr/bin/env python3
"""Regression contract for the particle-choice entry point in korean-editing."""
from __future__ import annotations

import re
import unittest

from skill_structure_test import REPOSITORY_ROOT, markdown_destinations


_PARTICLE_HEADING = "### ‘이/가’와 ‘은/는’의 선택"


def particle_section(content: str) -> str:
    """Return text before the next heading at this level or a parent level."""
    following = content.split(_PARTICLE_HEADING, 1)[1]
    return re.split(r"\n#{1,3}[ \t]+", following, maxsplit=1)[0]


class ParticleChoiceLinkContract(unittest.TestCase):
    """Keep the detailed particle-choice guidance discoverable from SKILL.md."""

    def test_entry_point_links_directly_to_particle_choice(self) -> None:
        skill_path = REPOSITORY_ROOT / "skills" / "korean-editing" / "SKILL.md"
        content = skill_path.read_text(encoding="utf-8")
        self.assertIn(_PARTICLE_HEADING, content)
        self.assertIn(
            "references/particle-choice.md",
            markdown_destinations(particle_section(content)),
            "The particle-choice section must link directly to its guidance.",
        )
        target = skill_path.parent / "references" / "particle-choice.md"
        self.assertTrue(target.is_file(), "The linked guidance must exist.")

    def test_link_in_following_heading_does_not_satisfy_contract(self) -> None:
        """A moved link must not count, even if the next heading is higher."""
        for level in ("#", "##", "###"):
            with self.subTest(level=level):
                sample = (
                    f"{_PARTICLE_HEADING}\nNo direct link.\n"
                    f"{level} Following section\n"
                    "[Unrelated link](references/particle-choice.md)\n"
                )
                self.assertNotIn(
                    "references/particle-choice.md",
                    markdown_destinations(particle_section(sample)),
                )


if __name__ == "__main__":
    unittest.main()
