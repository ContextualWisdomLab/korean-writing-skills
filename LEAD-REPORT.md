# 리드 보고 (writing-skills-lead)

확인일: 2026-09-20 · child run: `run_58eacbe56521` · root: `run_b22de9a1c59d`

## 초안 vs 검증 완료

| 산출물 | 상태 | 근거 |
|--------|------|------|
| `skills/korean-editing/` | **검증 완료(초안)** | skill validator 통과, 공식 PDF(K1·N41–43) 확인, 독립 블라인드 4/4 통과 |
| `skills/apa7-manuscript-writing/` | **초안(원문 미완)** | validator 통과, S1·S2·S8 일부 확인; Publication Manual 7·JARS PDF·Zotero/elderly-gad 미접근 |
| `evaluations/` | **검증 완료(1회차)** | 7사례 블라인드 실행·채점, A2 맥락 혼입 후 단독 재실행 통과 |

## 설치 경로

```
skills/korean-editing/SKILL.md
skills/apa7-manuscript-writing/SKILL.md
```

Codex/Cursor: 저장소 루트의 `skills/`를 스킬 경로에 추가하거나 심볼릭 링크.

## I'm not human 스킬

- 명칭 일치 설치본 **미발견**.
- 유사 기능: `humanize-korean` (로컬 v2.3.2), DaleSeo `humanizer` (GitHub). 의미 앵커·과잉교정 게이트만 H1로 기록.

## 강원국·김정선 반영

- G1: 『강원국의 글쓰기』p.21(교보ebook 미리보기) — 초고 후 퇴고.
- G2: 『강원국의 책쓰기 수업』목차 — 퇴고력(본문 미독).
- J1: 『열 문장 쓰는 법』— 한겨레 편집자 서평으로 방법 요약(저자 직접 인용·쪽수 없음).
- J2: 『내 문장이 그렇게 이상한가요?』— 출판사 서지·목차 수준.

## 워커 결과

| 워커 | outcome | 비고 |
|------|---------|------|
| korean-editing | succeeded | |
| apa7-manuscript | failed | 스킬 초안·validator OK, 필수 원문 접근 미완 |
| independent-eval | succeeded | round-1-review.md |

## 남은 작업

1. Publication Manual 7판·JARS 공식 PDF 직접 열람(Zotero/elderly-gad 경로).
2. APA 스킬 원문 대조 후 `failed` → 완료 전환.
3. 원격 commit 확인(아래 push 후).
