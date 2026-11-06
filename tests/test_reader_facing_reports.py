"""Static guidance contracts; behavioral evaluation is recorded separately."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read_utf8(relative_path):
    """Read a repository text file as UTF-8 regardless of the platform default."""
    return (ROOT / relative_path).read_text(encoding='utf-8')


class ReportGuidanceTests(unittest.TestCase):
    """Check the report guidance wording that routes agents to investigation first."""

    def test_route_and_delivery_scope(self):
        """SKILL.md keeps investigation tasks in agent notes, outside documents."""
        skill = read_utf8('skills/korean-editing/SKILL.md')
        self.assertIn('(references/reader-facing-reports.md)', skill)
        self.assertIn('에이전트가 더 조사할 일은 자신의 작업 노트·할 일 관리', skill)
        self.assertIn('문서 파일과 초안에는 확인 표지나 조사 과제 목록을 넣지 않는다', skill)
        self.assertIn('결과에 내재한 불확실성, 확인된 실패·제한·위험은 사실과 영향으로 보존한다', skill)
        self.assertIn('의미 보존 조건과 표기 점검을 대체하지 않는다', skill)
        self.assertNotIn('작성자용 확인 표지', skill)
        self.assertNotIn('독자용 표에 채워', skill)
        self.assertIn('교정 의뢰', skill)

    def test_inquiry_precedes_report_and_safety_is_preserved(self):
        """The report procedure describes the workflow without a phrase-swap table."""
        relative_path = 'skills/korean-editing/references/reader-facing-reports.md'
        self.assertTrue((ROOT / relative_path).exists(), 'reader-facing report procedure missing')
        text = read_utf8(relative_path)
        for term in ['원자료', '담당자', '접근', '작업 노트', '실적 → 남은 작업 → 조치 계획',
                     '결과에 내재한 불확실성', '문장 수리 절차', '표기 판단', '진척률을 보고할 때']:
            self.assertIn(term, text)
        self.assertNotIn('버릴 표현', text)
        self.assertNotIn('## 4. 문장 전환 예시', text)
        self.assertNotIn('| 주어진 사실 |', text)
        self.assertNotIn('미확인`, `확인 불가`', text)
        self.assertNotIn('완료 아님`', text)
        self.assertIn('조판 검증은 텍스트 추출과 별도로 한다', text)
        self.assertIn('(report-layout-verification.md)', text)
        self.assertIn('불필요한 부정 대비를 피한다', text)
        self.assertIn('담당자가 공용망 접근을 차단했다', text)
        self.assertIn('부재·실패·불확실성을 전달하는 부정', text)
        layout = read_utf8('skills/korean-editing/references/report-layout-verification.md')
        for term in ['모든 쪽을 이미지로 본다', '머리행을 반복한다',
                     '캡션은 도식에 실제로 있는 범위를 말한다', '직전 채택본과 대조한다']:
            self.assertIn(term, layout)

    def test_everyday_korean_scope(self):
        """Everyday generation uses the principles without imposing document workflows."""
        skill = read_utf8('skills/korean-editing/SKILL.md')
        for term in ['한국어 대화·답변·설명·음성 응답 원고', '일상 대화',
                     '짧은 대화에 문서용 조사·퇴고 절차나 학술지 형식을 일괄 적용하지 않는다',
                     '적용 과정을 답변마다 해설하지 않는다']:
            self.assertIn(term, skill)

    def test_change_summary_precedes_details(self):
        """Report entry points surface the existing-baseline comparison first."""
        text = read_utf8('skills/korean-editing/references/reader-facing-reports.md')
        for term in ['증감 요약 → 상세 내역', '보고서 상단', '기준값', '예상값',
                     '증감액', '증감률', '약', '추정', 'U1 사용자 선호']:
            with self.subTest(term=term):
                self.assertIn(term, text)
        for path in ['skills/korean-editing/SKILL.md', 'AGENTS.md']:
            with self.subTest(path=path):
                self.assertIn('기존 대비 증감', read_utf8(path))

    def test_change_comparison_preserves_denominator_and_uncertainty(self):
        """A headline must not turn incompatible or missing inputs into a rate."""
        text = read_utf8('skills/korean-editing/references/reader-facing-reports.md')
        for term in ['(비교값 - 기준값) / 기준값 × 100', '기준값이 0',
                     '기준값이 없', '음수', '통화', '세금', '일회성',
                     '월 비용', '연 비용', '범위', '%p', '반올림',
                     '맞춤법만 의뢰받았다면']:
            with self.subTest(term=term):
                self.assertIn(term, text)

    def test_zero_baseline_does_not_invent_occurrence(self):
        """Zero-to-zero and projected costs keep their distinct factual status."""
        text = read_utf8('skills/korean-editing/references/reader-facing-reports.md')
        for term in ['0 → 0', '변동 없음', '실제 발생과 예상 발생',
                     '증감률은 산출하지 않는다']:
            with self.subTest(term=term):
                self.assertIn(term, text)
        self.assertNotIn('증감액과 신규 발생 사실을 쓰고', text)

    def test_incompatible_scopes_do_not_produce_a_difference(self):
        """Unmatched scopes cannot justify an absolute change either."""
        text = read_utf8('skills/korean-editing/references/reader-facing-reports.md')
        self.assertIn('환산 근거가 없으면 차이도 계산하지 않는다', text)
        self.assertNotIn('기준값이 음수이거나 비교 범위가 다르면', text)

    def test_checklist_does_not_ship_placeholders(self):
        """The drafting checklist never tells agents to write placeholder markers."""
        text = read_utf8('skills/korean-editing/references/drafting-checklist.md')
        self.assertIn('초안과 문서 파일에는 확인 표지·공란·조사 과제를 넣지 않는다', text)
        self.assertNotIn('[확인 필요]', text)
        self.assertIn('reader-facing-reports.md', text)


if __name__ == '__main__':
    unittest.main()
