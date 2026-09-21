# Writing-skills lead recovery — 2026-09-21

담당: `term_6496a84a-aec1-402f-9f62-6efccd0a82aa` · dispatch `ctx_d8a9e643f75d` · task `task_1342050c2733` · root `run_b22de9a1c59d`

## 첫 실제 명령

```text
git fetch origin seonghobae/writing-skills-lead
git merge origin/seonghobae/writing-skills-lead
```

결과: fast-forward `ca94600` → `8c13690` (PR #1 head와 동일). 스킬·평가 파일 재작성 없음.

## 인수한 기존 산출물

| 항목 | 위치·증거 |
| --- | --- |
| PR | https://github.com/ContextualWisdomLab/korean-writing-skills/pull/1 — OPEN, MERGEABLE, mergeStateStatus BLOCKED (필수 검사 pending) |
| 한국어 스킬 | `skills/korean-editing/` — K5/K6 별도 채점 통과 기록 있음, 전체 타당화 아님 |
| APA7 스킬 | `skills/apa7-manuscript-writing/` — JARS Table 1·Manual 일부 절 반영, 남은 절·Table 2–8 미완 |
| 평가 | `evaluations/` — round-3 K5/K6; round-4 K7/K8 독립성 미확인; 2026-09-21 DOCX/HWPX 시각검토 보고 다수 |
| 원장 | `LEAD_QUEUE.md`, `LEAD-REPORT.md`, `TODO.md` |

## 미완료 과제 (우선)

1. late-life `term_8e77a233`와 DOCX/HWPX·원고 교정 우선 요구 확정 (원고 파일 직접 수정 금지).
2. dogfood: 전팀 실사용 피드백 수집 → Issue 연결 → 근거/사용성/선호 구분 수정 → 독립 재검증.
3. APA Manual 미열람 절·JARS 설계별 표: 원문 확인 후에만 규칙 추가.
4. K7/K8: 격리 채점자 없이 blind 독립성 주장 금지.
5. PR #1: 필수 검사 성공 확인 후 merge 판정 (CI 재실행 요청 안 함).
6. 강원국·김정선 원서 본문·I'm not human 설치본: 미확인 상태로 유지.

## 소유권

| 트랙 | 소유 |
| --- | --- |
| `skills/korean-editing/` | writing-skills lead (본 터미널) |
| `skills/apa7-manuscript-writing/` | writing-skills lead (본 터미널) |
| `evaluations/` | writing-skills lead (본 터미널); 채점은 격리 worker |
| 연구 원고·DOCX/HWPX 바이너리 | late-life lead `term_8e77a233` |

## 워커 배정

이전 writing-skills 터미널 3개 연결 해제. 활성 실행자 없음. 연구 우선순위 회신 후 필요한 워커만 신규 배정.

## dogfood

지시: `~/.local/orca-watchdog/msgs/WRITING-SKILLS-DOGFOOD-20260921.md`. 소비자에 main 참모 `term_7dc986ed`, root 포함.
추적 Issue: https://github.com/ContextualWisdomLab/korean-writing-skills/issues/2
root run handoff: `msg_c9d260043713`.

## late-life 협의

- 직접 terminal send 2회: Enter `turn_start` 미관측 (`a1fc289a`, `e49233c8`).
- `run_de4c37377cf3` 직송: `dispatch_run_mismatch`.
- ask `msg_0123342f31df`: 300s 무응답 → escalation 전송.
- 잠정 우선순위(CO 인계, 회신 전): G7-7 숫자셀 중간줄바꿈 · DOCX/HWPX 시각검토+재추출 · 원고값 무단교체 금지.
