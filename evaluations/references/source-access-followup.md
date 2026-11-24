# 원문 접근 후속 조사

확인일: 2026-09-20. 담당 역할: 원문 조사 worker. 조사 시간은 배정 후 10분 이내로 제한했다. 소유 파일은 APA 근거 장부, 루브릭 근거 장부, 이 보고서다. 스킬 본문·평가 실행과 출력·commit·push는 다루지 않았다.

## 실제 읽은 자료

### APA JARS-Quant (S8)

- 발행: American Psychological Association. Appelbaum, M., Cooper, H., Kline, R. B., Mayo-Wilson, E., Nezu, A. M., & Rao, S. (2018). *Journal article reporting standards for quantitative research in psychology: The APA Publications and Communications Board task force report*. *American Psychologist*, 73(1), 3–25. https://doi.org/10.1037/amp0000191
- 판본: 원 논문 뒤에 정오표 https://doi.org/10.1037/amp0000389 가 붙은 24쪽 PDF. Zotero 개인 parent `NWXTJ7QC`/첨부 `MA5XB6VW`, elderly-gad 정오표 parent `W4AJRLSI`/첨부 `WTHXWQ32`에서 같은 바이트를 읽었다. 그룹 원 논문 parent `49XLUQAT`에는 첨부가 없었다.
- 로컬 저장 위치는 공개 재현 계약에서 제외한다. 개인·그룹 첨부 키와 아래 SHA-256을 동일 바이트 식별자로 사용한다.
- 두 파일 SHA-256: `8e08c2fac20b64fa5f03ae8906c4ea1dc1c75275c8fbf8a9522828378c68777c`.
- 직접 읽은 범위: 인쇄 p.3/PDF p.1(서지·초록), 인쇄 p.5/PDF p.3(적용 구조), Table 1 인쇄 pp.6–8/PDF pp.4–6, 마지막 정오표 PDF p.24. `pdftotext -layout` 텍스트 기준이며 이미지 대조는 하지 않았다. PDF쪽은 1부터 센다.
- 짧은 구절: Table 1, Analytic strategy, 인쇄 p.7의 “Primary hypotheses”, “Secondary hypotheses”, “Exploratory hypotheses”. 방법에서 계획한 분석과 결과에서 실제 수행한 분석을 구분하는 근거다.
- 정오표는 인쇄 p.13 Clinical Trials와 p.25 참고문헌의 헬싱키 선언 인용을 2008년 판으로 수정한다. 현재 규정으로 제시하거나 Table 1이 수정되었다고 주장하지 않는다.
- 공개 PDF https://psycnet.apa.org/fulltext/2018-00750-002.pdf 는 웹 도구 robots 차단, 직접 HTTP 403이었다. 이번 확인의 근거는 공개 응답이 아니라 로컬 소장 PDF다. Publication Manual 7판 본문을 대신하지 않는다.

### 한국어 평가 논문

| 항목 | 직접 연 페이지·확인 위치 | 판본·확인 및 한계 |
| --- | --- | --- |
| R-KSL2015 (이전 R-KSL2019) | https://www.kci.go.kr/kciportal/landing/article.kci?arti_id=ART002002643 의 서지·국영문 초록·인용 내보내기 | 이은하, 한국국어교육학회, *새국어교육*, 103, 311–354, **2015**, DOI 10.15734/koed..103.201506.311. 기존 ID의 연도 오류 정정. 본문·루브릭 표 미독. |
| R-KIM2010 | https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART001459759 의 서지·영문초록 | 김정숙, 이중언어학회, *이중언어학*, 43, 81–99, 2010, DOI 10.17296/korbil.2010..43.81. 원문 버튼의 iframe은 직접 열람 불가 HTML. 본문 미독. |
| R-AHN2026 | https://www.earticle.net/Article/A483546 의 서지·국영문 초록·목차 | 안미홍, 국제한국언어문화학회, *한국언어문화학*, 23(1), 95–130, 2026.03. 첫 페이지 링크는 대체 이미지 `no_img_l.png`. 기관 로그인 안내를 확인했으나 전문 미확보. |

이 표의 권호·쪽수는 서지정보이며 실제 본문 열람 범위를 뜻하지 않는다. 초록 이상의 채점 규칙을 추가하지 않았다. 기존 ID를 참조하는 소유 범위 밖 파일은 수정하지 않았다.

## 로컬 응답 바이트 해시

직접 HTTPS 응답을 메모리에서 해시했다. HTML 전체를 보관하지 않았으므로 아래 값은 이번 응답 식별용이며 재현 가능한 원문 PDF 해시가 아니다. 로그인 폼의 토큰 등은 보고서에 옮기지 않았다.

| 응답 | SHA-256 |
| --- | --- |
| KCI ART002002643 HTML, 90,248바이트 | `1a31f52ca7143e8a95bb32ce92f8ad63e5ede3e64c07097a2ba94409178ba963` |
| KCI ART001459759 HTML, 99,757바이트 | `e9e82205b98b3e453e1bcc182870a61a84f27826010fe886b0b577e0778b25b5` |
| earticle A483546 HTML, 39,810바이트 | `5d3b38159eb85a75d2ed342a2532af9c0850cb9aa393a643ee7fd74cbdb4d1e8` |
| KCI 원문 iframe 차단 HTML, 444바이트 | `0038b321a4f108eb5f57a3e6338e66c0cffaa2fde48a28a8efad168f8463758d` |
| APA Numbers and Statistics Guide URL의 HTML, 212바이트 | `d02032286070b4dd9d8fbd985a7bdca8af8edf52b89ff177db3bfcb2c8a9c43d` |

KCI iframe URL: https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiOrteServHistIFrame.kci?sereArticleSearchBean.artiId=ART001459759&sereArticleSearchBean.orteFileId=KCI_FI001459759 . HTTP 200이어도 PDF가 아니며 “원문 직접 열람이 불가능합니다”라는 안내였다.

## 접근 범위와 미확인 항목

- 당시 노출 도구 목록에서 Zotero·브라우저 전용 도구를 발견하지 못했다. 웹 도구와 읽기 전용 SQLite, 직접 HTTPS를 사용했다. `.codegraph/`가 없으며 이번 소유 범위는 문헌 장부뿐이므로 코드 색인은 생성하지 않았다.
- 서로 다른 두 Zotero 로컬 DB를 확인했다. 한 DB에는 개인 library만, 다른 DB에는 개인 library와 elderly-gad group 6347780이 있었다. 구체적인 사용자 홈 경로는 공개 재현에 필요하지 않으므로 기록하지 않는다. 두 DB를 혼동하면 그룹 소장 여부를 잘못 판단한다.
- 두 번째 DB는 일반 읽기 연결이 잠겼다. `mode=ro&immutable=1`로 **주 DB만** 읽었으므로 WAL과 최신 동기화 상태를 반영하지 않는다. DB나 Zotero 자료를 수정하지 않았다.
- Manual 제목 `%publication%manual%`, `%APA%7%`, `%출판%매뉴얼%`와 세 한국어 논문의 제목 검색은 해당 개인·그룹 주 DB에서 0건이었다. 클라우드 소장본 부재를 뜻하지 않는다. Manual 7판의 본문·판권지·쪽·절은 미확인이다.
- 개인 Zotero local API의 publication-manual 질의는 15초 timeout, 그룹 API `https://api.zotero.org/groups/6347780/items?q=publication%20manual&format=json`은 403이었다.
- KUPIS https://kupis.kw.ac.kr/ 는 웹 도구 Internal Error, 직접 HTTPS는 기본 인증서 저장소에서도 issuer 검증 실패였다. 인증서 검증을 끄지 않았다. 기존 기관 SSO 세션 접근 여부는 미확인이다. 계정을 만들지 않았다.
- https://apastyle.apa.org/instructional-aids/numbers-statistics-guide.pdf 는 HTTP 200 HTML이다. 표기 규칙 근거로 쓰지 않았다.

## 인계

| 담당 | 다음 조치 | 완료 기준 | 증거·의존성 |
| --- | --- | --- | --- |
| 원문 접근 담당 | 기존 인증된 Zotero 또는 기관 SSO에서 Manual 7판과 한국어 논문 전문 확보 | 판권·제목·쪽/절을 직접 읽고 해시 기록 | 현재 DB 조회 한계와 접근 차단 해소 필요 |
| 저장소 유지 담당 | R-KSL2019 참조의 연도·ID 일치 검토 | 2015년 서지와 대응 | KCI ART002002643 직접 열람 |
| APA 작성 담당 | 기존 JARS 근거와 이번 판본·쪽수·정오표 기록 연결 | Table 1 근거 범위 보존 | 두 Zotero 첨부의 동일 해시 |

장부 링크·필수 식별자·해시 형식을 확인했다. 평가를 실행하거나 평가 출력에 접근하지 않았다. 원문 조사 범위 내 기록은 완료했으나 Manual·한국어 논문 전문 확인은 남아 있다.
