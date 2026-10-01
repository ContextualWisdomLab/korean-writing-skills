#!/usr/bin/env python3
"""Validate the public structure and local links of both Agent Skills."""

from __future__ import annotations

import re
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILL_PATHS = (
    REPOSITORY_ROOT / "skills" / "korean-editing" / "SKILL.md",
    REPOSITORY_ROOT / "skills" / "apa7-manuscript-writing" / "SKILL.md",
)
MARKDOWN_LINK = re.compile(r"\[[^]]*]\(([^)]+)\)")


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
    for field_name in ("name", "description"):
        if not re.search(rf"(?m)^{field_name}:\s*\S", frontmatter):
            errors.append(f"{skill_path}: missing {field_name} frontmatter")
    for target in MARKDOWN_LINK.findall(text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        relative_target = target.split("#", 1)[0]
        resolved_target = (skill_path.parent / relative_target).resolve()
        try:
            resolved_target.relative_to(skill_root)
        except ValueError:
            errors.append(f"{skill_path}: link leaves skill package {target}")
            continue
        if relative_target and not resolved_target.exists():
            errors.append(f"{skill_path}: broken local link {target}")
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
