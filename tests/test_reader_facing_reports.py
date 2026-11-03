"""Static guidance contracts; behavioral evaluation is recorded separately."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ReportGuidanceTests(unittest.TestCase):
    def test_route_and_delivery_scope(self):
        skill = (ROOT / 'skills/korean-editing/SKILL.md').read_text()
        self.assertIn('(references/reader-facing-reports.md)', skill)
        self.assertIn('에이전트 자신의 작업 노트·할 일 관리', skill)
        self.assertIn('문서 파일과 초안에는 확인 표지나 조사 과제 목록을 넣지 않는다', skill)
        self.assertNotIn('초안·교정 메모용 표지', skill)
        self.assertIn('교정 의뢰', skill)

    def test_inquiry_precedes_report_and_safety_is_preserved(self):
        path = ROOT / 'skills/korean-editing/references/reader-facing-reports.md'
        self.assertTrue(path.exists(), 'reader-facing report procedure missing')
        text = path.read_text()
        for term in ['원자료', '담당자', '접근', '의사결정', '담당·기한',
                     '임의로', '부정 표현', '공정률', '작업 노트', '실적 → 남은 작업 → 조치 계획']:
            self.assertIn(term, text)

    def test_checklist_does_not_ship_placeholders(self):
        text = (ROOT / 'skills/korean-editing/references/drafting-checklist.md').read_text()
        self.assertIn('초안과 문서 파일에는 확인 표지·공란·조사 과제를 넣지 않는다', text)
        self.assertNotIn('[확인 필요]', text)
        self.assertIn('reader-facing-reports.md', text)

if __name__ == '__main__':
    unittest.main()
