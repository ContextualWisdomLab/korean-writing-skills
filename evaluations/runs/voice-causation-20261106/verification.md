# 검증 범위

## 로컬 검사

Python 3.12.14에서 다음 명령을 실행했다. 새 실행 의존성이나 테스트 코드는 추가하지 않았다.

| 명령 | 실제 결과 |
| --- | --- |
| `uv sync --locked --python 3.12` | 잠긴 의존성 설치 완료 |
| `uv run --locked python -m unittest discover -s tests -p 'test_*.py' -q` | 119개, 통과 |
| `uv run --locked python tests/skill_structure_test.py` | `skill structure contract: ok` |
| `uv run --locked python tests/source_traceability_test.py` | `source traceability contract: ok` |
| `bash tests/public_hygiene_test.sh` | `public hygiene contract: ok` |
| `git diff --cached --check` | 종료 코드 0 |
| `uv run --locked python scripts/package_skills.py --output <새 저장소 밖 디렉터리>` | 두 preview ZIP과 manifest 생성 |

단위 검사 수에는 내용의 문법적 정확성이나 실제 퇴고 성능이 포함되지 않는다. 구조·출처 검사는 링크와 ID 계약을 확인하며, 출처의 해석은 별도 내용 검토 대상이다.

## 패키지와 입력 동일성

[패키지 manifest](package-manifest.json)의 ZIP SHA-256, 멤버 목록, 각 파일의 길이·SHA-256과 원본 스킬 바이트를 대조했다. 한국어 패키지 14파일과 APA 패키지 7파일, 총 21파일이 일치했다. 새 평가 문서는 스킬 패키지에 들어가지 않는다. 기존 `references/validation.md`는 패키지에는 포함되지만 블라인드 실행 스냅샷에서는 제외했다.

| 패키지 | ZIP SHA-256 |
| --- | --- |
| 한국어 | `31c36ee5e0cb07b44f9183aba57d0c6c5f815234fbe2d37b57a6d5d24c10ab63` |
| APA | `931ee058eb88470515abb9f83f41e664795f2f63543ad926af6c9efa3b73bdf9` |

동결한 입력·기준 3파일은 공개본과 바이트가 같다. 두 루브릭 사본은 공개 위치에 맞춰 상대 링크 네 곳만 바꾸었으며, 이를 되돌렸을 때 실행 사본과 바이트가 같은지 확인했다. [freeze.json](freeze.json)은 실행 사본의 해시와 공개 사본의 해시를 구분한다. 이 변경으로 채점 문구나 수용 기준을 바꾸지 않았다.

## 원격 근거와 한계

내용 커밋은 `0c2e6958961d73c2e78ce011fe564b9da0a00ff8`이며, 원격 트리 `92b859ef28d441e6443fe14eef9a1f29e2ac8087`가 로컬 staged 트리와 같은지 확인했다. 부모는 기준 main `0cd3281e075a5644498cf25f85d5563a2ea5ee67`다. [PR #26](https://github.com/ContextualWisdomLab/korean-writing-skills/pull/26)에 검토·평가 진행 상태를 명시한 뒤 열었다.

실제 GitHub Checks·리뷰·최종 head·병합 여부는 PR의 원격 상태로 별도 확인한다. 위 로컬 검사를 GitHub Actions 통과, 보호 브랜치 승인, 정식 release 또는 실제 팀 사용 검증으로 표시하지 않는다.

위 내용 커밋의 CodeRabbit 검사는 `completed / success`(`Finished`)로 끝났으며, 조회 시 inline review thread는 0건이었다. 해당 커밋의 PR용 GitHub Actions workflow run은 0건이었다. 이 결과는 내용 커밋의 관찰이며, 이후 평가 기록을 추가한 head의 자동 검사 결과로 승계하지 않는다.

## 인과 보존 보강 뒤 검증

최초 문법 응답에서 시간적 선후를 인과로 강화한 설명을 확인한 뒤, 기존 의미 보존 조건의 적용 범위를 수정 이유와 선택안까지 명시했다. [별도 내용 검토](causality-patch-review.md)에서 필수 수정이 없었으며, 후속 내용 커밋 `9bed9a94a390fb7d545ccfe73b72f4372944748c`의 원격 트리 `158adac0c7aac65570030d0f5b5a5e1f03c0fed3`가 staged 트리와 일치했다. [최종 스냅샷](final-freeze.json)은 이 내용을 고정한다.

이 판본에서 위 `unittest` 명령을 다시 실행해 **119개, 5.972초, OK**를 확인했고, 스킬 구조·출처 추적 검사도 통과했다. 변경한 것은 지침 문장 두 곳이며 실행 코드·의존성은 그대로다.

[최종 preview manifest](final-package-manifest.json)의 ZIP 해시·멤버 목록·21개 파일의 크기와 SHA-256·원본 바이트를 대조해 모두 일치함을 확인했다. 한국어 ZIP 해시는 `4a00c7a1f257ad0c39e00eda842c7f4d1d0d73ba01741e3885272bc3ebfee455`이며 APA ZIP 해시는 위 표와 같다. 앞선 `package-manifest.json`은 최초 후보의 패키지 기록으로 보존한다.

후속 내용 커밋의 CodeRabbit 검사는 `completed / neutral`, 제목 `Review rate limited`로 끝났고 inline review thread는 0건이었다. 이 커밋의 자동 내용 검토 통과로 표시하지 않는다. 두 파일의 후속 내용은 위 독립 검토와 로컬 검사로 확인했으며, 최종 평가 기록 추가 뒤의 head 상태는 PR에서 다시 확인한다.

## 동시 main 변경의 통합 검증

실행 중 main에 [PR #27](https://github.com/ContextualWisdomLab/korean-writing-skills/pull/27)의 경력 문서 보강이 합쳐졌다. main `6f9fec1972937eb5a2895d895e97b5ff323dae03`과 후속 내용 커밋을 부모로 둔 통합 커밋은 `4439a2183fe564494278d7ee809d06375f2cb79a`이며, 트리는 `06a4e2880e95cfa2ece077a57d6c821b407541e4`다. 원격 부모 2개와 트리를 직접 조회해 확인했다. 변경 이력의 충돌 한 곳은 양쪽 항목을 모두 보존해 해결했으며, 최신 main 대비 이 요청의 소스 변경은 기존 10파일 범위다.

통합 판본에서 `unittest` **119개, 6.836초, OK**, 스킬 구조·출처 연결 검사 통과를 확인했다. [통합 preview manifest](integrated-package-manifest.json)의 ZIP·멤버 목록·파일 21개의 길이·해시·원본 바이트도 대조해 일치했다. 한국어 ZIP SHA-256은 `753d46eab8c118918e3d56497736ab211eaf85bd9da10164b740d72638bc5d16`이며 APA는 이전과 같다.

통합 후 전체 스킬의 파일 7개가 후속 보강 스냅샷 R과 다르므로, R의 응답 점수를 이 통합 판본으로 승계하지 않는다. 새 능동·피동·사동 참고 문서는 바이트가 같고, 차이는 [통합 스냅샷 기록](integrated-freeze.json)에 열거한다. 이 문서의 검사·패키지 결과와 응답 채점의 버전별 범위는 서로 구분한다.

[병합 변경 보존 대조](integration-line-audit.json)에서는 공통 기준→R과 최신 main→통합본의 스킬 변경을 비교하고, 반대쪽 부모의 변경도 같은 방식으로 대조했다. 이번 요청의 스킬 6파일과 동시 main의 스킬 7파일에서 추가·삭제된 비어 있지 않은 줄의 다중집합이 각각 일치했다. 이는 변경 내용의 보존 검사이며 문장 순서나 의미 적합성의 증명은 아니다. main의 경력 평가 자료와 이력서·보고서·배치 지침 중 이번 요청이 수정하지 않은 파일들은 통합본과 main 사이에 diff가 없었다.

[독립 통합 검토](integration-review.md)에서도 필수 수정이 없었다. 검토자는 자동 병합된 지침 4개의 변경 구간과 인접 문맥, 변경 이력 충돌 해결, 양쪽 부모의 diff·blob 보존을 확인했다. 평가 자료 본문과 외부 출처를 읽거나 전체 문법 지침을 다시 평가하지 않았다.

## 평가 증거 공개 전 감사

새 증거를 staged 파일에 포함한 뒤 공개 파일 위생 검사와 `git diff --cached --check`가 통과했다. [최종 증거 감사](final-audit.json)는 동결 실행 문서 5개, 공개 입력·기준 3개, 링크만 조정한 루브릭 2개, 원본 출력 6개와 채점 자료 7개의 바이트·해시 대응을 확인했다. 통합 스킬 13파일과 실행 스냅샷 R의 13파일도 각각 해당 동결 기록과 일치했다.

추가된 Markdown의 상대 파일 링크는 모두 존재하는 저장소 내부 대상으로 연결됐다. 이 검사는 URL fragment나 외부 링크 전체의 현행 유효성을 검증하지 않으며, 공식·학술 원문의 실제 열람은 출처 장부의 범위를 따른다. 두 수용 평가자의 접근 범위 자기보고와 점수·중대 오류·통과 판정의 일관성을 확인했고, 후속 채점의 직접 인용은 원본 출력에 실제로 있는 문자열과 대조했다. 절차상 보류한 최초 채점은 수용 점수에 포함하지 않았다.
