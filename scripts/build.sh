#!/usr/bin/env bash
# Sync the single source of truth (shared/references) into every skill target,
# then package the Claude skill as an installable .skill bundle.
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
sync_refs "$ROOT/skills/codex/stop-slop-pl/references"
sync_refs "$ROOT/skills/claude/stop-slop-pl/references"

# Package the Claude skill as a .skill bundle (a zip whose root is the skill folder).
# Works for both claude.ai upload and Cowork "Save skill". Uses Python's zipfile
# so no external `zip` binary is required.
DIST="$ROOT/dist"
mkdir -p "$DIST"
python3 - "$ROOT/skills/claude" "$DIST/stop-slop-pl.skill" <<'PY'
import sys, zipfile, pathlib
base = pathlib.Path(sys.argv[1])
out = sys.argv[2]
root = base / "stop-slop-pl"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for p in sorted(root.rglob("*")):
        if p.is_file() and p.name != ".DS_Store":
            z.write(p, p.relative_to(base).as_posix())
PY

echo "Built ${DIST#$ROOT/}/stop-slop-pl.skill"
echo "Done."
