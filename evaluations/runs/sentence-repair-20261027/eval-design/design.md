# 한국어 문장 수리 행동 평가 — 동결 설계

## 1. 산출물과 상태

- 작성·동결일: 2026-10-27 KST. 디렉터리 이름의 `20261026`은 지정된 과업 식별자이며 실제 검증 시각을 뜻하지 않는다.
- 범위: 새 합성 대상문 12개, 입력 묶음 3개에 각각 4개. 문맥은 문장 수에 포함하지 않는 해석 참고용 항목이다. 실행자에게는 문장별 기대 행동 라벨을 공개하지 않는다.
- 파일: `C01.md`, `C02.md`, `C03.md`, `criteria.json`, `design.md`만 생성한다. 정답 교정문·모범답안·실행 결과·점수 파일은 없다.
- 이 작업은 **입력·기준의 설계와 동결**이다. 스킬이 실제로 잘 고쳤다는 결과, 기존판 대비 개선, 채점자 간 일치도 또는 실제 사용자 타당성을 검증한 것은 아니다.
- 기준은 이 합성 과업을 위한 편집 판단이다. 외부 규정의 직접 인용이나 새로운 어문 규정으로 제시하지 않는다.

## 2. 독립성 및 노출 한계

### 독립 설계와 완전 무노출은 다르다

설계자는 별도 위임 문맥에서 대상문과 의미 관계 기준을 새로 작성했다. 저장소의 스킬 초안·기존 예문·`evaluations`·다른 조사 결과는 열람하지 않았다. 외부 검색·저장소 쓰기·커밋·설치는 하지 않았다. 프로젝트의 `AGENTS.md`는 위임 메시지에 포함된 지침으로만 제공받았다. 기존 자료와의 문장 중복 전수 비교는 금지된 자료의 열람을 요구하므로 수행하지 않았다. 따라서 여기서 '새 합성'은 이번 과업의 직접 작성이라는 뜻이며, 미열람 자료와의 절대적 비중복을 인증하지 않는다.

다만 **상위 실행 지침의 필수 스킬 로딩으로 설치된 `korean-editing/SKILL.md` 본문을 사전 열람했다.** `evidence-backed-skill-development/SKILL.md`도 절차 확인용으로 열람했다. 두 스킬의 링크 문서·예문·출처 장부·평가 자료는 열지 않았다. 설치된 한국어 스킬과 저장소 후보 초안의 동일성·버전 관계는 확인하지 않았다.

따라서 이 설계는 작성자와 분리된 문맥에서 작성되었으나 **평가 대상 스킬에 대한 완전 무노출 블라인드 설계로 인증할 수 없다.** 이 노출 사실을 이후 평가 보고에서 누락하지 않는다. 완전 무노출이 필수 수용 조건이라면, 이 묶음을 그 요건의 충족 증거로 쓰지 말고 비노출 설계자의 새 입력이 필요하다. 이번 파일을 사후에 '엄격 독립 통과'로 재표기하지 않는다. 역할 분리만으로 서로 다른 모델을 사용했다는 사실도 입증되지 않는다.

### OS 격리는 별도 요건이다

| 구분 | 이 작업에서 확인된 범위 | 성립하지 않는 주장 |
| --- | --- | --- |
| 문맥·역할 분리 | 위임된 설계 문맥에서 직접 합성 | 동일 파일시스템에 있는 자료가 기술적으로 접근 불가였다는 주장 |
| 읽기 제한 | 위에서 밝힌 자료만 열람; 저장소 후보·예문·평가 미열람 | ACL·별도 사용자·컨테이너 등으로 읽기를 강제 차단했다는 주장 |
| 동결 | 바이트 SHA-256 기록, 완료 시 소유 파일의 모드를 `0444`로 설정 | 소유자도 변경할 수 없는 불변 저장소 또는 파일 교체 방지 |
| 향후 블라인드 | 실행자와 채점자에게 제공할 파일을 구분하는 절차 | 아직 실행하지 않은 접근 제어·익명화가 이미 성공했다는 주장 |

같은 macOS 사용자와 파일시스템을 사용했으며 OS 샌드박스를 만들지 않았다. 읽기 제한은 지시 기반이고, 읽기 전용 파일 모드는 실수 방지 장치일 뿐 OS 수준의 정보 격리나 강제 무결성 보장이 아니다.

## 3. 행동 분포와 유형

| 입력 | 실제 수리 | 정상문 유지 | 의미 보류 | 합계 |
| --- | ---: | ---: | ---: | ---: |
| C01 | 2 | 1 | 1 | 4 |
| C02 | 3 | 1 | 0 | 4 |
| C03 | 2 | 1 | 1 | 4 |
| 전체 | 7 | 3 | 2 | 12 |

전체 ID 집합은 `C01-01`부터 `C01-04`, `C02-01`부터 `C02-04`, `C03-01`부터 `C03-04`까지다. 각 입력은 같은 일반 지시문을 사용한다. 묶음별 행동 분포·대상 유형은 실행자용 파일에 적지 않았다.

| 항목 | 평가할 행동·관계 | 핵심 대조 |
| --- | --- | --- |
| C01-01 | 장점 주제와 서술부 호응 수리 | 세 단계·간격 조절 가능성 보존 |
| C01-02 | 주의 대상과 동사의 조사 호응 수리 | 주의 기울임을 단순 소리 인지로 약화하지 않기 |
| C01-03 | 정상 명사 서술 구조 유지 | 명사형을 일괄 비문 처리하지 않기; 전제의 논리 강도 보존 |
| C01-04 | 중의적 수식의 확정 보류 | 배지 착용자 두 해석을 임의 선택하지 않기 |
| C02-01 | 병렬 항목의 조사·서술어 공유 실패 수리 | 문맥에 명시된 서로 다른 두 업무를 복원 |
| C02-02 | 문맥으로 복원 가능한 서술어 누락 수리 | 완결 서술문 장르·세 개·완료 상태 보존 |
| C02-03 | 인용 바깥 호응 수리 | 인용 내부·조건·절반·가능성·시연자 귀속 보존 |
| C02-04 | 정상 피동 유지 | 미상 행위자를 새로 만들지 않기 |
| C03-01 | 중첩절에서 역할을 추적하며 바깥 호응 수리 | 보고와 검토의 귀속 보존; 분리 여부는 자유 |
| C03-02 | 조사 호응 수리 | 조건 부정·주절 부정·8건 중 2건·범위 밖 정보 보존 |
| C03-03 | 정상적인 수신자 주어 생략 유지 | 발화자와 수신자를 혼동하지 않기 |
| C03-04 | 정보가 없는 목적물의 확정 보류 | 목적어 생략 자체의 일반 금지와 구별; 목적물 추측 금지 |

유형 태그 15개의 실제 포함 집합은 `criteria.json`의 `coverage_requirements`와 항목별 `types`가 서로 일치해야 한다. 유형 수는 배타적인 사례 수가 아니며 한 문장이 여러 유형을 겸한다.

## 4. 기대 수정본을 만들지 않는 채점

각 항목의 의미 앵커·필수점검·유지 조건·보류 조건은 `criteria.json`이 소유한다. 수정문 문자열을 지정하거나 정규식으로 교정문을 판정하지 않는다. 문법적으로 적법하고 의미가 같은 어순 변경·서술어 선택·문장 분리·절 재배치 등 여러 대안을 허용한다. 직접 인용 내부의 보존 검사는 입력의 보호 구간을 대조하는 것이며 모범 교정문 검사가 아니다.

- **수리 7항목:** 뜻과 역할이 주어진 문맥에서 분명하다. 실제 교정문 없이 질문·진단만 내면 실패다. 일부 정보가 주어지지 않았다는 이유로 이미 복원 가능한 결함까지 회피하지 않는다.
- **유지 3항목:** 명사형·피동·생략이 있다는 이유로 고치지 않는다. 원문 유지도 완전한 성공이다. 표현만 바꾼 데 가산점을 주지 않되, 안전한 적법 대안을 특정 문자열과 다르다는 이유로 배척하지 않는다.
- **보류 2항목:** 어느 수식 관계·목적물 정보가 미정인지 구체화해야 한다. 질문 형식이나 두 개의 완성된 대안 작성은 필수가 아니다. 조건부 대안은 허용하지만, 하나를 확정 수정본으로 채택한 뒤 확인 문구를 덧붙이는 것은 보류로 인정하지 않는다.

축은 의미보존·비문해소·자연스러움·과잉교정억제이며 각각 0–3점이다. 최대값은 항목당 12점, 전체 144점이다. 네 축을 독립적으로 평가한다. 유창하지만 의미가 변한 결과는 자연스러움 점수로 의미 오류를 상쇄할 수 없다. 보류 항목의 자연스러움은 미정 정보를 억지로 채운 원문이 아니라 처리 설명의 명료성을 평가한다.

중대오류 `M01`–`M06`은 점수와 별도로 근거와 함께 기록한다. 핵심 의미 변경·근거 없는 보충·모호성 임의 확정·명백한 수리 회피·인용 훼손·항목 누락을 구별한다. 항목 통과의 임시 운영 기준은 모든 축 2점 이상이며 중대오류가 없는 경우다. 경험적으로 검증된 절단점이 아니며 총점 문턱으로 대체하지 않는다.

## 5. 후속 실행·채점의 접근 경계

아래는 후속 실행의 요구 사항이지, 이번 작업에서 수행했다는 기록이 아니다.

1. 작성자가 끝낸 기존판·후보판 스킬 스냅숏의 전체 파일 목록과 해시를 별도로 확보한다. 동결 입력의 해시를 먼저 대조한다.
2. 각 스냅숏 × 입력 묶음 조합을 새 실행 문맥에서 실행한다. 기존판과 후보판 비교라면 2판 × 3묶음 = 6회다. 실행자는 해당 스냅숏과 입력 묶음 하나만 받으며 `criteria.json`·`design.md`·다른 출력·평가 이력·버전 대응표를 받지 않는다. 의도한 격리 방식과 실제 허용 경로를 기록한다.
3. 응답을 이 동결 디렉터리 밖의 별도 실행 산출물로 보존하고 SHA-256을 기록한다. 실행 후 입력이나 기준을 바꾸어 실패를 지우지 않는다.
4. 버전 대응표를 분리한 상태로 출력에 익명 라벨을 부여한다. 새 채점자는 입력·기준·익명 출력만 보고, 항목 ID별 네 축 점수와 실제 출력 근거 및 중대오류를 기록한다. 설계자나 실행자의 자기평가를 독립 채점으로 부르지 않는다.
5. 채점 의견이 다르면 원래 점수를 보존하고 근거를 대조한 판정을 별도로 남긴다. 점수 평균으로 중대오류를 없애지 않는다. 판정이 고정된 뒤 대응표를 연다. 항목·행동별 승/무/패와 새 중대오류를 계산하며 동점을 개선으로 세지 않는다.

## 6. 바이트 동결과 해시 장부

SHA-256은 UTF-8 파일의 전체 바이트를 해시한 값이다. 아래 네 파일은 설계 본문과 별도로 대조할 페이로드다.

| 파일 | 바이트 | SHA-256 |
| --- | ---: | --- |
| C01.md | 1196 | b8479065cd011628c0a7bc4cd23c0a71953216af7b05d2569c5ba0ffe87ed6e6 |
| C02.md | 1322 | 223b9c76698c82122860a8b653854e6fc50fce92307530b8df324ba5cdbb3ce7 |
| C03.md | 1397 | e511fe6c5f201e646648065b004c30f4a35bf7f8685b990d4890173ba7a3a92c |
| criteria.json | 26201 | 572c7ca5535cdf125e3420c7cc9bc33660402dac1ef6f9f4b799756c0acb50f7 |

`design.md` 자신의 전체 바이트 해시는 자기 자신 안에 넣지 않는다. 자기참조 문제를 피하기 위해 완료 보고와 최종 Python 실행 출력에 **다섯 파일 모두의 해시**를 기록한다. 별도의 여섯 번째 장부 파일은 만들지 않는다. 이 문서의 해시는 완료 보고의 값을 기준으로 대조한다.

검증 뒤 다섯 파일의 모드를 `0444`로 설정한다. 이후 변경은 허가 없이 하지 않으며, 문제가 발견되면 원본을 덮어써 이력을 바꾸지 않고 후속 버전 작성 범위를 먼저 확인한다. 해시는 변조 탐지용이며 전자서명·인증된 시각 증명은 아니다.

## 7. 재현 가능한 Python 검증

아래 코드는 Python 표준 라이브러리만 사용한다. 파일을 생성·수정하지 않으며, 지정 디렉터리의 다섯 파일만 읽는다. 최종 검증에서는 모드 `0444` 확인도 별도로 수행한다. 문법적 자연스러움을 프로그램이 증명하는 코드는 아니며, 수량·집합·보호 구간·구조·해시 계약을 검증한다.

```python
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
import re

p = Path('evaluation-workspace/eval-design')
files = {'C01.md', 'C02.md', 'C03.md', 'criteria.json', 'design.md'}
assert not p.is_symlink()
assert {x.name for x in p.iterdir()} == files
assert all((p / n).is_file() and not (p / n).is_symlink() for n in files)
c = json.loads((p / 'criteria.json').read_text(encoding='utf-8'))
design = (p / 'design.md').read_text(encoding='utf-8')
expected_ids = {f'C{b:02d}-{i:02d}' for b in range(1, 4) for i in range(1, 5)}
ids = [x['id'] for x in c['cases']]
assert len(ids) == len(set(ids)) == 12
assert set(ids) == expected_ids
assert len({x['target'] for x in c['cases']}) == 12
assert set(c['expected_inventory']['files']) == files
assert c['expected_inventory']['targets_per_bundle'] == 4
assert c['expected_inventory']['total_targets'] == 12
assert c['expected_inventory']['bundles'] == ['C01', 'C02', 'C03']
assert Counter(x['action'] for x in c['cases']) == {'repair': 7, 'maintain': 3, 'hold': 2}
assert dict(Counter(x['action'] for x in c['cases'])) == c['expected_inventory']['actions']
observed = {}
per_bundle = {}
instructions = []
contexts = {}
for bundle in c['expected_inventory']['bundles']:
    text = (p / f'{bundle}.md').read_text(encoding='utf-8')
    found = re.findall(r'^## (C\d{2}-\d{2})\n- 문맥: ([^\n]+)\n> 대상문: ([^\n]+)$', text, re.M)
    assert len(found) == text.count('> 대상문:') == 4
    instructions.append(text.split('\n\n')[1])
    per_bundle[bundle] = len(found)
    for ident, context, target in found:
        assert ident not in observed
        assert ident.startswith(bundle + '-')
        assert context and target.endswith('.') and target.count('.') == 1
        observed[ident] = target
        contexts[ident] = context
assert len(set(instructions)) == 1
assert set(observed) == expected_ids
critical = {x['id'] for x in c['critical_errors']}
assert critical == {f'M{i:02d}' for i in range(1, 7)}
coverage = defaultdict(set)
for case in c['cases']:
    assert observed[case['id']] == case['target']
    assert case['bundle'] == case['id'].split('-')[0]
    assert case['action'] in {'repair', 'maintain', 'hold'}
    for field in ['meaning_anchors', 'required_checks', 'maintain_conditions', 'hold_conditions', 'types', 'critical_watch']:
        assert isinstance(case[field], list) and case[field]
        assert all(isinstance(x, str) and x for x in case[field])
    assert len(case['types']) == len(set(case['types']))
    assert set(case['critical_watch']) <= critical
    for tag in case['types']:
        coverage[tag].add(case['id'])
    for span in case.get('protected_spans', []):
        assert span in case['target']
assert len(coverage) == 15
assert set(coverage) == set(c['coverage_requirements'])
for tag, required_ids in c['coverage_requirements'].items():
    assert len(required_ids) == len(set(required_ids))
    assert coverage[tag] == set(required_ids)
assert len(c['axes']) == 4
assert {x['label'] for x in c['axes'].values()} == {'의미보존', '비문해소', '자연스러움', '과잉교정억제'}
assert all(set(x) == {'label', '0', '1', '2', '3'} for x in c['axes'].values())
assert c['scoring_protocol']['scale'] == [0, 1, 2, 3]
assert c['scoring_protocol']['maximum_per_case'] == 4 * 3
assert c['scoring_protocol']['maximum_total'] == 12 * 4 * 3
assert c['answer_key_policy']['corrected_reference_sentences'] is False
assert c['answer_key_policy']['exact_answer_matching'] is False

def check_no_answer_keys(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            assert not re.search(r'reference_answer|expected_output|model_answer|corrected_text|gold_answer', key, re.I)
            check_no_answer_keys(value)
    elif isinstance(obj, list):
        for value in obj:
            check_no_answer_keys(value)

check_no_answer_keys(c)
whole, subset = map(int, re.search(r'서류 (\d+)건 가운데 서명이 없는 (\d+)건', observed['C03-02']).groups())
assert (whole, subset) == (8, 2) and 0 < subset < whole and whole - subset == 6
assert '세 단계' in observed['C01-01']
assert '나사 세 개' in observed['C02-02']
assert '절반' in observed['C02-03']
manifest = re.findall(r'^\| (C0[123]\.md|criteria\.json) \| (\d+) \| ([0-9a-f]{64}) \|$', design, re.M)
assert len(manifest) == 4
assert {x[0] for x in manifest} == files - {'design.md'}
for name, size, digest in manifest:
    data = (p / name).read_bytes()
    assert len(data) == int(size)
    assert hashlib.sha256(data).hexdigest() == digest
print(json.dumps({
    'status': 'PASS',
    'checked_at_utc': datetime.now(timezone.utc).isoformat(),
    'file_count': len(files),
    'per_bundle': per_bundle,
    'case_count': len(ids),
    'unique_target_count': len(set(observed.values())),
    'exact_case_id_set': sorted(expected_ids),
    'actions': dict(Counter(x['action'] for x in c['cases'])),
    'coverage_tags': len(coverage),
    'axes': len(c['axes']),
    'levels': [0, 1, 2, 3],
    'maximum_total': c['scoring_protocol']['maximum_total'],
    'hashes': {name: hashlib.sha256((p / name).read_bytes()).hexdigest() for name in sorted(files)}
}, ensure_ascii=False, indent=2))
```
