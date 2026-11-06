"""Contract tests for application-scope routing and drafting prevention."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "korean-editing" / "SKILL.md"
ROUTING = ROOT / "skills" / "korean-editing" / "references" / "scope-routing.md"
SCENARIO = ROOT / "evaluations" / "scenarios" / "drafting-blind-inputs.md"
RUBRIC = ROOT / "evaluations" / "rubrics" / "drafting-korean-editing.md"


def test_scope_routing_is_linked_and_has_source_layers():
    skill = SKILL.read_text(encoding="utf-8")
    routing = ROUTING.read_text(encoding="utf-8")
    assert "](references/scope-routing.md)" in skill
    for phrase in ("표준어 규정", "외래어 표기법", "국어의 로마자 표기법", "표준국어대사전", "온라인가나다"):
        assert phrase in routing


def test_scope_routing_preserves_uncertainty_and_genre_boundaries():
    routing = ROUTING.read_text(encoding="utf-8")
    for phrase in ("[확인 필요", "규정 본문과 상담 답변", "장르 선택", "확인하지 못함", "미적용"):
        assert phrase in routing


def test_drafting_evaluation_packet_covers_application_limits():
    scenario = SCENARIO.read_text(encoding="utf-8")
    rubric = RUBRIC.read_text(encoding="utf-8")
    for phrase in ("인과 효과 추정치는 없음", "아직 회수하지 못함", "방법요인", "되요", "로써"):
        assert phrase in scenario
    for phrase in ("주장·근거·강도", "상관을 인과", "자료에 없는 행위자", "중대 오류"):
        assert phrase in rubric


def load_tests(loader, tests, pattern):
    """Include the existing function contracts in unittest discovery."""
    return unittest.TestSuite(
        unittest.FunctionTestCase(test)
        for name, test in globals().items()
        if name.startswith("test_") and callable(test)
    )
