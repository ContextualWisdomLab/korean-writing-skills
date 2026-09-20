# 리드 보고 (writing-skills-lead)

확인일: 2026-09-20 · child run: `run_58eacbe56521` · root: `run_b22de9a1c59d` · branch: `seonghobae/writing-skills-lead`

## 원격 commit (검증됨)

| commit | 내용 |
| --- | --- |
| `b668af1` | korean-editing: KBS·신문·피동·주어·KUPIS 기록 |
| `f2d5b67` | Rubric·PLD·Standards·AGENTS 근거 대응 |
| `dc7b005` | round-2 K5·K6 blind eval |

`evaluations/ARTIFACT-VERIFY.md`: round-2 **1차 commit pathspec 실패** → 2차 `dc7b005` 성공. GitHub API로 `round-2-k5-k6-blind.md` sha 확인.

## 초안 vs 검증

| 산출물 | 상태 | 근거 |
| --- | --- | --- |
| `skills/korean-editing/` | **초안+2차 보강** | validator; round-1 K1–K4 4/4; round-2 K5–K6(리드 단일 세션); U-KHU·N-Q·M-HANI·P-SONG |
| `skills/apa7-manuscript-writing/` | **초안(JARS Table1 부분)** | S8 Table 1; Manual 7·JARS PDF 미완 |
| `evaluations/` | **1–2회차 기록** | round-1-review.md, round-2-k5-k6-blind.md; analytic rubric·PLD framework |
| `AGENTS.md` | **근거 대응 표** | f2d5b67 |

## Standards·PLD·논문 루브릭 (06:48–06:51 지시)

| 산출물 | 경로 |
| --- | --- |
| 분석적 루브릭 | `evaluations/rubrics/analytic-korean-editing.md` |
| PLD·cut score 프레임 | `evaluations/rubrics/pld-and-standards-framework.md` |
| 근거 장부 | `evaluations/references/rubric-source-ledger.md` |
| AGENTS 대응 | `AGENTS.md` §근거 대응 |

- **S-STD2014**: 공식 PDF + Zotero `GKX4IKDH` / `A9MHWYKV`. PLD·Standard 5.21·scoring rubric 확인. cut score·가중치 **미설정**.
- **Performance Level Criterion**: Standards **정식 용어 아님**.
- **R-AHN2026·R-KIM2010·R-KSL2019**: 초록·서지만; 본문 미독.

## KUPIS·Zotero (06:43 지시)

| 시도 | 결과 |
| --- | --- |
| KUPIS 포털 | 200, **SSO 없이** 논문 PDF 미확보 |
| Zotero Standards | elderly-gad **확인** (위) |
| Zotero 한국어 루브릭 논문 | parent 서지·본문 **미완** |

## PR

https://github.com/ContextualWisdomLab/korean-writing-skills/pull/1 — CI pending, merge 대기.

## 남은 완료 조건

1. APA Publication Manual 7판 본문 (Zotero).
2. apastyle JARS PDF.
3. KUPIS/기관 SSO로 한국어 평가·담화 논문 **전문**.
4. K5·K6 **독립** 실행자 재평가.
5. Ahn 2026 등 루브릭 논문 본문·ICC 근거.

