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
  Families are derived from the IDs the two ledgers define, plus the committed
  ``BASELINE_FAMILIES``, so deleting a whole family does not hide its citations;
- an atomic ledger name, e.g. ``A-REF``, or an unknown name with a registered
  atomic prefix, e.g. ``A-STU``;
- an unknown hyphenated family with a number, e.g. ``B-NEW1``;
- ranges with ``–``, ``-``, ``~`` or ``—`` and lists with ``·``, ``/`` or
  ``,``. A spaced range (``S1 – 12``) or a comma item (``S1, 12``) without the
  family name counts only when the number is not followed by a Hangul word
  other than a particle, so ``K2 – 9개`` and ``G1, 2023년`` stay prose.
  Descending ranges and ranges longer than 50 are rejected; an ascending range
  whose two ends both have four digits (years) is checked at its ends only.

Prose includes link text and image alt text. Unknown families without a
hyphen, such as ``A4``, ``X9``, ``KS9`` or ``PDF1``, are not recognized, and
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
# Unhyphenated families that stay recognized even if a ledger loses them all.
BASELINE_FAMILIES = frozenset({"E", "G", "H", "J", "K", "N", "S", "U"})

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
NUMBER_END = r"(?![A-Za-z0-9_]|\.\d)"
# A bare number in a spaced range or comma list must not start a Hangul word
# (9개, 2023년); a following particle (12에서, 12은) is allowed.
BARE_NUMBER_END = NUMBER_END + r"(?![가-힣])|(?=[은는이가을를과와의에도로만])"
RANGE_TAIL = (
    r"(?:[–~—-]|[ \t][–~—-]|[–~—-][ \t]|[ \t][–~—-][ \t])(?:{family}(\d+)" + NUMBER_END + r"|(?<=[–~—-])(\d+)" + NUMBER_END
    + r"|(?<=[ \t])(\d+)(?:" + BARE_NUMBER_END + r"))"
)
LIST_TAIL = (
    r"(?:[·/](?:{family})?(\d+)" + NUMBER_END + r"|,(?![ \t]*(?:[A-Z]+(?:-[A-Z]+)*\d+)?[ \t]*[–~—-])[ \t]*(?:{family}(\d+)" + NUMBER_END
    + r"|(\d+)(?:" + BARE_NUMBER_END + r")))"
)
CARRY_GAP = re.compile(r"[ \t\u00a0]*[·,][ \t\u00a0]*")
QUALIFIER_BEFORE = re.compile(r"(?<![A-Za-z0-9-])(korean-editing|apa7-manuscript-writing)[ \t\u00a0]+$")
QUALIFIER_WINDOW = 64
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
            elif child.type == "image":
                flush()
                buffer.append("".join(c.content for c in child.children or [] if c.type == "text"))
                flush()
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
        self.all_numbered = set().union(BASELINE_FAMILIES, *self.numbered.values())

    def is_defined(self, skill: str, identifier: str) -> bool:
        return ALIASES.get(skill, {}).get(identifier, identifier) in self.defined.get(skill, {})


def _expand(prose: str, end: int, family: str, digits: str) -> tuple[list[str], int, str | None]:
    """Expand a range or list that follows ``family+digits`` at ``end``."""
    identifiers = [family + digits]
    escaped = re.escape(family)
    ranged = re.compile(RANGE_TAIL.format(family=escaped)).match(prose, end)
    if ranged:
        stop_digits = next(group for group in ranged.groups() if group)
        start, stop = int(digits), int(stop_digits)
        end = ranged.end()
        if len(digits) >= 4 and len(stop_digits) >= 4 and start <= stop:
            identifiers.append(family + stop_digits)
        elif stop < start:
            return identifiers, end, f"descending range {family}{digits}–{stop_digits}"
        elif stop - start > MAX_RANGE:
            return identifiers, end, f"range {family}{digits}–{stop_digits} is longer than {MAX_RANGE}"
        else:
            identifiers = [family + str(n) for n in range(start, stop + 1)]
    listed = re.compile(LIST_TAIL.format(family=escaped))
    ranged_after = re.compile(RANGE_TAIL.format(family=escaped))
    previous_text = identifiers[-1][len(family):]
    previous = int(previous_text)
    errors: list[str] = []
    while True:
        year_tail = re.match(r"[·/](\d{4,})(?![A-Za-z0-9_]|\.\d)", prose[end:])
        if year_tail and int(year_tail.group(1)) < previous:
            errors.append(f"descending range {family}{previous}–{year_tail.group(1)}")
            identifiers.append(family + year_tail.group(1))
            previous_text = year_tail.group(1)
            previous = int(previous_text)
            end += year_tail.end()
            continue
        item = listed.match(prose, end)
        if item:
            number = next(group for group in item.groups() if group)
            identifiers.append(family + number)
            previous = int(number)
            end = item.end()
            continue
        nxt = ranged_after.match(prose, end)
        if nxt is None:
            break
        number = next(group for group in nxt.groups() if group)
        stop = int(number)
        end = nxt.end()
        if stop < previous:
            errors.append(f"descending range {family}{previous}–{number}")
            identifiers.append(family + number)
        elif len(number) >= 4 and len(previous_text) >= 4 and int(number) >= previous:
            identifiers.append(family + number)
        elif stop - previous > MAX_RANGE:
            errors.append(f"range {family}{previous}–{number} is longer than {MAX_RANGE}")
            identifiers.append(family + number)
        else:
            identifiers.extend(family + str(n) for n in range(previous + 1, stop + 1))
        previous, previous_text = stop, number
    return identifiers, end, "; ".join(errors) or None


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
            qualified = QUALIFIER_BEFORE.search(prose, max(0, match.start() - QUALIFIER_WINDOW), match.start())
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
