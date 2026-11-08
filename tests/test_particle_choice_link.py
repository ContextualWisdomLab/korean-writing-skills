#!/usr/bin/env python3
"""Regression contract for the particle-choice entry point in korean-editing."""
from __future__ import annotations

from html.parser import HTMLParser
import posixpath
import unittest
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt

from skill_structure_test import REPOSITORY_ROOT


_PARTICLE_HEADING = "‘이/가’와 ‘은/는’의 선택"
_PARTICLE_TARGET = "references/particle-choice.md"


class _AnchorLinks(HTMLParser):
    """Collect destinations of rendered HTML anchors, not HTML comments."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.destinations: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "a":
            self.destinations.extend(
                value for key, value in attrs if key.lower() == "href" and value is not None
            )


def _local_destination(href: str) -> str | None:
    """Compare local file targets, accepting equivalent dot/percent-encoded paths."""
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    path = unquote(parsed.path)
    if path.startswith("/") or "\\" in path:
        return None
    normalized = posixpath.normpath(path)
    if normalized == ".." or normalized.startswith("../"):
        return None
    return normalized


def particle_section_links(content: str) -> list[str]:
    """Find rendered local destinations inside the actual particle-choice section."""
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
            if level == 3 and heading.type == "inline":
                visible_heading = "".join(
                    child.content
                    for child in (heading.children or [])
                    if child.type in {"text", "code_inline"}
                )
                if visible_heading == _PARTICLE_HEADING:
                    in_section = True
        elif in_section:
            destinations: list[str] = []
            if token.type == "inline":
                for child in token.children or []:
                    if child.type == "link_open":
                        href = child.attrGet("href")
                        if href is not None:
                            destinations.append(href)
                    elif child.type == "html_inline":
                        anchors = _AnchorLinks()
                        anchors.feed(child.content)
                        destinations.extend(anchors.destinations)
            elif token.type == "html_block":
                anchors = _AnchorLinks()
                anchors.feed(token.content)
                destinations.extend(anchors.destinations)
            for href in destinations:
                normalized = _local_destination(href)
                if normalized is not None:
                    links.append(normalized)
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

    def test_emphasized_heading_still_selects_section(self) -> None:
        sample = f"### **{_PARTICLE_HEADING}**\n[Read]({_PARTICLE_TARGET})\n"
        self.assertIn(_PARTICLE_TARGET, particle_section_links(sample))

    def test_html_anchor_in_section_is_visible_direct_link(self) -> None:
        for anchor in (
            f'<a href="{_PARTICLE_TARGET}">Read</a>',
            f"<a href='./{_PARTICLE_TARGET}'>Read</a>",
        ):
            with self.subTest(anchor=anchor):
                sample = f"### {_PARTICLE_HEADING}\n\n{anchor}\n"
                self.assertIn(_PARTICLE_TARGET, particle_section_links(sample))

    def test_html_anchor_outside_section_or_in_code_is_not_direct(self) -> None:
        anchor = f'<a href="{_PARTICLE_TARGET}">Read</a>'
        samples = (
            f"### {_PARTICLE_HEADING}\nNo link.\n## Next\n\n{anchor}\n",
            f"### {_PARTICLE_HEADING}\n```html\n{anchor}\n```\n",
            f"### {_PARTICLE_HEADING}\n`{anchor}`\n",
            f"### {_PARTICLE_HEADING}\n<!-- {anchor} -->\n",
        )
        for sample in samples:
            with self.subTest(sample=sample):
                self.assertNotIn(_PARTICLE_TARGET, particle_section_links(sample))

    def test_equivalent_local_paths_are_accepted(self) -> None:
        for path in (
            f"./{_PARTICLE_TARGET}",
            "references/../references/particle-choice.md",
            "references/particle%2Dchoice.md",
        ):
            with self.subTest(path=path):
                sample = f"### {_PARTICLE_HEADING}\n[Read]({path})\n"
                self.assertIn(_PARTICLE_TARGET, particle_section_links(sample))

    def test_external_and_parent_paths_are_not_accepted(self) -> None:
        for path in (
            "https://example.com/references/particle-choice.md",
            "../references/particle-choice.md",
            "/references/particle-choice.md",
        ):
            with self.subTest(path=path):
                sample = f"### {_PARTICLE_HEADING}\n[Read]({path})\n"
                self.assertNotIn(_PARTICLE_TARGET, particle_section_links(sample))



if __name__ == "__main__":
    unittest.main()
