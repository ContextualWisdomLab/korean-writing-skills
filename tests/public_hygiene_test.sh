#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

required_docs=(
  ARCHITECTURE.md
  CHANGELOG.md
  CLAUDE.md
  SECURITY.md
  docs/adr/0001-skill-product-boundary.md
  docs/product-technical-gap-baseline.md
)

for required_doc in "${required_docs[@]}"; do
  [[ -s "$required_doc" ]] || {
    printf 'missing required governance document: %s\n' "$required_doc" >&2
    exit 1
  }
done

removed_runtime_artifacts=(
  LEAD-RECOVERY-20260921.md
  LEAD-REPORT.md
  LEAD_QUEUE.md
  registered_agents.json
  task_""agent_mapping.json
  evaluations/runs/workspace.json
)

for removed_artifact in "${removed_runtime_artifacts[@]}"; do
  [[ ! -e "$removed_artifact" ]] || {
    printf 'runtime artifact is still public: %s\n' "$removed_artifact" >&2
    exit 1
  }
done

tracked_files=()
while IFS= read -r tracked_file; do
  tracked_files+=("$tracked_file")
done < <(git ls-files)

absolute_path_pattern='(^|[[:space:]`"'"'"'=(]|file://)(/User'
absolute_path_pattern+='s|/roo'
absolute_path_pattern+='t|/home|/workspace|/tm'
absolute_path_pattern+='p|/private/tm'
absolute_path_pattern+='p|/var/folder'
absolute_path_pattern+='s)/'
ephemeral_id_pattern='\b(term|ctx|ta'
ephemeral_id_pattern+='sk|run|msg)_[[:alnum:]-]{8,}\b'

for unsafe_fixture in \
  '/User'""'s/example/work/file.md' \
  '/work'""'space/example/file.md' \
  'file:///roo'""'t/evidence.json' \
  'term_'""'12345678' \
  'run_'""'deadbeef'; do
  printf '%s\n' "$unsafe_fixture" | rg -q \
    -e "$absolute_path_pattern" -e "$ephemeral_id_pattern" || {
    printf 'public hygiene matcher missed fixture: %s\n' "$unsafe_fixture" >&2
    exit 1
  }
done

for safe_fixture in 'run_id' 'task_id' 'http://localhost:23119/api'; do
  if printf '%s\n' "$safe_fixture" | rg -q \
    -e "$absolute_path_pattern" -e "$ephemeral_id_pattern"; then
    printf 'public hygiene matcher rejected stable fixture: %s\n' "$safe_fixture" >&2
    exit 1
  fi
done

scan_status=0
scan_output="$(rg -n -I \
  -e "$absolute_path_pattern" \
  -e "$ephemeral_id_pattern" \
  -- "${tracked_files[@]}")" || scan_status=$?
case "$scan_status" in
0)
  printf '%s\n' "$scan_output"
  printf 'public tree contains a machine-local path or ephemeral identifier\n' >&2
  exit 1
  ;;
1) ;;
*)
  printf 'public hygiene scan failed with status %s\n' "$scan_status" >&2
  exit "$scan_status"
  ;;
esac

for tracked_file in "${tracked_files[@]}"; do
  if [[ "$tracked_file" =~ (^|/)(term|ctx|task|run|msg)_[[:alnum:]-]{8,}($|[^[:alnum:]_-]) ]]; then
    printf 'public filename contains an ephemeral identifier: %s\n' "$tracked_file" >&2
    exit 1
  fi
done

printf 'public hygiene contract: ok\n'
