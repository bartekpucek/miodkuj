#!/usr/bin/env python3
"""Validate the Miodkuj repository, runtime, and release bundle contract."""

import ast
import importlib.util
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path


AUDIT_SPEC = importlib.util.spec_from_file_location(
    "audit_public_repo", Path(__file__).with_name("audit_public_repo.py")
)
if AUDIT_SPEC is None or AUDIT_SPEC.loader is None:
    raise RuntimeError("public repository audit module could not be loaded")
PUBLIC_REPO_AUDIT = importlib.util.module_from_spec(AUDIT_SPEC)
AUDIT_SPEC.loader.exec_module(PUBLIC_REPO_AUDIT)


RUNTIME = Path("plugins/miodkuj/skills/miodkuj")
REFERENCES = RUNTIME / "references"
BUNDLE = Path("dist/miodkuj.skill")
RELEASE_VERSION = "2.1.1"
CODEX_PLUGIN_MANIFEST = Path("plugins/miodkuj/.codex-plugin/plugin.json")
INSTALLATION_MANIFESTS = (
    Path(".claude-plugin/plugin.json"),
    Path(".claude-plugin/marketplace.json"),
    CODEX_PLUGIN_MANIFEST,
    Path(".agents/plugins/marketplace.json"),
)
INSTALLATION_MANIFEST_CONTRACTS = {
    Path(".claude-plugin/plugin.json"): (
        ("name", ("name",), "miodkuj"),
        ("version", ("version",), RELEASE_VERSION),
        ("repository", ("repository",), "https://github.com/bartekpucek/miodkuj"),
        ("skills", ("skills",), ["./plugins/miodkuj/skills/miodkuj"]),
    ),
    Path(".claude-plugin/marketplace.json"): (
        ("name", ("name",), "miodkuj"),
        ("plugins[0].name", ("plugins", 0, "name"), "miodkuj"),
        ("plugins[0].source", ("plugins", 0, "source"), "./"),
        ("plugins[0].version", ("plugins", 0, "version"), RELEASE_VERSION),
    ),
    CODEX_PLUGIN_MANIFEST: (
        ("name", ("name",), "miodkuj"),
        ("version", ("version",), RELEASE_VERSION),
        ("repository", ("repository",), "https://github.com/bartekpucek/miodkuj"),
        ("skills", ("skills",), "./skills/"),
        ("interface.displayName", ("interface", "displayName"), "Miodkuj"),
    ),
    Path(".agents/plugins/marketplace.json"): (
        ("name", ("name",), "miodkuj"),
        ("interface.displayName", ("interface", "displayName"), "Miodkuj"),
        ("plugins[0].name", ("plugins", 0, "name"), "miodkuj"),
        (
            "plugins[0].source",
            ("plugins", 0, "source"),
            {"source": "local", "path": "./plugins/miodkuj"},
        ),
        (
            "plugins[0].policy",
            ("plugins", 0, "policy"),
            {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        ),
        ("plugins[0].category", ("plugins", 0, "category"), "Writing"),
    ),
}
MANIFEST_PLUGIN_COUNTS = {
    Path(".claude-plugin/marketplace.json"): 1,
    Path(".agents/plugins/marketplace.json"): 1,
}
LEGACY_SLUG = "-".join(("stop", "slop", "PL"))
LEGACY_DISPLAY = " ".join(("Stop", "Slop", "PL"))
SKIPPED_FALLBACK_DIRECTORIES = {".git", "dist", "__pycache__"}
TEXT_CONTROL_BYTES = {9, 10, 13}
EXPECTED_DISPLAY_NAME = "Miodkuj"
EXPECTED_SHORT_DESCRIPTION = "Polszczyzna bez sztucznego tonu"
EXPECTED_DEFAULT_PROMPT = (
    "Use $miodkuj to make the minimum effective edit to this Polish text while "
    "preserving its facts, register, and voice."
)
ALLOWED_METADATA_KEYS = {
    "interface": frozenset(
        {"display_name", "short_description", "default_prompt"}
    ),
    "policy": frozenset({"allow_implicit_invocation"}),
}


def repository_files(root: Path) -> list[Path]:
    """Return repository-relevant files, honoring Git ignore rules when possible."""
    git_dir = root / ".git"
    if git_dir.exists():
        try:
            result = subprocess.run(
                ["git", "ls-files", "--cached", "-z"],
                cwd=root,
                capture_output=True,
                check=False,
            )
        except OSError:
            result = None
        if result is not None and result.returncode == 0:
            paths = (
                root / Path(relative)
                for relative in result.stdout.decode(
                    "utf-8", errors="surrogateescape"
                ).split("\0")
                if relative
            )
            return sorted(paths)

    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and not any(
            part in SKIPPED_FALLBACK_DIRECTORIES
            for part in path.relative_to(root).parts
        )
    )


def is_binary(contents: bytes) -> bool:
    """Return whether bytes contain NUL or non-text control characters."""
    return any(
        byte == 0 or byte == 127 or (byte < 32 and byte not in TEXT_CONTROL_BYTES)
        for byte in contents
    )


def files_by_name(folder: Path) -> dict[str, bytes]:
    """Return Markdown files keyed by basename for exact-content comparison."""
    if not folder.is_dir():
        return {}
    return {path.name: path.read_bytes() for path in sorted(folder.glob("*.md"))}


def validate_identity(root: Path, errors: list[str]) -> None:
    """Reject the old product identity in tracked-style paths and UTF-8 text."""
    legacy_slug = LEGACY_SLUG.casefold()
    legacy_display = LEGACY_DISPLAY.casefold()
    for path in repository_files(root):
        relative = path.relative_to(root)
        relative_text = relative.as_posix()
        if legacy_slug in relative_text.casefold():
            errors.append(f"legacy identifier in path: {relative_text}")

        try:
            raw_contents = path.read_bytes()
        except OSError:
            continue
        if is_binary(raw_contents):
            continue
        try:
            contents = raw_contents.decode("utf-8")
        except UnicodeDecodeError:
            continue
        normalized_contents = contents.casefold()
        if legacy_display in normalized_contents:
            errors.append(f"legacy display name in text: {relative_text}")
        if legacy_slug in normalized_contents:
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

    skill_files = sorted(
        path
        for path in root.rglob("SKILL.md")
        if not any(
            part in SKIPPED_FALLBACK_DIRECTORIES
            for part in path.relative_to(root).parts
        )
    )
    runtimes = {path.parent.relative_to(root) for path in skill_files}
    if runtimes != {RUNTIME}:
        for runtime in sorted(runtimes - {RUNTIME}):
            errors.append(f"unexpected runtime folder: {runtime}")
        if RUNTIME not in runtimes:
            errors.append(f"missing runtime folder: {RUNTIME}")


def read_json_object(path: Path, errors: list[str]) -> dict | None:
    """Read an installation manifest and require a JSON object."""
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        errors.append(f"invalid installation manifest: {path}: {exc}")
        return None
    if not isinstance(value, dict):
        errors.append(f"installation manifest must be an object: {path}")
        return None
    return value


def manifest_contract_value(value: dict, path: tuple[str | int, ...]) -> tuple[bool, object]:
    """Return a nested manifest value without trusting its intermediate shape."""
    current: object = value
    for component in path:
        if isinstance(component, str):
            if not isinstance(current, dict) or component not in current:
                return False, None
            current = current[component]
        elif not isinstance(current, list) or component >= len(current):
            return False, None
        else:
            current = current[component]
    return True, current


def validate_installation_manifest_contract(
    relative: Path, value: dict, errors: list[str]
) -> None:
    """Enforce the Task 1 Claude and Codex descriptor contract."""
    plugin_count = MANIFEST_PLUGIN_COUNTS.get(relative)
    if plugin_count is not None:
        plugins = value.get("plugins")
        if not isinstance(plugins, list) or len(plugins) != plugin_count:
            errors.append(
                f"installation manifest contract drift: {relative}: plugins"
            )

    for field, path, expected in INSTALLATION_MANIFEST_CONTRACTS[relative]:
        found, actual = manifest_contract_value(value, path)
        if not found or actual != expected:
            errors.append(
                f"installation manifest contract drift: {relative}: {field}"
            )


def validate_installation_manifests(root: Path, errors: list[str]) -> None:
    """Require the Claude and Codex marketplace manifests at one release version."""
    parsed: dict[Path, dict] = {}
    for relative in INSTALLATION_MANIFESTS:
        path = root / relative
        if not path.is_file():
            errors.append(f"missing installation manifest: {relative}")
            continue
        value = read_json_object(path, errors)
        if value is not None:
            parsed[relative] = value

    for relative, value in parsed.items():
        validate_installation_manifest_contract(relative, value, errors)

    for relative in (
        Path(".claude-plugin/plugin.json"),
        Path(".claude-plugin/marketplace.json"),
        CODEX_PLUGIN_MANIFEST,
    ):
        value = parsed.get(relative)
        if value is None:
            continue
        metadata = value.get("metadata")
        version = value.get("version")
        if version is None and isinstance(metadata, dict):
            version = metadata.get("version")
        if version != RELEASE_VERSION:
            errors.append(f"installation manifest version drift: {relative}")


def validate_references(root: Path, errors: list[str]) -> None:
    """Keep generated runtime references byte-for-byte aligned with their source."""
    shared = files_by_name(root / "shared/references")
    target = files_by_name(root / REFERENCES)
    if target != shared:
        errors.append(f"reference drift: {REFERENCES} differs from shared/references")


def parse_metadata_scalar(value: str, line_number: int) -> object:
    """Parse the scalar forms used by the repository's OpenAI metadata."""
    if value in {"true", "false"}:
        return value == "true"
    if value.startswith(("\"", "'")):
        try:
            parsed = ast.literal_eval(value)
        except (SyntaxError, ValueError) as error:
            raise ValueError(f"invalid quoted scalar on line {line_number}") from error
        if not isinstance(parsed, str):
            raise ValueError(f"non-string quoted scalar on line {line_number}")
        return parsed
    if not value:
        raise ValueError(f"missing scalar value on line {line_number}")
    raise ValueError(f"unsupported scalar syntax on line {line_number}")


def parse_openai_metadata(contents: str) -> dict[str, dict[str, object]]:
    """Parse the small two-level mapping supported by agents/openai.yaml."""
    metadata: dict[str, dict[str, object]] = {}
    section: str | None = None
    for line_number, raw_line in enumerate(contents.splitlines(), start=1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if "\t" in raw_line:
            raise ValueError(f"tabs are not allowed on line {line_number}")

        if raw_line.startswith(" "):
            match = re.fullmatch(r"  ([a-z][a-z0-9_]*):\s*(.*?)\s*", raw_line)
            if match is None or section is None:
                raise ValueError(f"invalid nested mapping on line {line_number}")
            key, raw_value = match.groups()
            if key not in ALLOWED_METADATA_KEYS[section]:
                raise ValueError(f"unsupported key {section}.{key}")
            if key in metadata[section]:
                raise ValueError(f"duplicate key {section}.{key}")
            metadata[section][key] = parse_metadata_scalar(raw_value, line_number)
            continue

        match = re.fullmatch(r"([a-z][a-z0-9_]*):\s*", raw_line)
        if match is None:
            raise ValueError(f"invalid top-level mapping on line {line_number}")
        section = match.group(1)
        if section not in ALLOWED_METADATA_KEYS:
            raise ValueError(f"unsupported top-level key {section}")
        if section in metadata:
            raise ValueError(f"duplicate top-level key {section}")
        metadata[section] = {}
    return metadata


def validate_metadata(root: Path, errors: list[str]) -> None:
    """Structurally check the portable runtime's Codex-facing metadata."""
    metadata_path = root / RUNTIME / "agents/openai.yaml"
    try:
        contents = metadata_path.read_text(encoding="utf-8")
    except OSError as error:
        errors.append(f"unreadable Codex metadata: {RUNTIME / 'agents/openai.yaml'}: {error}")
        return

    try:
        metadata = parse_openai_metadata(contents)
    except ValueError as error:
        errors.append(f"invalid Codex metadata: {error}")
        return

    interface = metadata.get("interface", {})
    policy = metadata.get("policy", {})
    if interface.get("display_name") != EXPECTED_DISPLAY_NAME:
        errors.append(f'Codex interface.display_name must be "{EXPECTED_DISPLAY_NAME}"')
    if interface.get("short_description") != EXPECTED_SHORT_DESCRIPTION:
        errors.append(
            "Codex interface.short_description must be "
            f'"{EXPECTED_SHORT_DESCRIPTION}"'
        )
    if interface.get("default_prompt") != EXPECTED_DEFAULT_PROMPT:
        errors.append(
            "Codex interface.default_prompt must exactly invoke $miodkuj with the "
            "approved prompt"
        )
    if policy.get("allow_implicit_invocation") is not True:
        errors.append("Codex policy.allow_implicit_invocation must be boolean true")


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


def validate_distribution_directory(root: Path, errors: list[str]) -> None:
    """Reject retired skill bundles alongside the canonical distribution artifact."""
    dist = root / "dist"
    if not dist.is_dir():
        return
    for path in sorted(dist.glob("*.skill")):
        if path.name != "miodkuj.skill":
            errors.append(f"unexpected distribution artifact: dist/{path.name}")


def validate_public_tree(root: Path, errors: list[str]) -> None:
    """Surface shared privacy findings when validating a Git repository."""
    if not (root / ".git").exists():
        return
    try:
        errors.extend(PUBLIC_REPO_AUDIT.scan_tree(root))
    except PUBLIC_REPO_AUDIT.AuditError:
        errors.append("public repository tree audit could not complete safely")


def validate_repo(root: Path) -> list[str]:
    """Return repository contract violations; an empty list means success."""
    errors: list[str] = []
    validate_identity(root, errors)
    validate_layout(root, errors)
    validate_installation_manifests(root, errors)
    validate_references(root, errors)
    validate_metadata(root, errors)
    validate_changelog(root, errors)
    validate_bundle(root, errors)
    validate_distribution_directory(root, errors)
    validate_public_tree(root, errors)
    return errors


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[1]
    failures = validate_repo(repo_root)
    if failures:
        for failure in failures:
            print(f"FAIL  {failure}")
        sys.exit(1)
    print("PASS  Miodkuj identity, runtime, metadata, references, and bundle")
