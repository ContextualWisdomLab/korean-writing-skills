#!/usr/bin/env python3
"""Check that every source ID cited by a shipped skill is defined in a ledger.

Each skill is packaged independently, so its source IDs must resolve in its own
``references/source-ledger.md``. A pointer to the other skill's ledger is
allowed only when the IDs are immediately qualified with that skill name, e.g.
``korean-editing K2``. Run: uv run --locked python tests/source_traceability_test.py

This is a citation-to-ledger gate. It does not prove that a ledger entry was
read correctly or that a rule is supported by its source.
"""
from __future__ import annotations

import re
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("korean-editing", "apa7-manuscript-writing")

# ID families owned by each skill. Single letters need a number; hyphenated
# families may appear bare (for example ``M-HANI``) as a family reference.
MULTI_FAMILIES = {
    "korean-editing": ("M-HANI", "M-HEO", "B-KBS", "U-KUPIS", "U-KHU", "P-SONG", "E-AKS", "N-Q"),
    "apa7-manuscript-writing": ("U-KHU",),
}
SINGLE_FAMILIES = {
    "korean-editing": ("K", "H", "G", "J", "E", "U", "N"),
    "apa7-manuscript-writing": ("S",),
}
# APA guide IDs are atomic uppercase names such as A-REF or A-SECONDARY-WEB.
APA_NAME = r"A-[A-Z]+(?:-[A-Z]+)*"
# Abbreviations whose definition sentence must stay in the named ledger entry.
ALIASES = {
    "korean-editing": {"N41": "K2", "N42": "K2", "N43": "K2"},
}
ALIAS_DEFINITION_TEXT = {("korean-editing", "K2"): "N41·N42·N43"}
# In APA prose H1–H5 normally means hypotheses, not the Korean ledger's H1.
EXCLUDED_SINGLE = {"apa7-manuscript-writing": {"H"}}

# A ledger ID has a number (S1, N-Q3) or a hyphenated family name (A-REF,
# U-KHU). Field labels such as ``- URL:`` or ``- SHA-256:`` are not
# definitions: every hyphenated segment of an ID must contain a letter.
ID_NAME = r"(?:[A-Z][A-Z0-9]*(?:-[A-Z0-9]*[A-Z][A-Z0-9]*)+|[A-Z]+\d+)"
HEADING_DEFINITION = re.compile(rf"({ID_NAME})\s+·")
TABLE_DEFINITION = re.compile(rf"^\|\s*({ID_NAME})\s*\|")
BULLET_DEFINITION = re.compile(rf"^-\s+({ID_NAME}):")


def _token_pattern(skill: str) -> re.Pattern[str]:
    multi = set(MULTI_FAMILIES["korean-editing"]) | set(MULTI_FAMILIES["apa7-manuscript-writing"])
    single = set(SINGLE_FAMILIES["korean-editing"]) | set(SINGLE_FAMILIES["apa7-manuscript-writing"])
    single -= EXCLUDED_SINGLE.get(skill, set())
    multi_alt = "|".join(sorted((re.escape(f) for f in multi), key=len, reverse=True))
    single_alt = "|".join(sorted(single))
    return re.compile(
        rf"(?<![A-Za-z0-9_%/.#-])(?:(?P<apa>{APA_NAME})|(?P<multi>{multi_alt})(?P<mdigits>\d*)"
        rf"|(?P<single>{single_alt})(?P<sdigits>\d+))(?![A-Za-z0-9_])"
    )


def _strip_non_prose(text: str) -> str:
    """Blank code, link destinations and URLs while keeping line positions."""
    blank = lambda match: re.sub(r"[^\n]", " ", match.group(0))
    text = re.sub(r"(?ms)^(```|~~~).*?^\1[^\n]*$", blank, text)
    text = re.sub(r"`[^`\n]*`", blank, text)
    text = re.sub(r"\]\([^)\n]*\)", blank, text)
    text = re.sub(r"<?https?://[^\s)>|]+>?", blank, text)
    return text


def ledger_definitions(ledger_text: str) -> tuple[dict[str, int], list[str]]:
    """Return defined IDs with their one-based line and duplicate errors."""
    defined: dict[str, int] = {}
    errors: list[str] = []
    for number, line in enumerate(ledger_text.splitlines(), 1):
        found: list[str] = []
        if line.startswith("## "):
            found = HEADING_DEFINITION.findall(line)
        else:
            for pattern in (TABLE_DEFINITION, BULLET_DEFINITION):
                match = pattern.match(line)
                if match and match.group(1) != "ID":
                    found.append(match.group(1))
        for identifier in found:
            if identifier in defined:
                errors.append(f"duplicate ledger ID {identifier} at lines {defined[identifier]} and {number}")
            else:
                defined[identifier] = number
    return defined, errors


def _ledger_section(ledger_text: str, identifier: str) -> str:
    lines = ledger_text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("## ") and identifier in HEADING_DEFINITION.findall(line):
            end = next((j for j in range(index + 1, len(lines)) if lines[j].startswith("## ")), len(lines))
            return "\n".join(lines[index:end])
    return ""


def cited_ids(text: str, skill: str) -> list[tuple[int, str, str | None]]:
    """Return (line, ID, qualifier skill or None) for every source-ID citation."""
    prose = _strip_non_prose(text)
    pattern = _token_pattern(skill)
    results: list[tuple[int, str, str | None]] = []
    previous_end = 0
    qualifier: str | None = None
    for match in pattern.finditer(prose):
        gap = prose[previous_end:match.start()]
        if qualifier and re.fullmatch(r"[\s·,]*", gap):
            pass
        else:
            qualified = re.search(r"(korean-editing|apa7-manuscript-writing)\s+$", gap)
            qualifier = qualified.group(1) if qualified else None
        line = prose.count("\n", 0, match.start()) + 1
        if match.group("apa"):
            identifiers = [match.group("apa")]
        else:
            family = match.group("multi") or match.group("single")
            digits = match.group("mdigits") if match.group("multi") else match.group("sdigits")
            identifiers = [family + digits] if digits or match.group("multi") else []
            end = match.end()
            if digits:
                family_ref = re.escape(family)
                span = re.compile(rf"[–-](?:{family_ref})?(\d+)(?![A-Za-z0-9_.])")
                listed = re.compile(rf"·(?:{family_ref})?(\d+)(?![A-Za-z0-9_.])")
                ranged = span.match(prose, end)
                if ranged and int(ranged.group(1)) > int(digits):
                    identifiers = [family + str(n) for n in range(int(digits), int(ranged.group(1)) + 1)]
                    end = ranged.end()
                while item := listed.match(prose, end):
                    identifiers.append(family + item.group(1))
                    end = item.end()
            previous_end = end
        if match.group("apa"):
            previous_end = match.end()
        results.extend((line, identifier, qualifier) for identifier in identifiers)
    return results


def validate_repository(root: Path) -> list[str]:
    """Validate both skills under ``root`` and return human-readable errors."""
    ledgers: dict[str, tuple[str, dict[str, int]]] = {}
    errors: list[str] = []
    for skill in SKILLS:
        ledger_path = root / "skills" / skill / "references" / "source-ledger.md"
        if not ledger_path.is_file():
            errors.append(f"{skill}: missing references/source-ledger.md")
            continue
        text = ledger_path.read_text(encoding="utf-8")
        defined, duplicate_errors = ledger_definitions(text)
        errors.extend(f"{skill}: {error}" for error in duplicate_errors)
        ledgers[skill] = (text, defined)
    for skill, (ledger_text, defined) in ledgers.items():
        for alias, target in ALIASES.get(skill, {}).items():
            required = ALIAS_DEFINITION_TEXT[(skill, target)]
            if required not in _ledger_section(ledger_text, target):
                errors.append(f"{skill}: alias {alias} lost its definition in ledger entry {target}")
    for skill in ledgers:
        for document in sorted((root / "skills" / skill).rglob("*.md")):
            relative = document.relative_to(root)
            for line, identifier, qualifier in cited_ids(document.read_text(encoding="utf-8"), skill):
                owner = qualifier or skill
                if owner not in ledgers:
                    continue
                ledger_text, defined = ledgers[owner]
                target = ALIASES.get(owner, {}).get(identifier, identifier)
                family_members = [name for name in defined if name.startswith(identifier)]
                bare_family = identifier in MULTI_FAMILIES.get(owner, ()) and family_members
                if target in defined or bare_family:
                    continue
                where = f"{relative}:{line}"
                if qualifier is None and any(
                    ALIASES.get(other, {}).get(identifier, identifier) in data[1]
                    for other, data in ledgers.items() if other != skill
                ):
                    errors.append(f"{where}: {identifier} belongs to another skill ledger; qualify it with that skill name")
                else:
                    errors.append(f"{where}: source ID {identifier} is not defined in {owner} ledger")
    return errors


def main() -> int:
    errors = validate_repository(REPOSITORY_ROOT)
    if errors:
        print("\n".join(errors))
        return 1
    print("source traceability contract: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
