"""RED/GREEN contracts for the rule-to-source traceability gate."""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("source_traceability", ROOT / "tests/source_traceability_test.py")
trace = importlib.util.module_from_spec(spec)
spec.loader.exec_module(trace)

KOREAN_LEDGER = """# 출처 장부

## K2 · 어문 규정
이 셋을 N41·N42·N43으로 예문에서 표시한다.

## E1 · 편집 판단과 U1 · 사용자 선호

## H1 · 설치본 참고

## N-Q1 · 상담
## N-Q2 · 상담
## N-Q3 · 상담
## M-HANI1 · 신문
## M-HANI2 · 신문
## M-HEO1 · 신문
## U-KHU2 · 대학
## U-KHU3 · 대학
## P-SONG2008 · 학술
## P-SONG2013 · 학술
## G1 · 저자
## G2 · 저자
"""

APA_LEDGER = """# 근거 장부

| ID | 자료 |
| --- | --- |
| S1 | 안내 |
| S2 | 안내 |
| A-BIAS-WEB | 웹 |

- A-REF: 안내
- A-NUM: 안내

## U-KHU · 대학 교육 자료
"""


class TraceabilityContracts(unittest.TestCase):
    def check(self, korean_text="", apa_text="", korean_ledger=KOREAN_LEDGER, apa_ledger=APA_LEDGER):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for skill, ledger, text in (
                ("korean-editing", korean_ledger, korean_text),
                ("apa7-manuscript-writing", apa_ledger, apa_text),
            ):
                references = root / "skills" / skill / "references"
                references.mkdir(parents=True)
                (references / "source-ledger.md").write_text(ledger, encoding="utf-8")
                (root / "skills" / skill / "SKILL.md").write_text(
                    "---\nname: sample\ndescription: valid\n---\n" + text, encoding="utf-8"
                )
            return trace.validate_repository(root)

    def assertRejected(self, **documents):
        self.assertTrue(self.check(**documents), documents)

    def assertAccepted(self, **documents):
        self.assertEqual([], self.check(**documents))

    # RED: an undefined source ID must fail.
    def test_undefined_korean_ids_are_rejected(self):
        for text in ("규정(N44)", "N-Q4", "U-KHU5", "E-AKS2", "N-Q1–4", "M-HANI2·5"):
            with self.subTest(text=text):
                self.assertRejected(korean_text=text)

    def test_undefined_apa_ids_are_rejected(self):
        for text in ("S10", "A-FOO", "A-STU"):
            with self.subTest(text=text):
                self.assertRejected(apa_text=text)

    def test_unqualified_cross_skill_id_is_rejected(self):
        for text in ("M-HANI1", "| G1 | 저자 |"):
            with self.subTest(text=text):
                self.assertRejected(apa_text=text)

    def test_qualified_cross_skill_id_must_exist_in_owner_ledger(self):
        self.assertRejected(apa_text="korean-editing G3")

    def test_alias_drift_is_rejected(self):
        ledger = KOREAN_LEDGER.replace("이 셋을 N41·N42·N43으로 예문에서 표시한다.", "")
        self.assertRejected(korean_text="N41", korean_ledger=ledger)

    def test_field_labels_are_not_definitions(self):
        ledger = KOREAN_LEDGER + "\n- URL: https://example.org\n- SHA-256: `abc`\n- SHA-256: `def`\n"
        self.assertAccepted(korean_ledger=ledger)
        self.assertNotIn("SHA-256", trace.ledger_definitions(ledger)[0])

    def test_duplicate_definition_is_rejected(self):
        self.assertRejected(korean_ledger=KOREAN_LEDGER + "\n## G1 · 다른 저자\n")

    # GREEN controls.
    def test_ranges_lists_and_aliases_are_accepted(self):
        self.assertAccepted(
            korean_text="N41–43, N41·N42, N-Q1–3, G1–G2, U-KHU2·3, P-SONG2008·2013, E1, U1, 출처 장부의 H1",
            apa_text="S1-S2, S1–2, A-REF·A-NUM, A-BIAS-WEB, U-KHU",
        )

    def test_qualified_cross_skill_ids_are_accepted(self):
        self.assertAccepted(apa_text="| korean-editing G1 | 저자 |\nkorean-editing N-Q1·N-Q2, korean-editing U-KHU2·3")

    def test_non_source_tokens_are_ignored(self):
        self.assertAccepted(
            korean_text="2.18–2.24, 7.17, Table 2–8, A4, SHA-256, `#2091은`, `W2091`, `d54ac2805e`, *N*, *SD*, "
            "[원문](https://example.org/a%B3%A0K9.pdf), https://doi.org/10.1037/amp0000191\n\n```\nN-Q9\n```\n",
            apa_text="H1: 가설 예시. H5도 가설이다.",
        )

    def test_bare_family_name_is_accepted_when_a_member_exists(self):
        self.assertAccepted(korean_text="M-HANI·M-HEO 권고")

    # Review 94385d6 D1: a qualifier must not leak past a line, blank line,
    # link, URL or code span, nor onto another skill's family.
    def test_qualifier_does_not_leak(self):
        for text in (
            "korean-editing G1\n\nE1 규칙을 적용한다.",
            "korean-editing G1\nE1 규칙",
            "[korean-editing G1](https://example.org) E1",
            "korean-editing G1 https://example.org E1",
            "korean-editing G1 `x`, E1",
            "korean-editing G1 그리고 E1",
        ):
            with self.subTest(text=text):
                self.assertRejected(apa_text=text)

    def test_qualifier_does_not_capture_own_family(self):
        self.assertAccepted(apa_text="korean-editing G1, S2")
        self.assertAccepted(apa_text="korean-editing M-HANI1–2, M-HEO1")

    # D2: sentence-final ranges and lists must keep their end.
    def test_sentence_final_ranges_and_lists_are_checked(self):
        for text in ("상담 N-Q1–5.", "칼럼 M-HANI1·5.", "근거는 N-Q1–N-Q4. 끝"):
            with self.subTest(text=text):
                self.assertRejected(korean_text=text)
        for text in ("근거는 S1-S12.", "S1–S3. 끝"):
            with self.subTest(text=text):
                self.assertRejected(apa_text=text)
        self.assertAccepted(korean_text="상담 N-Q1–3. 칼럼 M-HANI1·2.")

    # D3: other range separators, and malformed descending ranges.
    def test_other_range_separators_and_descending_ranges(self):
        for text in ("S1~12", "S1—12", "S1 – 12", "S1/S12", "S2–S1"):
            with self.subTest(text=text):
                self.assertRejected(apa_text=text)
        self.assertAccepted(apa_text="S1~2, S1 – 2, S1/S2")

    # D4: families come from the ledgers; qualified tokens use the owner's families.
    def test_families_are_derived_from_ledgers(self):
        ledger = KOREAN_LEDGER + "\n## R-NIKL1 · 새 자료\n"
        self.assertRejected(korean_text="R-NIKL9 근거", korean_ledger=ledger)
        self.assertAccepted(korean_text="R-NIKL1 근거", korean_ledger=ledger)

    def test_unregistered_hyphenated_ids_are_rejected(self):
        for text in ("B-NEW1 근거", "M-KBS1 근거"):
            with self.subTest(text=text):
                self.assertRejected(korean_text=text)
        self.assertAccepted(korean_text="SHA-256, UTF-8, COVID-19, K-ANX")

    def test_qualified_hypothesis_family_uses_owner_ledger(self):
        self.assertRejected(apa_text="korean-editing H7 참고")
        self.assertAccepted(apa_text="korean-editing H1 참고")

    # D5: heading definitions are anchored, with an explicit 과/와 joiner.
    def test_heading_definitions_are_anchored(self):
        self.assertEqual({"K3"}, set(trace.ledger_definitions("## K3 · 자료 (K9 · 메모)\n")[0]))
        self.assertEqual({"E1", "U1"}, set(trace.ledger_definitions("## E1 · 편집 판단과 U1 · 사용자 선호\n")[0]))

    # D6: heading and table labels are not definitions either.
    def test_heading_and_table_labels_are_not_definitions(self):
        self.assertEqual({}, trace.ledger_definitions("## URL · x\n## SHA-256 · y\n| URL | z |\n| SHA-256 | w |\n- DOI: v\n")[0])

    # D7: CommonMark code spans, comments and invalid link destinations.
    def test_code_comments_and_invalid_link_destinations(self):
        self.assertAccepted(apa_text="``S99`` and <!-- S98 -->")
        self.assertRejected(apa_text="[주의](S12 참조)")
        self.assertAccepted(korean_text="A-B 비교")

    # D8: bounded expansion and year-like IDs.
    def test_large_ranges_are_rejected_and_year_ids_are_endpoints(self):
        self.assertRejected(apa_text="S1–10000000")
        self.assertAccepted(korean_text="P-SONG2008–2013")

    def test_shipped_skills_are_traceable(self):
        self.assertEqual([], trace.validate_repository(ROOT))


if __name__ == "__main__":
    unittest.main()
