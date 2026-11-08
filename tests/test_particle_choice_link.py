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


# HTML void elements cannot contain a hidden descendant.
_VOID_HTML_TAGS = frozenset({
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
})


class _AnchorLinks(HTMLParser):
    """Collect HTML hrefs only when no HTML ancestor is hidden."""

    def __init__(self) -> None:
        """Prepare the open-element stack for this rendered section."""
        super().__init__(convert_charrefs=True)
        self.destinations: list[str] = []
        self._elements: list[tuple[str, bool]] = []
        self._hidden_depth = 0

    @property
    def is_hidden(self) -> bool:
        """Whether the current HTML element is inside a hidden ancestor."""
        return self._hidden_depth > 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Collect visible anchor hrefs and track hidden HTML elements."""
        tag = tag.lower()
        hidden = any(name.lower() == "hidden" for name, _ in attrs)
        if tag == "a" and not (hidden or self.is_hidden):
            self.destinations.extend(
                value for key, value in attrs if key.lower() == "href" and value is not None
            )
        if tag not in _VOID_HTML_TAGS:
            self._elements.append((tag, hidden))
            if hidden:
                self._hidden_depth += 1

    def handle_endtag(self, tag: str) -> None:
        """End the matching element and all unmatched inner elements."""
        tag = tag.lower()
        for index in range(len(self._elements) - 1, -1, -1):
            if self._elements[index][0] == tag:
                self._hidden_depth -= sum(is_hidden for _, is_hidden in self._elements[index:])
                del self._elements[index:]
                break

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
    anchors = _AnchorLinks()
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
                    if child.type == "link_open" and not anchors.is_hidden:
                        href = child.attrGet("href")
                        if href is not None:
                            destinations.append(href)
                    elif child.type == "html_inline":
                        # Feed inline fragments in sequence so a hidden ancestor
                        # around a later anchor is not accidentally forgotten.
                        before = len(anchors.destinations)
                        anchors.feed(child.content)
                        destinations.extend(anchors.destinations[before:])
            elif token.type == "html_block":
                before = len(anchors.destinations)
                anchors.feed(token.content)
                destinations.extend(anchors.destinations[before:])
            for href in destinations:
                normalized = _local_destination(href)
                if normalized is not None:
                    links.append(normalized)
    return links

class ParticleChoiceLinkContract(unittest.TestCase):
    """Keep the detailed particle-choice guidance discoverable from SKILL.md."""

    def test_entry_point_links_directly_to_particle_choice(self) -> None:
        """Require the real entry point to link to an existing guidance file."""
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
        """Unused reference definitions never count as displayed links."""
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
        """Code examples must not terminate the real Markdown section."""
        sample = (
            f"### {_PARTICLE_HEADING}\n"
            "```md\n## Example, not a heading\n```\n"
            f"[Read the guidance]({_PARTICLE_TARGET})\n"
        )
        self.assertIn(_PARTICLE_TARGET, particle_section_links(sample))

    def test_quoted_or_fenced_title_does_not_start_section(self) -> None:
        """Quoted headings and fenced examples are not section titles."""
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
        """The section is identified by its rendered heading text."""
        sample = f"### **{_PARTICLE_HEADING}**\n[Read]({_PARTICLE_TARGET})\n"
        self.assertIn(_PARTICLE_TARGET, particle_section_links(sample))

    def test_html_anchor_in_section_is_visible_direct_link(self) -> None:
        """Normal HTML anchor markup can directly link to the guidance."""
        for anchor in (
            f'<a href="{_PARTICLE_TARGET}">Read</a>',
            f"<a href='./{_PARTICLE_TARGET}'>Read</a>",
        ):
            with self.subTest(anchor=anchor):
                sample = f"### {_PARTICLE_HEADING}\n\n{anchor}\n"
                self.assertIn(_PARTICLE_TARGET, particle_section_links(sample))

    def test_html_anchor_outside_section_or_in_code_is_not_direct(self) -> None:
        """Ignore HTML in other sections, comments, and code examples."""
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

    def test_hidden_html_ancestors_do_not_satisfy_contract(self) -> None:
        """Only displayed HTML/Markdown links satisfy the direct-link contract."""
        target = _PARTICLE_TARGET
        samples = (
            f'<p hidden><a href="{target}">Read</a></p>',
            f'<div hidden><p><a href="{target}">Read</a></p></div>',
            f'<a hidden href="{target}">Read</a>',
            f'<span hidden>[Read]({target})</span>',
        )
        for hidden_only in samples:
            with self.subTest(hidden_only=hidden_only):
                content = f"### {_PARTICLE_HEADING}\n\n{hidden_only}\n"
                self.assertNotIn(target, particle_section_links(content))

        visible = f'<p hidden><a href="{target}">Hidden</a></p>\n\n<a href="{target}">Visible</a>'
        self.assertIn(target, particle_section_links(f"### {_PARTICLE_HEADING}\n\n{visible}\n"))

    def test_hidden_inline_parent_does_not_hide_later_visible_links(self) -> None:
        """Closing an inline hidden parent restores subsequent link visibility."""
        content = (
            f"### {_PARTICLE_HEADING}\n\n"
            f'<span hidden><a href="{_PARTICLE_TARGET}">Hidden</a></span> '
            f'[Read]({_PARTICLE_TARGET})\n'
        )
        self.assertIn(_PARTICLE_TARGET, particle_section_links(content))

    def test_equivalent_local_paths_are_accepted(self) -> None:
        """Equivalent relative paths resolve to the same guidance file."""
        for path in (
            f"./{_PARTICLE_TARGET}",
            "references/../references/particle-choice.md",
            "references/particle%2Dchoice.md",
        ):
            with self.subTest(path=path):
                sample = f"### {_PARTICLE_HEADING}\n[Read]({path})\n"
                self.assertIn(_PARTICLE_TARGET, particle_section_links(sample))

    def test_external_and_parent_paths_are_not_accepted(self) -> None:
        """Exclude remote and escaping links from the local-file contract."""
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
