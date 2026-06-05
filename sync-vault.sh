#!/usr/bin/env bash
# Sync selected vault folders into Quartz content/ for deployment.
# Run before `git commit && git push` to update the site.
set -euo pipefail

VAULT="$HOME/Documents/History"
CONTENT="$HOME/quartz/content"

# These are the folders we track. Everything else in the vault stays out.
declare -a FOLDERS=(
  "Dissertation"
  "Primary Sources"
  "Reading Notes"
  "Evernote/Books"
)

echo "Syncing vault folders to content/..."

for folder in "${FOLDERS[@]}"; do
  src="$VAULT/$folder"
  dst="$CONTENT/$folder"
  if [ -d "$src" ]; then
    mkdir -p "$(dirname "$dst")"
    rsync -a --delete "$src/" "$dst/"
    echo "  OK  $folder"
  else
    echo "  ??  $folder (not found)"
  fi
done

echo "Done. Run: git add -A && git commit -m \"update\" && git push"
