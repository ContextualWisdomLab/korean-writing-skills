# 한국어 글쓰기·APA7 스킬 개발 TODO

> Orca child run: `run_58eacbe56521` · root run: `run_b22de9a1c59d` · 리드: writing-skills-lead

## 진행 상태

| 트랙 | 담당 | 상태 | 다음 조치 | 완료 증거 | 의존성 |
|------|------|------|-----------|-----------|--------|
| 한국어 규범·퇴고 | writing-skills-lead | **보강(2차)** | K5·K6 blind eval | validator + KBS·피동·주어·KUPIS | — |
| APA7 논문 작성 | apa7-manuscript-worker | **초안(실패 보고)** | Publication Manual·JARS 원문 | `skills/apa7-manuscript-writing/` | Zotero/elderly-gad |
| 독립 평가 | independent-eval-worker | **완료** | — | `evaluations/runs/round-1-review.md` | — |
| 강원국·김정선 | writing-skills-lead | **반영(부분)** | 원서 본문 추가 확인 | source-ledger G1–J2 | — |
| 경희대·대학 교육 | writing-skills-lead | **반영** | — | U-KHU1–4, examples·validation | — |
| KBS·신문·피동·주어 | writing-skills-lead | **반영** | KUPIS 기관 로그인 | N-Q·M-HANI·M-HEO·B-KBS·P-SONG | KUPIS SSO |
| APA 원문 | — | **미완(완료 조건)** | Manual 7·JARS·Zotero | apa source-ledger | 접근 경로 |
| 리드 검증 | writing-skills-lead | **진행** | PR merge | PR URL | APA 원문 |

## I'm not human 스킬

- **결과**: 설치본 미발견 (`.codex/skills`, `.claude/skills`, `.cursor` 검색)
- **대체 참고**: `humanize-korean` (v2.3.2) — 의미 앵커 보존·번역투 패턴 탐지·과잉교정 방지 게이트 재사용 검토
- **다음**: marketplace/외부 저장소 추가 검색 또는 사용자 확인

## 원문 시작점 (확인일: 2026-09-20)

| 출처 | URL | 비고 |
|------|-----|------|
| 공공언어 바로 쓰기(개정판) | https://www.korean.go.kr/front/etcData/etcDataView.do?etc_seq=699 | PDF 첨부 1건 |
| 한국어 어문 규범 | https://www.korean.go.kr/kornorms/main/main.do | 표준어·외래어·로마자 |
| APA Style JARS | https://www.apa.org/pubs/journals/resources/apa-style-jars.html | JARS-Quant 등 |
| APA Publication Manual 7판 | Zotero 개인·elderly-gad 6347780 | 소장본 직접 확인 |

## 완료 기준 (리드)

- [ ] 3 스킬 SKILL.md + references, skill validator 통과
- [ ] 독립 평가 시나리오·루브릭 (작성자 답 비공개)
- [ ] 원격 commit + 설치 가능 경로 보고
- [ ] 초안 vs 검증 완료 구분 보고
