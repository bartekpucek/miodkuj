#!/usr/bin/env python3
"""Portable validator for a SKILL.md skill folder.

Checks the rules that matter for Claude / Claude Code skill loading:
  - SKILL.md exists and has YAML-style frontmatter
  - name: lowercase kebab-case, <= 64 chars, no reserved words, matches folder
  - description: non-empty, <= 200 chars, no angle brackets
  - every references/*.md mentioned in the body actually exists

Stdlib only, no third-party deps. Usage:
    python3 scripts/validate_skill.py plugins/miodkuj/skills/miodkuj
"""
import re
import sys
from pathlib import Path

RESERVED = ("anthropic", "claude")
MAX_DESCRIPTION_LENGTH = 200


def fail(msgs, m):
    msgs.append(("FAIL", m))


def ok(msgs, m):
    msgs.append(("ok", m))


def validate(skill_dir: Path) -> bool:
    msgs = []
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.is_file():
        print(f"FAIL  {skill_dir}: no SKILL.md")
        return False

    text = skill_md.read_text(encoding="utf-8")
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not fm_match:
        print(f"FAIL  {skill_dir}: no YAML frontmatter (--- ... ---)")
        return False
    frontmatter, body = fm_match.group(1), text[fm_match.end():]

    def field(key):
        m = re.search(rf"^{key}:\s*(.+?)\s*$", frontmatter, re.MULTILINE)
        return m.group(1).strip() if m else None

    name = field("name")
    desc = field("description")

    # name checks
    if not name:
        fail(msgs, "missing 'name'")
    else:
        if not re.fullmatch(r"[a-z0-9-]+", name):
            fail(msgs, f"name '{name}' must be lowercase letters, digits, hyphens only")
        else:
            ok(msgs, f"name '{name}' format")
        if len(name) > 64:
            fail(msgs, f"name too long ({len(name)} > 64)")
        if any(w in name for w in RESERVED):
            fail(msgs, f"name contains reserved word ({', '.join(RESERVED)})")
        if name != skill_dir.name:
            fail(msgs, f"name '{name}' != folder '{skill_dir.name}'")
        else:
            ok(msgs, "name matches folder")

    # description checks
    if not desc:
        fail(msgs, "missing 'description'")
    else:
        if len(desc) > MAX_DESCRIPTION_LENGTH:
            fail(
                msgs,
                f"description too long ({len(desc)} > {MAX_DESCRIPTION_LENGTH})",
            )
        else:
            ok(msgs, f"description length {len(desc)}/{MAX_DESCRIPTION_LENGTH}")
        if "<" in desc or ">" in desc:
            fail(msgs, "description contains angle brackets (not allowed)")
        else:
            ok(msgs, "description has no XML tags")

    # body length
    n_lines = body.count("\n") + 1
    if n_lines > 500:
        fail(msgs, f"SKILL.md body {n_lines} lines (> 500 recommended)")
    else:
        ok(msgs, f"body {n_lines} lines (<= 500)")

    # referenced files exist
    refs = sorted(set(re.findall(r"references/[\w./-]+\.md", body)))
    for ref in refs:
        if (skill_dir / ref).is_file():
            ok(msgs, f"resolves {ref}")
        else:
            fail(msgs, f"missing referenced file {ref}")

    failed = any(level == "FAIL" for level, _ in msgs)
    print(f"\n{'FAIL' if failed else 'PASS'}  {skill_dir}")
    for level, m in msgs:
        print(f"  [{level}] {m}")
    return not failed


if __name__ == "__main__":
    targets = sys.argv[1:]
    if not targets:
        print("usage: validate_skill.py <skill_dir> [<skill_dir> ...]")
        sys.exit(2)
    results = [validate(Path(t)) for t in targets]
    sys.exit(0 if all(results) else 1)
