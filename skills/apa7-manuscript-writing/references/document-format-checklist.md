# 투고 원고 서식·문서 생성 체크리스트

적용 대상: 학술지 **투고** 원고(전문 논문). 학생 논문 안내(A-STU)만으로 투고본을 수용하지 않는다. 학술지 규정이 APA와 다르면 학술지가 우선이다.

근거 절은 Manual 7판 RedShelf 리더(book 1302723, `platform.virdocs.com`, 2026-09-21 14:31Z–14:45Z 재열람, `/read/1302723/15/`·`/30/`). 2장 목차 시작 Page 28과 7장 Page 194는 절 쪽이 아니다. Format(`ch02sec3`)으로 들어갔을 때 쪽 칸은 43이었고 그 화면에 2.17–2.19가 보였다. 2.8·2.21·2.22의 단독 인쇄쪽은 그 재열람에서 분리하지 않았다.

## 생성 전

- 입력 md의 git commit과 SHA-256을 로그에 고정한다.
- 본문 md를 고치는 동안 기존 `dist/manuscript_interim_*.docx|hwpx`를 덮어쓰지 않는다. 미리보기 산출은 별도 디렉터리(예: `dist/apa7_style_preview_<commit>/`).
- 논문 본문 파일은 연구 리드 소유다. 이 스킬은 서식 점검·생성 옵션만 다룬다.

## 투고본 요소 (2.1, 2.18)

2026-09-21 재열람에서 2.1 표제는 “Professional Paper Required Elements”까지 확인했다. 그 다음 요소 목록은 검색 조각이 끊겨 이번 재열람의 세칙으로 쓰지 않는다. 전문 제목 쪽(Figure 2.1) 요소 목록에는 “running head (also included on all pages; see Section 2.8), and page number (also included on all pages; see Section 2.18)”가 있다. 이것은 2.1 요소 목록 전체가 아니다.

쪽번호 문장은 매뉴얼이 Section 2.18로 가리킨다. 모든 논문의 모든 쪽 머리 오른쪽이고, 제목 쪽이 1쪽이다. “All papers should contain the page number, flush right, in the header of every page.” “The title page is page number 1.”

## 러닝헤드 (2.8)

투고 원고에만 러닝헤드가 필요하다. “Running heads are required only for manuscripts being submitted for publication.” 학생 논문은 “Running heads are not required for student”까지 확인했다. 그 다음 단어는 끊겼다. 쪽머리 문장은 “Student papers need only the page number in the page header, unless the instructor or institution also requires a”까지다. 요구 대상의 명사는 미검증이다.

러닝헤드는 쪽머리 왼쪽, 모두 대문자, 글자·구두점·공백 합 최대 50자다. “The running head should contain a maximum of 50 characters, counting letters, punctuation, and spaces between words as characters.” “Write the running head in the page header, flush left, in all-capital letters,” 쪽번호는 오른쪽이다. “When both elements appear, the”와 “be flush left and the page number should be flush right.” 사이는 끊겼다.

**어느 쪽에도 `Running head` 표지를 붙이지 않는다.** 2.8 원문: “do not include the label “Running head” to identify the running head on any page”. 파일에 그 표지가 있으면 투고본에서는 뺀다.

## 글꼴 (2.19) — 한글 글꼴은 미확인

본문 전체는 같은 글꼴. 선택으로 확인한 목록: 11-point Calibri, 11-point Arial, 10-point Lucida Sans Unicode, 또는 12-point Times New Roman, 11-point Georgia, 10-point Computer Modern. 그림 안 산세리프 8–14포인트, 코드는 모노스페이스.

**한글 글꼴 이름(나눔고딕 등)은 이 절에 없다. 미확인.** 학회 한글 양식이 있으면 학회를 따른다. 목록에 없다고 해서 Times로 한글 본문을 일괄 치환하지 않는다.

## 줄간격·여백·정렬 (2.21–2.24)

- 줄간격 구간의 원문: “Double-space the entire paper, including the title page; abstract; text; headings; block quotations; reference list; table and figure numbers, titles, and notes; and appendices”. 이 문장 바로 앞에 절 번호 2.21이 붙어 있지는 않다. 같은 구간의 끝은 “Do not add extra spacing between paragraphs.”이고, 검색 적중은 “add extra spacing between paragraphs. 2.22 Margins”이다. 같은 장 목록 줄은 “2.21 Line Spacing 2.22 Margins”다. 본문에서 2.21 표제가 그 문장에 붙어 있는 것은 보지 못했다. 제목 앞뒤는 “It is not necessary to add blank lines before or after headings, even if a heading falls at the end of a page.” 필수가 아니라는 문장이지, 빈 줄 금지로 바꾸지 않는다. 표 칸·그림 이미지는 “may be single-spaced, one-and-a-half-spaced, or double-spaced”. 참고문헌 항목의 이중 줄간격(2.12)과 아래 2.23·2.24는 01:16 스냅샷 범위이며 이번 재열람 인용은 아니다.
- 2.22 Margins: “Use 1-in. (2.54-cm) margins on all sides (top, bottom, left, and right) of the page.” 제본하는 학위논문은 “Dissertations and theses may have different requirements if they are to be bound (e.g., 1.5-in. left margins).” 문서에 `pgMar`가 없으면 생성기가 1인치를 쓰는지 확인한다. 학술지 여백 원문을 열지 않았으면 1인치를 학술지 규칙으로 바꾸지 않는다.
- 왼쪽 정렬, 오른쪽은 들쭉날쭉. 양쪽 맞춤 금지(2.23). 본문 첫 줄 0.5 in 들여쓰기. 초록 첫 줄은 들여쓰지 않는다(2.24).
- 참고문헌 **표제**와 **항목**을 나누어 본다. 표제(한글 원고는 "참고문헌")는 굵게·가운데(2.12). 영어 "References"로 바꾸지 않는다. 항목은 첫 줄 왼쪽, 다음 줄 0.5 in 내어쓰기(2.12; 2.24 예외). 표제를 가운데로 둔 것을 항목 왼쪽 정렬과 한 문장으로 섞지 않는다. 참고문헌은 본문 뒤 새 쪽에서 시작한다(2.12).

## 표·그림 위치 (7.6)

2026-09-21 재열람에서 확인한 문장만 세칙으로 쓴다. 배치는 두 가지다. 참고문헌 뒤 별 쪽에 두거나, 첫 callout 뒤에 본문에 넣는다. 학술지·과제가 정한 쪽을 따른다. 본문과 같은 쪽이면 “insert a double-spaced blank line between the text and the table or figure”. 한 쪽보다 긴 표는 “If a table is longer than one page, repeat the heading row on each subsequent pa”까지다. 뒤는 끊겼다. 표 번호·제목의 굵게·이탤릭 규칙은 7.10·7.11에 해당하나, 그 두 절은 확인 범위에 없으므로 세칙으로 채점하지 않는다. **표 제목과 표 본문을 다른 쪽에 두지 말라는 문장은 이 재열람에서 찾지 못했다. 그 배치를 7.6이나 7.18 위반으로 쓰지 않는다.** 캡션만 앞쪽에 남는 현상은 아래 시각 점검의 구현 관찰이다. 짧은 표를 쪽 시작·끝에 두라는 문장, 표를 나누라는 문장은 이번 재열람의 세칙이 아니다. 이전 열람에서 적은 7.17 선·음영은 그 스냅샷 범위로 남긴다.

## 색

본문 글자색 규정은 2.19에서 확인하지 않았다. **미확인.** 강조색을 APA 세칙으로 넣지 않는다.

## 생성 후

DOCX/HWPX에서 러닝헤드 표지, 줄간격, 문단 간격, 여백, 표 callout을 위 절과 대조한다. HWPX `height=4000`은 표 행 `cellSz`(hwpunit, 빌더 환산 40pt)이지 본문 글자 크기가 아니다. 글자 크기는 `hh:charPr height`를 본다.

생성기 XML만으로 내어쓰기·정렬·기울임을 단정하지 않는다. 직접 속성, 상속 스타일, 최종 렌더를 구분한다. APA 2.12·2.23·2.24와 A-REF 학술지명·권 기울임은 원문 규정이고, 특정 파일의 XML·렌더는 구현 관찰이다.

DOCX는 문단 `w:ind`와 `basedOn` 체인, 번호 매기기 `numPr`(참고문헌 항목에 없으면 번호 매기기 hanging은 해당 없음), 그리고 워드프로세서 또는 LibreOffice 쪽 이미지를 본다. HWPX 머리글 네임스페이스 `http://www.hancom.co.kr/hwpml/2011/head`에서 확인한 요소는 `hh:margin` 아래 `hh:intent`(첫 줄), `hh:left`(왼쪽)이다. 이 패키지에 `hanging` 속성과 paraPr의 `indent` 속성은 없다. 음수 `hh:intent`는 같은 파일의 다른 paraPr에서 나타날 수 있으나, 참고문헌 문단이 그 id를 가리키는지는 `paraPrIDRef`로 본다. HWPX 쪽 PNG가 `@rhwp/core` 등 비한글 앱이면 한글 앱 최종 렌더로 쓰지 않는다. 생성기 코드 수정은 HWPX 전담 소유이며 이 스킬이 생성기를 고치지 않는다.

## 고정 렌더 시각 점검 (구현 검증)

이 절은 미리보기 PNG를 여는 절차다. Manual 8.4 인용 대응이 아니고, 2.12·7.18 원문 문장을 새로 만든 것도 아니다. 원문 규정은 위 절, 그 규정이 이 파일의 쪽에 보이는지는 아래다.

1. 대상은 고정 폴더 하나다. MANIFEST·DOCX·HWPX SHA-256과 rebuild/tip을 그 폴더에서 다시 계산한다. 다른 렌더 폴더 관측을 복사하지 않는다. 진행 중인 `dist/`를 이 점검의 대상으로 쓰지 않는다.
2. 그 패키지의 DOCX 쪽 PNG와 HWPX 쪽 PNG를 **모두** 연다. `italic="1"`, `<hh:italic`, `CENTER`, `intent="-3600"` 문자열이 머리글에 있어도 시각 통과로 쓰지 않는다. 통과는 같은 빌드 PNG(또는 한글 앱 쪽)와 그 파일 SHA-256을 XML과 한 줄에 적을 때만 적는다.
3. 표가 쪽을 넘으면 앞쪽과 다음 쪽을 같이 연다.
   - 캡션만 한 쪽에 있고 첫 데이터 행이 다음 쪽에 있으면 구현 관찰로 기록한다. 표 제목과 표 본문의 분리 금지는 2026-09-21 재열람에서 찾지 못했으므로 이 관찰을 APA 위반으로 채점하지 않는다.
   - 열 머리 행이 갈려 마지막 칸만 다음 쪽에 있으면 기록한다.
   - 이어지는 쪽에 열 머리 전체가 없으면 기록한다. 01:16 스냅샷은 다음 쪽에 열 제목 행을 반복하라고 한다. 2026-09-21 재열람은 “repeat the heading row on each subsequent pa”에서 끊긴다. 반복이 PNG에 있는지는 이 항목의 구현 관찰이다. “(계속)” 표지와 표 아래 “주”의 형식은 이 문장으로 채점하지 않는다. 7.7–7.16과 7.19 이후는 미독이다.
4. 칸과 본문에서 단어·약호·숫자·괄호가 **글자 중간**에서 끊기는지 본다. 칸 너비 때문에 단어 경계에서 줄이 바뀌는 것과 구별한다.
5. 본문 한 줄만 있는 쪽, 제목이 앞 문장 바로 뒤에 붙은 쪽, 표 주가 본문과 떨어진 빈 쪽을 기록한다.
6. 각 문제는 `폴더 | DOCX 또는 HWPX SHA-256 | 쪽 파일 SHA-256 | 본 것`을 같은 줄에 적는다. 이전 판 해시를 현재 판 결과로 쓰지 않는다.
7. 그림과 그림 번호·제목이 다른 쪽이면 구현 관찰로 적는다. 제목을 그림 위 또는 아래에 두라는 절, 둘을 같은 쪽에 두라는 절은 확인 범위에 없다.
8. 한 행이 쪽을 가로지르고 다음 쪽의 머리행이 그 행의 나머지보다 앞에 있으면 구현 관찰이다. 칸 순서는 원천 표의 행·칸 주소로 보고, 렌더의 테두리 겹침을 7.17이나 어문 규정으로 바꾸지 않는다.

관찰 예(생성기 미수정, 해당 ZIP만): `air_render_b5bacc8_hangul_refsapa_20260920_201626` HWPX `560263aa…`는 `italic="1"`이고 `<hh:italic` 자식은 0건. 같은 빌드 정규화 `page_014.png` `87b08c7f…`에서 학술지명이 기울어 보이지 않음. DOCX `page_014.png` `88ca1e86…`에서는 기울임. `air_render_d532d95_tablecol_20260921_064848` HWPX `046a3fea…`의 `page_003.png` `addadb86…` / `page_004.png` `bd409f7c…`는 표 1 열 머리 마지막 칸이 다음 쪽으로 갈리고 이어지는 쪽에 열 머리 전체가 없음. 첫 열 `(DT)` 약호는 그 4쪽에서 한 줄이다.
