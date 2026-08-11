#!/usr/bin/env bash
# Validate every skill target in the repo.
# Usage: ./scripts/validate.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 "$ROOT/scripts/validate_skill.py" \
  "$ROOT/skills/codex/stop-slop-pl" \
  "$ROOT/skills/claude/stop-slop-pl"
python3 -m unittest discover -s "$ROOT/tests" -p "test_*.py" -v
python3 "$ROOT/scripts/validate_repo.py"
