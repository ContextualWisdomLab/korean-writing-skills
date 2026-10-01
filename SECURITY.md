# Security

## 지원 범위

보호 브랜치와 최신 immutable release가 보안 수정의 기준이다. 아직 release가
없으므로 현재 PR과 기본 브랜치의 차이를 배포된 안전성으로 해석하지 않는다.

## 보고

공개 Issue에 원문, 연구 참여자 정보, API key, 로컬 경로 또는 공격 payload를
붙이지 않는다. ContextualWisdomLab의 비공개 보안 보고 경로로 재현 단계와
영향 범위만 전달한다.

## 저장소 경계

- 스킬은 사용자의 원문이나 Zotero 자료를 repository에 복사하지 않는다.
- source ledger에는 필요한 최소 서지·확인 범위·hash·공개 URL만 기록한다.
- 공개 평가에는 합성 입력만 사용한다.
- 로컬 절대경로와 ephemeral Agent/run 식별자는 공개 재현 계약이 아니다.
- 외부 원문과 도구는 각 라이선스와 접근 조건을 유지한다.
