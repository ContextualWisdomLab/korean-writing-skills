# 평가 공개 사본의 서식·provenance

확인일: 2026-10-02. 담당: 통합 후보 서식 수정 워커. 수정 전 공개 사본의 정확한 commit은 `67b74f359d0ad48226933493ed8307ada9b1f417`이다. 아래 경로는 저장소 루트 기준이며, 수정 후 열은 이번 작업 트리 파일의 SHA-256이다. 수정 전 파일은 `git show 67b74f359d0ad48226933493ed8307ada9b1f417:<경로>`로 꺼내 대조한다.

## 변경 범위

- 파일 5개의 EOF 빈 줄을 각 1줄 제거했다. 나머지 3개 파일의 행 끝 공백 8건은 역슬래시 강제 줄바꿈으로 바꿔 Markdown 줄바꿈을 보존했다.
- `independent-scoring.md`의 output 해시 설명은 과거 공개 사본과 이번 공개 사본을 구분하고 이 기록을 연결하도록 고쳤다. 입력 문장·실행 출력 본문·채점 점수·판정은 바꾸지 않았다. 새 실행이나 재채점이 아니다.
- 기존 freeze·manifest·evidence·output-hashes 기록과 그 안의 원본 해시·시점·commit은 그대로 보존했다. 과거 실행 전 동결 해시를 이번 서식의 해시로 바꾸지 않는다. 그 해시는 각 기록에 명시된 당시 판본·commit·보존 원문에 대응하며, 현재 파일의 해시라고 해석하지 않는다.

## 공개 파일 SHA-256

| 경로 | 수정 전 공개 사본 (`67b74f359d0ad48226933493ed8307ada9b1f417`) | 수정 후 공개 사본 |
| --- | --- | --- |
| `evaluations/ARTIFACT-VERIFY.md` | `a7941433f4603d45ae96e0228c42c72d42ba9aeb1694c21b4b27ab2641eb2e4c` | `5f80ce5ff47e107e7422b05b3ac2357594337e0f4e8379c0518d09d1cfea6217` |
| `evaluations/rubrics/analytic-korean-editing.md` | `17bb4edb291bf28861ff7689d7ffc3b2df0bf5ba111329dd5bda106cb5b37ca5` | `0d42c968dc51887afebc053e039597da6448c0baeb4db9b570991863edcd65a3` |
| `evaluations/rubrics/pld-and-standards-framework.md` | `d2b670abd923ba7977148cc9d8fa71868e9495b9317d56169132093797a41c7e` | `8ab2943362c5df0c5507565a5b29776dba2657ac6f0c175927e15a830662742c` |
| `evaluations/runs/round-3-k5-k6/K5.md` | `1c8afa28dbcacd8c755f9771350a00ef17f5280fa5d1f7e5c748cf68df3d911d` | `238de6e1e26e23839527eae4131aa1492bad87924266e905c76cd56b3a4ed3ce` |
| `evaluations/runs/round-3-k5-k6/K6.md` | `70ecc7c5505d3e5cc2001cb6a3b5ae0e1be66c4afe9f477ef90349286028d285` | `6e6c3c48e1b62139d7303c10afc69ca8982753672d4d7b6056bf5994915c0287` |
| `evaluations/runs/round-4-k7-k8/independent-scoring.md` | `c56c39eb6b7a67d1c431733b912f6a6fbcb18801d35e560d1e50b455c2d50d9f` | `017cafacc39782ef5822868057f8d072c505de4c605701f1c284bc03dddf372c` |
| `evaluations/runs/round-4-k7-k8/output.md` | `aab77471cae6184943ea350f5ff4c7013f0aa58f68fa625a46535e02519c57d6` | `65db0ccacbc1242f4fb8414954c39276dc2f796656896fe904800d78be1bacbe` |
| `evaluations/runs/round-4-k7-k8/scoring.md` | `3b0fc0342d5df67c6653708ae3757dfefc265eaa372ae230ddfe2893f9249748` | `24471959db6c7ba91e958d6d6ae8e517c7f8840e6a744f581f4ac1275893d236` |

`independent-scoring.md`에 남은 당시 output 원본 `6b59f5b18c91b0f865f6ac4c5d04b805af1530b4a3d5dfea7c80101e5ce026ba`와 당시 scoring 기록 `3ff5cd1e68b5a9d61cb75cd98deca864d6ff36fd45c002bd741cee8890dd96da`는 사후 계산된 역사적 기록이다. 위 표의 수정 전 공개 파일 해시와 혼동하지 않는다. 공개 사본의 서식 정리는 당시 원본 해시나 채점 시점의 독립성 증거를 새로 입증하지 않는다.
