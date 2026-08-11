#!/usr/bin/env python3
"""Validate repository-wide synchronization and packaging contracts."""

import json
import sys
import zipfile
from pathlib import Path


TARGETS = (
    Path("skills/codex/stop-slop-pl/references"),
    Path("skills/claude/stop-slop-pl/references"),
)


def files_by_name(folder: Path) -> dict[str, bytes]:
    """Return Markdown files keyed by basename for exact-content comparison."""
    return {path.name: path.read_bytes() for path in sorted(folder.glob("*.md"))}


def validate_repo(root: Path) -> list[str]:
    """Return repository contract violations; an empty list means success."""
    errors = []
    shared = files_by_name(root / "shared/references")
    for relative in TARGETS:
        target = files_by_name(root / relative)
        if target != shared:
            errors.append(
                f"reference drift: {relative} differs from shared/references"
            )

    plugin = json.loads(
        (root / ".claude-plugin/plugin.json").read_text(encoding="utf-8")
    )
    marketplace = json.loads(
        (root / ".claude-plugin/marketplace.json").read_text(encoding="utf-8")
    )
    versions = {
        plugin["version"],
        marketplace["metadata"]["version"],
        marketplace["plugins"][0]["version"],
    }
    if len(versions) != 1:
        errors.append(f"version mismatch: {sorted(versions)}")
    version = next(iter(versions))
    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    if f"## [{version}]" not in changelog:
        errors.append(f"changelog missing version {version}")

    metadata = (
        root / "skills/codex/stop-slop-pl/agents/openai.yaml"
    ).read_text(encoding="utf-8")
    if "$stop-slop-pl" not in metadata:
        errors.append("Codex default_prompt must mention $stop-slop-pl")

    archive = root / "dist/stop-slop-pl.skill"
    if not archive.is_file():
        errors.append("missing dist/stop-slop-pl.skill")
    else:
        source_root = root / "skills/claude/stop-slop-pl"
        expected = {
            f"stop-slop-pl/{path.relative_to(source_root).as_posix()}": path.read_bytes()
            for path in sorted(source_root.rglob("*"))
            if path.is_file() and path.name != ".DS_Store"
        }
        with zipfile.ZipFile(archive) as bundle:
            actual = {name: bundle.read(name) for name in sorted(bundle.namelist())}
        if actual != expected:
            errors.append(
                "built skill artifact differs from skills/claude/stop-slop-pl"
            )

    return errors


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[1]
    failures = validate_repo(repo_root)
    if failures:
        for failure in failures:
            print(f"FAIL  {failure}")
        sys.exit(1)
    print("PASS  repository synchronization, metadata, and bundle")
