#!/usr/bin/env python3
"""Validate the public structure and local links of both Agent Skills.

Use the locked dependencies: uv run --locked python tests/skill_structure_test.py.
This structure gate checks actual CommonMark destinations, not code examples
or HTML admission; the separate preview packager has a stricter policy.
"""
from __future__ import annotations

from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from markdown_it import MarkdownIt


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILL_PATHS = (
    REPOSITORY_ROOT / "skills" / "korean-editing" / "SKILL.md",
    REPOSITORY_ROOT / "skills" / "apa7-manuscript-writing" / "SKILL.md",
)


def markdown_destinations(text: str) -> list[str]:
    """Collect rendered links/images and reference definitions via CommonMark."""
    parser = MarkdownIt("commonmark")
    # Collect even destinations suppressed by the default renderer policy.
    parser.validateLink = lambda target: True
    environment = {}
    tokens = parser.parse(text, environment)
    targets = [item["href"] for item in environment.get("references", {}).values()]
    targets.extend(item["href"] for item in environment.get("duplicate_refs", []))
    pending = list(tokens)
    while pending:
        token = pending.pop()
        if token.type in {"link_open", "image"}:
            target = token.attrGet("href" if token.type == "link_open" else "src")
            if target is not None:
                targets.append(target)
        pending.extend(token.children or [])
    return targets


def validate_skill(skill_path: Path) -> list[str]:
    """Return structural errors for one public Agent Skill."""
    errors: list[str] = []
    skill_root = skill_path.parent.resolve()
    text = skill_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return [f"{skill_path}: missing YAML frontmatter"]
    try:
        closing_index = lines.index("---", 1)
    except ValueError:
        return [f"{skill_path}: unterminated YAML frontmatter"]
    frontmatter = "\n".join(lines[1:closing_index])
    try:
        metadata = yaml.safe_load(frontmatter)
    except yaml.YAMLError:
        errors.append(f"{skill_path}: invalid YAML frontmatter")
        metadata = None
    if not isinstance(metadata, dict):
        errors.append(f"{skill_path}: frontmatter must be a mapping")
    else:
        for field_name in ("name", "description"):
            value = metadata.get(field_name)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{skill_path}: missing or invalid {field_name} frontmatter")
    for document_path in skill_root.rglob("*.md"):
        document_text = document_path.read_text(encoding="utf-8")
        if document_path == skill_path:
            document_text = "\n".join(lines[closing_index + 1:])
        for target in markdown_destinations(document_text):
            parts = urlsplit(target)
            if parts.scheme.lower() in {"http", "https", "mailto"}:
                continue
            if parts.scheme or parts.netloc:
                errors.append(f"{document_path}: unsupported link scheme {target}")
                continue
            relative_target = unquote(parts.path)
            resolved_target = (document_path.parent / relative_target).resolve()
            try:
                resolved_target.relative_to(skill_root)
            except ValueError:
                errors.append(f"{document_path}: link leaves skill package {target}")
                continue
            if relative_target and not resolved_target.exists():
                errors.append(f"{document_path}: broken local link {target}")
    return errors


def main() -> int:
    """Validate both shipped skills and print a bounded result."""
    errors = [error for skill_path in SKILL_PATHS for error in validate_skill(skill_path)]
    if errors:
        print("\n".join(errors))
        return 1
    print("skill structure contract: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
