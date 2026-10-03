# Changelog

## Unreleased

- `main`의 실제 미보호 상태와 175-file review 한도를 Gap 기준선에 반영하고,
  PR #4를 Draft로 되돌렸다.
- 유효 delta를 보존한 채 175-file 변경을 PR #5(94 files) → PR #6(49 files)
  → PR #4(32 files)의 reviewable non-force Draft stack으로 분할했다.
- 한국어 퇴고와 APA 7 원고 작성 Agent Skill 초안을 추가했다.
- 확인한 원문 범위와 미확인 범위를 source ledger에 분리했다.
- 동결 입력·출력·채점·한계를 포함하는 제한된 합성 평가 증거를 추가했다.
- repository 공개 경계, 보안 보고 절차, Gap baseline, Skill 구조 검사와
  fail-closed 공개 hygiene 검사를 추가했다.
- 독립 설치 단위 밖으로 나가는 Skill 상대 링크를 금지하고 평가 증거를 실행
  의존성과 분리했다.
- 중앙 gitleaks가 적용되지 않는 문서·평가 repository 경계를 보완해 GitHub·OpenAI·AWS
  credential과 private-key signature의 재유입을 fail-closed 검사한다.

보호 브랜치 병합과 immutable release 전에는 배포 완료로 간주하지 않는다.
