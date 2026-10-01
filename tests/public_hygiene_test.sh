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

absolute_path_pattern='(^|[[:space:]`"'"'"'=(])(/User'
absolute_path_pattern+='s|/roo'
absolute_path_pattern+='t|/tm'
absolute_path_pattern+='p|/private/tm'
absolute_path_pattern+='p|/var/folder'
absolute_path_pattern+='s)/'
ephemeral_id_pattern='\b(term|ctx|ta'
ephemeral_id_pattern+='sk|run|msg)_[[:alnum:]-]+'

if rg -n -I \
  -e "$absolute_path_pattern" \
  -e "$ephemeral_id_pattern" \
  -- "${tracked_files[@]}"; then
  printf 'public tree contains a machine-local path or ephemeral identifier\n' >&2
  exit 1
fi

printf 'public hygiene contract: ok\n'
