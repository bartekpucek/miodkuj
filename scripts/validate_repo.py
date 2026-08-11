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

PLUGIN_MANIFEST = Path(".claude-plugin/plugin.json")
MARKETPLACE_MANIFEST = Path(".claude-plugin/marketplace.json")


def files_by_name(folder: Path) -> dict[str, bytes]:
    """Return Markdown files keyed by basename for exact-content comparison."""
    return {path.name: path.read_bytes() for path in sorted(folder.glob("*.md"))}


def read_manifest(root: Path, relative: Path, errors: list[str]) -> dict | None:
    """Read a JSON manifest or append one human-readable contract violation."""
    path = root / relative
    try:
        contents = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        errors.append(f"missing manifest: {relative}")
        return None
    except OSError as error:
        errors.append(f"unreadable manifest: {relative}: {error}")
        return None

    try:
        manifest = json.loads(contents)
    except json.JSONDecodeError as error:
        errors.append(
            f"invalid JSON: {relative}: line {error.lineno}, column {error.colno}"
        )
        return None

    if not isinstance(manifest, dict):
        errors.append(f"invalid manifest structure: {relative}")
        return None
    return manifest


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

    plugin = read_manifest(root, PLUGIN_MANIFEST, errors)
    marketplace = read_manifest(root, MARKETPLACE_MANIFEST, errors)
    version_values = []

    if plugin is not None:
        plugin_version = plugin.get("version")
        if isinstance(plugin_version, str) and plugin_version:
            version_values.append(plugin_version)
        else:
            errors.append(f"invalid manifest structure: {PLUGIN_MANIFEST}")

    if marketplace is not None:
        try:
            marketplace_versions = (
                marketplace["metadata"]["version"],
                marketplace["plugins"][0]["version"],
            )
        except (KeyError, IndexError, TypeError):
            errors.append(f"invalid manifest structure: {MARKETPLACE_MANIFEST}")
        else:
            if all(
                isinstance(version, str) and version
                for version in marketplace_versions
            ):
                version_values.extend(marketplace_versions)
            else:
                errors.append(f"invalid manifest structure: {MARKETPLACE_MANIFEST}")

    if len(version_values) == 3:
        versions = set(version_values)
        if len(versions) != 1:
            errors.append(f"version mismatch: {sorted(versions)}")
        else:
            version = version_values[0]
            changelog_path = root / "CHANGELOG.md"
            try:
                changelog = changelog_path.read_text(encoding="utf-8")
            except OSError as error:
                errors.append(f"unreadable changelog: CHANGELOG.md: {error}")
            else:
                if f"## [{version}]" not in changelog:
                    errors.append(f"changelog missing version {version}")

    metadata_path = root / "skills/codex/stop-slop-pl/agents/openai.yaml"
    try:
        metadata = metadata_path.read_text(encoding="utf-8")
    except OSError as error:
        errors.append(
            "unreadable Codex metadata: "
            f"skills/codex/stop-slop-pl/agents/openai.yaml: {error}"
        )
    else:
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
        try:
            with zipfile.ZipFile(archive) as bundle:
                actual = {
                    name: bundle.read(name) for name in sorted(bundle.namelist())
                }
        except (OSError, RuntimeError, zipfile.BadZipFile) as error:
            errors.append(f"invalid skill bundle: dist/stop-slop-pl.skill: {error}")
        else:
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
