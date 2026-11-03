# 설치와 제한 범위 사용

이 제품은 두 Agent Skill이다. Python 명령이 원고를 자동 교정하는 서비스는 아니다. 에이전트가 `SKILL.md`와 필요한 근거 파일을 읽고 수정안·확인 요청을 작성한다. Python은 preview 패키징·검증과 선택한 에이전트에 스킬 파일을 설치하는 데 사용한다.

## 사용 범위

- `korean-editing`: 한국어 문단·문장·표기를 의미 보존 중심으로 퇴고한다. 이미 자연스러우면 그대로 둔다. AI 작성 여부를 판정하지 않는다.
- `apa7-manuscript-writing`: 확인한 APA 7·공식 안내·JARS 항목으로 원고와 심사 응답을 점검한다. 미확인 Manual 절·쪽, 연구 결과·IRB·동의·서지정보를 발명하지 않는다. APA 전체 적합성 인증이 아니다.
- 학술지 규정과 APA가 다르면 해당 투고 규정을 확인하고 차이를 기록한다. 한국어 어순에 APA 영어 문법을 강제하지 않는다.

## Preview 패키지 만들기

저장소 루트에서 Python 3.10 이상과 `uv`를 사용한다. 아래 전체 검증에는 Git, Bash, ripgrep(`rg`)도 필요하다. 링크 검사에는 버전과 해시를 잠근 `markdown-it-py`, 구조 검사와 패키징의 YAML frontmatter 파싱에는 `PyYAML` 의존성이 필요하다. API key는 필요하지 않다. 아래 명령은 에이전트의 `terminal` 도구로도 실행할 수 있다.

```bash
uv sync --locked --python 3.14
uv run --locked python scripts/package_skills.py --output "$HOME/skill-preview-output"
uv run --locked python -m unittest discover -s tests -p 'test_*.py' -v
uv run --locked python tests/skill_structure_test.py
uv run --locked python tests/source_traceability_test.py
bash tests/public_hygiene_test.sh
```

출력 디렉터리는 새로 정한다. 원본 스킬 디렉터리 안에 만들지 않는다. 빌드는 변경 중이지 않은 입력 트리와 운영자가 통제하는 출력 부모 디렉터리에서만 실행한다. 악의적인 동시 파일 교체를 막는 OS 격리 기능은 없다. ZIP 두 개와 `manifest.json`을 함께 보관한다. ZIP에는 각 스킬의 `SKILL.md`와 그 스킬의 근거 파일이 들어간다. 기존 `references/validation.md`에는 역사적 검증 사례가 있으므로 새 블라인드 평가 실행자의 열람 범위에서 제외한다. 저장소 전체, 새 평가 기준·정답, 사용자 원고, Zotero 원문 전문은 배포 대상이 아니다. manifest의 artifact SHA-256은 내려받은 파일의 digest와 대조한다. 파일별 해시는 압축 해제 후 확인한다. 성공한 구조·해시 검사는 내용의 타당성이나 hosted 승인과 별개다.

### Markdown 검사 경계

빌드 파서는 CommonMark의 실제 링크·이미지·참조·HTML 의미를 읽는다. 패키저는 그 위에 보수적인 허용 정책을 적용한다. 정의가 없는 명시적 참조, 서로 다른 목적지의 중복 정의, 위험한 코드 예제 링크를 거부하며, 코드 안의 링크도 별도로 검사한다. 따라서 일반 Markdown 렌더러가 평문으로 표시할 일부 입력도 빌드에서는 거부될 수 있다. 단순한 `[확인 필요]` 문구는 링크로 간주하지 않는다.

HTML은 수동적인 요소와 명시적인 단일 URL 속성만 허용한다. 스크립트·CSS·이벤트 속성·내장 문서·`srcset`은 지원하지 않는다. 렌더링은 메모리 안에서 검사 용도로만 하며 URL을 열거나 HTML을 실행하지 않는다. HTML sanitizer가 아니므로 이 패키저의 검사 결과를 사용자 HTML을 서비스 화면에 안전하게 게시할 수 있다는 인증으로 사용하지 않는다. [파서 공식 보안 안내](https://markdown-it-py.readthedocs.io/en/latest/security.html)와 [토큰·렌더링 안내](https://markdown-it-py.readthedocs.io/en/latest/using.html)를 확인했다(2026-10-04).

## 에이전트별 설치

`scripts/install_skills.py`는 preview 패키저와 같은 구조·링크 검사를 통과한 파일만 선택한 에이전트의 스킬 디렉터리에 복사한다. 네트워크·계정·에이전트 설정은 바꾸지 않는다. 스킬이 항상 적용되도록 만드는 자동 로드·규칙 설정도 하지 않는다.

```bash
# 설치할 경로를 먼저 확인한다. 에이전트 디렉터리는 바꾸지 않는다.
uv run --locked python scripts/install_skills.py --agent claude --agent codex --dry-run

# 사용자 전체 범위에 korean-editing을 설치한다.
uv run --locked python scripts/install_skills.py --agent claude --agent codex

# 두 스킬을 특정 프로젝트에만 설치한다.
uv run --locked python scripts/install_skills.py --agent cursor --skill all \
  --scope project --project /path/to/project
```

`--skill`을 생략하면 `korean-editing`만 설치한다. `--skill all`은 두 스킬을 모두 설치한다. `--agent`는 여러 번 지정할 수 있다.

| `--agent` | 사용자 범위(`--scope user`) | 프로젝트 범위(`--scope project`) |
|---|---|---|
| `hermes` | `$HERMES_HOME/skills`, 미설정 시 `~/.hermes/skills` | `.hermes/skills` |
| `claude` | `~/.claude/skills` | `.claude/skills` |
| `codex` | `~/.agents/skills` | `.agents/skills` |
| `opencode` | `~/.config/opencode/skills` | `.opencode/skills` |
| `cursor` | `~/.cursor/skills` | `.cursor/skills` |
| `gemini` | `~/.gemini/skills` | `.gemini/skills` |
| `antigravity` | `~/.gemini/config/skills` | `.agents/skills` |
| `agents` | `~/.agents/skills` | `.agents/skills` |

경로는 2026-11-03에 각 공식 문서([Hermes](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills), [Claude Code](https://code.claude.com/docs/en/skills), [Codex](https://developers.openai.com/codex/skills), [OpenCode](https://opencode.ai/docs/skills), [Cursor](https://cursor.com/docs/context/skills), [Gemini CLI](https://geminicli.com/docs/cli/skills), [Antigravity](https://antigravity.google/docs/skills))에서 확인했다. 설치된 에이전트 버전이 다른 경로를 쓰면 그 버전의 문서를 따른다.

- `.agents/skills`는 여러 에이전트가 함께 읽는 공유 경로다. Codex·Antigravity 프로젝트 범위나 `agents`를 고르면 OpenCode·Cursor·Gemini CLI 등도 같은 스킬을 발견할 수 있다. 같은 경로를 가리키는 선택은 한 번만 설치한다.
- Cursor는 `.claude/skills`와 `.codex/skills`도, OpenCode는 `.claude/skills`와 `.agents/skills`도 읽는다. 여러 에이전트에 설치하면 한 에이전트가 같은 이름의 스킬을 두 곳에서 발견할 수 있다. 중복 발견 시 선택 방식은 에이전트마다 다르므로 사용할 경로를 확인하고, 불필요한 복사본은 사용자 수정 사항을 보존한 뒤 정리한다. 설치 도구가 다른 경로의 중복까지 탐색하지는 않는다.
- Hermes의 프로젝트 범위 스킬은 해당 프로젝트를 신뢰한 경우에만 읽힌다. Cursor는 `~/.cursor/skills`만 클라우드에 동기화하며 `~/.agents/skills`와 프로젝트 스킬은 로컬에 남는다.
- 같은 이름의 스킬이 이미 있고 내용이 같으면 `unchanged`로 두고 다시 쓰지 않는다. 내용이 다르면 설치를 멈춘다. 기존 판본을 확인한 뒤 `--replace`를 붙이면 기존 폴더를 같은 스킬 루트의 상위 디렉터리 아래 `.korean-writing-skill-backups/`로 옮기고 새 판본을 설치한다. 백업 경로는 결과 JSON의 `backup`에 나온다.
- 경로 중간에 심볼릭 링크가 있으면 설치하지 않는다. 링크로 공유한 스킬 디렉터리를 의도치 않게 바꾸지 않기 위해서다.
- 여러 대상을 한 번에 설치하다가 중간에 파일 시스템 오류가 나면 앞서 끝난 대상은 설치된 상태로 남는다. 실행 중인 에이전트가 같은 스킬을 동시에 수정하지 않을 때 사용한다.
- 설치 후 새 세션에서 스킬 목록을 확인한다. Claude Code는 세션 중 새 스킬 디렉터리를 만들었다면 `/reload-skills`, Gemini CLI와 Antigravity CLI는 `/skills reload`로 목록을 다시 읽는다. 파일 해시가 같아도 에이전트가 스킬을 인식했다는 뜻은 아니다.

## Hermes에 수동 설치

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

## 설치본 업데이트

설치 도구는 설치할 때 파일 해시를 영수증으로 기록한다. 업데이트는 이미 설치한 스킬만 대상으로 하며, 설치 이후 사용자가 고친 사본과 영수증이 없는 사본은 건드리지 않고 `skipped-modified`로 알린다. 교체 전에는 백업을 남긴다.

```bash
# 이미 설치한 스킬을 현재 저장소 내용으로 갱신
uv run --locked python scripts/install_skills.py --agent claude --agent cursor --update

# 공식 저장소 main을 받아 한 번 갱신하고 결과를 JSON으로 출력
uv run --locked python scripts/auto_update_skills.py --agent claude --dry-run
uv run --locked python scripts/auto_update_skills.py --agent claude

# 터미널에서 하루 한 번 확인(기본 86400초, 최소 60초). 스케줄러는 등록하지 않는다.
uv run --locked python scripts/auto_update_skills.py --agent claude --watch
```

`auto_update_skills.py`는 공식 저장소 `main`만 받으며 다른 저장소나 ref를 지정하는 옵션이 없다. 받은 스킬의 Markdown만 꺼내 로컬 검증을 거치고, 내려받은 스크립트는 실행하지 않는다. 설치된 적 없는 에이전트에는 새로 설치하지 않는다. 비정상 종료로 `update.lock`이 남으면 내용을 확인한 뒤 직접 지운다. 주기 실행(cron·launchd) 등록은 사용자가 선택하며 이 저장소는 등록하지 않는다.
