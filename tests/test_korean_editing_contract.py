"""Presence contracts for the drafting-time Korean editing guidance."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "korean-editing" / "SKILL.md"
CHECKLIST = ROOT / "skills" / "korean-editing" / "references" / "drafting-checklist.md"


def test_drafting_checklist_is_linked_and_scope_is_explicit():
    skill = SKILL.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    assert "](references/drafting-checklist.md)" in skill
    assert "N-WEB" in skill and "N-PUNCT" in skill
    assert "규정이 아니다" in skill
    assert "초안 작성 전·중 점검표" in checklist


def test_drafting_guidance_preserves_uncertainty_and_source_scope():
    """Keep unresolved work outside drafts while retaining stated uncertainty."""
    text = CHECKLIST.read_text(encoding="utf-8")
    for phrase in (
        "에이전트 자신의 작업 노트·할 일 관리에 기록",
        "초안과 문서 파일에는 확인 표지·공란·조사 과제를 넣지 않는다",
        "상관",
        "인과",
        "아직 확인하지 못했다",
        "아직 없다",
        "인용 귀속",
        "정규식으로 일괄 치환하지 않는다",
        "유의한",
        "N-EXAMPLES",
        "외래어·로마자·고유명사 게이트",
        "신뢰구간",
    ):
        assert phrase in text


def test_common_confusions_are_meaning_based():
    text = CHECKLIST.read_text(encoding="utf-8")
    rules = {
        "되/돼": "`되어`로 풀리면 `돼`",
        "안/않": "`안`은 보통 서술어 앞의 부정 부사이고",
        "로서/로써": "재료·수단·도구·시간상 한계이면 `로써`",
        "-대/-데": "남에게 들은 내용을 전하면 `-대`",
        "에요/예요": "`아니예요`로 쓰지 않는다",
        "웬/왠": "`왜인지`이면 `왠지`",
    }
    for pair, rule in rules.items():
        assert pair in text
        assert rule in text


def load_tests(loader, tests, pattern):
    """Include the existing function contracts in unittest discovery."""
    return unittest.TestSuite(
        unittest.FunctionTestCase(test)
        for name, test in globals().items()
        if name.startswith("test_") and callable(test)
    )
