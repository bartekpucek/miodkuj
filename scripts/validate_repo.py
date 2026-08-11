#!/usr/bin/env python3
"""Validate the Miodkuj repository, runtime, and release bundle contract."""

import sys
import zipfile
from pathlib import Path


RUNTIME = Path("skills/miodkuj")
REFERENCES = RUNTIME / "references"
BUNDLE = Path("dist/miodkuj.skill")
RELEASE_VERSION = "2.0.0"
OBSOLETE_MANIFESTS = (
    Path(".claude-plugin/plugin.json"),
    Path(".claude-plugin/marketplace.json"),
)
LEGACY_SLUG = "-".join(("stop", "slop", "PL"))
LEGACY_DISPLAY = " ".join(("Stop", "Slop", "PL"))
SKIPPED_DIRECTORIES = {".git", "dist", "__pycache__"}


def repository_files(root: Path) -> list[Path]:
    """Return ordinary repository files, excluding generated and VCS content."""
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and not any(part in SKIPPED_DIRECTORIES for part in path.relative_to(root).parts)
    )


def files_by_name(folder: Path) -> dict[str, bytes]:
    """Return Markdown files keyed by basename for exact-content comparison."""
    if not folder.is_dir():
        return {}
    return {path.name: path.read_bytes() for path in sorted(folder.glob("*.md"))}


def validate_identity(root: Path, errors: list[str]) -> None:
    """Reject the old product identity in tracked-style paths and UTF-8 text."""
    for path in repository_files(root):
        relative = path.relative_to(root)
        relative_text = relative.as_posix()
        if LEGACY_SLUG in relative_text:
            errors.append(f"legacy identifier in path: {relative_text}")

        try:
            contents = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if LEGACY_DISPLAY in contents:
            errors.append(f"legacy display name in text: {relative_text}")
        if LEGACY_SLUG in contents:
            errors.append(f"legacy identifier in text: {relative_text}")


def validate_layout(root: Path, errors: list[str]) -> None:
    """Require one portable runtime and no platform-specific copies."""
    runtime_root = root / RUNTIME
    for required, predicate in (
        (Path("SKILL.md"), Path.is_file),
        (Path("agents/openai.yaml"), Path.is_file),
        (Path("references"), Path.is_dir),
    ):
        target = runtime_root / required
        if not predicate(target):
            errors.append(f"missing runtime file: {RUNTIME / required}")

    skills_root = root / "skills"
    skill_files = sorted(skills_root.rglob("SKILL.md")) if skills_root.is_dir() else []
    runtimes = {path.parent.relative_to(root) for path in skill_files}
    if runtimes != {RUNTIME}:
        for runtime in sorted(runtimes - {RUNTIME}):
            errors.append(f"unexpected runtime folder: {runtime}")
        if RUNTIME not in runtimes:
            errors.append(f"missing runtime folder: {RUNTIME}")

    for platform in ("claude", "codex"):
        copy = skills_root / platform
        if copy.exists():
            errors.append(f"platform-specific runtime copy: skills/{platform}")

    for manifest in OBSOLETE_MANIFESTS:
        if (root / manifest).exists():
            errors.append(f"obsolete plugin manifest: {manifest}")


def validate_references(root: Path, errors: list[str]) -> None:
    """Keep generated runtime references byte-for-byte aligned with their source."""
    shared = files_by_name(root / "shared/references")
    target = files_by_name(root / REFERENCES)
    if target != shared:
        errors.append(f"reference drift: {REFERENCES} differs from shared/references")


def validate_metadata(root: Path, errors: list[str]) -> None:
    """Check the portable runtime's Codex-facing metadata without a YAML parser."""
    metadata_path = root / RUNTIME / "agents/openai.yaml"
    try:
        metadata = metadata_path.read_text(encoding="utf-8")
    except OSError as error:
        errors.append(f"unreadable Codex metadata: {RUNTIME / 'agents/openai.yaml'}: {error}")
        return

    if 'display_name: "Miodkuj"' not in metadata:
        errors.append('Codex display_name must be "Miodkuj"')
    if "$miodkuj" not in metadata:
        errors.append("Codex default_prompt must mention $miodkuj")


def validate_changelog(root: Path, errors: list[str]) -> None:
    """Require a changelog entry for the portable-skill release."""
    changelog_path = root / "CHANGELOG.md"
    try:
        changelog = changelog_path.read_text(encoding="utf-8")
    except OSError as error:
        errors.append(f"unreadable changelog: CHANGELOG.md: {error}")
        return
    if f"## [{RELEASE_VERSION}]" not in changelog:
        errors.append(f"changelog missing version {RELEASE_VERSION}")


def validate_bundle(root: Path, errors: list[str]) -> None:
    """Compare every archive entry and byte with the canonical runtime."""
    archive = root / BUNDLE
    if not archive.is_file():
        errors.append(f"missing {BUNDLE}")
        return

    source_root = root / RUNTIME
    expected = {
        f"miodkuj/{path.relative_to(source_root).as_posix()}": path.read_bytes()
        for path in sorted(source_root.rglob("*"))
        if path.is_file() and path.name != ".DS_Store"
    }
    try:
        with zipfile.ZipFile(archive) as bundle:
            entries = bundle.infolist()
            actual = {entry.filename: bundle.read(entry) for entry in entries}
    except (OSError, RuntimeError, zipfile.BadZipFile) as error:
        errors.append(f"invalid skill bundle: {BUNDLE}: {error}")
        return

    names = [entry.filename for entry in entries]
    if (
        len(names) != len(set(names))
        or len(actual) != len(expected)
        or set(actual) != set(expected)
        or actual != expected
    ):
        errors.append(f"built skill artifact differs from {RUNTIME}")


def validate_repo(root: Path) -> list[str]:
    """Return repository contract violations; an empty list means success."""
    errors: list[str] = []
    validate_identity(root, errors)
    validate_layout(root, errors)
    validate_references(root, errors)
    validate_metadata(root, errors)
    validate_changelog(root, errors)
    validate_bundle(root, errors)
    return errors


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[1]
    failures = validate_repo(repo_root)
    if failures:
        for failure in failures:
            print(f"FAIL  {failure}")
        sys.exit(1)
    print("PASS  Miodkuj identity, runtime, metadata, references, and bundle")
