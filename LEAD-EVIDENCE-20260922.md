# Lead recovery 첫 실측 증거 — 2026-09-22 12:3x UTC

## Goal (define-goal quality bar)

PR #3을 병합 가능 판정(병합 또는 근거 있는 terminal BLOCKED)까지 shepherd하고,
보존 증거를 확정하며, 공개 저장소에 연구 원고 렌더·참여자 자료를 남기지 않고,
retired worktree를 --force/rm 없이 처리한다.
증거: exact head 해시, `gh pr checks 3` 출력, bundle verify+SHA-256, tar manifest+바이트 대조,
Tree/diff 무결성 스캔, current-head CodeRabbit review. 성공 기준은 전부 이진 판정이다.
범위 밖: 중앙 GitHub CI 수정(dot-github lead 소유 — 증거·의존성만 전달),
late-life 원고 직접 수정, 경계 정리 외 신규 스킬 내용.
병합은 필수 검사 green + current-head 비저자 승인 확인 후에만 수행한다.

## Exact head

- REPO_ROOT: `/Users/seonghobae/orca/workspaces/korean-writing-skills/writing-skills-lead-recovery-20260921`
- local HEAD = origin branch = origin/pr/3/head = `bffb0cc57fe5ddefbafb4b342787e25b603bd2b6`
- PR #3: OPEN, base main, `mergeable=MERGEABLE`, `mergeStateStatus=BLOCKED`
- canonical docs: repo에 `docs/engineering/` 없음. `AGENTS.md`를 authoritative source로 사용, 없음은 발명하지 않음.

## PR #3 checks (gh pr checks 3, 2026-09-22 ~12:15 UTC)

- fail: CodeQL compatibility analysis, noema-review, opencode-review
- pass: CodeRabbit(Review completed), Admit current pull request head, Detect changed scope,
  Scorecard, Semgrep, Trivy, coverage-evidence 등
- pending: Dispatch current-head CodeQL scan, strix
- skipping: dependency-review, osv-scan, gitleaks, cancel-closed-pr-runs
- 실패 job 로그 상세는 미확보: `gh run view` 404 + `gh api` 403 rate limit
  (user 8172694, 2026-09-22 12:22:13 UTC). 중앙 CI 문제는 dot-github lead 소유이므로
  중복 수정 없이 본 증거와 의존성만 전달한다. API 추가 호출은 backoff한다.

## 보존 검증 (완전 — 새 보존 파일 불필요)

- bundle `~/.local/orca-watchdog/preserve/writing-skills-lead-retired-65883a7.bundle`
  SHA-256 `b99c31b93488a36af07b05f2892a2c24b81d3174431b15c54b9a844570674835`,
  `git bundle verify` 정상, 17 refs, tip `65883a7` 포함.
- tar `~/.local/orca-watchdog/preserve/writing-skills-lead-retired-untracked.tgz`
  SHA-256 `bacd5276b0f118851c5d12d791cba15af39d90d399c1ad5ada9ba1f744beed39`,
  6 entries (p0-review 3파일 + 2 json).
- retired tip의 origin/main 대비 commit 수: 인계서 43과 달리 실측 **52**.
  bundle clone 대조 결과 52개 해시 전부 동일 — 43이 아닌 52 전체가 보존됨.
- untracked 바이트 대조: 5파일 전부 SAME (report.md `c854ade5…`, findings.json `0af42124…`,
  png-sha256.txt `c42c27e3…`, 2 json `44136fa3…`). subagent가 별도 /tmp 추출로 재확인.
- 누락 바이트 없음 → 기존 archive에 덮어쓰지 않고 새 파일 추가하지 않음.

## PR #1 검증 + 연구 혼입 검사

- PR #1: CLOSED, head `44c789e`. `merge-base --is-ancestor 44c789e bffb0cc` = YES.
  PR1-only commit 0개, PR3-only 18개. 범용 변경은 #3에 흡수됨.
- PR1-only 연구 렌더 병합 없음: PR1 Tree·PR3 Tree 바이너리 0개
  (`hwpx|docx|pdf|png|jpg` 매치 없음, Binary 패치 0).
  PR1 diff의 `manuscript_interim_*` 언급은 SHA-256 문자열·미리보기 경로명에 한정되며
  커밋된 바이너리 없음. `bc7e727`이 b5bacc8 렌더 리뷰 104줄을 PR에서 제거했고,
  `5ecc2ad`가 deliverables를 gitignore했다. 평가 케이스는 가상 사례임을 명시.
- `git diff main...HEAD` 내 `/Users/` 절대경로 0건.
  잔류 `~/Documents/Zotero/`, `/tmp/` 표기는 provenance 기록이며 참여자 자료·비밀정보 아님.

## 독립 검증 (blind)

- subagent가 작성자 정답·draft skill을 보지 않고 원본 1건을 직접 열람:
  로컬 Zotero PDF `A9MHWYKV/9780935302356.pdf` (8,961,125 bytes, 241pp,
  SHA-256 `b47005a0…e21e3de06f34941` 일치), PDF pp.118–119 추출.
- Standard 5.21 문장 확인:
  "When proposed score interpretations involve one or more cut scores,
  the rationale and procedures used for establishing cut scores should be documented clearly."
- 판정: 인쇄 pp.107–108 / PDF pp.118–119 근거 요구 주장을 SUPPORTS.

## Retired worktree (제거 미시도 — 조건 미충족)

- `/Users/seonghobae/orca/workspaces/korean-writing-skills/writing-skills-lead`
  상태: `## seonghobae/writing-skills-lead...origin/seonghobae/writing-skills-lead [gone]`,
  untracked 3경로 잔류 (`evaluations/runs/20260921-262eff8-p0-review/`,
  `registered_agents.json`, `task_agent_mapping.json`).
- 보존은 바이트 단위로 완전하나 worktree에 untracked가 남아 있어
  일반 제거 조건(보존 완전 + untracked/dirty 없음)이 불충족 → 제거 미시도.
  --force·직접 rm 사용 없음. 원문 오류 없음(시도 자체를 보류).
- recovery worktree untracked 2건(`registered_agents.json`, `task_agent_mapping.json`,
  각 2 bytes `{}`)은 orca 관리 파일로 유지.

## Blocker와 해제 조건

1. GitHub API 403 rate limit — 해제: reset 후 `gh pr view 3`·checks 재조회. 그 전까지 API 호출 자제.
2. 실패 3 checks의 귀책이 중앙 CI인지 PR인지 미확정 — 해제: dot-github lead의 중앙 수정 또는
   재실행 후 fail 로그 확보. 중복 수정 금지.
3. 병합 — 해제 조건: 필수 검사 green + current-head CodeRabbit review evidence +
   비저자 승인 확인. 셋 중 하나라도 없으면 병합하지 않는다.
4. retired worktree 제거 — 해제 조건: 3개 untracked 경로의 비파괴적 정리(삭제가 아닌
   정당한 귀속 확인) 후 일반 `orca worktree rm` (no --force) 재시도.

## 다음 조치 (유휴 금지)

- 본 파일 commit·push 후 새 head 기준으로 checks/CodeRabbit review 재확인.
- rate limit 해제 후 실패 3 checks 로그 확보 → 중앙 CI이면 dot-github lead에 증거 전달.
- late-life 소유 원고는 건드리지 않고 범용 스킬만 유지.
