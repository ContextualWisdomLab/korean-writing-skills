# 전담 리드 작업 원장

확인일: 2026-09-21. **현 리드**: recovery worktree `writing-skills-lead-recovery-20260921`, terminal `term_6496a84a-aec1-402f-9f62-6efccd0a82aa`, dispatch `ctx_d8a9e643f75d`, task `task_1342050c2733`, 조정자 `term_97546d94-0dc6-4649-8e87-8f6d226f5d9d`, root `run_b22de9a1c59d`. 이전 Grok `term_e9fcf167`·Codex `term_731b94a7`·후속 `term_1c33634e`는 연결 해제되어 재시작하지 않는다. 연구 원고 파일은 late-life lead `term_8e77a233-6919-4b13-8d55-2ee97973efba` 소유다.

## 2026-09-21 인수 스냅샷

| 구분 | 상태 |
| --- | --- |
| 첫 실제 명령 | `git fetch origin seonghobae/writing-skills-lead` 후 `git merge origin/seonghobae/writing-skills-lead` (fast-forward → `8c13690`) |
| 기존 산출물 | PR #1 OPEN, head `8c13690`; `skills/korean-editing/`, `skills/apa7-manuscript-writing/`, `evaluations/` 54파일 인수. 재작성 없음 |
| 필수 CI | MERGEABLE·BLOCKED. 다수 pass, strix/CodeQL/opencode-review/noema-review/coverage/trivy/scorecard 등 pending·queued. 재실행 요청 안 함 |
| 기존 실행자 | 한국어 스킬 task completed, APA 스킬 task failed(이후 Manual 부분 반영은 PR 커밋에 존재). 활성 writing-skills worker 없음 → 연구 우선순위 확인 후만 배정 |
| dogfood | `~/.local/orca-watchdog/msgs/WRITING-SKILLS-DOGFOOD-20260921.md` — 전팀 실사용 피드백 수집·Issues 연결·재검증 지휘. 피드백만으로 완료 금지 |

### 소유권 분담 (현 리드)

| 트랙 | 소유 파일 | 다음 산출물 |
| --- | --- | --- |
| 한국어 원문·퇴고 | `skills/korean-editing/` | 미열람 원서(G1·J2)·KUPIS·논문 전문은 새 열람 증거 있을 때만 갱신. dogfood 사례를 Issue에 연결 |
| APA7 작성 | `skills/apa7-manuscript-writing/` | Manual 7.7+/8.12+/10.4+, JARS Table 2–8은 해당 설계·쪽 확인 후만. 원고 수치·IRB 복사 금지 |
| 독립 평가 | `evaluations/` | K7/K8 독립성 미확인 → 격리 Run만 blind. DOCX/HWPX 시각검토 보고는 연구 lead 통합용 수정안만 작성 |
| 연구 원고·렌더 | late-life `term_8e77a233` | 이 트리는 원고·DOCX/HWPX **직접 수정 금지**. 교정·서식 권고만 전달 |

### 연구 lead 협의

CO 인계(`CO-RESEARCH-HANDOFF-20260921T0934Z.md`) 기준 연구측 다음 조건: G7-7 숫자 셀 중간줄바꿈, DOCX/HWPX 시각검토+재추출, 현재 원고값 무단교체 금지. `term_8e77a233` 직접 질의는 Enter turn_start 미관측 → root escalation. **잠정**으로 CO 인계 조건을 우선 요구로 쓰고, late-life 회신이 오면 교체한다. 수정안만 작성해 연구 lead가 통합한다.

### dogfood

Issue #2. root `msg_c9d260043713`. 피드백 수집 후 근거/사용성/선호 구분 수정·독립 재검증. 피드백만으로 완료하지 않음.

**#1 fmls lead (`msg_c9c8b0f2594f`, tip `8c13690` 3문장 운영보고):** 주어·앵커 실측 유효. (a)(b)(c)는 사용성 위주 → tip `a894519`/`5b310a3` 일부 반영 후 조사 부착·표·목록·문장경로 보강. ~2분은 선호·메트릭(규범화 안 함). 전체 타당화·원고·dangling SHA는 잔여.

---

이전 확인일: 2026-09-20. 글쓰기 작업 트리 담당(당시): Grok `term_e9fcf167-27ac-4b49-bd51-6015d1f77ff1`, dispatch `ctx_325b127e6817`.

## 인수와 파일 소유

main `ca94600ed058c0e7448ac69a537b8453241d139b`와 PR #1 `51c1c890d9b09a7aa11010e9398232977c337116`을 확인한다. 두 로컬 작업 트리는 인수 시 깨끗하다. 기존 PR 작업 트리에서 이 원장과 기록의 수용 범위만 정리한다. 기존 스킬·APA 근거 파일은 보존한다.

Air `ctx_a68eae315695`는 연구 run `run_de4c37377cf3`의 기존 작업이다. `worker-show`와 `worker-read`로 MacBookAir의 `writing-apa-jars-20260920`, 브랜치 `seonghobae/writing-apa-jars-sourcecheck-20260920` 및 JARS 본문 대조 진행을 확인한다. 인수 때에는 완료 결과나 통합할 commit을 받지 않는다. 후속 작업에서 completed/released와 연구 PR #237의 `7d34241` 두 문서를 직접 확인한다. 직접 인계 메시지는 Run 경계로 거절되어 root에 한 번 전달을 요청한다(`msg_5add53e4803d`). 연구 리드의 승인을 후속 작업 조건으로 삼지 않는다. 기존 dispatch lifecycle은 원래 Run에 남긴다.

| 작업 | 담당·소유 파일 | 증거 | 다음 조치·수용 조건 | 의존성 |
| --- | --- | --- | --- | --- |
| APA/JARS 원고 대조 | 기존 Air `ctx_a68eae315695`; 연구 저장소 작업 파일 | PR #237 `7d34241`; 쪽수 정정 `28c8c442` | 이 리드가 두 문서를 직접 읽고 Sampling procedures를 소장 PDF와 대조; 정확한 쪽수만 APA 스킬에 반영 | Manual 7·원고 고유 공백은 별도; Air lifecycle 종료 |
| APA 스킬 통합 | 이 Grok; `skills/apa7-manuscript-writing/` | source-ledger·A-NUM·A-REF·A-JARSQ + Manual 6.36·6.44·7.1·7.4·7.5·8.4·8.10·10.1–10.3 도입 | 확인한 절만 세칙으로 반영. 원고 고유 수치·IRB 복사 금지. 영어 수사 한글 강제 금지 | 연구 리드 승인 불필요 |
| 한국어 원문 대조 | 이 OpenCode; `skills/korean-editing/references/` 후속 검토 | 기존 source-ledger의 국립국어원·대학·KBS·신문·강원국·김정선 항목 + U-KHU4 간접 인용절 자구 재확인(2026-09-20) | 기존 기록을 새 열람으로 계산하지 않음; 발행기관·제목·판본·URL·쪽/절·확인일·제한 문장을 원문과 대조 | 원서 본문(J2·G1 퇴고 표)·미확인 논문 전문·KUPIS는 남은 조건 |
| 주어·능동·피동·사동 | 이 Codex; 한국어 스킬 후속 검토 | SKILL.md와 K5/K6 입력·출력 | 행위자·대상·범위·책임·불확실성 보존; 생략 주어를 화자로 단정하지 않음 | 새로운 예문은 별도 실행자와 채점자 필요 |
| PLD·판정준거 | 이 Codex; 평가 문서 | 근거 장부 ctx_812ff2c52f7e; standards-20260920/evidence.json | 개인·그룹 동일 PDF 해시와 원문·이미지 대조, 개념 구별 및 독립 검토 완료 | 척도 타당화·채점자 일치도·중대 오류 열거와 명시 제약 해석은 후속 |
| 기존 평가 검증 | 이 Codex; manifest 읽기 전용 | round-3-k5-k6 manifest 8개 SHA-256 현재 바이트 일치 | 두 사례의 별도 점수만 수용; 전체 타당화·채점자 일치도·APA 준수로 확대하지 않음 | 전체 접근 감사는 아님 |
| 기록 독립 검토 | 별도 Codex `/root/review_acceptance`; 읽기 전용 | 평가·원장 주장 일관성 검토 | 발견 사항을 리드가 최소 수정; 신규 블라인드 행동평가로 집계하지 않음 | 검토 완료; 신규 행동평가는 별도 |
| PR 통합·원격 | 이 Codex; 이 원장·기록 수정 | PR #1 head 및 현재 checks | 수정 파일만 commit/push 후 원격 SHA 확인; merge는 필수 검사와 검토 충족 뒤 판정 | 현재 필수 checks pending; CodeRabbit 표시는 Review rate limited |

## 원문 확인 절차

연구 저장소 `[redacted-research-lead]-v3/.agents/skills/source-check/SKILL.md`를 읽는다. 개인·elderly-gad 양쪽 검색, PDF와 인쇄 쪽 대응, 주장에 해당하는 문장과 제한 문장 대조, 인용한 양과 실제 판정량의 일치, OCR 이미지 대조 여부를 적용한다. 캐시 검색 결과만으로 쪽수를 붙이지 않는다. 이번 인수에서는 문헌 원문을 새로 확인했다고 보고하지 않는다.

이 절차에 따라 기존 출처의 확인 기록과 현재 리드의 파일 검증을 구분한다. 연구 참여자 자료·비공개 원문 PDF·전체 도서 본문을 공개 저장소에 추가하지 않는다. 추적 대상이 Markdown·JSON 문서뿐이고 코드 탐색이 없어 이번 문서 인수에는 CodeGraph 인덱스를 만들지 않는다. 무거운 빌드와 CI 재실행 요청은 하지 않는다.

## 독립 검토 반영

별도 Codex는 기존 평가 기록만 읽고 두 불일치를 찾는다. PLD 문서에서 검증된 시험 절단점과 축별 2점의 내부 통과 경계를 구분하고, TODO에서 철회된 round-2를 완료 증거에서 제외한다. 기존 실행·채점 원본과 스킬은 바꾸지 않는다. `review.md`의 제한된 리드 수용과 채점자의 실행 전체 보류는 함께 유지한다.


## 원문 보완과 사례 검사 · ctx_812ff2c52f7e

이번 변경은 Standards 원문의 수준 기술·루브릭·경계 정의를 직접 확인해 개념 혼동을 고친다. 개인·그룹 소장본의 동일 SHA와 원문 다섯 쪽 이미지 대조를 근거 장부에 남긴다. 로컬 API 시간 초과와 주 DB 스냅샷의 최신성 한계도 구별한다. [사례·원문 검토 결과](evaluations/runs/standards-20260920/review.md)는 별도 채점자와 원문 검토자의 원본·해시를 제공한다. 가상 후보 네 건 중 행위자와 사동 관계를 바꾼 두 건은 실패, 유지가 필요한 두 건은 통과다. 새 스킬 실행이나 경계 타당화 결과로 집계하지 않는다.

Air 결과의 주어 복원 후보는 연구 원고의 문맥에 한정한다. ‘이 연구는’을 모든 생략 주어에 넣는 공통 규칙으로 채택하지 않는다. JARS의 보고 누락 점검은 일반 스킬에 적용하되 원고별 IRB·동의·보상·연구 수치를 복사하지 않는다. Sampling procedures의 실제 위치는 인쇄 6/PDF 4이며, 이전 Air 문서의 인쇄 7/PDF 5 표기를 직접 정정한다.

root 지시 `msg_6af691cbeb9c`에 따라 연구 PR #237도 이 Codex가 정정한다. Air dispatch의 completed/released, 원격 작업 트리의 깨끗한 `7d34241`, 활성 작성자 부재를 확인한 뒤 문서 한 개만 commit·push한다. [정정 commit 28c8c442](https://github.com/ContextualWisdomLab/[redacted-research-repo]/commit/28c8c4427e13f0bfdc4eb53bbe01234b78ed8762), [이슈 7 정정](https://github.com/ContextualWisdomLab/[redacted-research-repo]/issues/7#issuecomment-5749293598), [이슈 8 보완](https://github.com/ContextualWisdomLab/[redacted-research-repo]/issues/8#issuecomment-5749293705). 이슈 7의 ‘연구 기록 없이는 채울 수 있다’는 잘못된 문장도 후속 댓글에서 바로잡는다.

후속 담당은 이 작업 트리와 root다. 연구리드에게 관리 일을 넘기지 않는다.

## 잔여 항목 (2026-09-20 22:50 KST)

| 항목 | 담당 | 현재 증거 | 다음 조치 |
| --- | --- | --- | --- |
| 한국어 문장·능동/피동/사동·생략 주어 | 실행 기록 소유 | K5/K6 기존 통과(합산 안 함). K7·K8 본문 축 점수 있음, **독립성 미확인** | 격리 Run 채점만 blind로 부를 수 있음 |
| 논문근거 루브릭 | 평가 문서 소유 | three-axis.md; round-3-k5-k6 | 전체 타당화·채점자 일치도 미실시 |
| PLD vs 통과 경계 | 평가 문서 소유 | three-axis PLD 칸 vs 축별 2점 내부 경계 vs Standards cut score 미설정. actor-responsibility-criteria는 항목 규칙 | 세 개념을 한 점수로 부르지 않음. 한국어 평가 논문 전문 미확보 |
| AGENTS 정확인용 | 이 작업 트리 | AGENTS.md 근거 표; source-ledger | 미열람을 사실로 쓰지 않음. I'm not human 설치본 미발견 |
| Manual 7 남은 절 | 원문 조사 | 2.1·2.8·2.18–2.24·7.6 확인(2026-09-21). 5.1 규칙 미채택 | 7.7 이후, 8.12 이후, 10.4 이후, 한글 글꼴, 개별 절 인쇄쪽 |
| K7·K8 채점 | 기록 소유 | 본문 축 점수 있음. **독립성 미확인**(차단 로그 없음). K7 이유 줄 출처 없음=근거 결함 | 격리 Run 채점자만 blind로 부를 수 있음 |
| JARS Table 2–8 | 원문 조사 | Table 1만 S8·A-JARSQ | 설계별 표는 해당할 때만 원문 |
| PR #1 검사 | root·이 트리 | MERGEABLE, head는 push 후 SHA로 갱신. 2026-09-20 23:26 조회 시 필수 검사 QUEUED | 필수 검사 성공 뒤에만 merge. 재실행 요청 안 함 |
| 연구 원고 APA 적용 | 연구 담당 `run_de4c37377cf3` | 지침 `/tmp/writing-apa7-guidance-for-research-20260920.md` | 이 트리는 원고 파일을 고치지 않음 |
