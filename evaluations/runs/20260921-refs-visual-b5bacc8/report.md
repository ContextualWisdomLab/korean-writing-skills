# 독립 시각 검토: b5bacc8 Hangul refsapa 렌더

확인: 2026-09-21. 읽기 전용. 원고·생성기 파일은 수정하지 않음.  
구판 `87ee671` / `air_render_87ee671_*` 관찰을 현재 결과로 쓰지 않음.

## 산출물

경로: `/private/tmp/paper-60-recount-wt/docs/delivery_interim_20260920/air_render_b5bacc8_hangul_refsapa_20260920_201626`

| 항목 | 값 |
| --- | --- |
| tip | `b5bacc8fcc9bb64b1650ca314079b62fe1810bef` (MANIFEST) |
| worktree HEAD (검토 시) | `47e9753` |
| DOCX | `manuscript_interim_20260921.docx` SHA-256 `79f88b678cf53f81782e8b4714518d8ed92882a89c914905ba43ae3447109276` |
| HWPX | `manuscript_interim_20260921.hwpx` SHA-256 `560263aac8f53c3f23476b7c5d1bf1a09b001a3aecf99202e1b8719a51ca4918` |
| `docx_pages/` | 18쪽, LibreOffice → PDF → pdftoppm |
| `pages/` | 16쪽, `@rhwp/core` 0.7.7 (한글 앱 렌더 아님) |

이 해시는 이 폴더에서 다시 계산해 MANIFEST와 일치했다.

## 참고문헌 — DOCX `docx_pages/page_014.png` (LibreOffice)

직접 본 쪽 이미지와 같은 파일 OOXML.

- **표제**: "참고문헌"이 쪽 가운데. 문단 `w:jc center`, 런 `w:b`. `w:pageBreakBefore`. 결론 본문과 같은 쪽에 붙지 않음.
- **항목 내어쓰기**: 첫 줄은 왼쪽, 둘째 줄부터 들여 있음(Balsamo·Barlow·Britton·Feldman·Fresco). OOXML `w:ind left="720" hanging="720"` (720 twips = 0.5 in), `w:jc left`, `w:line="480"`. FirstParagraph/BodyText에 직접 속성이 붙어 있음.
- **이탤릭**: 학술지명+권이 기울임으로 보임. 예: *Clinical Interventions in Aging, 13*; *Perspectives on Psychological Science, 9*; *Behavior Therapy, 43*. 호 `(5)` 등은 정자체.
- `page_015.png`·`page_016.png`에서도 내어쓰기·학술지 기울임이 이어짐. `page_018.png`는 English Abstract.

규정 대조는 2.12(표제 가운데·항목 내어쓰기)·2.21(이중 줄간격, line=480)·A-REF(학술지명·권 기울임, 호 비기울임). 이 쪽 이미지 범위에서 DOCX는 그 세 가지가 보인다. APA 전체 준수·투고 완료를 주장하지 않음.

## 참고문헌 — HWPX `pages/page_014.png` (@rhwp/core)

같은 ZIP의 XML과 이 PNG를 나눔.

- XML: 표제 `paraPrIDRef="22"` (`horizontal="CENTER"`, `pageBreakBefore="1"`, PERCENT 200). 항목 `paraPrIDRef="23"` (`horizontal="LEFT"`, `hh:intent="-3600"`, `hh:left="3600"`, PERCENT 200). 학술지 런 `charPrIDRef="27"`.
- **PNG**: 표제 "참고문헌"이 왼쪽. 항목 줄바꿈이 첫 줄과 같은 왼쪽선(내어쓰기 안 보임). 단어 사이가 넓게 벌어져 양쪽 맞춤처럼 보임. 학술지 기울임은 이 PNG에서 확인하지 못함.
- `pages/page_015.png`도 같은 레이아웃.

XML에 있는 CENTER/내어쓰기/PERCENT 200이 이 rhwp PNG에는 나타나지 않음. 이 PNG를 한글 앱 최종본이나 APA 서식 완료 증거로 쓰지 않음.

## 본문·표·그림 (회귀)

`87ee671`과 숫자를 비교하지 않음. 이 폴더의 쪽만 봄.

- **DOCX page_001**: 중간본 배너, 제목, 영문 부제(기울임), 국문 초록, 1. 서론. `Running head:` 표지는 이 쪽에 없음. 본문 인용(Teachman, 2006 등)이 보임.
- **DOCX page_007**: 표 3과 표 3 (계속). 칸 "미보고" 유지. 7열 모형 비교 헤더(*R*²·Δ*R*²·*F*·*df*·*p*)가 보임. 표 번호 callout "표 3".
- **DOCX page_008**: 그림 1(연구 모형)과 표 4. 그림 캡션·표 4 "미보고" 칸. 3.3절 본문.
- **HWPX page_001**: 같은 초록·서론 내용. 배너 있음.
- **HWPX page_007**: 표 3 계속·모형 비교, "미보고" 유지. 레이아웃은 열 간격이 넓음.
- **HWPX page_008**: 그림 1과 그림 1 캡션. 도식이 보임.

DOCX 표 7개, 그림 1개(drawing 1). 선언 표는 이 쪽들에 없음. 필수 결과 표가 비어 삭제된 상태는 아님.

## 쪽 수

DOCX 18쪽, HWPX PNG 16쪽. 이중 줄간격·내어쓰기가 DOCX에만 렌더되어 쪽 수가 갈라진 것으로 읽음. 내용 소실로 단정하지 않음.

## 다음 (연구·생성기 담당)

- DOCX LibreOffice 쪽은 참고문헌 표제 가운데·항목 내어쓰기·학술지 기울임이 이 렌더에서 보임. 유지 확인은 생성기 담당.
- HWPX는 XML과 rhwp PNG가 갈라짐. 한글 앱 쪽이 있으면 그쪽으로 서식을 확인하고, rhwp PNG만으로 서식 완료를 주장하지 않음.
- 표 "미보고" 칸 채움은 검증된 수치 담당. 이 검토는 서식·회귀만.

APA 전체 준수·투고 완료를 주장하지 않음.
