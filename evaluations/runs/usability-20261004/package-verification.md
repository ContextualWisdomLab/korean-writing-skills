# Preview 설치 검증

확인일: 2026-10-04. 대상 스킬 바이트는 [skill-freeze.json](skill-freeze.json)에 기록했다. 이 기록은 로컬 실행 증거이며 공식 release·hosted 검사·GitHub 승인·기본 브랜치 통합이 아니다.

## 실행 결과

- `python3 tests/skill_structure_test.py`: exit 0, `skill structure contract: ok`.
- 초기 `python3 -m unittest discover -s tests -p 'test_package_skills.py' -v`: exit 0, 16 tests, OK. 구현자의 최종 추가 보강 후 같은 명령을 다시 실행하여 exit 0, 19 tests, OK를 확인했다. 초기 16건을 최종 후보의 검사로 대신하지 않는다.
- `python3 scripts/package_skills.py --output …`: 서로 다른 새 출력 디렉터리에서 두 번 실행했다. 각 실행 exit 0, ZIP 두 개와 manifest 생성.
- 초기 두 빌드의 ZIP·manifest SHA-256이 모두 같았다. 최종 패키저 SHA-256 `1ce3743607c31860f17cc13780f2bf6cb9cae012df0320a246d193b6150366ef`와 시험 파일 SHA-256 `9a396d8009079814f3900f5244098b43da01ced0cb8df36f0d7c066ca9e7bc88`에서 두 번 재빌드했다. 최종 digest도 아래 세 값과 동일했고, 압축 해제·11개 파일 해시·구조·Hermes 발견 검사를 다시 통과했다.
- 빌드는 변경 중이지 않은 입력 트리와 운영자가 통제하는 출력 부모 디렉터리를 전제로 한다. 검사와 읽기 사이의 악의적 동시 파일 교체에 대한 격리 경계는 제공하지 않는다.
- ZIP 압축 해제 후 파일 목록·크기·SHA-256을 manifest와 대조했다. 11/11 파일이 일치했다.
- 원 저장소의 다른 파일 없이 새 `skills/` 디렉터리에 두 스킬을 풀었다. 각 스킬의 구조·상대 링크 검사가 통과했다.
- 임시 `HERMES_HOME`을 지정하고 `hermes skills list --source local`을 실행했다. exit 0, `apa7-manuscript-writing`과 `korean-editing` 두 개가 local·enabled로 나타났다. 기존 활성 프로필은 변경하지 않았다.

| 산출물 | SHA-256 |
| --- | --- |
| `apa7-manuscript-writing-preview.zip` | `dc647b2bb4b93991f46f44b652218c584bf85dba78c1132bb9b1537fff7d373e` |
| `korean-editing-preview.zip` | `046dd049343afe22f303646831e316f8d83c42d9daac86733be216ab75e9a7a8` |
| `manifest.json` | `4a3687f2362a0f02964f3d60bb87dfbdc2711b6f86098acdd8204e30b62f9eb8` |

## 독립 검토 실패와 보류

최종 19시험 판본을 독립 검토한 결과, blockquote·목록 안의 참조 정의와 여러 줄 참조 라벨을 스캐너가 놓치는 우회 4건을 실제 재현했다. 일반 inline·최상위 참조의 음성 대조군 2건은 거부되었지만, 해당 우회는 ZIP에 그대로 포함되었다. 패키저의 외부 파일 읽기나 ZIP 멤버 경로 이탈을 관찰한 것은 아니며, 모든 내부 링크를 검사한다는 계약 위반이다.

따라서 위 시험·설치 검증은 결함이 남은 판본의 역사적 결과다. preview 패키지를 검토 승인판으로 배포하지 않는다. 우회 회귀시험과 최소 수정, 전체 재검증·새 독립 검토가 필요하다. 기존 스킬 내용의 해시는 바뀌지 않았으나 패키저 검증 완료 주장과 구별한다.

## 참조 우회 수정 후 부모 재검증

수정 전 네 사례에서 `PackagingError not raised`라는 RED를 확인했다는 구현자의 보고를 보존한다. 수정 후 부모는 새 패키저 SHA-256 `6071d81e26c163918fad0b6d7a18fedc1fc634bdbd378c7915ad636c000d180a`와 시험 파일 SHA-256 `fa26f4e6f9d59d72c850e94e78587fdecc2ec46e1c6458b5f0ae804d6df3ead4`를 직접 계산했다. 같은 전체 unittest 명령에서 exit 0, 23 tests, OK를 확인했고 구조 검사·diff 공백 검사도 통과했다. 수정본으로 서로 다른 새 디렉터리에서 두 번 다시 빌드했다. 두 ZIP과 manifest digest는 위 값과 같고 11개 파일의 압축 해제·해시·구조 검사가 재통과했다. 새 독립 검토는 아직 진행 중이며, 이전 불합격을 지우거나 새 승인을 선취하지 않는다.

## 두 번째 독립 검토의 추가 실패

23시험 판본의 새 검토는 기존 참조 우회 4건 차단과 안전 대조군 6건을 확인했다. 그러나 링크 라벨에 이스케이프된 닫는 대괄호가 있으면 inline 목적지를 놓치는 별도 우회 2건을 실제 재현했다. 따라서 이 판본도 NONPASS다. 부모 재검증 통과와 별개로 두 번째 수정 사이클을 진행하며, 전체 수정본의 새 독립 검토 전에는 commit·push하지 않는다. 스킬 파일과 합성 출력·채점 결과는 변경하지 않는다.

## 두 번째 수정 후 부모 재검증

인라인 라벨 수집을 escape-aware 상태형 scanner로 바꾼 후보에서 부모가 전체 unittest 24 tests, exit 0, OK와 구조·공백 검사를 확인했다. 패키저 SHA-256은 `7be575fad8384e12ec28d2a5e103424fe18750e8534ba14fe0bc9ce02cbc879f`, 시험은 `421912e50fb2d4c235d176ca237b22eb43d84bf45e9921319e6782c689e31d1a`다. 앞선 19·23시험 통과와 독립 검토 NONPASS는 그대로 보존한다. 이 최신 판본의 독립 검토는 진행 중이다.

## 두 번째 수정본의 최종 독립 검토 실패

최종 검토는 정확한 `7be575…`/`421912…` 바이트에서 전체 24시험, 알려진 우회 6건 차단, 안전 대조 6건과 실제 반복 빌드를 확인했다. 그러나 링크 라벨의 코드 스팬 또는 HTML 속성 안에 닫는 대괄호가 있으면 실제 목적지를 놓치는 우회 2건을 추가 재현했다. 따라서 최종 후보도 NONPASS다. 외부 파일 읽기·실행·ZIP 멤버 이탈을 관찰한 것은 아니지만 링크 검증 계약은 만족하지 못한다.

자동 수정 사이클 두 회를 마쳤으므로 추가 수정과 commit·push를 중단한다. 다음 선택은 검증된 Markdown 파서 도입 또는 패키저를 이번 납품 범위에서 제외하는 것이다. 이 결정 전에는 승인판 배포를 주장하지 않는다. 스킬 보강·합성 평가 통과와 패키저 불합격은 별개로 보존한다.

사용자가 후속 조치로 검증된 Markdown 파서 의존성 도입과 재검토를 승인했다. 정규식·수작업 대괄호 scanner를 더 보강하는 대신 잠긴 파서 기반으로 전환한다. 승인 자체는 구현·검증 완료가 아니며, 새 후보의 시험·빌드·독립 검토 후에만 commit·push한다.

## 파서 전환 후 부모 재검증

사용자가 승인한 새 접근에서 `markdown-it-py==4.2.0`과 `mdurl==0.1.2`를 `uv.lock`에 잠갔다. `uv sync --locked --python 3.14`는 성공했다. 부모가 `uv run --locked python -B -m unittest discover -s tests -p test_package_skills.py -v`를 실행하여 exit 0, 29 tests, OK를 확인했다. 기존 수제 scanner의 24시험과 신규 5시험을 함께 실행했고 구조 검사도 통과했다.

후보 패키저 SHA-256은 `9b92af14d794bfd8c8c8be1ee18a8f390c190f68384f84169321739cda2147ec`, 시험은 `6fb6363df8a0ed284ba652f68490649063843aab2eae3b4128e0c140d2d22b2a`, `pyproject.toml`은 `e9d905e21d56f8cb6f32cebf4d39d39d75e21361f19305be204d1a82d490438f`, `uv.lock`은 `9972a62afabdaa9f449a30b1e24a5a0e43ba594541d97a97f4ec54c1f82c8849`다.

부모는 파서 기반 후보를 두 번 빌드하여 ZIP·manifest digest의 동일성과 위 산출물 해시를 확인했다. 11개 파일을 새 디렉터리에 풀어 해시·상대 링크 검사를 통과했고, 임시 Hermes home에서 두 스킬이 local·enabled로 나타났다. 스킬 원문이 같으므로 ZIP 바이트도 같다. 파서의 렌더 의미와 별도의 보수적 admission 정책을 구분하며 HTML sanitizer나 OS 격리를 제공한다고 주장하지 않는다. 새 정확한 후보의 독립 검토는 아직 진행 중이다.

## 파서 기반 후보의 최종 독립 검토 통과

별도 검토자가 정확한 파서 기반 후보 전체와 최종 사용 안내를 읽고 29시험, 알려진 8우회 거부·출력 부재, 대응 안전 대조 8건의 목적지 수집·바이트 보존, 반복 빌드 2회·11개 파일, 구조·공개 hygiene를 직접 검증했다. `package-review-accepted.json`에 최종 파일 해시와 범위를 기록했다. 부모도 그 6개 파일의 SHA-256을 재대조하여 모두 일치함을 확인했다. 기존 24시험 메서드의 AST도 변경되지 않았다.

검토 초기에 사용 안내의 병렬 변경으로 해시 검사가 한 번 실패했다. 검토자는 최종 문서 전체를 다시 읽고 파일·index가 안정된 검증 구간에서 전체 검사·대조·빌드를 다시 실행했다. 그 초기 실패와 이전 수제 scanner NONPASS를 보존한다. 최종 로컬 검토는 PASS이며 GitHub 승인·hosted CI·공식 release와 구별한다.

## 한계

스킬 목록 발견은 실제 대화에서 slash 호출이 성공했다는 증거가 아니다. 스킬 기반 행동은 별도 격리 실행·채점으로 확인한다. 설치 환경 시험은 이 로컬 Hermes CLI 한 환경이며 다른 OS·에이전트 환경의 호환성은 미시험이다. manifest는 자기기술 해시 장부로, 서명·타임스탬프 공증·SBOM·공식 배포 provenance가 아니다. 원문 규칙의 타당도나 전체 APA 적합성은 해시 검사로 입증되지 않는다.
