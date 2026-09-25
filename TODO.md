# 한국어 글쓰기·APA7 스킬 개발 TODO

공개 저장소에는 재사용 가능한 스킬·근거·평가 계약만 남긴다. 로컬 터미널, dispatch/run/task 식별자, 임시 작업 디렉터리, 연구 원고 인계 상태는 제품 산출물이 아니므로 이 원장에서 추적하지 않는다.

## 진행 상태

| 트랙 | 상태 | 다음 조치 | 완료 증거 | 의존성 |
|------|------|-----------|-----------|--------|
| 한국어 규범·퇴고 | **보강(3차)** | 일반화·추가 사례는 별도 검증 | round-3-k5-k6 + validator | — |
| APA7 논문 작성 | **부분 확인** | 7.7 이후·8.12 이후·10.4 이후·JARS Table 2–8 중 해당 범위 원문 확인 | `skills/apa7-manuscript-writing/` | 확인한 원문 절·쪽 기록 |
| 독립 평가 | **두 사례 채점 완료** | 개별 사례 통과와 전체 타당화를 계속 구분 | `evaluations/runs/round-3-k5-k6/review.md` | 입력·스킬·출력 SHA-256 |
| 강원국·김정선 | **반영(부분)** | 원서 본문 추가 확인 | source-ledger G1–J2 | — |
| 경희대·대학 교육 | **반영** | — | U-KHU1–4, examples·validation | — |
| KBS·신문·피동·주어 | **반영** | KUPIS 접근이 실제 가능할 때 관련 원문 확인 | N-Q·M-HANI·M-HEO·B-KBS·P-SONG | KUPIS 접근 |
| Rubric·PLD·Standards | **반영(잠정)** | 한국어 평가 논문 전문 확보 | pld-and-standards-framework.md·rubric-source-ledger.md; round-2는 철회 이력 | Zotero/원문 접근 |
| APA 원문 | **부분 확인** | 판권지·미확인 절과 필요한 인쇄쪽만 추가 확인 | source-ledger의 2026-09-20~21 확인 기록 | 소장본 접근 |
| PR 검증 | **진행** | 현재 exact head의 적용 가능한 필수 검사와 비작성자 검토 확인 | PR #4 | 원문 미확인과 CI 실패·대기를 구분 |

## I'm not human 스킬

- **결과**: 당시 설치본을 확인하지 못했다.
- **대체 참고**: `humanize-korean` v2.3.2에서 의미 앵커 보존·번역투 패턴 탐지·과잉교정 방지 아이디어를 참고하되, 별도 제품을 동일 스킬로 취급하지 않는다.
- **다음**: 정확한 설치본이나 공식 배포 위치가 확인될 때만 비교한다.

## 원문 시작점 (확인일: 2026-09-20)

| 출처 | URL | 비고 |
|------|-----|------|
| 공공언어 바로 쓰기(개정판) | https://www.korean.go.kr/front/etcData/etcDataView.do?etc_seq=699 | PDF 첨부 1건 |
| 한국어 어문 규범 | https://www.korean.go.kr/kornorms/main/main.do | 표준어·외래어·로마자 |
| APA Style JARS | https://www.apa.org/pubs/journals/resources/apa-style-jars.html | JARS-Quant 등 |
| APA Publication Manual 7판 | Zotero 개인·elderly-gad 소장본 | 확인한 절만 근거 장부에 기록 |

## 완료 기준

- [x] 두 스킬의 `SKILL.md`와 필요한 references가 존재하고 skill validator를 통과함
- [x] 독립 평가 시나리오·루브릭과 K5·K6 별도 채점 기록을 보존함 — 전체 타당화로 해석하지 않음
- [x] 초안·개별 사례 채점·문헌 미확인 범위를 구분함
- [ ] 공개 tip에서 로컬 절대경로·ephemeral agent/run 식별자·연구 원고 인계 기록을 제거하되 평가의 역할·해시·독립성 근거는 보존함
- [ ] current exact head의 적용 가능한 CI/security/review를 통과함
