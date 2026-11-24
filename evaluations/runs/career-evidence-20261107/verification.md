# 검증 기록

확인일: 2026-11-07. 이 기록은 경력 중심 글쓰기 보강의 최종 스킬 스냅샷을 대상으로 한다. 입력·기준·스킬 해시는 `final-freeze.json`에 있으며 완료 후 실제 저장소 파일과 다시 대조했다.

| 검사 | 실행 명령·범위 | 관찰 결과 |
| --- | --- | --- |
| 기존 단위 검사 | `uv run --locked python -m unittest discover -s tests -p 'test_*.py'` | 119개 통과. CPython 3.11.17. 원출력은 `unit-tests.txt`, 실행 정보는 `unit-tests.json` |
| 스킬 기본 검사 | skill-creator의 `quick_validate.py`에 `skills/korean-editing` 전달 | `Skill is valid!` |
| 스킬 구조·로컬 링크 | `uv run --locked python tests/skill_structure_test.py` | `skill structure contract: ok` |
| 출처 ID 대응 | `uv run --locked python tests/source_traceability_test.py` | `source traceability contract: ok` |
| 공개 자료 위생 | `bash tests/public_hygiene_test.sh` | `public hygiene contract: ok` |
| Preview 빌드 | `uv run --locked python scripts/package_skills.py --output OUTPUT_DIRECTORY` | 두 ZIP과 manifest 생성. 실제 출력 경로는 공개 기록에 남기지 않음 |
| 변경 형식 | `git diff --check`, 스테이징 후 `git diff --cached --check` | 오류 없음 |
| 내용 검토 | 작성자와 다른 검토자가 스킬 변경을 검토 | 지적 세 건 수정 후 같은 검토자가 재확인 |
| 적용 점검 | 고정 기준과 합성 두 입력, 새 작성자와 과제별 별도 채점자 | 두 과제 통과. 최초 출력·판정 보존 |

스킬 구현 코드를 새로 추가하거나 검사기를 변경하지 않았다. 고정된 기존 의존성을 사용했다. 구조·해시 검사는 원문 적합성이나 표현의 품질을 대신하지 않으며, preview 빌드는 실제 사용자 환경 설치·공식 release를 뜻하지 않는다. GitHub 호스팅 검사와 로컬 검사도 구분한다. 원격 반영 상태는 연결된 PR과 커밋에서 확인한다.
