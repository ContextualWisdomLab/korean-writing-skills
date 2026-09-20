# 산출물·원격 검증 기록

확인일: 2026-09-20. 담당: writing-skills-lead.

## round-2-k5-k6-blind.md commit 실패 원인

| 시각(대략) | 이벤트 | 결과 |
| --- | --- | --- |
| 16:06 | `Write` 도구로 `evaluations/runs/round-2-k5-k6-blind.md` 생성 | 로컬 파일 3836 bytes |
| 16:07 1차 | `git add evaluations/runs/round-2-k5-k6-blind.md && git commit` **동일 셸** | **실패** — `fatal: pathspec ... did not match any files` (파일이 아직 untracked·add 타이밍 이슈) |
| 16:07 2차 | `git add` + `git commit` 재시도 | **성공** `dc7b005` |

**원인**: 1차 commit에서 add 대상 파일이 staging에 올라가기 전에 pathspec이 실패했거나, 화면에 보인 실패가 1차 시도였음. **2차 commit 이후 원격 반영 완료.**

## 원격 검증 (GitHub)

| 경로 | 로컬 | 원격 commit | GitHub API |
| --- | --- | --- | --- |
| `evaluations/runs/round-2-k5-k6-blind.md` | 3836 B, `2cd1e01…` | `dc7b005` | sha `2cd1e0143988ad46265d0112df8d7fe426f6dfb4` ✓ |
| `evaluations/rubrics/pld-and-standards-framework.md` | 5522 B | `f2d5b67` | (동일 브랜치) |
| `evaluations/rubrics/analytic-korean-editing.md` | 4538 B | `f2d5b67` | |
| `evaluations/references/rubric-source-ledger.md` | 4281 B | `f2d5b67` | |
| `AGENTS.md` (근거 대응 절) | 4996 B | `f2d5b67` | |

브랜치: `seonghobae/writing-skills-lead` — `git status` clean, `origin`과 동기화(2026-09-20 확인).

## Zotero Standards 2014 (elderly-gad) — 2026-09-20 재확인

| 항목 | 값 |
| --- | --- |
| library | groups/6347780 (elderly-gad) |
| item key | `GKX4IKDH` |
| title | Standards for educational and psychological testing |
| date | 2014 |
| attachment key | `A9MHWYKV` |
| file | `~/Documents/Zotero/storage/A9MHWYKV/9780935302356.pdf` |
| 확인 본문 | 인쇄 p.100 부근 Cut Scores·**performance-level descriptors**; Standard **5.21** (Cluster 4 Cut Scores); glossary **performance-level descriptor** |
| Performance Level Criterion | **용어 미확인** (전문 검색 0건) |

공개 PDF([testingstandards.net](https://testingstandards.net/uploads/7/6/6/4/76643089/standards_2014edition.pdf))와 Zotero 소장본 **동일 판** 대조 — PLD·cut score 서술 일치.

## KUPIS·한국어 루브릭 논문

| 시도 | 결과 |
| --- | --- |
| kupis.kw.ac.kr 포털 | HTTP 200, **기관 로그인 없이** 전문 검색·PDF 미확보 |
| Zotero personal `분석적 루브릭` | attachment hit만, 서지 parent 미확정 |
| Zotero group `글쓰기 평가` | API timeout/빈 응답 |
| earticle A483546 (안미홍 2026) | ArticleDownload → HTML, **전문 미확보** |
| KCI ART001459759·ART002002643 | **초록·랜딩만** 확인 |

## 완료 주장 금지 항목

- K5·K6 **독립** 실행자 재실행 (round-2는 리드 단일 세션)
- Ahn 2026·KSL 논문 **본문** 기반 루브릭 항목
- KUPIS 경유 **원문** 확보
- APA Publication Manual 7 Zotero/elderly-gad 본문
- PR #1 merge (CI pending)

