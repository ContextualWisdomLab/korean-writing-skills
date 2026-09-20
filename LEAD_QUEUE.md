# 전담 리드 작업 원장

확인일: 2026-09-20. 전담 리드: Codex `term_731b94a7-ac3c-437c-876c-df9f8416eb66`, dispatch `ctx_b7f2a390f5cd`, root `run_b22de9a1c59d`. 종료된 Cursor 리드는 재시작하지 않는다. 운영·검토·후속 배정은 이 리드와 root가 맡는다.

## 인수와 파일 소유

main `ca94600ed058c0e7448ac69a537b8453241d139b`와 PR #1 `51c1c890d9b09a7aa11010e9398232977c337116`을 확인한다. 두 로컬 작업 트리는 인수 시 깨끗하다. 기존 PR 작업 트리에서 이 원장과 기록의 수용 범위만 정리한다. 기존 스킬·APA 근거 파일은 보존한다.

Air `ctx_a68eae315695`는 연구 run `run_de4c37377cf3`의 기존 작업이다. `worker-show`와 `worker-read`로 MacBookAir의 `writing-apa-jars-20260920`, 브랜치 `seonghobae/writing-apa-jars-sourcecheck-20260920` 및 JARS 본문 대조 진행을 확인한다. 이 시점에는 완료 결과나 통합할 commit을 받지 않는다. 직접 인계 메시지는 Run 경계로 거절되어 root에 한 번 전달을 요청한다(`msg_5add53e4803d`). 연구 리드의 승인을 후속 작업 조건으로 삼지 않는다. 기존 dispatch lifecycle은 원래 Run에 남긴다.

| 작업 | 담당·소유 파일 | 증거 | 다음 조치·수용 조건 | 의존성 |
| --- | --- | --- | --- | --- |
| APA/JARS 원고 대조 | 기존 Air `ctx_a68eae315695`; 연구 저장소 작업 파일 | 2026-09-20 worker-read에서 개인·그룹 JARS PDF 탐색과 본문 대조 관찰 | 이 리드가 완료 보고·commit·본문 위치를 읽고 일반 스킬에 적용 가능한 내용만 검토 | 기존 Air 결과; 중복 조사 시작하지 않음 |
| APA 스킬 통합 | 이 Codex; `skills/apa7-manuscript-writing/` 후속 수정 | 현재 PR의 source-ledger·validation | Manual 7 실제 본문, 공식 APA/JARS 및 개인·그룹 Zotero 조회 범위를 구분; 원고 고유 수치·설계·IRB를 공통 규칙에 복사하지 않음 | Air 결과와 별개로 부족한 본문은 직접 확보; 연구리드 승인 불필요 |
| 한국어 원문 대조 | 이 Codex; `skills/korean-editing/references/` 후속 검토 | 기존 source-ledger의 국립국어원·대학·KBS·신문·강원국·김정선 항목 | 기존 기록을 새 열람으로 계산하지 않음; 발행기관·제목·판본·URL·쪽/절·확인일·제한 문장을 원문과 대조 | 원서 부분 확인과 미확인 논문 전문은 남은 조건 |
| 주어·능동·피동·사동 | 이 Codex; 한국어 스킬 후속 검토 | SKILL.md와 K5/K6 입력·출력 | 행위자·대상·범위·책임·불확실성 보존; 생략 주어를 화자로 단정하지 않음 | 새로운 예문은 별도 실행자와 채점자 필요 |
| PLD·판정준거 | 이 Codex; 평가 문서 | pld-and-standards-framework.md와 three-axis.md | 수준 기술·채점 규칙·내부 통과 경계·검증된 절단점을 구분; Zotero Standards 원문 재대조 전 기존 쪽수를 새 확인으로 보고하지 않음 | 개인·그룹 원문 및 PDF/인쇄 쪽 대응 |
| 기존 평가 검증 | 이 Codex; manifest 읽기 전용 | round-3-k5-k6 manifest 8개 SHA-256 현재 바이트 일치 | 두 사례의 별도 점수만 수용; 전체 타당화·채점자 일치도·APA 준수로 확대하지 않음 | 전체 접근 감사는 아님 |
| 기록 독립 검토 | 별도 Codex `/root/review_acceptance`; 읽기 전용 | 평가·원장 주장 일관성 검토 | 발견 사항을 리드가 최소 수정; 신규 블라인드 행동평가로 집계하지 않음 | 검토 완료; 신규 행동평가는 별도 |
| PR 통합·원격 | 이 Codex; 이 원장·기록 수정 | PR #1 head 및 현재 checks | 수정 파일만 commit/push 후 원격 SHA 확인; merge는 필수 검사와 검토 충족 뒤 판정 | 현재 필수 checks pending; CodeRabbit 표시는 Review rate limited |

## 원문 확인 절차

연구 저장소 `[redacted-research-lead]-v3/.agents/skills/source-check/SKILL.md`를 읽는다. 개인·elderly-gad 양쪽 검색, PDF와 인쇄 쪽 대응, 주장에 해당하는 문장과 제한 문장 대조, 인용한 양과 실제 판정량의 일치, OCR 이미지 대조 여부를 적용한다. 캐시 검색 결과만으로 쪽수를 붙이지 않는다. 이번 인수에서는 문헌 원문을 새로 확인했다고 보고하지 않는다.

이 절차에 따라 기존 출처의 확인 기록과 현재 리드의 파일 검증을 구분한다. 연구 참여자 자료·비공개 원문 PDF·전체 도서 본문을 공개 저장소에 추가하지 않는다. 추적 대상이 Markdown·JSON 문서뿐이고 코드 탐색이 없어 이번 문서 인수에는 CodeGraph 인덱스를 만들지 않는다. 무거운 빌드와 CI 재실행 요청은 하지 않는다.

## 독립 검토 반영

별도 Codex는 기존 평가 기록만 읽고 두 불일치를 찾는다. PLD 문서에서 검증된 시험 절단점과 축별 2점의 내부 통과 경계를 구분하고, TODO에서 철회된 round-2를 완료 증거에서 제외한다. 기존 실행·채점 원본과 스킬은 바꾸지 않는다. `review.md`의 제한된 리드 수용과 채점자의 실행 전체 보류는 함께 유지한다.
