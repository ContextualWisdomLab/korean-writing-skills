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

    def test_shipped_skills_are_traceable(self):
        self.assertEqual([], trace.validate_repository(ROOT))


if __name__ == "__main__":
    unittest.main()
