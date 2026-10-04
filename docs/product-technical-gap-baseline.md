# Product and Technical Gap Baseline

기준 시점: 2026-10-03

관찰 기준(이 문서 변경 직전):
`main@ca94600ed058c0e7448ac69a537b8453241d139b`, Draft PR #5
`f5de04263ea4c3785a8ccbb7bd4ab360e178a986`, Draft PR #6
`2b140986fd4fb4a7715141a249bf12d55e5427be`, Draft PR #4
`6070799af53ed730d90e48b1c1e011eb9ecfdd17`. GitHub branch API는
`main`을 `protected:false`로 보고하며 repository ruleset은 없다.

2026-10-04 재확인: Git 원격·공개 PR 본문에서 PR #4의 descendant
`d7cade69f30ffc580cdb468152ed82dc21c2c4ef`와 PR #5/#6/#4의
94/49/34-file 스택을 확인했다. 위 보호·CI·승인 수치는 과거 관찰이며
이번 `gh` 인증 실패 상태에서 현재 API 값으로 재검증한 것이 아니다.
이번 제한 범위 작업과 수용 기준은 [실사용판 개발 계약](usability-plan.md)에 둔다.
새 Python 패키저가 추가되는 경우 CodeQL 적용 언어를 다시 판단해야 하며,
아래의 과거 skip을 새 head의 성공이나 비적용 판정으로 이어받지 않는다.

상태: Proposed

## Goal과 Loop

**Goal**: 출처 범위를 과장하지 않고 의미를 보존하는 한국어 퇴고와 APA 7
원고 작성 Agent Skill을 독립적으로 설치·검토할 수 있게 한다.

**Loop**: 원문 직접 확인 → source ledger 갱신 → 규칙 최소 수정 → 동결된 합성
사례와 독립 채점 → 공개 hygiene·CI·review → 유효한 default-branch 거버넌스
확인 → ordinary merge → immutable release.

## PRD

| 사용자 | 해야 할 일 | 수용 기준 | 상태 |
| --- | --- | --- | --- |
| 한국어 저자·편집자 | 의미를 보존하며 문장·문단 퇴고 | 수치·불확실성·인용 보존, 과잉 교정 방지 | Proposed |
| 학술 저자 | 확인된 APA 7·JARS 범위로 원고 점검 | 확인 절·쪽과 미확인 범위를 구분 | Proposed |
| 검토자 | 평가 주장의 근거와 한계를 재구성 | 입력·판본·출력·채점·hash·한계 연결 | Partial |
| 실제 사용자·팀 | 실업무에서 설치·호출하고 피드백 제공 | 사용한 스킬 digest·작업 유형·비식별 예문·도움·어색함·의미손실·과잉교정·지연·수정·독립 재검증. 미사용은 미사용으로 기록 | Open — 합성 평가와 별도 |

## TRD

- 배포 단위: `skills/korean-editing/`, `skills/apa7-manuscript-writing/`.
- 근거 정책 경계: 각 skill의 `references/source-ledger.md`; 자동 traceability는 미구현.
- 검증 경계: `evaluations/`, `tests/public_hygiene_test.sh`,
  `tests/skill_structure_test.py`.
- 금지 경계: 사용자 원문·참여자 자료·비밀정보, 검사에 열거한 workstation
  절대경로·ephemeral ID·GitHub/OpenAI/AWS credential·private-key signature.
- 현재 실행 서비스, DB, UI, 인증, container와 network API는 없다.

## UML과 Context Map

Context Map과 구성요소 책임은 `ARCHITECTURE.md`가 소유한다. 처리 순서는
다음과 같다.

```mermaid
sequenceDiagram
  participant A as Author
  participant S as Skill
  participant E as Evidence ledger
  participant R as Reviewer
  A->>S: 원문과 목적 제공
  S->>E: 확인한 규칙 범위 조회
  S-->>A: 수정안과 확인 요청
  R->>E: 판본·hash·한계 검토
```

## ERD

DB를 소유하지 않으므로 ERD는 적용하지 않는다. 파일 기반 근거를 DB 권위로
가장하지 않는다. 향후 영속 서비스가 생기면 최소 3NF 스키마와 보존·삭제
계약을 별도 ADR에서 정의한다.

## Gap와 Action

| Gap | Evidence | Action | Status |
| --- | --- | --- | --- |
| default branch에 제품 구현과 유효한 보호가 없음 | `main@ca94600e…`에는 `AGENTS.md`와 `README.md`만 있고 branch API는 `protected:false`; repository ruleset 없음 | `.github` canonical owner에서 유효한 조직/default-branch 보호를 입증한 뒤 exact-head 검사·비작성자 review와 ordinary merge | Blocked |
| public hygiene가 중앙 gitleaks skip과 수동 확인에 의존 | PR #4 exact-head Security job과 과거 runtime artifact | RED credential fixture 뒤 `tests/public_hygiene_test.sh`에 GitHub/OpenAI/AWS credential·private-key signature를 fail-closed 통합 | Implemented on PR head |
| Skill 독립 설치 시 repository 외부 문맥에 의존할 수 있음 | `skills/korean-editing/SKILL.md`의 평가 rubric 링크 | package 밖 상대 링크를 fail-closed 검사하고 평가 증거는 실행 의존성에서 분리 | Implemented on PR head |
| 단일 PR이 hosted review 한도를 넘음 | 기존 base-to-head 175 files; CodeRabbit은 100-file 한도로 review를 건너뜀 | PR #5(94 files) → PR #6(49 files) → PR #4(34 files) non-force stack을 유지하고 각 exact head에서 review 수행; 모든 유효 delta는 PR #4 최종 descendant에 보존 | Implemented in PR stack |
| 최신 head의 독립 review 부재 | PR #5/#6/#4 exact head 승인 0건, unresolved thread 0건; 각 head의 PR workflow run 0건, CodeRabbit status만 success | 유효한 거버넌스를 만든 뒤 세 current head의 적용 가능한 hosted Checks와 독립 review를 확보 | Blocked |
| CodeQL 적용 언어 0건 | exact-head CodeQL PR run `36966902575`는 `skipped`; SAST `36966902465`와 Security `36966902494`만 terminal success | CodeQL skip을 GREEN으로 승격하지 않고 향후 지원 언어 추가 시 재검증 | Not applicable, not GREEN |
| outbound LICENSE 미정 | root LICENSE 없음 | 저작권·외부 자료 경계 확인 후 조직 소유자가 결정 | Open |
| APA 원문 확인 범위 불완전 | `TODO.md`, APA source ledger | 필요한 절만 직접 확인하고 미확인은 유지 | In progress |
| 평가의 일반화 근거 부족 | 사례별 1회·자기보고 한계 | 반복·독립 채점 설계를 별도 계획으로 확장 | Open |
| 규칙↔source ID 추적이 수동 | source ledger와 SKILL.md | traceability validator 설계·fixture 추가 | Open |
| immutable 배포 계약 부재 | release/tag 0개 | manifest·version·digest·SBOM·provenance·clean-install conformance·rollback 절차 정의 | Open |
| Issue #2가 폐기된 PR #1을 가리킴 | Issue #2 본문과 successor reconciliation comment | PR #4 successor와 현재 acceptance를 기록 | Implemented on PR head |

## Release gate

PR #5 → PR #6 → PR #4의 모든 유효 delta가 유효한 default-branch
거버넌스를 거쳐 순서대로 통합되고, 각 exact-head 검사와 독립 review가 끝나며,
release artifact가 생성되기 전에는 GitHub Pages 공개·제품 완료·APA 준수·전체
타당화를 주장하지 않는다.
