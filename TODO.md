# 한국어 글쓰기·APA7 스킬 개발 TODO

> 현재 담당·수용 조건: [전담 리드 원장](LEAD_QUEUE.md). 아래 run·리드는 이전 작업 이력이다.

> Orca child run: `run_58eacbe56521` · root run: `run_b22de9a1c59d` · 리드: `term_1c33634e-e367-4777-a76a-de0f1bde7dcf`

## 진행 상태

| 트랙 | 담당 | 상태 | 다음 조치 | 완료 증거 | 의존성 |
|------|------|------|-----------|-----------|--------|
| 한국어 규범·퇴고 | writing-skills-lead | **보강(3차)** | 일반화·추가 사례는 별도 검증 | round-3-k5-k6 + validator | — |
| APA7 논문 작성 | apa7-manuscript-worker | **초안** | Publication Manual 본문 및 JARS 추가 설계표 | `skills/apa7-manuscript-writing/` | Zotero/elderly-gad |
| 독립 평가 | 격리 실행·별도 채점 worker | **두 사례 채점 완료** | 전체 타당화와 구별 | `evaluations/runs/round-3-k5-k6/review.md` | 입력·스킬·출력 SHA-256 |
| 강원국·김정선 | writing-skills-lead | **반영(부분)** | 원서 본문 추가 확인 | source-ledger G1–J2 | — |
| 경희대·대학 교육 | writing-skills-lead | **반영** | — | U-KHU1–4, examples·validation | — |
| KBS·신문·피동·주어 | writing-skills-lead | **반영** | KUPIS 기관 로그인 | N-Q·M-HANI·M-HEO·B-KBS·P-SONG | KUPIS SSO |
| Rubric·PLD·Standards | writing-skills-lead | **반영(잠정)** | 한국어 평가 논문 전문 확보 | pld-and-standards-framework.md·rubric-source-ledger.md; round-2는 철회 이력 | Zotero API; Ahn PDF |
| APA 원문 | 원문 조사 worker·다음 담당 | **부분 확인** | Manual 7 본문 확보 | source-access-followup; JARS Table 1 소장본 대조 | 인증된 Zotero·기관 경로 |
| 리드 검증 | writing-skills-lead | **진행** | scoped commit·원격 HEAD·필수 검사 확인 | PR #1 | 원문 미확인과 CI 대기 구분 |

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

- [x] 2 스킬 SKILL.md + references, skill validator 통과 (2026-09-20 복구 재실행)
- [x] 독립 평가 시나리오·루브릭 (작성자 답 비공개); K5·K6 별도 채점 2건 통과, 전체 타당화 아님
- [ ] 이번 scoped commit의 원격 HEAD 확인; 스킬 경로는 README에 기록
- [x] 초안·두 사례 채점·문헌 미확인 범위를 구분
