#!/usr/bin/env python3
"""Check that source IDs cited by a shipped skill are defined in a ledger.

Each skill is packaged independently, so its source IDs must resolve in its own
``references/source-ledger.md``. A pointer to the other skill's ledger is
allowed only when the IDs are qualified with that skill name in the same prose
run, e.g. ``korean-editing K2`` or ``korean-editing M-HANI1–4, M-HEO1``.
Run: uv run --locked python tests/source_traceability_test.py

Recognized citation forms (prose only; CommonMark code, HTML, link
destinations and bare URLs are skipped, and prose runs break at line ends):

- a ledger family followed by a number, e.g. ``N-Q3``, ``S8``, ``P-SONG2008``.
  Families are derived from the IDs the two ledgers define;
- an atomic ledger name, e.g. ``A-REF``, or an unknown name with a registered
  atomic prefix, e.g. ``A-STU``;
- an unknown hyphenated family with a number, e.g. ``B-NEW1``;
- ranges with ``–``, ``-``, ``~`` or ``—`` (optionally spaced) and lists with
  ``·`` or ``/``. Descending ranges and ranges longer than 50 are rejected;
  four-digit numbers (years) are endpoints, not expanded.

Unknown single-letter tokens such as ``A4`` or ``X9`` are not recognized, and
unqualified ``H`` numbers in the APA skill are read as hypotheses. This is a
citation-to-ledger gate for the forms above. It does not prove that a ledger
entry was read correctly or that a rule is supported by its source.
"""
from __future__ import annotations

import re
from pathlib import Path

from markdown_it import MarkdownIt

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("korean-editing", "apa7-manuscript-writing")

# Abbreviations whose definition sentence must stay in the named ledger entry.
ALIASES = {
    "korean-editing": {"N41": "K2", "N42": "K2", "N43": "K2"},
}
ALIAS_DEFINITION_TEXT = {("korean-editing", "K2"): "N41·N42·N43"}
# In APA prose an unqualified H1–H5 normally means hypotheses.
EXCLUDED_UNQUALIFIED_FAMILIES = {"apa7-manuscript-writing": {"H"}}
MAX_RANGE = 50

# A ledger ID has a number (S1, N-Q3) or a hyphenated family name (A-REF,
# U-KHU). Field labels such as ``URL`` or ``SHA-256`` are not definitions:
# every hyphenated segment of an ID must contain a letter.
ID_NAME = r"(?:[A-Z][A-Z0-9]*(?:-[A-Z0-9]*[A-Z][A-Z0-9]*)+|[A-Z]+\d+)"
HEADING_DEFINITION = re.compile(rf"^##\s+({ID_NAME})\s+·")
# Only an explicit 과/와 joiner adds a second ID to the same heading.
HEADING_JOINED_DEFINITION = re.compile(rf"(?:과|와)\s+({ID_NAME})\s+·")
TABLE_DEFINITION = re.compile(rf"^\|\s*({ID_NAME})\s*\|")
BULLET_DEFINITION = re.compile(rf"^-\s+({ID_NAME}):")

# A bare name must not continue as ``-digits`` (SHA-256, UTF-8, COVID-19).
TOKEN = re.compile(
    r"(?<![A-Za-z0-9_%/.#-])(?P<name>[A-Z]+(?:-[A-Z]+)*)(?P<digits>\d+)?"
    r"(?(digits)(?![A-Za-z0-9_])|(?![A-Za-z0-9_]|-[A-Za-z0-9]))"
)
RANGE_TAIL = r"[ \t]?[–~—-][ \t]?(?:{family})?(\d+)(?![A-Za-z0-9_]|\.\d)"
LIST_TAIL = r"[·/](?:{family})?(\d+)(?![A-Za-z0-9_]|\.\d)"
CARRY_GAP = re.compile(r"[ \t]*[·,][ \t]*")
QUALIFIER_BEFORE = re.compile(r"(?:^|[^A-Za-z0-9-])(korean-editing|apa7-manuscript-writing)[ \t]+$")
URL = re.compile(r"<?https?://[^\s)>|]+>?")


def family_of(identifier: str) -> str:
    return re.sub(r"\d+$", "", identifier)


def ledger_definitions(ledger_text: str) -> tuple[dict[str, int], list[str]]:
    """Return defined IDs with their one-based line and duplicate errors."""
    defined: dict[str, int] = {}
    errors: list[str] = []
    for number, line in enumerate(ledger_text.splitlines(), 1):
        found: list[str] = []
        if line.startswith("## "):
            first = HEADING_DEFINITION.match(line)
            if first:
                found = [first.group(1), *HEADING_JOINED_DEFINITION.findall(line, first.end())]
        else:
            for pattern in (TABLE_DEFINITION, BULLET_DEFINITION):
                match = pattern.match(line)
                if match:
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
        match = HEADING_DEFINITION.match(line)
        if match and match.group(1) == identifier:
            end = next((j for j in range(index + 1, len(lines)) if lines[j].startswith("## ")), len(lines))
            return "\n".join(lines[index:end])
    return ""


def prose_segments(text: str) -> list[tuple[int, str]]:
    """Return (one-based line, text) prose runs from CommonMark inline text.

    Runs break at line ends, code, HTML, link boundaries and bare URLs, so a
    qualifier cannot carry across them.
    """
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        closing = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
        if closing is not None:
            lines[: closing + 1] = [""] * (closing + 1)
    segments: list[tuple[int, str]] = []
    for token in MarkdownIt("commonmark").parse("\n".join(lines)):
        if token.type != "inline" or token.map is None:
            continue
        line = token.map[0] + 1
        buffer: list[str] = []

        def flush() -> None:
            joined = "".join(buffer)
            buffer.clear()
            segments.extend((line, part) for part in URL.split(joined) if part.strip())

        for child in token.children or []:
            if child.type == "text":
                buffer.append(child.content)
            elif child.type in {"softbreak", "hardbreak"}:
                flush()
                line += 1
            elif child.type in {"em_open", "em_close", "strong_open", "strong_close"}:
                continue
            else:
                flush()
        flush()
    return segments


class _Index:
    """Defined IDs and numbered families derived from both ledgers."""

    def __init__(self, ledgers: dict[str, dict[str, int]]):
        self.defined = ledgers
        self.numbered: dict[str, set[str]] = {}
        self.atomic_prefixes: set[str] = set()
        for skill, defined in ledgers.items():
            names = set(defined) | set(ALIASES.get(skill, {}))
            self.numbered[skill] = {family_of(name) for name in names if re.search(r"\d$", name)}
            self.atomic_prefixes |= {name.split("-")[0] for name in names if "-" in name and not re.search(r"\d$", name)}
        self.all_numbered = set().union(*self.numbered.values())

    def is_defined(self, skill: str, identifier: str) -> bool:
        return ALIASES.get(skill, {}).get(identifier, identifier) in self.defined.get(skill, {})


def _expand(prose: str, end: int, family: str, digits: str) -> tuple[list[str], int, str | None]:
    """Expand a range or list that follows ``family+digits`` at ``end``."""
    identifiers = [family + digits]
    escaped = re.escape(family)
    ranged = re.compile(RANGE_TAIL.format(family=escaped)).match(prose, end)
    if ranged:
        stop_digits = ranged.group(1)
        start, stop = int(digits), int(stop_digits)
        end = ranged.end()
        if len(digits) >= 4 or len(stop_digits) >= 4:
            identifiers.append(family + stop_digits)
        elif stop < start:
            return identifiers, end, f"descending range {family}{digits}–{stop_digits}"
        elif stop - start > MAX_RANGE:
            return identifiers, end, f"range {family}{digits}–{stop_digits} is longer than {MAX_RANGE}"
        else:
            identifiers = [family + str(n) for n in range(start, stop + 1)]
    listed = re.compile(LIST_TAIL.format(family=escaped))
    while item := listed.match(prose, end):
        identifiers.append(family + item.group(1))
        end = item.end()
    return identifiers, end, None


def check_document(text: str, skill: str, index: _Index) -> list[tuple[int, str]]:
    """Return (line, message) errors for one skill document."""
    errors: list[tuple[int, str]] = []
    excluded = EXCLUDED_UNQUALIFIED_FAMILIES.get(skill, set())
    for line, prose in prose_segments(text):
        carry: str | None = None
        position = 0
        for match in TOKEN.finditer(prose):
            if match.start() < position:
                continue
            family, digits = match.group("name"), match.group("digits") or ""
            qualified = QUALIFIER_BEFORE.search(prose, 0, match.start())
            if qualified:
                owner: str | None = qualified.group(1)
            elif (
                carry
                and CARRY_GAP.fullmatch(prose[position:match.start()])
                and family in index.numbered.get(carry, set()) | set(index.defined.get(carry, {}))
            ):
                owner = carry
            else:
                owner = None
            context = owner or skill
            if digits:
                known = family in index.all_numbered
                if (known and owner is None and family in excluded) or (not known and "-" not in family):
                    position, carry = match.end(), None
                    continue
                identifiers, position, malformed = _expand(prose, match.end(), family, digits)
                if malformed:
                    errors.append((line, f"malformed source ID {malformed}"))
            else:
                position = match.end()
                if "-" in family and family in index.numbered.get(context, set()):
                    carry = owner  # bare family reference such as M-HANI
                    continue
                atomic = family.split("-")[0] in index.atomic_prefixes and re.fullmatch(r"[A-Z]+(?:-[A-Z]{2,})+", family)
                if not (atomic or family in index.defined.get(context, {})):
                    carry = None
                    continue
                identifiers = [family]
            carry = owner
            for identifier in identifiers:
                if index.is_defined(context, identifier):
                    continue
                if owner is None and any(index.is_defined(other, identifier) for other in SKILLS if other != skill):
                    errors.append((line, f"{identifier} belongs to another skill ledger; qualify it with that skill name"))
                else:
                    errors.append((line, f"source ID {identifier} is not defined in {context} ledger"))
    return errors


def validate_repository(root: Path) -> list[str]:
    """Validate both skills under ``root`` and return human-readable errors."""
    texts: dict[str, str] = {}
    ledgers: dict[str, dict[str, int]] = {}
    errors: list[str] = []
    for skill in SKILLS:
        ledger_path = root / "skills" / skill / "references" / "source-ledger.md"
        if not ledger_path.is_file():
            errors.append(f"{skill}: missing references/source-ledger.md")
            continue
        texts[skill] = ledger_path.read_text(encoding="utf-8")
        ledgers[skill], duplicate_errors = ledger_definitions(texts[skill])
        errors.extend(f"{skill}: {error}" for error in duplicate_errors)
    for skill, ledger_text in texts.items():
        for alias, target in ALIASES.get(skill, {}).items():
            if ALIAS_DEFINITION_TEXT[(skill, target)] not in _ledger_section(ledger_text, target):
                errors.append(f"{skill}: alias {alias} lost its definition in ledger entry {target}")
    index = _Index(ledgers)
    for skill in ledgers:
        for document in sorted((root / "skills" / skill).rglob("*.md")):
            relative = document.relative_to(root)
            for line, message in check_document(document.read_text(encoding="utf-8"), skill, index):
                errors.append(f"{relative}:{line}: {message}")
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
