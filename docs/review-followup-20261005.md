# 8aa89922에 대한 후속 지적 정산

기준 source: `8aa89922d29f0fdb2610b1dfac93fb7f39473cc1`. PR #5의 `f5de04263ea4c3785a8ccbb7bd4ab360e178a986`에 달린 inline 12건과 `d7cade69f30ffc580cdb468152ed82dc21c2c4ef` → `8aa89922` 전체 45경로 증분 검토의 DOC-1–3을 현재 source에 대조했다. 자동 제안을 그대로 적용하지 않았다. 이 문서는 후속 판단이며 기존 평가의 입력·출력·criteria·루브릭·점수·실패·해시를 바꾸지 않는다.

## 검토와 게시의 범위

- 2026-10-04 패키저 6파일 독립 검토와 합성 K17·K18·A3 비교는 해당 범위의 역사 증거다. 신구 각 3/3·세 비교 동률이며 실제 팀 사용이나 일반 성능 개선이 아니다.
- 2026-10-05 `8aa89922` branch 게시와 원격 ref 일치를 확인했다. 같은 날 전체 45경로 독립 증분 검토는 base/head blob·파일 해시·전체 diff에 결속됐고, 제한 범위 preview에서 새 중대 결함은 발견하지 않았으나 아래 DOC-1–3 및 미완 gate가 남았다. 패키저 6파일 검토를 전체 45경로 검토로 바꿔 부르지 않는다.
- 이 successor는 지적이 남은 문서·구조 검사·hygiene만 고친다. 기존 29개 패키저 시험이나 행동 평가·채점은 반복하지 않는다. 로컬 한정 회귀·독립 코드 검토는 현재 exact-head hosted 필수 검사·비작성자 공식 승인·Ready·merge·release를 대체하지 않는다.
- canonical CI는 이 저장소가 소유하지 않는다. 구조 검사 실행 환경도 잠긴 의존성을 설치한 뒤 `uv run --locked python tests/skill_structure_test.py`를 사용해야 한다. 이 작업은 조직 workflow·PR ref·보호 설정을 수정하지 않는다.

## 12+3건 판정

| ID | 현재 source 대조 | 후속 조치 |
| --- | --- | --- |
| 4179819746 | 유효. 175는 diff 파일 수, 검토 한도는 100 | CHANGELOG에서 두 수치를 구분 |
| 4179819765 | 유효한 기준 모호함. K16은 두 필수 지점 누락 시 실패라고 하면서 2점 이하라고 적음 | 동결 기준은 보존. 아래 E-1에 향후 판정 해석과 한계 기록 |
| 4179819770 | 현재 source에서 이미 해결. `status.md`와 세 기록이 모두 추적되어 있고 blind 수용 조건·독립성 미확인이 명시됨 | PR #5 head `f5de042`에는 실제로 없었고 후속 stack의 `2b0d86c`부터 추적됨. 현재 source 기준의 작성자 초기 부재 판단만 철회. 원본과 정상 locator 보존; E-2는 판단 오류 정정 |
| 4179819773 | PR #5 head `f5de042`에는 부재, 후속 stack에서 추가되어 현재 source에서 해결. 지적의 4개 출력 경로가 모두 존재 | 링크·출력 파일을 삭제하거나 미포함으로 바꾸지 않음 |
| 4179819777 | 유효. 분석 루브릭의 `1–2处`는 오타 | 원본 보존. E-3에 `1–2곳` 해석 기록 |
| 4179819782 | 유효한 판정 요약 누락. 1점도 통과하지 않음 | 원본 보존. E-4에서 각 축 2점 이상 기준 확인 |
| 4179819786 | 유효한 출처 보존 결함. 쪽수 제외 요청은 학위논문 출처·2023년 삭제 허가가 아님 | K11 기준·출력·점수는 보존. E-5에서 과거 통과 주장의 사용 범위 제한 |
| 4179819788 | 부분 유효. 역사 K12의 r·N 일반체는 표기 충족 근거가 아님. E·R까지 통계 기호라 단정하는 제안은 채택하지 않음 | 출력·점수 보존. E-6에 표기 결함 기록 |
| 4179819791 | 요약 보강 필요. 장부는 2.1 이전 스냅샷 보고와 재열람 표제만 확인을 구분 | README·verified-scope에 재열람 범위와 필수 요소 목록 채점 제외를 명시. 이전 보고를 삭제하지 않음 |
| 4179819795 | RED 재현. 한글·줄바꿈 파일명이 Git 인용 문자열로 전달돼 scan error | NUL 구분 경로 수집으로 최소 수정 |
| 4179819803 | RED 재현. 미완성 YAML·목록 값·공백 문자열을 허용 | 잠긴 PyYAML safe_load로 mapping·비어 있지 않은 문자열 검사 |
| 4179819807 | RED 재현. 없는 참조형 링크·패키지 밖 참조 이미지가 통과 | 기존 잠긴 CommonMark 파서로 인라인·참조형·이미지·정의 목적지 검사. 코드 span은 실제 링크로 오인하지 않음 |
| DOC-1 | 유효. 요약에 N-Q3 누락 | 온라인가나다 3건 및 기관 상담 분류로 동기화 |
| DOC-2 | 유효한 상태·범위 혼동 위험 | TODO에 역사 6파일 검토·합성 평가·45경로 검토·실제 게시를 분리 |
| DOC-3 | 유효한 현재 판정 오인 위험. 문서 상단에는 이미 경고가 있음 | CodeQL 행 자체도 역사 skip으로 표시. Python을 포함한 현재 head의 admission·check는 별도 미확인 |

합계: successor 수정 8건(실행 결함 3건, 문서·상태 5건), 동결 원본 대신 별도 errata 5건, 현재 source에서 이미 해결 2건. E-2는 작성자의 잘못된 부재 판단을 정정한 기록이며 원본 결함으로 계수하지 않는다. 부분 유효 지적은 어느 부분을 채택·제외했는지 위 표와 아래에 분리했다.

## 동결 평가 errata — 소급 편집·재채점 없음

### E-1 — K16 기준

대상: `evaluations/fixtures/K16/criteria.md` 25–27행. 두 필수 지점 중 하나만 지적한 경우는 해당 사례의 필수 gate 미충족으로 실패다. 향후 별도 기준에서는 그 실패를 1점 이하로 명시해 2점 통과 경계와 혼동하지 않는다. 정식 척도명 미인지도 향후 별도 기준에서는 의미 보존 1점 이하(실패)로 명시하되, 없는 내용의 발명이나 인과 강화와 같은 중대 오류를 자동으로 부여하지 않는다. 기존 Y 선택 오류 조건과 역사 채점은 변경하지 않는다. 이는 미래 기준의 명료화이며 기존 실행을 새 기준으로 재채점한 결과가 아니다.

### E-2 — 실제 평가 기록 위치

초기 후속 문서의 파일 부재 판단은 잘못됐다. `evaluations/protocol.md`가 가리키는 [status.md](../evaluations/runs/round-4-k7-k8/status.md)는 immutable 8aa와 현재 source 모두에 추적되어 있고, 본문 축 채점과 blind 독립성 미확인·수용 조건을 실제로 기록한다. [독립성 제한을 적은 교차검토](../evaluations/runs/round-4-k7-k8/independent-scoring.md)·[출력](../evaluations/runs/round-4-k7-k8/output.md)·[작성자 채점](../evaluations/runs/round-4-k7-k8/scoring.md)도 존재한다. 4179819770은 현재 source에서 이미 해결된 지적으로 판정하고 파일 부재·잘못된 locator 주장을 철회한다. 같은 workspace subagent 검토의 blind 독립성 미확인은 유지한다. 역사 protocol·status·출력·점수는 변경하지 않는다.

### E-3 — 오타

대상: `evaluations/rubrics/analytic-korean-editing.md`의 의미 보존 2점 설명. `1–2处`는 `1–2곳`의 오타로 읽는다. 점수 범주·판정 결과·원본 해시는 변경하지 않는다.

### E-4 — 각 축의 통과 경계

대상: `evaluations/rubrics/pld-and-standards-framework.md`의 “한 축 0이면 사례 실패”. 이는 1점 통과를 허용하는 문장이 아니다. [three-axis.md](../evaluations/rubrics/three-axis.md)의 각 축 2점 이상이고 중대 오류가 없어야 한다는 규칙에 따라, 한 축이라도 2점 미만이면 실패다. 중대 오류 즉시 0과 평균 상쇄 금지는 그대로다. 과거 점수 변경·절단점 타당화 주장은 하지 않는다.

### E-5 — K11 출처 사실

대상: `evaluations/runs/20260924-round6/criteria.md`, `K11-output.md` 및 당시 채점. 입력은 연구자의 2023년 석사학위논문에 사용한 자료라는 사실을 제공했다. 출력은 학위논문·2023년을 지우고 인용 여부를 확인 요청으로 옮겼으므로, 본문 의미 보존 3점을 출처 완전 보존의 근거로 사용하지 않는다. 날짜·온라인 수집·EFA/CFA·미산출 결과가 보존된 부분과 출처 손실을 구분한다. 현재 APA SKILL의 자료 출처를 조용히 지우지 말라는 규칙과 reporting-workflow의 출처 보존 예시는 이미 존재한다. 과거 criteria·출력·점수를 고쳐 통과로 만들지 않고, 새 원문을 다룰 때 출처와 제공된 연도를 보존한다. 기존 기록에서 본문 밖 이동을 허용한 것은 저자 확인 없이 출처 사실을 선택 정보로 만드는 일반 규칙이 아니다.

### E-6 — K12 통계 표기

대상: `evaluations/runs/20260924-round6/K12-output.md` 및 당시 G1 표기 판정. 교정문에서 r·N이 일반체이므로 역사 G1 충족 판정을 기울임 표기의 성공 증거로 쓰지 않는다. 향후 수정안에서는 원 값 `.31`·`212`를 보존하며 통계 기호 *r*·*N*을 기울임 처리한다. E·R은 이 입력의 척도 약칭이므로 r·N과 같은 통계 기호라고 자동 분류하지 않는다. 새로운 APA 절은 열지 않았고 장부의 A-NUM 확인 범위만 사용했다. 동결 출력·criteria·점수는 바꾸지 않으며 미제공 df·p·CI를 계산하거나 채우지 않는다.

## PR #6 신규 3건 — 기존 12+3과 별도 cohort

아래 3건은 4180015792·4180015795·4180015800이며, 위 12 inline + DOC-1–3의 15건에 합쳐 같은 검토로 부르지 않는다. 별도 추가 errata 3건이다. 원 manifest·comparability·criteria·output·score·review와 모든 동결 해시는 수정하지 않는다.

### E-7 — typed digest와 설명 분리 (4180015792)

대상: `evaluations/runs/20260925-k14-head-a567c84/manifest.json:33`. 원 `executor.prompt_as_received_normalized_sha256` 값은 `94842fa158f54e817a3e4ef0d187617fe91fc11dccdad965253e3fcf1184e729(원 K14와 같음)`이다. digest 뒤 설명이 붙어 typed SHA-256의 형식이 아니다. 별도 successor 표현은 다음처럼 분리한다.

```json
{
  "retained_prompt_normalized_sha256": "94842fa158f54e817a3e4ef0d187617fe91fc11dccdad965253e3fcf1184e729",
  "retained_prompt_note": "원 K14와 같음이라는 역사 manifest의 설명; 새로운 사전 prompt hash 증명 아님"
}
```

64자리 hex 형식을 확인했으며 역사 manifest를 읽어 설명과 값을 분리한 것이다. 실행 전 원 prompt 바이트를 새로 확보하거나 새로운 실행·사전 provenance를 증명한 것이 아니다. 원 field와 값은 그대로 보존한다.

### E-8 — 확인된 설정 차이와 단회 비교 한계 (4180015795)

대상: `evaluations/runs/20260925-k14-postfix/review.md:5,19`. 5행은 설정 차이를 이미 적었으나 19행은 설정 동일 여부도 확인하지 않았다고 하므로 두 문장은 서로 맞지 않는다. 같은 폴더의 `comparability.json:4–5,8–10`에는 두 실행의 모델이 모두 `gpt-6-sol`이고, 원 실행은 medium·CLI 0.155.1·local, postfix는 low·CLI 0.156.1·s1이라고 기록되어 있다. 원 실행만 `examples.md`, postfix만 `jars-quant-table1.md`를 열었으며 두 실행 모두 `reporting-workflow.md`를 열었다는 기록도 있다. 이 확인은 보존된 비교 문서에 대한 직접 대조이며 원 세션을 새로 실행하거나 모든 실행 metadata를 재인증한 것은 아니다.

따라서 설정 동일 여부 미확인이 아니라 **기술된 설정·열람 파일 차이가 확인된 단회 비교**로 읽는다. 수정 전 실패·수정 후 통과의 역사 결과는 유지하지만 스킬 변경의 단독 인과 효과로 해석하지 않는다. `evaluations/runs/20260925-k14-postfix-medium/review.md`의 같은 추론 강도 후속 locator와 단회·혼입 요인·접근 자기보고 한계도 유지한다. 새 모델 호출·성능 실험·채점은 하지 않았다.

### E-9 — 제공된 정식 척도명의 일부 누락 (4180015800)

대상: `evaluations/runs/20260925-round9/K13-output.md:5`. `inputs/K13.md:2`는 “과제 지연 경향 척도(DT)”와 “학업 몰입 척도(AC)”를 제공하고 `criteria.md:19–23`은 정식 이름을 보존하도록 한다. 출력은 “과제 지연 경향(DT)”·“학업 몰입(AC)”로 `척도`를 뺐다. `K13-scoring.md:68,78,83` 및 `review.md:25,29`는 이 생략을 인식했지만 중복 회피로 읽어 감점 없이 통과로 기록했다.

역사 통과는 정식명칭을 완전히 보존한 성공 증거가 아니다. W의 두 의미 구분·RD 정의·수치 보존과 정식명칭 누락은 다른 항목이다. 역사 출력·score·판정을 고쳐 통과로 만들거나 새 점수로 덮지 않는다. 현재 APA SKILL의 정식명칭 일관성 규칙은 이미 있으므로 중복 규칙을 만들지 않는다. 새 원고에서는 제공된 두 완전명칭·약어·숫자를 보존하며 일반 개념명과 도구의 정식 명칭을 구별한다.

## 실제 검증 계약과 남은 gate

한정 회귀는 `tests/test_review_followup.py`에 두었다. 수정 전 12개 검사 중 9개 실패와 3개 안전 대조 통과를 확인했고, 실행 결함 수정 후 초기 12개 모두 통과했다. 이후 YAML mapping과 name 타입 대조를 추가한 최종 한정 회귀는 13개 모두 통과했다. 이는 기존 29개 시험 재실행이 아니며 소규모 합성 코드 계약의 결과다. 동결 평가 177개 파일의 수정 전후 SHA-256을 별도로 대조한다. 전체 구조·public hygiene·diff whitespace는 기존 정상 gate를 그대로 적용한다.

후속 검토에는 실제 successor delta와 파일 해시·수정 전후 회귀 결과·177파일 보존 결과를 제공한다. 검토자의 read-only 판정과 작성자의 수정은 분리한다. 이 문서에 독립 검토가 끝나기 전 완료 판정을 선기입하지 않는다.

미완 gate는 source provenance·신규 규칙 행동 검증·실행 독립성·채점 정규화·Hermes 설치/호출 호환·Issue #2 실제 팀 사용·APA publication scope·현재 exact-head hosted approval·LICENSE/immutable release다. 과거 시험·정상 게시·한정 후속 수리로 이 gate를 닫지 않는다.

## 실행 의존성 근거

초기 초안에 선기입한 공식 문서 열람 주장은 근거에서 제외한다. 2026-10-05 동일 세션 복구 후 실제 web.run으로 다음 공식 본문을 직접 열었다. 이는 늦은 확인이며 초안 작성 전 열람이나 과거 기록을 소급 인증하지 않는다. [PyYAML Documentation의 Loading YAML](https://pyyaml.org/wiki/PyYAMLDocumentation)은 일반 load의 객체 생성 위험과 safe_load의 제한을 설명한다. 이 validator는 safe_load를 사용하고 결과의 타입을 따로 검사한다. [markdown-it-py Using](https://markdown-it-py.readthedocs.io/en/latest/using.html)의 token·environment 구조를 사용한다. [Git ls-files의 -z/OUTPUT](https://git-scm.com/docs/git-ls-files)은 NUL 구분과 파일명 인용 없는 출력을 설명한다. 이 열람은 실행 helper의 근거이지 APA 원문 재열람이나 과거 기록의 소급 인증이 아니다.
