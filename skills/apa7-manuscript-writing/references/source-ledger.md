# 근거 장부

확인일: 2026-09-20. 담당: APA 스킬 작성 worker, task_f6b0edbebdae. 범위: skills/apa7-manuscript-writing 전체. 공식 자료를 검색 결과 요약만으로 규칙화하지 않았다. 본문을 얻은 자료와 접근 실패를 구별한다. 매뉴얼 확인이 완료되지 않아 현재 상태는 **원문 확인 미완료 초안**이다. JARS-Quant Table 1은 아래 추가 조사에서 로컬 소장 PDF로 재확인했다.

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


## 2026-09-20 추가 원문 조사 · task_3ac9c39fee07

담당: 원문 조사 worker. 상세 접근 기록은 [source-access-followup.md](../../../evaluations/references/source-access-followup.md). 이전 조회의 `~/Zotero`와 실제 첨부 경로 `~/Documents/Zotero`는 서로 다른 DB다. 이전의 그룹 0행을 현재 소장 라이브러리 전체의 부재로 해석하지 않는다.

- `~/Documents/Zotero/zotero.sqlite`: 일반 읽기 전용 연결은 `database is locked`. `mode=ro&immutable=1`로 주 DB만 조회하여 개인 library 1, elderly-gad library 2 / group 6347780을 확인했다. WAL을 반영하지 않으므로 최신 동기화 상태나 완전한 부재 판정에는 사용할 수 없다.
- 개인 JARS-Quant parent `NWXTJ7QC` / 첨부 `MA5XB6VW`; 그룹 원 논문 parent `49XLUQAT`에는 첨부가 없고, 정오표 parent `W4AJRLSI` 아래 첨부 `WTHXWQ32`에 원 논문과 정오표를 합친 PDF가 있다. 첨부 이름이나 parent 제목만으로 본문을 정오표 단독으로 판단하면 안 된다.
- 두 PDF의 SHA-256은 동일: `8e08c2fac20b64fa5f03ae8906c4ea1dc1c75275c8fbf8a9522828378c68777c`. 파일은 각각 `~/Documents/Zotero/storage/MA5XB6VW/`와 `WTHXWQ32/`의 `Appelbaum et al. - 2018 - “Journal article reporting standards for quantitative research in psychology The APA Publications and Commun.pdf`다.
- S8 판본: Appelbaum, Cooper, Kline, Mayo-Wilson, Nezu, Rao (2018), APA, *American Psychologist*, 73(1), 3–25, DOI https://doi.org/10.1037/amp0000191. 정오표 DOI https://doi.org/10.1037/amp0000389 가 마지막 PDF p.24에 붙어 있다. `pdftotext -layout`으로 직접 읽었으며 페이지 이미지는 대조하지 않았다.
- 실제 열람: 인쇄 p.3/PDF p.1의 제목·저자·DOI; 인쇄 p.5/PDF p.3의 적용 구조; Table 1 인쇄 pp.6–8/PDF pp.4–6의 Title/Abstract/Introduction/Method/Results/Discussion. 짧은 구절: “Primary hypotheses”, “Secondary hypotheses”, “Exploratory hypotheses”(인쇄 p.7, Analytic strategy). 연구 설계에 맞는 보고 항목 선택, 사전·탐색 분석 구분, 결측 처리, 효과크기·구간 보고 근거로 사용한다. 자료나 분석 결과를 새로 만드는 허가가 아니다.
- 정오표 PDF p.24: 인쇄 p.13 Clinical Trials와 p.25 참고문헌의 헬싱키 선언 인용을 2008년 판으로 정정한다. 이 정오표를 현행 연구윤리 규정으로 확대하지 않는다. Table 1 수정이라는 주장은 하지 않는다.
- APA Manual 7: 두 DB의 제목 검색과 `~/Documents/Zotero` 개인·그룹 주 DB에서 `%publication%manual%`, `%APA%7%`, `%출판%매뉴얼%` 검색 0건. 최신 클라우드 소장본의 부재는 미확인이다. 개인 API 15초 timeout, 그룹 API 403이 다시 발생했다. Manual 본문·쪽·절은 여전히 미독이다.
- Numbers and Statistics Guide 직접 HTTP 응답은 200이지만 212바이트 HTML(SHA-256 `d02032286070b4dd9d8fbd985a7bdca8af8edf52b89ff177db3bfcb2c8a9c43d`)이다. PDF를 읽었다고 처리하지 않는다.


## 2026-09-20 공개 안내 PDF 직접 대조 · task_ff07a5046360

담당: 단독 작성 OpenCode. 방법: 작업 트리 직접 HTTP는 3개 URL 모두 212바이트 차단 HTML(SHA-256 `d0203228…`)만 반환하므로, 같은 날 별도 세션이 저장한 기존 로컬 파일 `/tmp/apa-src-20260920/u01·u02·u07.body`를 `%PDF` 매직·SHA-256·`pdftotext -layout`으로 직접 대조했다. 아래 해시는 본 작성자가 계산한 값이다. Grok 보고서(`/tmp/writing-apa-source-20260920.md`)의 해시·쪽 주장과 일치함을 확인한 뒤에만 기록한다. 긴 인용은 옮기지 않는다.

- A-REF: APA, *Reference Guide for Journal Articles, Books, and Edited Book Chapters*, 7th Edition, 2026-03-23 갱신. https://apastyle.apa.org/instructional-aids/reference-guide.pdf , SHA-256 `fc74e6a4…6c94f7` (99,646B, 2쪽). 확인: 영문 논문 제목 sentence case, 학술지명 주요 단어 대문자, 학술지명·권 기울임·호 비기울임, DOI 뒤 마침표 없음, 출판사 소재지 없음. 한계: Section 10.1–10.3 지시만 있고 Manual 10장 본문·미출판·재인용·한국어 표기는 미확인. 기존 S1의 Exa 추출 기록은 유지하고 쪽 있는 PDF 확인을 추가한다.
- A-NUM: APA, *Number and Statistics Guide, APA Style 7th Edition*, 2024-09-11 갱신. https://apastyle.apa.org/instructional-aids/numbers-statistics-guide.pdf , SHA-256 `6a1b2b67…cd1dc86` (153,566B, 2쪽). 확인: 표·그림 정확 *p*(*p* < .001은 "<.001"), 1 초과 불가 통계의 선행 0 생략, 라틴 기호 기울임·그리스 문자 비기울임, *M*·*SD*·*p*·*N*·*n* 미정의·CI 등 다른 약어 정의, 표·본문 통계 중복 금지, 반올림 원칙, 본문 기호 대신 말 사용. 한계: Manual 6.32–6.45·Table 6.5 본문 미독, 숫자-단어 규칙(10 기준 등)은 영어 표기 관례이므로 한글 강제 아님. 기존 S6의 212B HTML 기록은 당시 기록으로 유지한다.
- A-JARSQ: APA, *JARS-Quant Table 1*, © 2024. https://apastyle.apa.org/jars/quant-table-1.pdf , SHA-256 `11c042b1…97d60c2d` (3쪽). 확인: 표 제목 "New Data Collections", Sampling procedures(p.2, IRB·윤리·안전 모니터링 "Describe"형), 1차·2차·탐색 가설 구분, NHST 정확 *p*, 효과크기·CI(가능할 때), 2차 자료 분석 표시. 한계: Table 2–8·Module 미독, Qual/Mixed 표 미사용. 기존 S4의 212B HTML 기록은 당시 기록으로 유지한다.
- S5 Manual 7판 본문은 여전히 미독이다. 위 안내서가 가리키는 절 번호를 Manual 열람으로 바꾸지 않는다.

## 2026-09-20 Sampling procedures 본문·이미지 대조

담당: Codex `ctx_812ff2c52f7e`. Appelbaum 등(2018), *American Psychologist*, 73(1), 3–25, DOI `10.1037/amp0000191`, APA 발행. 기존 S8 소장본 중 개인 item `NWXTJ7QC` / attachment `MA5XB6VW` PDF를 직접 읽는다. SHA-256 `8e08c2fac20b64fa5f03ae8906c4ea1dc1c75275c8fbf8a9522828378c68777c`. 인쇄 p.6/PDF p.4의 Table 1 Sampling procedures에서 참여자와의 합의·보상과 IRB·윤리·안전 모니터링 항목을 확인하고 같은 쪽 렌더링과 자구를 대조한다. 짧은 원문: “Institutional Review Board agreements, ethical standards met, and safety monitoring”. PDF 4쪽의 머리글 인쇄 숫자는 6이다. 공개 원문 시작점: https://doi.org/10.1037/amp0000191.

판정: 위 내용을 보고 누락 점검에 쓰는 것은 뒷받침한다. 이 표는 개별 연구가 심의를 받았는지 또는 어떤 보상을 했는지 증명하지 않는다. 누락을 채우려면 실제 연구 기록이 필요하다는 적용은 프로젝트의 사실 보존 원칙이며, 원문에 없는 연구 사실을 JARS 문구로 대신하지 않는다. Manual 7판 조판 규칙 검증과도 구별한다.
