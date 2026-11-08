#!/usr/bin/env python3
"""Regression contract for the particle-choice entry point in korean-editing."""
from __future__ import annotations

import unittest

from markdown_it import MarkdownIt

from skill_structure_test import REPOSITORY_ROOT


_PARTICLE_HEADING = "‘이/가’와 ‘은/는’의 선택"
_PARTICLE_TARGET = "references/particle-choice.md"


def particle_section_links(content: str) -> list[str]:
    """Find rendered links inside the real top-level particle-choice section."""
    parser = MarkdownIt("commonmark")
    parser.validateLink = lambda target: True
    tokens = parser.parse(content)
    in_section = False
    links: list[str] = []
    for index, token in enumerate(tokens):
        if token.type == "heading_open" and token.level == 0:
            level = int(token.tag[1:])
            if in_section and level <= 3:
                break
            heading = tokens[index + 1]
            if (
                level == 3
                and heading.type == "inline"
                and heading.content == _PARTICLE_HEADING
            ):
                in_section = True
        elif in_section and token.type == "inline":
            links.extend(
                child.attrGet("href")
                for child in (token.children or [])
                if child.type == "link_open" and child.attrGet("href") is not None
            )
    return links


class ParticleChoiceLinkContract(unittest.TestCase):
    """Keep the detailed particle-choice guidance discoverable from SKILL.md."""

    def test_entry_point_links_directly_to_particle_choice(self) -> None:
        skill_path = REPOSITORY_ROOT / "skills" / "korean-editing" / "SKILL.md"
        content = skill_path.read_text(encoding="utf-8")
        self.assertIn(
            _PARTICLE_TARGET,
            particle_section_links(content),
            "The particle-choice section must render a direct guidance link.",
        )
        target = skill_path.parent / _PARTICLE_TARGET
        self.assertTrue(target.is_file(), "The linked guidance must exist.")

    def test_link_in_following_heading_does_not_satisfy_contract(self) -> None:
        """A link under a later top-level heading must not satisfy the entry point."""
        for level in ("#", "##", "###"):
            with self.subTest(level=level):
                sample = (
                    f"### {_PARTICLE_HEADING}\nNo direct link.\n"
                    f"{level} Following section\n"
                    f"[Unrelated link]({_PARTICLE_TARGET})\n"
                )
                self.assertNotIn(_PARTICLE_TARGET, particle_section_links(sample))

    def test_unused_reference_definition_is_not_a_visible_link(self) -> None:
        sample = (
            f"### {_PARTICLE_HEADING}\nNo direct link.\n"
            f"[particle]: {_PARTICLE_TARGET}\n"
        )
        self.assertNotIn(_PARTICLE_TARGET, particle_section_links(sample))

    def test_reference_link_uses_document_wide_definition(self) -> None:
        """A rendered reference link may be defined after this section."""
        sample = (
            f"### {_PARTICLE_HEADING}\n[Read the guidance][particle]\n"
            f"## Following section\n[particle]: {_PARTICLE_TARGET}\n"
        )
        self.assertIn(_PARTICLE_TARGET, particle_section_links(sample))

    def test_heading_inside_fenced_code_does_not_end_section(self) -> None:
        sample = (
            f"### {_PARTICLE_HEADING}\n"
            "```md\n## Example, not a heading\n```\n"
            f"[Read the guidance]({_PARTICLE_TARGET})\n"
        )
        self.assertIn(_PARTICLE_TARGET, particle_section_links(sample))

    def test_quoted_or_fenced_title_does_not_start_section(self) -> None:
        samples = (
            f"> ### {_PARTICLE_HEADING}\n\n[Outside]({_PARTICLE_TARGET})\n",
            (
                "```md\n"
                f"### {_PARTICLE_HEADING}\n"
                "```\n"
                f"[Outside]({_PARTICLE_TARGET})\n"
            ),
        )
        for sample in samples:
            with self.subTest(sample=sample.splitlines()[0]):
                self.assertNotIn(_PARTICLE_TARGET, particle_section_links(sample))


if __name__ == "__main__":
    unittest.main()
