"""Presence contracts for the drafting-time Korean editing guidance."""
from pathlib import Path

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
    text = CHECKLIST.read_text(encoding="utf-8")
    for phrase in (
        "[확인 필요]",
        "상관",
        "인과",
        "아직 확인하지 못했다",
        "아직 없다",
        "인용 귀속",
        "정규식으로 일괄 치환하지 않는다",
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
