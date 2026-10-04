# 설치와 제한 범위 사용

이 제품은 두 Agent Skill이다. Python 명령이 원고를 자동 교정하는 서비스는 아니다. 에이전트가 `SKILL.md`와 필요한 근거 파일을 읽고 수정안·확인 요청을 작성한다. Python은 preview 패키징과 검증에만 사용한다.

## 사용 범위

- `korean-editing`: 한국어 문단·문장·표기를 의미 보존 중심으로 퇴고한다. 이미 자연스러우면 그대로 둔다. AI 작성 여부를 판정하지 않는다.
- `apa7-manuscript-writing`: 확인한 APA 7·공식 안내·JARS 항목으로 원고와 심사 응답을 점검한다. 미확인 Manual 절·쪽, 연구 결과·IRB·동의·서지정보를 발명하지 않는다. APA 전체 적합성 인증이 아니다.
- 학술지 규정과 APA가 다르면 해당 투고 규정을 확인하고 차이를 기록한다. 한국어 어순에 APA 영어 문법을 강제하지 않는다.

## Preview 패키지 만들기

저장소 루트에서 Python 3.10 이상과 `uv`를 사용한다. 링크 검사에는 버전과 해시를 잠근 `markdown-it-py` 의존성이 필요하다. API key는 필요하지 않다. 아래 명령은 에이전트의 `terminal` 도구로도 실행할 수 있다.

```bash
uv sync --locked --python 3.14
uv run --locked python scripts/package_skills.py --output "$HOME/skill-preview-output"
uv run --locked python -m unittest discover -s tests -p 'test_package_skills.py' -v
uv run --locked python tests/skill_structure_test.py
bash tests/public_hygiene_test.sh
```

출력 디렉터리는 새로 정한다. 원본 스킬 디렉터리 안에 만들지 않는다. 빌드는 변경 중이지 않은 입력 트리와 운영자가 통제하는 출력 부모 디렉터리에서만 실행한다. 악의적인 동시 파일 교체를 막는 OS 격리 기능은 없다. ZIP 두 개와 `manifest.json`을 함께 보관한다. ZIP에는 각 스킬의 `SKILL.md`와 그 스킬의 근거 파일이 들어간다. 기존 `references/validation.md`에는 역사적 검증 사례가 있으므로 새 블라인드 평가 실행자의 열람 범위에서 제외한다. 저장소 전체, 새 평가 기준·정답, 사용자 원고, Zotero 원문 전문은 배포 대상이 아니다. manifest의 artifact SHA-256은 내려받은 파일의 digest와 대조한다. 파일별 해시는 압축 해제 후 확인한다. 성공한 구조·해시 검사는 내용의 타당성이나 hosted 승인과 별개다.

### Markdown 검사 경계

빌드 파서는 CommonMark의 실제 링크·이미지·참조·HTML 의미를 읽는다. 패키저는 그 위에 보수적인 허용 정책을 적용한다. 정의가 없는 명시적 참조, 서로 다른 목적지의 중복 정의, 위험한 코드 예제 링크를 거부하며, 코드 안의 링크도 별도로 검사한다. 따라서 일반 Markdown 렌더러가 평문으로 표시할 일부 입력도 빌드에서는 거부될 수 있다. 단순한 `[확인 필요]` 문구는 링크로 간주하지 않는다.

HTML은 수동적인 요소와 명시적인 단일 URL 속성만 허용한다. 스크립트·CSS·이벤트 속성·내장 문서·`srcset`은 지원하지 않는다. 렌더링은 메모리 안에서 검사 용도로만 하며 URL을 열거나 HTML을 실행하지 않는다. HTML sanitizer가 아니므로 이 패키저의 검사 결과를 사용자 HTML을 서비스 화면에 안전하게 게시할 수 있다는 인증으로 사용하지 않는다. [파서 공식 보안 안내](https://markdown-it-py.readthedocs.io/en/latest/security.html)와 [토큰·렌더링 안내](https://markdown-it-py.readthedocs.io/en/latest/using.html)를 확인했다(2026-10-04).

## Hermes에 설치

[Hermes 공식 Skills System 안내](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)는 활성 프로필의 `skills/` 디렉터리와 `/스킬이름` 호출을 설명한다. 아래 수동 설치는 로컬 preview용이다. 승인된 immutable release가 생기기 전에는 기본 브랜치의 GitHub hub 설치를 출시판으로 소개하지 않는다.

1. ZIP을 먼저 임시 검증 디렉터리에 푼다. ZIP 하나에 `korean-editing/` 또는 `apa7-manuscript-writing/`가 들어 있어야 한다.
2. manifest의 파일 목록·digest와 일치하는지 확인한다. 설치된 스킬 이름이 겹치는지도 확인한다.
3. 활성 Hermes home을 확인한다. `HERMES_HOME`을 설정했다면 그 디렉터리를 쓰고, 설정하지 않은 default 프로필은 `~/.hermes`다. 다른 프로필이나 공유 스킬을 덮어쓰지 않는다.
4. 필요한 스킬의 **폴더 전체**를 그 home의 `skills/` 아래에 복사한다. `SKILL.md`만 복사하면 근거 파일이 없어 불완전한 설치다. 같은 이름이 이미 있으면 덮어쓰기 전에 백업과 판본 대조를 한다.
5. 새 Hermes 세션에서 설치된 스킬 목록을 확인한다. 진행 중 세션의 카탈로그가 즉시 갱신된다고 가정하지 않는다.
6. `/korean-editing` 또는 `/apa7-manuscript-writing`을 사용한다. 인식되지 않으면 폴더 구조·활성 home·같은 이름의 로컬 우선순위를 확인한다.

명령을 설치 도구로 자동 실행하는 방식이나 다른 에이전트 환경의 호출 호환성은 별도 시험이 필요하다. Hermes가 외부 디렉터리를 검색하도록 설정할 수도 있지만, 쓰기 가능한 외부 스킬은 에이전트에 의해 수정될 수 있다. 공동 소유 저장소를 운영 스킬 경로로 연결하지 않는다.

## 입력과 결과

한국어 퇴고 요청에는 원문, 독자·장르, 수정 범위, 보호할 용어를 준다. 교정문만 원하는지 중요한 근거 설명도 원하는지 밝힌다.

```text
/korean-editing
안내문을 일반 독자가 읽기 쉽게 고쳐 주세요. 날짜·금액과 직접 인용은 보존하고,
문단과 문장까지 고치되 확인되지 않은 사실은 추가하지 마세요.
원문: 신청은 11월 12일 까지 받습니다. 참가비는 없습니다. 누리집에서 신청할수 있습니다.
```

기대 결과는 수정본이며, 의미에 영향을 주는 변경의 이유와 남은 확인 사항이 필요할 때 함께 나온다. 단어 개수·변경률만으로 의미 보존을 증명하지 않는다.

APA 요청에는 원고·학술지 규정·연구 설계·실제 분석 산출물·실제 읽은 문헌을 제공한다. 민감한 자료는 사용자가 허가한 작업 공간에만 둔다. 이 공개 저장소에 넣지 않는다.

```text
/apa7-manuscript-writing
한국어 투고 초안의 방법·결과를 점검해 주세요. 학술지 서식은 별도 파일입니다.
확인된 분석 산출물만 근거로 쓰고, IRB·동의·표본 제외 기준이 없으면 확인 필요로 남겨 주세요.
주장-증거 대응, 누락 자료, 인용 귀속, 학술지와 APA의 충돌을 구분해 주세요.
```

기대 결과는 수정안, 자료 누락 목록, 근거 파일과 원고 위치의 대응, 적용 범위·충돌·미확인 사항이다. 수행하지 않은 분석이나 심사 응답의 수정을 완료로 답하지 않는다.

## 업데이트·제거·복구

- 업데이트 전에 기존 폴더와 manifest를 보관한다. 새 preview를 새 디렉터리에 풀고 검증한 뒤 활성 home의 해당 스킬만 교체한다. 서로 다른 판본의 references를 섞지 않는다.
- 동작이 나빠지면 이전 폴더 전체와 manifest로 되돌리고 새 세션에서 확인한다. source ledger의 과거 접근 실패와 평가 실패는 삭제하지 않는다.
- 수동 설치 제거는 설치 때 복사한 해당 폴더만 대상으로 한다. 에이전트가 다른 스킬·프로필·원고를 함께 지우지 않는다. 사용자 수정본은 먼저 보관한다. hub를 통해 설치한 판본은 해당 hub의 관리 명령을 따르며 수동 preview와 혼동하지 않는다.

## 실제 사용 피드백

[Issue #2](https://github.com/ContextualWisdomLab/korean-writing-skills/issues/2)의 실제 팀 사용은 합성 평가와 별도다. 실제 사용한 판본·작업 유형, 비식별 전후 예문, 도움·어색함·의미손실·과잉교정·지연, 수정 여부와 독립 재검증을 기록한다. 쓰지 않았다면 미사용으로 보고한다. 고객 원문·연구 참여자 자료·비밀정보를 공개 댓글에 붙이지 않는다.
