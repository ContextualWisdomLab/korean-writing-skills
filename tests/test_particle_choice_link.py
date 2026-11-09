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

# Non-rendering HTML containers never provide a clickable Markdown link.
_NONVISIBLE_HTML_TAGS = frozenset({
    "head", "noscript", "option", "optgroup", "script", "select",
    "style", "template", "textarea", "title",
})


class _AnchorLinks(HTMLParser):
    """Collect visibly labelled HTML links outside hidden ancestors."""

    def __init__(self) -> None:
        """Prepare the open-element stack and pending anchor for this section."""
        super().__init__(convert_charrefs=True)
        self.destinations: list[str] = []
        self._elements: list[tuple[str, bool]] = []
        self._hidden_depth = 0
        self._anchor: tuple[str | None, list[str]] | None = None
        self._anchor_depth: int | None = None

    @property
    def is_hidden(self) -> bool:
        """Whether the current HTML element is inside a hidden ancestor."""
        return self._hidden_depth > 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Track hidden elements and start collecting a named visible anchor."""
        tag = tag.lower()
        if tag in {"td", "th", "tr"} and not any(
            open_tag == "table" for open_tag, _ in self._elements
        ):
            # Browsers ignore row and cell starts outside table context.
            return
        reconstructed_anchor: str | None = None
        if tag == "p":
            # Closing a paragraph removes its anchor from the element stack,
            # but HTML keeps the anchor as an active formatting element.
            for index in range(len(self._elements) - 1, -1, -1):
                open_tag, _ = self._elements[index]
                if open_tag == "p":
                    if (
                        self._anchor is not None
                        and self._anchor_depth is not None
                        and index <= self._anchor_depth
                        and not self.is_hidden
                    ):
                        reconstructed_anchor = self._anchor[0]
                    self.handle_endtag("p")
                    break
                if open_tag in {
                    "button", "div", "table", "template", "td", "th",
                    "section", "article", "blockquote", "li",
                }:
                    break
        if tag in {"td", "th", "tr"}:
            # A new cell or row implicitly closes a cell in the same table.
            # A template or nested table cannot close a surrounding cell.
            for open_tag, _ in reversed(self._elements):
                if open_tag in {"table", "template"}:
                    break
                if open_tag in {"td", "th"}:
                    self.handle_endtag(open_tag)
                    break
        if tag == "tr":
            # Only a row in a table can close another row and its hidden state.
            for open_tag, _ in reversed(self._elements):
                if open_tag in {"table", "template"}:
                    break
                if open_tag == "tr":
                    self.handle_endtag(open_tag)
                    break
        properties = {key.lower(): value for key, value in attrs}
        hidden = "hidden" in properties or tag in _NONVISIBLE_HTML_TAGS
        if tag == "a" and not (hidden or self.is_hidden):
            accessible_name = properties.get("aria-label") or properties.get("title") or ""
            self._anchor = (properties.get("href"), [accessible_name])
            self._anchor_depth = len(self._elements)
        elif tag == "img" and self._anchor is not None and not (hidden or self.is_hidden):
            self._anchor[1].append(properties.get("alt") or "")
        if tag not in _VOID_HTML_TAGS:
            self._elements.append((tag, hidden))
            if hidden:
                self._hidden_depth += 1
        if reconstructed_anchor is not None and not self.is_hidden:
            # The next paragraph reconstructs the still-active anchor; its
            # later text belongs to that link, not to an unlinked sibling.
            self._anchor = (reconstructed_anchor, [])
            self._anchor_depth = len(self._elements)
            self._elements.append(("a", False))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Keep non-void HTML elements open despite an XHTML-style slash."""
        self.handle_starttag(tag, attrs)

    def handle_data(self, data: str) -> None:
        """Add visible HTML or Markdown text to the open anchor's label."""
        if self._anchor is not None and not self.is_hidden:
            self._anchor[1].append(data)

    def handle_endtag(self, tag: str) -> None:
        """Complete named anchors and close matching HTML elements."""
        tag = tag.lower()
        for index in range(len(self._elements) - 1, -1, -1):
            # A stray cell/row end tag inside a template or nested table
            # must not close an outer table cell or its visible anchor.
            if tag in {"td", "th", "tr"} and self._elements[index][0] in {"table", "template"}:
                break
            if self._elements[index][0] == tag:
                # An ancestor's close can implicitly close a valid anchor.
                # Preserve its own visible label, but never borrow sibling text.
                if self._anchor_depth is not None and index <= self._anchor_depth:
                    if self._anchor is not None:
                        href, label_parts = self._anchor
                        if href is not None and "".join(label_parts).strip():
                            self.destinations.append(href)
                    self._anchor = None
                    self._anchor_depth = None
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
                children = token.children or []
                for position, child in enumerate(children):
                    if child.type == "link_open" and not anchors.is_hidden:
                        href = child.attrGet("href")
                        label_parts: list[str] = []
                        for inner in children[position + 1:]:
                            if inner.type == "link_close":
                                break
                            if inner.type in {"text", "code_inline", "image"}:
                                label_parts.append(inner.content)
                        if href is not None and "".join(label_parts).strip():
                            destinations.append(href)
                    elif child.type == "html_inline":
                        # Feed fragments in sequence; HTML anchors may enclose
                        # Markdown text, including across inline token boundaries.
                        before = len(anchors.destinations)
                        anchors.feed(child.content)
                        destinations.extend(anchors.destinations[before:])
                    elif child.type in {"text", "code_inline", "image"}:
                        anchors.handle_data(child.content)
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

    def test_unlabelled_links_do_not_satisfy_contract(self) -> None:
        """A direct link must offer visible text or an accessible HTML label."""
        target = _PARTICLE_TARGET
        rejected = (
            f"[]({target})",
            f"[ ]({target})",
            f'<a href="{target}"></a>',
            f'<a href="{target}">   </a>',
            f'<a href="{target}"><span hidden>Hidden</span></a>',
        )
        for link in rejected:
            with self.subTest(link=link):
                content = f"### {_PARTICLE_HEADING}\n{link}\n"
                self.assertNotIn(target, particle_section_links(content))
        accessible = f'<a href="{target}" aria-label="Read the guidance"></a>'
        content = f"### {_PARTICLE_HEADING}\n{accessible}\n"
        self.assertIn(target, particle_section_links(content))

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

    def test_select_options_do_not_satisfy_direct_link_contract(self) -> None:
        """Links inside a selector are not rendered clickable; later links remain valid."""
        target = _PARTICLE_TARGET
        selector = f'<select><option><a href="{target}">Read</option></select>'
        rejected = (
            selector,
            f'<option><a href="{target}">Read</a></option>',
            f'<select><option><a href="{target}" aria-label="Read"></a></option></select>',
            f'<select>[Read]({target})</select>',
        )
        for markup in rejected:
            with self.subTest(markup=markup):
                content = f"### {_PARTICLE_HEADING}\n\n{markup}\n"
                self.assertNotIn(target, particle_section_links(content))
        visible = selector + f' <a href="{target}">Visible</a>'
        self.assertIn(
            target,
            particle_section_links(f"### {_PARTICLE_HEADING}\n\n{visible}\n"),
        )

    def test_self_closing_select_does_not_expose_links(self) -> None:
        """A non-void slash keeps links hidden until the HTML element closes."""
        target = _PARTICLE_TARGET
        samples = (
            (f'Notice: <select/> [Read]({target})', []),
            (f'Notice: <select/> [Hidden]({target})</select> [Visible]({target})', [target]),
            (f'Notice: <input hidden/> [Visible]({target})', [target]),
        )
        for markup, expected in samples:
            with self.subTest(markup=markup):
                content = f"### {_PARTICLE_HEADING}\n\n{markup}\n"
                self.assertEqual(expected, particle_section_links(content))

    def test_hidden_inline_parent_does_not_hide_later_visible_links(self) -> None:
        """Closing an inline hidden parent restores subsequent link visibility."""
        content = (
            f"### {_PARTICLE_HEADING}\n\n"
            f'<span hidden><a href="{_PARTICLE_TARGET}">Hidden</a></span> '
            f'[Read]({_PARTICLE_TARGET})\n'
        )
        self.assertIn(_PARTICLE_TARGET, particle_section_links(content))

    def test_unclosed_html_anchor_cannot_borrow_label_from_sibling(self) -> None:
        """An implicitly closed anchor must not borrow a later table-cell label."""
        target = _PARTICLE_TARGET
        sample = (
            f"### {_PARTICLE_HEADING}\n\n"
            f'<table><tr><td><a href="{target}"></td>'
            '<td>Later text</a></td></tr></table>\n'
        )
        self.assertNotIn(target, particle_section_links(sample))

    def test_new_table_cell_implicitly_closes_unlabelled_anchor(self) -> None:
        """A following table cell cannot label an anchor in the previous cell."""
        target = _PARTICLE_TARGET
        examples = (
            (
                f'<table><tr><td><a href="{target}">\n\n'
                '<td>\n\nLater text </a>\n\n</td></tr></table>'
            ),
            (
                f'<table><tr><td><a href="{target}">\n\n'
                '<th>\n\nLater text </a>\n\n</th></tr></table>'
            ),
        )
        for html in examples:
            with self.subTest(html=html):
                sample = f"### {_PARTICLE_HEADING}\n\n{html}\n"
                self.assertNotIn(target, particle_section_links(sample))

        labelled = (
            f'<table><tr><td><a href="{target}">Visible\n\n'
            '<td>\n\nLater text</a></td></tr></table>'
        )
        sample = f"### {_PARTICLE_HEADING}\n\n{labelled}\n"
        self.assertIn(target, particle_section_links(sample))

    def test_template_cell_does_not_close_visible_outer_link(self) -> None:
        """A cell inside a hidden template must not close the outer table cell."""
        target = _PARTICLE_TARGET
        markup = (
            f'<table><tr><td><a href="{target}">'
            '<template><td>Hidden</td></template>'
            'Read</a></td></tr></table>'
        )
        sample = f"### {_PARTICLE_HEADING}\n\n{markup}\n"
        self.assertIn(target, particle_section_links(sample))

    def test_new_table_row_implicitly_closes_previous_cell_link(self) -> None:
        """A new row cannot supply a label to an unclosed anchor in the old row."""
        target = _PARTICLE_TARGET
        examples = (
            (f'<table><tr><td><a href="{target}">'
             '<tr>Later</a><td></td></tr></table>', []),
            (f'<table><tr><td><a href="{target}">Visible'
             '<tr>Later</a><td></td></tr></table>', [target]),
        )
        for markup, expected in examples:
            with self.subTest(markup=markup):
                sample = f"### {_PARTICLE_HEADING}\n\n{markup}\n"
                self.assertEqual(expected, particle_section_links(sample))

    def test_stray_template_cell_endtag_preserves_outer_visible_link(self) -> None:
        """An unmatched cell end inside template cannot close the outer anchor."""
        target = _PARTICLE_TARGET
        for tag in ("td", "th"):
            with self.subTest(tag=tag):
                markup = (
                    f'<table><tr><{tag}><a href="{target}">'
                    f'<template></{tag}></template>'
                    f'Read</a></{tag}></tr></table>'
                )
                sample = f"### {_PARTICLE_HEADING}\n\n{markup}\n"
                self.assertEqual([target], particle_section_links(sample))

    def test_hidden_previous_row_does_not_hide_next_row_link(self) -> None:
        """Starting a new row clears the previous row's implicit hidden scope."""
        target = _PARTICLE_TARGET
        markup = (
            '<table><tr hidden><td>Hidden'
            f'<tr><td><a href="{target}">Visible</a></td></tr></table>'
        )
        sample = f"### {_PARTICLE_HEADING}\n\n{markup}\n"
        self.assertEqual([target], particle_section_links(sample))

    def test_stray_row_outside_table_cannot_reveal_hidden_link(self) -> None:
        """An invalid row outside a table cannot close a hidden ancestor."""
        target = _PARTICLE_TARGET
        examples = (
            (
                f'<tr><div hidden><tr><a href="{target}">Hidden</a></div>',
                [],
            ),
            (
                f'<tr><div hidden><tr><a href="{target}">Hidden</a></div>'
                f'<a href="{target}">Visible</a>',
                [target],
            ),
        )
        for markup, expected in examples:
            with self.subTest(markup=markup):
                sample = f"### {_PARTICLE_HEADING}\n\n{markup}\n"
                self.assertEqual(expected, particle_section_links(sample))

    def test_stray_hidden_row_outside_table_does_not_hide_visible_link(self) -> None:
        """Browsers ignore hidden row start tags outside a table."""
        target = _PARTICLE_TARGET
        for markup in (
            f'<tr hidden><a href="{target}">Read</a>',
            f'<tr hidden><tr><a href="{target}">Read</a>',
        ):
            with self.subTest(markup=markup):
                sample = f"### {_PARTICLE_HEADING}\n\n{markup}\n"
                self.assertEqual([target], particle_section_links(sample))

    def test_stray_table_cells_outside_table_cannot_hide_links(self) -> None:
        """Browsers ignore td/th starts outside a table, including hidden cells."""
        target = _PARTICLE_TARGET
        for tag in ("td", "th"):
            for markup in (
                f'<{tag} hidden><a href="{target}">Read</a>',
                f'<{tag} hidden><tr><a href="{target}">Read</a>',
            ):
                with self.subTest(tag=tag, markup=markup):
                    sample = f"### {_PARTICLE_HEADING}\n\n{markup}\n"
                    self.assertEqual([target], particle_section_links(sample))

    def test_new_paragraph_reconstructs_active_visible_anchor(self) -> None:
        """HTML restores an open formatting anchor after closing its paragraph."""
        target = _PARTICLE_TARGET
        examples = (
            (f'<p><a href="{target}"><p>Read</a>', [target]),
            (f'<p><a href="{target}"><p><strong>Read</strong></a>', [target]),
            (f'<p><a href="{target}"><p></a>Outside', []),
            (f'<div hidden><p><a href="{target}"><p>Hidden</a></div>', []),
        )
        for markup, expected in examples:
            with self.subTest(markup=markup):
                sample = f"### {_PARTICLE_HEADING}\n\n{markup}\n"
                self.assertEqual(expected, particle_section_links(sample))

    def test_new_paragraph_implicitly_closes_hidden_paragraph(self) -> None:
        """A later paragraph is visible unless an enclosing div remains hidden."""
        target = _PARTICLE_TARGET
        examples = (
            (
                f'<div><p hidden>Hidden<p><a href="{target}">Visible</a></p></div>',
                [target],
            ),
            (
                f'<div hidden><p hidden>Hidden<p><a href="{target}">Hidden</a></p></div>',
                [],
            ),
        )
        for markup, expected in examples:
            with self.subTest(markup=markup):
                sample = f"### {_PARTICLE_HEADING}\n\n{markup}\n"
                self.assertEqual(expected, particle_section_links(sample))

    def test_hidden_previous_cell_does_not_hide_visible_sibling(self) -> None:
        """An implicit cell close restores visibility for the following cell."""
        target = _PARTICLE_TARGET
        for tag in ("td", "th"):
            with self.subTest(tag=tag):
                markup = (
                    f'<table><tr><{tag} hidden><a href="{target}">Hidden</a>'
                    f'<{tag}><a href="{target}">Visible</a></{tag}></tr></table>'
                )
                sample = f"### {_PARTICLE_HEADING}\n\n{markup}\n"
                self.assertEqual([target], particle_section_links(sample))

    def test_implicitly_closed_html_anchor_preserves_own_label(self) -> None:
        """Keep a visible label when a parent closes an unclosed anchor."""
        target = _PARTICLE_TARGET
        examples = (
            f'<table><tr><td><a href="{target}">Visible</td><td>Later</a></td></tr></table>',
            f'<table><tr><td><a href="{target}"><strong>Visible</strong></td>'
            '<td>Later</a></td></tr></table>',
        )
        for html in examples:
            with self.subTest(html=html):
                sample = f"### {_PARTICLE_HEADING}\n\n{html}\n"
                self.assertIn(target, particle_section_links(sample))

    def test_links_inside_nonvisible_html_elements_do_not_count(self) -> None:
        """Markdown syntax inside nonrendered HTML is not a clickable link."""
        target = _PARTICLE_TARGET
        for tag in ("title", "style", "script", "template", "textarea"):
            with self.subTest(tag=tag):
                sample = (
                    f"### {_PARTICLE_HEADING}\n\n"
                    f'Notice: <{tag}>[Read]({target})</{tag}>\n'
                )
                self.assertNotIn(target, particle_section_links(sample))
        block_after_title = (
            f"### {_PARTICLE_HEADING}\n\n"
            f'<title>[Hidden]({target})</title> [Visible]({target})\n'
        )
        self.assertNotIn(target, particle_section_links(block_after_title))
        visible_after_title = (
            f"### {_PARTICLE_HEADING}\n\n"
            f'Notice: <title>[Hidden]({target})</title> [Visible]({target})\n'
        )
        self.assertIn(target, particle_section_links(visible_after_title))

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
