# 근거 장부

확인일: 2026-09-20. 담당: APA 스킬 작성 worker, task_f6b0edbebdae. 범위: skills/apa7-manuscript-writing 전체. 공식 자료를 검색 결과 요약만으로 규칙화하지 않았다. 본문을 얻은 자료와 접근 실패를 구별한다. 매뉴얼·JARS 확인이 완료되지 않아 현재 상태는 **원문 확인 미완료 초안**이다.

## 직접 읽은 APA 공식 본문

| ID | 발행기관·제목·판본 | URL | 실제 읽은 쪽/절 | 확인 방법과 적용 범위 |
| --- | --- | --- | --- | --- |
| S1 | American Psychological Association, Reference Guide for Journal Articles, Books, and Edited Book Chapters, 7th Edition, 2026-03-23 갱신 | https://apastyle.apa.org/instructional-aids/reference-guide.pdf | Journal Article; Book; Chapter in an Edited Book; 말미 갱신 정보. 추출본에는 페이지 경계가 없어 쪽수는 기록하지 않음 | web open은 차단되었으나 Exa URL 본문 추출에서 제목·세 자료 유형·갱신 정보까지 확인. 영문 참고문헌의 저자 순서, 제목 대문자, 기울임, DOI와 출판사 소재지 처리에 한정해 사용. 안내가 매뉴얼 10.1–10.3을 가리키지만 해당 매뉴얼 절 자체를 읽었다고 간주하지 않음. |
| S2 | American Psychological Association, Tables and Figures, 2019, 웹 자료(판 표시 없음) | https://apastyle.apa.org/style-grammar-guidelines/tables-figures | Tables and Figures 본문 개요 | Exa URL 본문 추출로 효율적 전달·이해·접근성 목적 확인. 세부 표 선·주석 형식 근거로 확장하지 않음. 매뉴얼 7장 안내는 확인했지만 7장 자체는 미독. |

## U-KHU · 대학 교육 자료(교차 참고, APA 규범 아님)

- 경희대 도서관 [리포트 작성법](https://libguides.khu.ac.kr/global/writing/01): 사회과학·교육·공학 분야 참고문헌에 APA 스타일 **선택** 안내(2026-09-20 확인).
- 스킬 적용: 투고 학술지·소속 대학원 규정 > APA Publication Manual > 대학 교육 안내 순으로 충돌을 처리한다. U-KHU 문구를 APA 7 전체 준수의 증거로 쓰지 않는다.

## 접근을 시도했으나 규칙 근거로 사용하지 않은 자료

| ID | 기관·제목·판본 | URL·경로 | 결과와 다음 조치 |
| --- | --- | --- | --- |
| S3 | APA, APA Style Journal Article Reporting Standards, 웹 자료 | https://www.apa.org/pubs/journals/resources/apa-style-jars.html | web open은 iframe 1행, Exa는 Incapsula 실패. 실제 JARS 항목 미독. 접근 가능한 공식 본문 확보 필요. |
| S4 | APA, Quantitative Research Reporting Standards / 일반 양적 보고 체크리스트(요청 URL 기준, 본문 제목 미확인) | https://apastyle.apa.org/jars/quantitative ; https://apastyle.apa.org/jars/quant-table-1.pdf | 웹은 iframe, 직접 HTTP는 PDF 대신 212바이트 HTML. Exa PDF 추출은 다른 제목의 2023년 BMRC 논문을 반환하여 거부. URL이 맞더라도 본문 제목·저자 일치 확인 전 근거로 사용하지 않음. |
| S5 | APA, Publication Manual of the American Psychological Association, 7판(요청 판본) | https://apastyle.apa.org/products/publication-manual-7th-edition ; 개인 Zotero 및 elderly-gad 6347780 | 상품 페이지는 iframe. 매뉴얼 본문·쪽·절 미독. 아래 소장본 조회 참조. |
| S6 | APA, Numbers and Statistics Guide(요청 URL 기준, 본문 제목·판본 미확인) | https://apastyle.apa.org/instructional-aids/numbers-statistics-guide.pdf | web open iframe, Exa Incapsula. 세부 통계 서식 미확정. |
| S7 | APA, Bias-Free Language / General Principles(요청 URL 기준) | https://apastyle.apa.org/style-grammar-guidelines/bias-free-language ; https://apastyle.apa.org/style-grammar-guidelines/bias-free-language/general-principles | web·Exa 차단. 잠정 편집 절차와 APA 규칙을 구별. |
| S8 | Appelbaum, M., et al., Journal article reporting standards for quantitative research in psychology, *American Psychologist*, 73(1), 3–25, 2018 (JARS-Quant task force report) | https://psycnet.apa.org/fulltext/2018-00750-002.pdf ; [EQUATOR](https://www.equator-network.org/reporting-guidelines/journal-article-reporting-standards-for-quantitative-research-in-psychology-the-apa-publications-and-communications-board-task-force-report/) | 리드 확인(2026-09-20): PDF 텍스트 추출본에서 **Table 1** Abstract·Introduction·Method(Inclusion, Sample size, Data diagnostics, Analytic strategy)·Results(Participant flow, Missing data, Inferential statistics, primary/secondary/exploratory 구분)·Discussion 항목 직접 대조. `references/jars-quant-table1.md`에 요약. apastyle `quant-table-1.pdf`는 212B HTML 차단. Publication Manual 7판 대체 아님. |
| S9 | APA, Basic Principles of Citation(요청 URL 기준) | https://apastyle.apa.org/style-grammar-guidelines/citations/basic-principles | Exa 차단. 세부 인용 규칙 미확정. |

### Zotero 소장본 조회

- 개인: `/Users/seonghobae/Zotero/zotero.sqlite`를 SQLite 읽기 전용 URI로 열었다. libraries 결과는 `(1, user)` 하나다. title 필드에서 `Publication Manual` 또는 `APA 7` 포함 검색은 0건이다. 이는 이 로컬 DB의 검색 결과이며 개인 클라우드 소장본 부재를 뜻하지 않는다.
- 로컬 groups 테이블은 0행이다. elderly-gad가 로컬에 동기화되어 있다고 확인할 수 없다.
- 개인 로컬 API `http://localhost:23119/api/users/0/items?q=publication%20manual&format=json`은 20초 시간 초과다.
- 그룹 API `https://api.zotero.org/groups/6347780/items?q=publication%20manual&format=json`은 HTTP 403이다. 그룹 검색 미완료이며 소장본 없음으로 보고하지 않는다. 인증 정보는 파일이나 보고서에 넣지 않았다.
- 대체 경로 `https://secure.smu.ca/webfiles/APAManual7thEdition.pdf`는 직접 요청 HTTP 404였다. 검색에 나타난 파일을 읽었다고 기록하지 않았다.
- 조정자에게 접근 경로 지원을 요청했다. 다음 담당자는 접근 가능한 개인·그룹 API 또는 첨부파일로 판본·본문을 확인하고 실제 읽은 절만 추가한다.

## 작업 기록과 완료 기준

| 담당 | 현재 증거 | 다음 조치 | 완료 기준·의존성 |
| --- | --- | --- | --- |
| APA 작성 worker | SKILL.md, reporting-workflow.md, 이 장부 | 원문 확인 범위를 보존하며 validator 실행 | frontmatter·링크 검증 통과. 이는 APA 내용 검증과 별개. |
| 원문 접근 담당·조정자 | 로컬 조회 0건, 개인 API timeout, 그룹 API 403, 공식 사이트 차단 | 개인 및 elderly-gad 소장본·JARS 본문 확보 | 7판 식별 및 실제 읽은 절과 각 규칙의 대응. 미확인 항목을 해소해야 원문 조사 완료. |
| 독립 평가자 | [검증 기록](validation.md): 독립 평가 완료 | 원문 확보 후 APA 세칙 추가 평가 | 의미·한국어 자연스러움·과잉 교정은 제한된 사례 통과. APA 전체 준수는 미판정. |
| 조정자 | 소유 경로 외 파일 미수정 | 통합 검토 후 commit·원격 확인 | 원격 commit을 실제 확인하기 전 전체 작업 완료 보고 금지. |

이 저장소는 점검 당시 `.codegraph/`가 없었다. 현재 작업은 Markdown 문서 3개이며 코드 심볼·호출 관계 탐색이 없어 인덱싱하지 않기로 판단했다. CodeGraph CLI 존재와 init 옵션을 확인했으며, 코드가 추가되거나 코드 탐색이 필요해지면 인덱싱한다.
