# 전담 리드 작업 원장

확인일: 2026-09-20. 전담 리드: Codex `term_731b94a7-ac3c-437c-876c-df9f8416eb66`, 현재 dispatch `ctx_812ff2c52f7e`(인수 `ctx_b7f2a390f5cd`), root `run_b22de9a1c59d`. 종료된 Cursor 리드는 재시작하지 않는다. 운영·검토·후속 배정은 이 리드와 root가 맡는다.

## 인수와 파일 소유

main `ca94600ed058c0e7448ac69a537b8453241d139b`와 PR #1 `51c1c890d9b09a7aa11010e9398232977c337116`을 확인한다. 두 로컬 작업 트리는 인수 시 깨끗하다. 기존 PR 작업 트리에서 이 원장과 기록의 수용 범위만 정리한다. 기존 스킬·APA 근거 파일은 보존한다.

Air `ctx_a68eae315695`는 연구 run `run_de4c37377cf3`의 기존 작업이다. `worker-show`와 `worker-read`로 MacBookAir의 `writing-apa-jars-20260920`, 브랜치 `seonghobae/writing-apa-jars-sourcecheck-20260920` 및 JARS 본문 대조 진행을 확인한다. 인수 때에는 완료 결과나 통합할 commit을 받지 않는다. 후속 작업에서 completed/released와 연구 PR #237의 `7d34241` 두 문서를 직접 확인한다. 직접 인계 메시지는 Run 경계로 거절되어 root에 한 번 전달을 요청한다(`msg_5add53e4803d`). 연구 리드의 승인을 후속 작업 조건으로 삼지 않는다. 기존 dispatch lifecycle은 원래 Run에 남긴다.

| 작업 | 담당·소유 파일 | 증거 | 다음 조치·수용 조건 | 의존성 |
| --- | --- | --- | --- | --- |
| APA/JARS 원고 대조 | 기존 Air `ctx_a68eae315695`; 연구 저장소 작업 파일 | PR #237 `7d34241`; 쪽수 정정 `28c8c442` | 이 리드가 두 문서를 직접 읽고 Sampling procedures를 소장 PDF와 대조; 정확한 쪽수만 APA 스킬에 반영 | Manual 7·원고 고유 공백은 별도; Air lifecycle 종료 |
| APA 스킬 통합 | 이 OpenCode; `skills/apa7-manuscript-writing/` 후속 수정 | 현재 PR의 source-ledger·validation + A-NUM(`6a1b2b67…`)·A-REF(`fc74e6a4…`)·A-JARSQ(`11c042b1…`) 직접 대조(`/tmp/apa-src-20260920/u02·u01·u07`) | Manual 7 실제 본문, Table 2–8·Qual/Mixed 본문, 원고 고유 수치·설계·IRB를 공통 규칙에 복사하지 않음; 영어 수사 규칙 한글 강제 금지 | Air 결과와 별개로 부족한 본문은 직접 확보; 연구리드 승인 불필요 |
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

후속 담당은 이 OpenCode와 root다. Manual 7 본문, JARS Table 2–8·Qual/Mixed 본문, 한국어 평가 논문 전문과 강원국·김정선 원서 본문, 정확한 I'm not human 설치본, 현 루브릭 재채점 또는 동결본 비교 기록(동결 `a6006a30…`·현 `96022f61…` 채점표 동일 확인)·새 스킬 실행·별도 채점, PR #1 필수 검사·검토는 계속 남는다. 이번 원문 검토자는 `/root/standards_source_review`, 사례 채점자는 `/root/standards_case_scorer`이며 둘 다 지정 작업을 마친다. 연구리드의 반복 승인에 의존하지 않는다.
