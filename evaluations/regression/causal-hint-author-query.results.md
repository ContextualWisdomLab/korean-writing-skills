# 회귀 검사 결과 — 원문이 시사한 인과를 확인 요청으로 넘기는가

검사 정의는 [causal-hint-author-query.md](causal-hint-author-query.md)에 있고 8회차 동결 대상이라 고치지 않는다. 그 문서 이력 표의 “기록 예정” 행 결과를 여기 적는다.

| 스킬 상태 | 실행 | 결과 | 근거 |
| --- | --- | --- | --- |
| 수정 전 | 7회차 blind K12 | 실패 | [K12-output](../runs/20260925-round7-blind/K12-output.md) |
| 수정 전 | 재현 실행 1회 | 실패 | [K12-output](../runs/20260925-k12-repro/K12-output.md) |
| 수정 후(`3e9b165`) | 8회차 회귀 실행 1회 | **통과** | [regression/K12-output](../runs/20260925-round8/regression/K12-output.md) — 인과 문장의 표현·강도는 두고 “종단 설계·실험 조작·시간적 선후 근거가 있는지” 저자 확인 요청을 남김. 수치 불변, 인과 강화 없음 |
| 수정 후(`3e9b165`) | 8회차 K12 독립 실행 | 통과(확인 요청 있음) | [K12-output](../runs/20260925-round8/K12-output.md) |

네 실행 모두 실행자는 `korean-editing`의 SKILL.md(와 예문)만 열었다. 같은 경로에서 결과가 실패에서 통과로 바뀌었으므로 수정한 위치가 원인이었다는 진단과 맞는다. 수정 후 결과는 두 번이며 재현성을 측정한 것은 아니다.
