# PR #28 리뷰 반영과 추가 검증

검토일: 2026-11-08. [PR #28](https://github.com/ContextualWisdomLab/korean-writing-skills/pull/28)의 CodeRabbit 리뷰는 `633729d16bc6ef7dc0f29ba0e559df4dc0cdff78`을 대상으로 했다. 리뷰 본문의 수정 제안 7건과 평가 보완 제안 1건을 저장소의 현재 내용·실행 결과·공식 원문과 대조했다. 인라인 제안은 5개 스레드로 묶여 있다.

## 수정 제안의 판단과 반영

| 제안 | 확인한 문제와 반영 |
| --- | --- |
| 작성과 교정의 입력 구분 | README가 모든 요청에 원문을 요구하는 것으로 읽혔다. 독자·장르·보존 자료는 공통으로 받고, 교정은 원문·수정 범위, 새 작성은 목적·확인된 사실 자료를 받도록 나누었다. |
| 러닝헤드의 최대 길이 | `50자`만 적힌 요약을 공백·문장 부호 포함 `최대 50자`로 명확히 했다. 대문자·왼쪽 배치·표지 생략 조건은 유지했다. |
| 학생 논문의 러닝헤드 예외 | 공식 APA Page Header에서 교수자나 기관이 요구하는 학생 논문에도 러닝헤드를 사용함을 확인했다. 현행 체크리스트와 보고 절차까지 맞추고, 과거의 끊긴 Manual 열람 기록은 그대로 남겼다. |
| 자료 출처·재사용의 공개 표시 | 별도 기록만으로 원고의 출처 고지를 대신할 수 있는 표현을 고쳤다. 본문·저자 주 등 독자가 볼 위치에 출처·재사용 사실을 남기고, 학위논문에 기반한 논문의 저자 주 안내를 공식 근거와 연결했다. 한국어 스킬의 같은 조건도 맞추었다. |
| 학위논문 직접 인용의 위치 | 내부 작업용 대조 쪽수와 실제 직접 인용의 위치 정보를 구별했다. 직접 인용의 저자·연도·쪽수 또는 대체 위치는 보존한다. |
| 검증된 명령의 갱신 | 사용자가 현재 사용 안내의 명령 갱신을 요청하고 현재 CLI나 공식 문서로 대체 명령·옵션을 확인한 경우에만 수정할 수 있도록 했다. 문장 교정만 요청했거나 대체 명령이 미확인이면 보존하며, 과거 로그·직접 인용·동결 평가는 갱신 대상에서 제외했다. 명령 편집을 실행 권한으로 취급하지 않는다. |
| 링크를 거치는 임시 경로 | `TMPDIR`의 심볼릭 링크 때문에 설치 도구가 테스트 준비 경로를 거부하는 문제를 재현했다. 테스트의 기준 경로에 `Path.resolve()`만 적용했으며, 실제 설치·업데이트 코드는 바꾸지 않았다. |

APA의 새 확인 범위는 [APA 근거 장부](../../../skills/apa7-manuscript-writing/references/source-ledger.md)에 기록했다. 직접 연 원문은 [Page Header](https://apastyle.apa.org/style-grammar-guidelines/paper-format/page-header), [Plagiarism의 Exceptions](https://apastyle.apa.org/style-grammar-guidelines/citations/plagiarism), [직접 인용의 쪽수 안내](https://apastyle.apa.org/style-grammar-guidelines/citations/quotations/page-numbers), [2024 JARS-Quant Table 1](https://apastyle.apa.org/jars/quant-table-1.pdf)의 PDF 1쪽 Author Note다. 웹 본문을 읽은 것을 Manual의 추가 절 열람으로 기록하지 않는다.

## 임시 경로 문제의 재현

Python 3.14.9에서 실제 임시 디렉터리를 가리키는 심볼릭 링크를 만들고 `TMPDIR`로 지정했다. 같은 조건에서 기존 `test_auto_update_skills.py`의 9개 테스트를 실행했다.

| 판본 | 관찰 결과 |
| --- | --- |
| 수정 전 | 9개 모두 `setUp()`에서 `InstallError: symlinked installation paths are refused`로 실패. 2.419초, 종료 코드 1. |
| `.resolve()` 적용 후 | 9개 통과. 3.593초, 종료 코드 0. 기존의 설치 대상 링크·위험한 upstream 링크 거부 검사도 통과했다. |

## 독립 내용 검토

작성에 참여하지 않은 검토자가 README와 한국어 스킬·지침 교정 절차·E1 장부의 네 파일을 대조했다. 의미·조건 손실이나 명령 실행 권한의 확장을 발견하지 못했다. APA의 네 파일은 조정 담당자가 위 공식 원문과 변경분을 별도로 대조했다. 이 검토는 문서상 조건·근거 일관성을 확인한 것이며 실제 원고나 일반 성능의 검증이 아니다.

## 다섯 문장 경계 사례

리뷰의 평가 보완 제안에 따라 두 문단·다섯 문장의 새 합성 과제를 추가했다. [입력](boundary-input.md)과 [관찰 기준](boundary-criteria.md)을 실행 전에 작성하고 [판본·해시](boundary-freeze.json)를 동결했다. 적용 판본은 `633729d16bc6ef7dc0f29ba0e559df4dc0cdff78`이며, 이 판본의 전체 한국어 스킬 사본을 별도로 추출해 새 문맥의 실행자에게 제공했다. 후속 리뷰 수정에서도 짧은 운영·CI 보고의 문단 순서 지침은 바뀌지 않았다.

실행자의 [최초 출력](boundary-output.md)은 두 문단의 순서와 담당자·시점·18건 중 17건 통과·1건 실행 중·전체 결과 미확인을 유지했다. 별도 평가자가 입력·기준·출력만 읽어 네 관찰 기준이 충족됐다고 [판정](boundary-scoring.md)했다. 읽은 파일 목록은 교정문에 포함하지 않도록 별도로 요청한 메타데이터다. 한 사례의 출력으로 내부 절차 생략이나 다른 분량·장르의 일반 성능을 입증하지 않는다.

## 전체 단위 검사

리뷰 수정분을 반영하고 `uv sync --locked --python 3.14`로 잠근 환경을 확인한 뒤 다음 명령을 실행했다. Python 3.14.9에서 152개가 18.423초에 통과했고 종료 코드는 0이다.

```bash
uv run --locked python -m unittest discover -s tests -p 'test_*.py' -v
```

원시 출력의 마지막 부분:

```text
Ran 152 tests in 18.423s

OK
```

스킬 구조·상대 링크 검사와 출처 ID 추적 검사도 통과했다. 변경 문서의 로컬 링크, 경계 과제의 동결 해시, 평가 판본과 최종 수정본의 짧은 보고 지침 일치를 확인했다. 리뷰 수정분의 스킬 파일로 ZIP 두 개와 `manifest.json`을 생성했다. 패키징 성공은 공식 출시나 APA 전체 적합성의 인증이 아니다.
