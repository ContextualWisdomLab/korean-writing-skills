# 한국어 글쓰기·퇴고·APA 7 Agent Skills

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/ContextualWisdomLab/korean-writing-skills)

직접 확인한 공신력 있는 자료를 근거로 한국어 글의 의미와 주장 강도를 보존하며 퇴고하고, 확인된 범위 안에서 APA 7 학술 원고를 작성·점검하는 재사용 가능한 Agent Skills 저장소입니다.

> 이 저장소는 자동 교정 서비스나 실행 서버가 아닙니다. 에이전트가 `SKILL.md`와 필요한 근거 파일을 읽고 수정안, 확인 요청, 누락 자료와 적용 범위를 제시합니다.

## 제공 스킬

### `korean-editing`

경로: [`skills/korean-editing/`](skills/korean-editing/)

한국어 문장의 문단 구조, 논리, 번역투, 문장 호응, 맞춤법과 띄어쓰기를 의미 보존 중심으로 점검합니다. 다음 자료를 함께 제공합니다.

- 초안 작성 전·중 점검: 주장·근거·범위·행위자·시점·불확실성 점검
- 문단·문장 퇴고: 최소 교정과 구조 재구성 구분, 조건·예외·인용 귀속 보존
- 표기 판단: 확인된 규정·사전·공식 상담의 적용 범위와 허용형 구분
- [이력서·경력기술서](skills/korean-editing/references/resume-writing.md): 직무 요구와 실제 경험 연결, 개인 기여·팀 성과·수치의 범위 확인
- [업무·의사결정 보고서](skills/korean-editing/references/reader-facing-reports.md): 권고·비용 영향·결정 요청, 같은 기준의 대안 비교, 실행 조치
- [매력적인 문장](skills/korean-editing/references/engaging-sentences.md): 독자와 말투에 맞는 구체성·정보 배열·호흡, 사실과 조건 보존
- 출처 장부와 실전 예문: [`source-ledger.md`](skills/korean-editing/references/source-ledger.md), [`examples.md`](skills/korean-editing/references/examples.md)
- 범위 라우팅과 검증 자료: 표준어·어휘·외래어·로마자·장르 질문을 적절한 근거로 보냄

현재 한국어 스킬은 한글 맞춤법 제41–50항과 문장 부호의 확인된 선택 절을 중심으로 하며, 그 밖의 표기는 실제 교정 때 현행 공식 원문이나 사전에서 다시 확인합니다. 개별 사례 평가 통과는 전체 규범 타당화나 실제 팀 사용 검증을 뜻하지 않습니다.

장르별 작성 지침은 대학·공공기관의 권고와 학술 연구를 구분해 사용합니다. 출처 장부에는 직접 읽은 본문·초록의 범위와 적용 한계를 기록했습니다. 외국어권 연구의 결과를 한국어 채용 성과나 이 스킬의 성능으로 약속하지 않습니다. [세 유형별 요청 예시](docs/usage.md#목적별-작성-요청)에서 필요한 입력을 확인할 수 있습니다.

### `apa7-manuscript-writing`

경로: [`skills/apa7-manuscript-writing/`](skills/apa7-manuscript-writing/)

한국어 학술 원고와 심사 응답을 연구 질문, 실제 분석 산출물, 인용 자료와 대조하며 작성·점검합니다.

- IMRaD 구조와 주장–증거 연결
- 양적 연구 보고와 JARS-Quant Table 1 점검
- 표·그림·통계·인용·참고문헌 점검
- 연구 결과, IRB, 동의, 서지정보를 발명하지 않는 누락 자료 처리
- APA 7, 학술지 투고 규정, 한국어 어문 규정의 충돌 구분

이 스킬은 직접 확인한 APA 7·JARS 범위에 한정한 초안입니다. *Publication Manual* 전체나 JARS 전체의 적합성을 인증하지 않으며, 확인하지 않은 절·쪽수·보고 의무는 원문을 확보한 뒤 적용합니다.

## 빠른 시작

각 스킬은 `SKILL.md`와 해당 디렉터리의 `references/`를 함께 사용합니다. 저장소 전체를 에이전트의 활성 스킬 경로로 연결하지 말고, 필요한 스킬 폴더만 배포 단위로 사용하세요.

```text
/korean-editing
안내문을 일반 독자가 읽기 쉽게 고쳐 주세요. 날짜·금액과 직접 인용은 보존하고,
확인되지 않은 사실은 추가하지 마세요.
원문: 신청은 11월 12일 까지 받습니다. 누리집에서 신청할수 있습니다.
```

```text
/apa7-manuscript-writing
한국어 투고 초안의 방법·결과를 점검해 주세요. 실제 분석 산출물만 근거로 쓰고,
IRB·동의·표본 제외 기준이 없으면 [확인 필요]로 남겨 주세요.
```

입력에는 원문 또는 원고, 독자와 장르, 대상 학술지, 수정 범위, 보존할 용어·수치·인용, 실제 분석 산출물을 포함하세요. 결과는 수정안과 함께 중요한 확인 사항, 누락 자료, 적용 범위와 미확인 사항을 구분해 제시해야 합니다.

## 설치 및 preview 패키지

설치·호출·입력·출력·업데이트·제거 절차는 [사용 안내](docs/usage.md)를 따릅니다. 두 스킬은 서로 독립적인 ZIP과 SHA-256 `manifest.json`으로 preview 패키징할 수 있습니다.

저장소 루트에서 Python 3.10 이상과 `uv`를 사용합니다. 아래 명령은 지원 하한인 Python 3.10으로 실행합니다.

```bash
uv sync --locked --python 3.10
uv run --locked python scripts/package_skills.py --output "$HOME/skill-preview-output"
```

preview 패키지에는 각 스킬의 `SKILL.md`와 해당 스킬의 근거 파일만 포함됩니다. 저장소 전체, 평가 기준·정답, 사용자 원고, 참여자 자료, Zotero 원문 전문은 배포 대상이 아닙니다. preview 설치는 공식 release나 APA 전체 인증이 아닙니다.

Hermes에 수동 설치할 때는 manifest와 파일별 digest를 먼저 확인한 뒤, 활성 프로필의 `skills/` 아래에 필요한 스킬 폴더 전체를 복사하세요. `SKILL.md`만 복사하면 근거 파일이 없어 불완전한 설치가 됩니다. 다른 프로필이나 기존 사용자 수정본을 덮어쓰지 말고, 설치 후 새 세션에서 스킬 목록과 호출을 확인하세요.

## 평가와 검증 범위

평가·회귀 증거는 [`evaluations/`](evaluations/)에 보관합니다. 동결 입력, 스킬 판본, 출력, 채점과 한계를 함께 기록하며, 개별 합성 사례의 통과를 전체 성능이나 실제 사용 효과로 확대하지 않습니다.

최근 한국어 초안 작성 전·중 점검의 5사례 preflight는 다음 범위를 확인했습니다.

- 상관과 인과, 불확실성 보존
- 실행 완료·결과 미회수·실패 부재의 구분
- 용어·기호의 역할 구분
- 상태·개수·원인 미확인의 보존
- 문맥에 따른 혼동 표현 교정

그 평가에서 확인된 `유의한` 등 통계적 의미를 근거 없이 추가하지 않는 후속 guard도 반영했습니다. 이 결과는 5사례의 제한된 증거이며 전체 타당화가 아닙니다. 평가 설계·결과·남은 항목은 [`TODO.md`](TODO.md)와 [`evaluations/runs/drafting-preflight-20261102/`](evaluations/runs/drafting-preflight-20261102/)에서 확인할 수 있습니다.

## 문서와 현재 한계

- [사용 안내](docs/usage.md): 설치, 호출, preview, 입력·결과, 업데이트·제거
- [Architecture](ARCHITECTURE.md): 제품 경계와 구성요소 책임
- [제품·기술 Gap 기준선](docs/product-technical-gap-baseline.md): 현재 요구와 미완료 항목
- [실사용판 개발 계약](docs/usability-plan.md): 제한 범위 preview와 실제 사용 검증의 분리
- [`CHANGELOG.md`](CHANGELOG.md): 변경 내역
- [`TODO.md`](TODO.md): 남은 원문 확인, 평가, 검증, 실제 팀 사용 항목

현재 별도 서비스·DB·UI·인증·네트워크 런타임은 없습니다. 실제 팀 사용(Issue #2), 현재 exact head의 hosted CI·보안·비작성자 검토, 보호 브랜치 병합, immutable release는 합성 평가와 별도의 미완료 범위입니다.

## 공개 범위와 보안

이 저장소에는 사용자 원문, 연구 참여자 자료, 비밀정보와 개인 원문 전문을 넣지 않습니다. 공개 hygiene 검사는 다음 명령으로 실행할 수 있습니다.

```bash
bash tests/public_hygiene_test.sh
```

보안 취약점은 [`SECURITY.md`](SECURITY.md)의 절차를 따르세요. 문서와 평가 기록은 저장소 안의 상대 경로로 연결하며, 로컬 절대경로·임시 실행 디렉터리·에이전트 운영 식별자를 재사용 가능한 제품 계약으로 취급하지 않습니다.
