#!/usr/bin/env python3
"""Build preview ZIPs; not a release or APA certification.

Usage: uv run --locked --python 3.14 scripts/package_skills.py --output DIR
API: package_skills(repository_root, output_directory) returns manifest data.
DIR must not exist and must be outside the repository. No overwrite option.
Archives use a skill-named top-level directory and sorted Markdown members.
Only the two allowlisted skill trees and their Markdown files are read.
External HTTP(S)/mailto citations are allowed; filesystem links must resolve
within the same archive. CommonMark parsing/rendering plus separate conservative
admission rules check links, code examples and an allowlisted HTML subset.
Run against a quiescent source tree and an output parent you control.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import io
import json
import re
import shutil
import stat
import sys
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt
from markdown_it.rules_block import reference as _reference_rule
from markdown_it.rules_inline import image as _image_rule, link as _link_rule
from markdown_it.rules_block.state_block import StateBlock


SKILL_NAMES = ("apa7-manuscript-writing", "korean-editing")
REQUIRED_REFERENCES = {
    "korean-editing": ("examples.md", "source-ledger.md", "validation.md"),
    "apa7-manuscript-writing": (
        "document-format-checklist.md", "jars-quant-table1.md",
        "reporting-workflow.md", "source-ledger.md", "validation.md",
        "verified-scope.md",
    ),
}


class PackagingError(ValueError):
    """Invalid or unsafe preview input; no output may be published."""


class _HTMLLinks(HTMLParser):
    """Collect rendered URLs; never execute HTML or fetch a destination."""

    def __init__(self, code_example=False):
        super().__init__(convert_charrefs=True)
        self.targets = []
        self.code_example = code_example

    URL_ATTRIBUTES = {"href", "src", "action", "poster", "data", "cite", "background"}
    TAGS = set("a abbr b blockquote br caption code col colgroup dd del details div dl dt em figcaption figure h1 h2 h3 h4 h5 h6 hr i img ins kbd li mark ol p pre q s samp small span strong sub summary sup table tbody td th thead tr u ul var".split())
    ATTRIBUTES = URL_ATTRIBUTES | set("alt title class id name lang dir width height colspan rowspan scope start reversed type open align".split())

    ACTIVE_TAGS = {"script", "style", "iframe", "object", "embed", "svg", "math", "link", "meta", "base", "form", "input", "button", "textarea", "select"}

    def handle_starttag(self, tag, attrs):
        # Bare placeholders such as <commit> in code are not rendered HTML.
        if self.code_example and tag not in self.TAGS and tag not in self.ACTIVE_TAGS and not attrs:
            return
        if tag not in self.TAGS:
            raise PackagingError("unsupported HTML element: " + tag)
        for key, value in attrs:
            if key == "srcset":
                raise PackagingError("HTML srcset is unsupported; use explicit src links")
            if key not in self.ATTRIBUTES:
                raise PackagingError("unsupported HTML attribute: " + key)
            if key in self.URL_ATTRIBUTES:
                if value is None:
                    raise PackagingError("empty HTML link")
                self.targets.append(value)

    def handle_endtag(self, tag):
        if self.code_example and tag not in self.ACTIVE_TAGS:
            return
        if tag not in self.TAGS:
            raise PackagingError("unsupported HTML element: " + tag)

    def handle_decl(self, decl):
        raise PackagingError("HTML declarations are unsupported")

    def handle_pi(self, data):
        raise PackagingError("HTML processing instructions are unsupported")

    def unknown_decl(self, data):
        raise PackagingError("HTML declarations are unsupported")


def _strict_inline(rule, image=False):
    """Reject unresolved explicit link syntax, using the parser's label helper.

    This is a preview admission restriction, not CommonMark rendering behavior:
    CommonMark would render undefined references/malformed links as plain text.
    Silent lookahead remains unchanged, including code-span/HTML precedence.
    """
    def checked(state, silent):
        start = state.pos
        accepted = rule(state, silent)
        opening = start + (1 if image else 0)
        expected_start = state.src[start:start + 2] == "![" if image else state.src[start:start + 1] == "["
        if not accepted and not silent and expected_start:
            if opening < state.posMax and state.src[opening] == "[":
                end = state.md.helpers.parseLinkLabel(state, opening, False)
                if end >= 0 and state.src[end + 1:end + 2] in {"(", "["}:
                    raise PackagingError("undefined reference or malformed inline link")
        return accepted
    return checked


def _collect_embedded_definitions(state):
    """Conservative policy: also admit-check definitions inside paragraphs/code.

    CommonMark only recognizes definitions at block boundaries. Earlier preview
    inputs included paragraph-embedded definitions, so use the pinned parser's
    reference rule rather than a second handwritten reference grammar.
    """
    for token in state.tokens:
        if token.type not in {"inline", "code_block", "fence"}:
            continue
        block = StateBlock(token.content, state.md, state.env, [])
        for line in range(block.lineMax):
            start = block.bMarks[line] + block.tShift[line]
            if block.src[start:start + 1] == "[":
                _reference_rule(block, line, block.lineMax, False)


def _markdown_parser():
    parser = MarkdownIt("commonmark", {"html": True})
    # Default validateLink suppresses file/javascript destinations. Admission
    # must see them and reject through our own URL/path policy, not lose them.
    parser.validateLink = lambda target: True
    parser.core.ruler.before("inline", "preview_definitions", _collect_embedded_definitions)
    parser.inline.ruler.at("link", _strict_inline(_link_rule))
    parser.inline.ruler.at("image", _strict_inline(_image_rule, image=True))
    return parser


def _walk_tokens(tokens):
    for token in tokens:
        yield token
        if token.children:
            yield from _walk_tokens(token.children)


def _link_targets(text: str, _depth: int = 0) -> list[str]:
    """Collect CommonMark rendered links/images/HTML and unused definitions.

    Explicit malformed/undefined link syntax is conservatively rejected by a
    separate admission rule; plain bracketed prose remains plain text. Code
    examples are recursively parsed as standalone Markdown for admission only;
    paragraph-embedded definitions also remain conservatively checked. These
    are deliberate restrictions beyond actual CommonMark rendering, not a
    replacement handwritten grammar. Raw HTML permits only passive elements
    and explicit single-URL attributes: CSS/events/embedded documents and srcset
    are unsupported, not sanitized. Rendering never leaves memory or fetches.
    """
    if _depth > 32:
        raise PackagingError("code example nesting exceeds preview limit")
    parser = _markdown_parser()
    env = {}
    tokens = parser.parse(text, env)
    collector = _HTMLLinks(code_example=_depth > 0)
    collector.feed(parser.renderer.render(tokens, parser.options, env))
    collector.close()
    targets = collector.targets
    references = env.get("references", {})
    targets.extend(reference["href"] for reference in references.values())
    for duplicate in env.get("duplicate_refs", []):
        if duplicate["href"] != references[duplicate["label"]]["href"]:
            raise PackagingError("ambiguous reference link")
        targets.append(duplicate["href"])
    # Tokens also retain links nested in image alt content and raw HTML that
    # rendered alt text escapes. They still need conservative admission checks.
    for token in _walk_tokens(tokens):
        if token.type in {"link_open", "image"}:
            target = token.attrGet("href" if token.type == "link_open" else "src")
            if target is not None:
                targets.append(target)
        elif token.type in {"html_inline", "html_block"}:
            raw = _HTMLLinks(code_example=_depth > 0)
            raw.feed(token.content)
            raw.close()
            targets.extend(raw.targets)
        elif token.type in {"code_inline", "code_block", "fence"}:
            targets.extend(_link_targets(token.content, _depth + 1))
    return targets


def _validate_links(path: Path, skill_root: Path, documents: set[Path], text: str) -> None:
    for target in _link_targets(text):
        target = html.unescape(target)
        for _ in range(8):
            decoded = unquote(target, errors="strict")
            if decoded == target:
                break
            target = decoded
        if "%" in target or "\\" in target or any(ord(char) < 32 for char in target):
            raise PackagingError("ambiguous link in " + path.name)
        parsed = urlsplit(target)
        if parsed.scheme in {"http", "https", "mailto"}:
            if parsed.scheme != "mailto" and not parsed.netloc:
                raise PackagingError("invalid external link in " + path.name)
            continue
        if parsed.scheme or parsed.netloc or parsed.path.startswith("/"):
            raise PackagingError("unsafe link in " + path.name)
        if not parsed.path:
            continue
        resolved = (path.parent / parsed.path).resolve()
        try:
            resolved.relative_to(skill_root.resolve())
        except ValueError:
            raise PackagingError("link leaves skill package: " + path.name) from None
        if resolved not in documents:
            raise PackagingError("link target not packaged: " + path.name)


def _reject_symlink_components(path: Path) -> None:
    for component in (path,) + tuple(path.parents):
        if component.is_symlink():
            raise PackagingError("symlink path component is not allowed")


def _snapshot(skill_root: Path) -> dict[Path, bytes]:
    _reject_symlink_components(skill_root)
    if not skill_root.is_dir():
        raise PackagingError("missing skill directory: " + skill_root.name)
    documents = {}
    pending = [skill_root]
    while pending:
        directory = pending.pop()
        for path in sorted(directory.iterdir()):
            if "\\" in path.name or ":" in path.name or any(ord(char) < 32 for char in path.name):
                raise PackagingError("unsafe archive filename")
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                raise PackagingError("symlink entry is not allowed: " + path.name)
            if stat.S_ISDIR(mode):
                pending.append(path)
            elif not stat.S_ISREG(mode):
                raise PackagingError("nonregular entry is not allowed: " + path.name)
            elif path.suffix == ".md":
                documents[path] = path.read_bytes()
    return documents


def package_skills(repository_root: Path, output_directory: Path) -> dict:
    """Package the two allowlisted Markdown skill trees without rewriting text."""
    root = Path(repository_root).absolute()
    output = Path(output_directory).absolute()
    _reject_symlink_components(root)
    _reject_symlink_components(output)
    root = root.resolve()
    output = output.resolve()
    if output == root or root in output.parents or output in root.parents:
        raise PackagingError("output must be outside the repository and its ancestors")
    if output.exists():
        raise PackagingError("output already exists; choose a new directory")
    snapshots = {}
    for name in SKILL_NAMES:
        skill_root = root / "skills" / name
        snapshots[name] = _snapshot(skill_root)
        required = ["SKILL.md"] + ["references/" + filename for filename in REQUIRED_REFERENCES[name]]
        for relative in required:
            if skill_root / relative not in snapshots[name]:
                raise PackagingError("missing required document: " + name + "/" + relative)
            if not snapshots[name][skill_root / relative].strip():
                raise PackagingError("empty required document: " + name + "/" + relative)
        text = snapshots[name][skill_root / "SKILL.md"].decode("utf-8")
        lines = text.splitlines()
        if not lines or lines[0] != "---" or "---" not in lines[1:]:
            raise PackagingError("invalid frontmatter: " + name)
        closing = lines.index("---", 1)
        frontmatter = "\n".join(lines[1:closing])
        if not re.search(r"(?m)^name:\s*" + re.escape(name) + r"\s*$", frontmatter):
            raise PackagingError("invalid skill name: " + name)
        if not re.search(r"(?m)^description:\s*\S", frontmatter) or not "\n".join(lines[closing + 1:]).strip():
            raise PackagingError("missing description or body: " + name)
        documents = {path.resolve() for path in snapshots[name]}
        for path, data in snapshots[name].items():
            _validate_links(path, skill_root, documents, data.decode("utf-8"))
    manifest = {
        "schema_version": 1,
        "status": "preview",
        "limitations": ["not an official release", "not APA 7 certification"],
        "packages": [],
    }
    artifacts = {}
    for name in SKILL_NAMES:
        buffer = io.BytesIO()
        files = []
        skill_root = root / "skills" / name
        with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_STORED) as archive:
            for path in sorted(snapshots[name], key=lambda item: item.relative_to(skill_root).as_posix()):
                member = name + "/" + path.relative_to(skill_root).as_posix()
                data = snapshots[name][path]
                info = zipfile.ZipInfo(member, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                archive.writestr(info, data)
                files.append({"path": member, "size": len(data), "sha256": hashlib.sha256(data).hexdigest()})
        artifact = name + "-preview.zip"
        artifacts[artifact] = buffer.getvalue()
        manifest["packages"].append({
            "skill": name, "artifact": artifact,
            "sha256": hashlib.sha256(artifacts[artifact]).hexdigest(), "files": files,
        })
    artifacts["manifest.json"] = (json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    _reject_symlink_components(output)
    output.mkdir(parents=True, exist_ok=False)
    try:
        for filename, data in artifacts.items():
            (output / filename).write_bytes(data)
    except BaseException:
        shutil.rmtree(output)
        raise
    return manifest


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Build two deterministic preview skill ZIPs (not an official release).")
    parser.add_argument("--output", required=True, type=Path, help="New directory outside the repository; existing paths are never overwritten.")
    args = parser.parse_args(argv)
    try:
        package_skills(Path(__file__).resolve().parents[1], args.output)
    except PackagingError as error:
        print("preview packaging failed: " + str(error), file=sys.stderr)
        return 1
    except (OSError, UnicodeError, ValueError):
        print("preview packaging failed: unreadable input or output", file=sys.stderr)
        return 1
    print("preview packaging: 2 ZIPs and manifest.json created (not an official release)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
