"""Presence contracts for the drafting-time Korean editing guidance."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "korean-editing" / "SKILL.md"
CHECKLIST = ROOT / "skills" / "korean-editing" / "references" / "drafting-checklist.md"


def test_drafting_checklist_is_linked_and_scope_is_explicit():
    skill = SKILL.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    assert "drafting-checklist.md" in skill
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
    for phrase in ("되/돼", "안/않", "로서/로써", "-대/-데", "에요/예요", "웬/왠"):
        assert phrase in text
