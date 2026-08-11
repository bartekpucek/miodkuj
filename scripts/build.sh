#!/usr/bin/env bash
# Sync the single source of truth (shared/references) into the portable skill,
# then package it as an installable .skill bundle.
#
# Usage: ./scripts/build.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/shared/references"

if [ ! -d "$SRC" ]; then
  echo "error: $SRC not found" >&2
  exit 1
fi

sync_refs() {
  local dest="$1"
  mkdir -p "$dest"
  rm -f "$dest"/*.md
  cp "$SRC"/*.md "$dest"/
  echo "  synced -> ${dest#$ROOT/}"
}

echo "Syncing references from shared/references ..."
sync_refs "$ROOT/skills/miodkuj/references"

# Package the portable skill as a .skill bundle (a zip whose root is the skill
# folder). Uses Python's zipfile so no external `zip` binary is required.
DIST="$ROOT/dist"
mkdir -p "$DIST"
python3 - "$ROOT/skills" "$DIST/miodkuj.skill" <<'PY'
import sys, zipfile, pathlib
base = pathlib.Path(sys.argv[1])
out = sys.argv[2]
root = base / "miodkuj"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as bundle:
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.name != ".DS_Store":
            bundle.write(path, path.relative_to(base).as_posix())
PY

echo "Built ${DIST#$ROOT/}/miodkuj.skill"
echo "Done."
