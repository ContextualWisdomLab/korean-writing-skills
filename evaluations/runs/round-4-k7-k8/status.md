# K7·K8 패킷

입력은 [blind-inputs.md](../../scenarios/blind-inputs.md) K7·K8과 `K7.md`·`K8.md`가 같다. 판정 준거는 [actor-responsibility-criteria.md](../../rubrics/actor-responsibility-criteria.md).

**상태: 본문 축 채점 있음. 독립성 미확인. 스킬 전체 타당화 아님.**

root `msg_df68845a5117`: 채점자 ID·세션·입력 해시·작성자 점수 차단 로그가 없으면 blind 독립평가로 쓰지 말 것. 기록은 [independent-scoring.md](independent-scoring.md) 상단. K7 이유 줄(어문 규정·기관 권고, 출처 없음)은 근거 정확성 결함이며 본문 보존 점수와 분리한다.

실행자 subagent `01a0bf8c-f317-71c0-9c3c-e032cbe43f01`가 `/tmp/k7k8-exec-skill/`만 받고 교정문을 씀([output.md](output.md)). 준거 파일은 실행자에게 주지 않았다. 채점자는 문항 작성 세션이 원문·출력·three-axis·actor-responsibility-criteria로 채점함([scoring.md](scoring.md)). K7·K8 모두 축별 2점 이상, 중대 오류 없음.

실행자는 두 원문을 거의 그대로 두어 사동·피동·가능성·생략 주어를 훼손하지 않았다. K5·K6과 합산하지 않는다. 채점자 일치도는 없다.

교차검토 subagent `01a0bfaf-80da-75f3-b9c7-1a2d1be76101` 산출은 같은 parent 세션·isolation none. 미열람 자기보고만 있어 **blind 독립평가로 쓰지 않음**. `worker-start --agent opencode`는 consumer_fenced.
