# 로컬 검사와 원격 검토 범위

확인일: 2026-11-06. 최종 스킬 파일은 `regression-v3-freeze.json`의 해시와 일치한다. 원격 스킬 내용은 `621298d6c1cb06b14b410ce2e39bceae84ed4a8d`에서 확인했다. 이후 평가 기록·요약 문서와 테스트 목적 docstring을 정리했다. 최종 PR head·Checks·병합 커밋은 [PR #25](https://github.com/ContextualWisdomLab/korean-writing-skills/pull/25)에서 확인한다.

## 로컬 자동 검사

Python 3.12.14에서 아래 검사를 실제 실행했다. Python 3.14나 원격 GitHub Actions 실행으로 표시하지 않는다.

| 검사 | 실제 결과 | 확인 범위 |
| --- | --- | --- |
| `uv run --locked python -m unittest discover -s tests -p 'test_*.py' -q` | 119개 통과 | 저장소 자동 회귀 검사. 글쓰기 효과의 측정과 구별 |
| `uv run --locked python tests/skill_structure_test.py` | `skill structure contract: ok` | 스킬 구조·참고 파일의 설치 경계 |
| `uv run --locked python tests/source_traceability_test.py` | `source traceability contract: ok` | 인식한 출처 ID와 장부 정의 대응. 원문의 의미 적합성을 자동 검증하지 않음 |
| `bash tests/public_hygiene_test.sh` | `public hygiene contract: ok` | 새 평가 파일을 stage한 상태의 공개 파일 검사 |
| `git diff --cached --check` | 오류 없음 | 공백·패치 형식 검사 |
| 평가 증거 대조 | 모든 대응 일치 | 입력·루브릭·출력·채점·스킬 SHA-256, 이력서·문장의 v2/v3 읽은 파일 동일성, 판정 규칙 |

기준판의 기본 unittest 실행은 113개만 수집했다. 함수형 검사 6개를 직접 실행했을 때 1개가 오래된 확인 표지 기대값으로 실패했다. 기존 작업 노트 분리 정책에 맞춰 기대값을 정정하고 두 모듈에 `load_tests`를 추가해 기본 명령에서 119개를 수집하도록 했다. 새 테스트 의존성을 추가하지 않았다.

## 패키지

`scripts/package_skills.py`로 두 preview ZIP과 manifest를 만들고, ZIP 전체 SHA-256, 멤버 목록, 각 파일의 바이트 길이·SHA-256을 대조했다. 한국어 패키지 13개 파일과 APA 패키지 7개 파일 모두 일치했다. 최종 패키지 해시는 공개 평가 manifest의 `final_preview_packages`에 있다. 이는 패키지 조립 검증이며 공식 release나 실제 에이전트 환경의 설치 완료가 아니다.

## 원격 검토

CodeRabbit의 첫 head `4506bf3ccd14df046e6c5ecf2423b615736be825` 검토는 보고서 예문에 관한 지적 1건을 남겼다. 원자료에 없는 실행 조건을 덧붙인다는 지적을 확인해 고쳤고, 독립 재검토와 원격 파일 확인 후 스레드를 해결했다. Docstring coverage 경고에 대해서는 diff에서 추가·수정한 테스트 함수 3개 모두 목적 설명이 있음을 AST로 확인했다. CodeRabbit의 coverage 재측정 결과로 주장하지 않는다.

수정 head `621298d6c1cb06b14b410ce2e39bceae84ed4a8d`의 CodeRabbit Check는 `completed / neutral`, 제목은 `Review rate limited`였다. 시간당 할당량 제한으로 추가 검토 단계가 생략되었다. 확인 당시 PR-triggered GitHub Actions 실행은 없었다. 로컬 검사 통과와 독립 검토를 원격 CI 통과·GitHub 승인·보호 브랜치 충족으로 바꾸어 기록하지 않는다. 보호 설정이나 필수 검사 규칙은 변경하지 않았다.
