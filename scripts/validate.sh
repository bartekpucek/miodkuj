#!/usr/bin/env bash
# Validate the portable skill and repository packaging contract.
# Usage: ./scripts/validate.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 "$ROOT/scripts/validate_skill.py" "$ROOT/plugins/miodkuj/skills/miodkuj"
python3 -m unittest discover -s "$ROOT/tests" -p "test_*.py" -v
python3 "$ROOT/scripts/validate_repo.py"
python3 "$ROOT/scripts/smoke_install.py" --structural-only --platform all
