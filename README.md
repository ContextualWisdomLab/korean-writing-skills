# 한국어 글쓰기·퇴고·APA7 스킬

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/ContextualWisdomLab/korean-writing-skills)

공신력 있는 원문에 근거하여 한국어다운 문장·글 구조 퇴고와 APA 7 학술 논문 작성을 돕는 에이전트 스킬 저장소.

## 스킬

| 스킬 | 경로 | 상태 |
|------|------|------|
| 한국어 퇴고 | `skills/korean-editing/` | 초안 — K5/K6 별도 채점 통과, 전체 타당화 미완료 |
| APA7 논문 | `skills/apa7-manuscript-writing/` | 초안 — JARS Table 1·Manual **일부 절** 직접 확인(2.1은 재열람 표제만 확인·필수 요소 목록 채점 제외; 2.2·2.8·2.12·2.18–2.24·6.36·6.44·7.1·7.4–7.6·7.17·7.18·8.4·8.10·10.1–10.3 도입; 8.6 일부). Publication Manual **전체**·잔여 절은 미확인 |

## 평가

독립 평가 기록은 `evaluations/`에 둔다. `evaluations/runs/round-1-review.md`, `evaluations/runs/round-3-k5-k6/review.md`, K16의 실패·수정 후 재평가는 실행자·채점자 분리와 접근 범위의 한계를 함께 기록한다. 개별 사례 통과를 전체 타당화나 APA 준수의 증거로 확대하지 않는다. [후속 지적·동결 평가 errata](docs/review-followup-20261005.md)는 역사 원본과 점수를 고치지 않고 해석의 한계를 별도로 기록한다.

## 진행

남은 원문 확인·평가·검증 항목은 `TODO.md`에서 관리한다. 터미널·dispatch·run 식별자와 연구 원고 인계 기록 같은 로컬 운영 상태는 공개 저장소의 제품 산출물이 아니므로 추적하지 않는다.

제품 경계와 현재 Gap은 `ARCHITECTURE.md`와
`docs/product-technical-gap-baseline.md`에서 관리한다. 공개 hygiene 계약은
`bash tests/public_hygiene_test.sh`로 확인한다.

## 제한 범위 preview 사용

설치·호출·입력·출력·업데이트·제거 절차는 [사용 안내](docs/usage.md)를 따른다. 두 ZIP과 SHA-256 manifest를 로컬에서 만들 수 있다. 기본 브랜치의 공식 출시본이나 APA 전체 인증은 아니다.

현재 작업의 PR·Issue·요구사항·Gap 대응과 에이전트별 책임은 [실사용판 개발 계약](docs/usability-plan.md)에 기록한다. 합성 평가와 Issue #2가 요구한 실제 팀 사용은 따로 관리한다.

## 설치 경로 구분

이 저장소의 퇴고 스킬은 `skills/korean-editing/`이다. Claude superpowers 플러그인의 `writing-skills`(스킬 작성 TDD)와 이름이 비슷해도 다른 스킬이다.

- 한국어 퇴고: `skills/korean-editing/`
- APA: `skills/apa7-manuscript-writing/`

문서와 평가 기록은 저장소 안 상대 경로로 가리킨다. 작업 브랜치·로컬 절대경로·임시 실행 디렉터리는 재사용 가능한 계약이 아니므로 문서 식별자로 사용하지 않는다.
