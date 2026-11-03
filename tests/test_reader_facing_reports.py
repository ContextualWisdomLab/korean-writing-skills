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
        self.assertIn('에이전트 자신의 작업 노트·할 일 관리', skill)
        self.assertIn('문서 파일과 초안에는 확인 표지나 조사 과제 목록을 넣지 않는다', skill)
        self.assertNotIn('초안·교정 메모용 표지', skill)
        self.assertNotIn('작성자용 확인 표지', skill)
        self.assertIn('교정 의뢰', skill)

    def test_inquiry_precedes_report_and_safety_is_preserved(self):
        """The report procedure describes the workflow without a phrase-swap table."""
        relative_path = 'skills/korean-editing/references/reader-facing-reports.md'
        self.assertTrue((ROOT / relative_path).exists(), 'reader-facing report procedure missing')
        text = read_utf8(relative_path)
        for term in ['원자료', '담당자', '접근', '의사결정', '실적 → 남은 작업 → 조치 계획',
                     '초안 작성 전에 확인을 마친다', '합의된 산정 기준']:
            self.assertIn(term, text)
        self.assertNotIn('버릴 표현', text)
        self.assertNotIn('## 4. 문장 전환 예시', text)
        self.assertNotIn('| 주어진 사실 |', text)

    def test_checklist_does_not_ship_placeholders(self):
        """The drafting checklist never tells agents to write placeholder markers."""
        text = read_utf8('skills/korean-editing/references/drafting-checklist.md')
        self.assertIn('초안과 문서 파일에는 확인 표지·공란·조사 과제를 넣지 않는다', text)
        self.assertNotIn('[확인 필요]', text)
        self.assertIn('reader-facing-reports.md', text)


if __name__ == '__main__':
    unittest.main()
