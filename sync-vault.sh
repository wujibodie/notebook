#!/usr/bin/env bash
# Sync selected vault folders into Quartz content/ for deployment.
# Run this before `git commit && git push` to update the site.
set -euo pipefail

VAULT="$HOME/Documents/History"
CONTENT="$HOME/quartz/content"

declare -a FOLDERS=(
  "Dissertation"
  "Primary Sources"
  "Reading Notes"
  "Evernote/Books"
)

for folder in "${FOLDERS[@]}"; do
  src="$VAULT/$folder"
  dst="$CONTENT/$folder"
  if [ -d "$src" ]; then
    mkdir -p "$(dirname "$dst")"
    rsync -a --delete "$src/" "$dst/"
    echo "  synced  $folder"
  else
    echo "  SKIP    $folder (not found)"
  fi
done

# Also copy top-level .md files that aren't in excluded folders
for f in "$VAULT"/*.md; do
  [ -f "$f" ] && cp "$f" "$CONTENT/"
done

echo "Done. Run git add/commit/push to deploy."
