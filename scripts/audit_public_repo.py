#!/usr/bin/env python3
"""Audit the public Git tree, release archive, and reachable history."""

import argparse
import io
import os
import re
import subprocess
import sys
import zipfile
from collections.abc import Iterable, Iterator
from pathlib import Path


PUBLIC_GIT_EMAIL = "65296954+bartekpucek@users.noreply.github.com"
EXPECTED_SKILL_ARCHIVE = Path("dist/miodkuj.skill")
INTERNAL_IDENTIFIERS = (
    "".join(("T", "T", "C")),
    " ".join(("Target", "Creators")),
)
_INTERNAL_PLANNING_FOLDER = "".join(("super", "powers"))
_INTERNAL_DESIGN_METHOD = "".join(("s", "dd"))
_INTERNAL_REVIEW_FOLDER = "-".join(("review", "package"))
REDACTION = "[REDACTED]"

_INTERNAL_IDENTIFIER_RE = re.compile(
    r"(?<!\w)(?:"
    + "|".join(re.escape(value) for value in INTERNAL_IDENTIFIERS)
    + r")(?!\w)",
    re.IGNORECASE,
)
_POSIX_HOME_RE = re.compile(
    r"(?<![A-Za-z0-9_])/(?:Users|home)/"
    r"[^/\s\"'<>|]+/(?:[^\s\"'<>|)\]},;]*)"
)
_WINDOWS_HOME_RE = re.compile(
    r"(?i)(?<![A-Za-z0-9_])[A-Z]:\\Users\\"
    r"[^\\\s\"'<>|]+\\(?:[^\s\"'<>|)\]},;]*)"
)
_EMAIL_RE = re.compile(
    r"(?<![A-Za-z0-9.!#$%&'*+/=?^_`{|}~-])"
    r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+"
)
_INTERNAL_PATH_RE = re.compile(
    r"(?i)(?<![A-Za-z0-9_-])(?:"
    + re.escape("." + _INTERNAL_PLANNING_FOLDER)
    + r"|docs[\\/]"
    + re.escape(_INTERNAL_PLANNING_FOLDER)
    + r"|"
    + re.escape(_INTERNAL_DESIGN_METHOD)
    + r"(?=[\\/])|"
    + re.escape(_INTERNAL_REVIEW_FOLDER)
    + r"s?(?=[\\/])"
    + r")(?:[\\/][^\s\"'<>|)\]},;:]*)?"
)


class AuditError(RuntimeError):
    """Raised when repository data cannot be inspected safely."""


def _git(root: Path, *arguments: str, input_data: bytes | None = None) -> bytes:
    try:
        result = subprocess.run(
            ["git", *arguments],
            cwd=root,
            capture_output=True,
            check=False,
            input=input_data,
        )
    except OSError as exc:
        raise AuditError("git command unavailable") from exc
    if result.returncode != 0:
        raise AuditError("git command failed")
    return result.stdout


def _decode(data: bytes) -> str:
    return data.decode("utf-8", errors="surrogateescape")


def _sensitive_matches(text: str) -> list[tuple[str, str]]:
    matches: list[tuple[str, str]] = []
    for category, pattern in (
        ("internal path", _INTERNAL_PATH_RE),
        ("absolute home path", _POSIX_HOME_RE),
        ("absolute home path", _WINDOWS_HOME_RE),
        ("internal identifier", _INTERNAL_IDENTIFIER_RE),
    ):
        matches.extend((category, match.group(0)) for match in pattern.finditer(text))

    for match in _EMAIL_RE.finditer(text):
        literal = match.group(0)
        if literal.casefold() != PUBLIC_GIT_EMAIL.casefold():
            matches.append(("private email metadata", literal))

    return list(dict.fromkeys(matches))


def _redact(text: str) -> str:
    literals = {
        literal for _, literal in _sensitive_matches(text) if literal
    }
    for literal in sorted(literals, key=len, reverse=True):
        text = text.replace(literal, REDACTION)
    return text


def _finding(category: str, object_identifier: str, path: str) -> str:
    return (
        f"category={category}; "
        f"object={_redact(object_identifier)}; "
        f"path={_redact(path)}"
    )


def _scan_source(
    label: str, data: bytes, object_identifier: str
) -> list[str]:
    matches = _sensitive_matches(label)
    matches.extend(_sensitive_matches(_decode(data)))
    categories = sorted({category for category, _ in matches})
    return [_finding(category, object_identifier, label) for category in categories]


def scan_bytes(label: str, data: bytes) -> list[str]:
    """Return redacted privacy findings for one labeled byte sequence."""
    return _scan_source(label, data, "BYTES")


def _tracked_sources(root: Path) -> Iterator[tuple[str, bytes, str]]:
    tracked = _git(root, "ls-files", "--stage", "-z")
    for entry in tracked.split(b"\0"):
        if not entry:
            continue
        header, separator, raw_relative = entry.partition(b"\t")
        fields = header.split()
        if not separator or len(fields) != 3:
            raise AuditError("unexpected git index entry")
        relative = _decode(raw_relative)
        path = root / Path(relative)
        try:
            if path.is_symlink():
                data = os.readlink(path).encode("utf-8", errors="surrogateescape")
            else:
                data = path.read_bytes()
        except OSError:
            data = _git(root, "show", ":" + relative)
        object_identifier = _decode(
            _git(root, "hash-object", "--stdin", input_data=data)
        ).strip()
        yield relative, data, object_identifier


def _archive_sources(
    archive_label: str, data: bytes, object_identifier: str
) -> Iterator[tuple[str, bytes, str]]:
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            for member in sorted(archive.infolist(), key=lambda item: item.filename):
                if member.is_dir():
                    continue
                label = archive_label + "!" + member.filename
                try:
                    contents = archive.read(member)
                except Exception as exc:
                    raise AuditError("skill archive member could not be read") from exc
                yield label, contents, object_identifier
    except AuditError:
        raise
    except Exception as exc:
        raise AuditError("skill archive could not be inspected") from exc


def _dist_archive_sources(root: Path) -> Iterator[tuple[str, bytes, str]]:
    dist = root / "dist"
    if not dist.is_dir():
        return
    for archive in sorted(dist.glob("*.skill")):
        relative = archive.relative_to(root).as_posix()
        try:
            data = archive.read_bytes()
        except OSError as exc:
            raise AuditError("skill archive could not be read") from exc
        object_identifier = _decode(
            _git(root, "hash-object", "--stdin", input_data=data)
        ).strip()
        yield from _archive_sources(relative, data, object_identifier)


def scan_tree(root: Path) -> list[str]:
    """Scan tracked paths and generated skill archives in the current tree."""
    root = root.resolve()
    try:
        findings: list[str] = []
        for label, data, object_identifier in _tracked_sources(root):
            findings.extend(_scan_source(label, data, object_identifier))

        dist = root / "dist"
        if dist.is_dir():
            for archive in sorted(dist.glob("*.skill")):
                relative = archive.relative_to(root)
                if relative != EXPECTED_SKILL_ARCHIVE:
                    try:
                        data = archive.read_bytes()
                    except OSError as exc:
                        raise AuditError("skill archive could not be read") from exc
                    object_identifier = _decode(
                        _git(root, "hash-object", "--stdin", input_data=data)
                    ).strip()
                    findings.append(
                        _finding(
                            "unexpected skill artifact",
                            object_identifier,
                            relative.as_posix(),
                        )
                    )

        for label, data, object_identifier in _dist_archive_sources(root):
            findings.extend(_scan_source(label, data, object_identifier))
        return sorted(set(findings))
    except AuditError:
        raise
    except Exception as exc:
        raise AuditError("tree scan could not complete") from exc


def _reachable_objects(root: Path) -> dict[str, str]:
    raw_objects = _git(
        root,
        "rev-list",
        "--objects",
        "--all",
        "--no-object-names",
    )
    objects: dict[str, str] = {}
    for raw_object in raw_objects.splitlines():
        object_identifier = raw_object.decode("ascii", errors="ignore").strip()
        if not object_identifier or object_identifier in objects:
            continue
        object_type = _decode(
            _git(root, "cat-file", "-t", object_identifier)
        ).strip()
        objects[object_identifier] = object_type
    return objects


def _historical_blob_paths(
    root: Path, blob_identifiers: set[str]
) -> dict[str, set[str]]:
    paths: dict[str, set[str]] = {}
    commits = dict.fromkeys(_git(root, "rev-list", "--all").splitlines())
    for raw_commit in commits:
        commit = raw_commit.decode("ascii", errors="ignore").strip()
        if not commit:
            continue
        tree = _git(root, "ls-tree", "-r", "-z", "--full-tree", commit)
        for entry in tree.split(b"\0"):
            if not entry:
                continue
            header, separator, raw_path = entry.partition(b"\t")
            fields = header.split()
            if not separator or len(fields) != 3:
                raise AuditError("unexpected git tree entry")
            object_identifier = fields[2].decode("ascii", errors="ignore")
            if fields[1] != b"blob" or object_identifier not in blob_identifiers:
                continue
            paths.setdefault(object_identifier, set()).add(_decode(raw_path))
    return paths


def _reachable_blob_sources(
    root: Path, objects: dict[str, str] | None = None
) -> Iterator[tuple[str, bytes, str]]:
    reachable = objects if objects is not None else _reachable_objects(root)
    blob_identifiers = {
        object_identifier
        for object_identifier, object_type in reachable.items()
        if object_type == "blob"
    }
    paths = _historical_blob_paths(root, blob_identifiers)
    for object_identifier in sorted(blob_identifiers):
        data = _git(root, "cat-file", "blob", object_identifier)
        labels = paths.get(object_identifier) or {"<unknown>"}
        for path in sorted(labels):
            yield path, data, object_identifier
            if path.casefold().endswith(".skill"):
                yield from _archive_sources(path, data, object_identifier)


def _reachable_tag_sources(
    root: Path, objects: dict[str, str] | None = None
) -> Iterator[tuple[str, bytes, str]]:
    reachable = objects if objects is not None else _reachable_objects(root)
    for object_identifier, object_type in sorted(reachable.items()):
        if object_type != "tag":
            continue
        data = _git(root, "cat-file", "tag", object_identifier)
        yield "<annotated-tag>", data, object_identifier


def _metadata_sources(root: Path) -> Iterator[tuple[str, bytes, str]]:
    metadata = _git(root, "log", "--all", "--format=%H%x09%ae%x09%ce")
    for line in metadata.splitlines():
        fields = line.split(b"\t", 2)
        if len(fields) != 3:
            continue
        commit = fields[0].decode("ascii", errors="ignore")
        yield "<author-email>", fields[1], commit
        yield "<committer-email>", fields[2], commit


def scan_history(root: Path) -> list[str]:
    """Scan reachable blobs, annotated tags, and commit email metadata."""
    root = root.resolve()
    try:
        findings: list[str] = []
        objects = _reachable_objects(root)
        for label, data, object_identifier in _reachable_blob_sources(root, objects):
            findings.extend(_scan_source(label, data, object_identifier))
        for label, data, object_identifier in _reachable_tag_sources(root, objects):
            findings.extend(_scan_source(label, data, object_identifier))
        for label, data, object_identifier in _metadata_sources(root):
            findings.extend(_scan_source(label, data, object_identifier))
        return sorted(set(findings))
    except AuditError:
        raise
    except Exception as exc:
        raise AuditError("history scan could not complete") from exc


def _replacement_literals(
    sources: Iterable[tuple[str, bytes, str]],
) -> set[str]:
    literals: set[str] = set()
    for label, data, _ in sources:
        for _, literal in _sensitive_matches(label):
            literals.add(literal)
        for _, literal in _sensitive_matches(_decode(data)):
            literals.add(literal)
    return literals


def write_filter_repo_replacements(root: Path, output: Path) -> None:
    """Write exact rewrite literals to a private file outside the repository."""
    root = root.resolve()
    output = output.expanduser().resolve()
    if output == root or output.is_relative_to(root):
        raise ValueError("replacement output must be outside the repository")
    if output.is_symlink():
        raise ValueError("replacement output must not be a symbolic link")

    sources = list(_tracked_sources(root))
    sources.extend(_dist_archive_sources(root))
    objects = _reachable_objects(root)
    sources.extend(_reachable_blob_sources(root, objects))
    sources.extend(_reachable_tag_sources(root, objects))
    sources.extend(_metadata_sources(root))
    literals = _replacement_literals(sources)
    lines = [f"literal:{literal}==>{REDACTION}\n" for literal in sorted(literals)]
    payload = "".join(lines).encode("utf-8", errors="surrogateescape")

    descriptor = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "wb", closefd=False) as destination:
            destination.write(payload)
    finally:
        os.close(descriptor)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--tree", action="store_true", help="scan the tracked tree")
    mode.add_argument("--history", action="store_true", help="scan reachable history")
    mode.add_argument("--all", action="store_true", help="scan tree and history")
    parser.add_argument(
        "--write-replacements",
        metavar="PATH",
        type=Path,
        help="write exact rewrite literals to a private path outside the repository",
    )
    return parser


def main(argv: list[str] | None = None, *, root: Path | None = None) -> int:
    parser = _parser()
    arguments = parser.parse_args(argv)
    if not any(
        (
            arguments.tree,
            arguments.history,
            arguments.all,
            arguments.write_replacements is not None,
        )
    ):
        parser.error("choose --tree, --history, --all, or --write-replacements")

    repository = (root or Path.cwd()).resolve()
    try:
        if arguments.write_replacements is not None:
            write_filter_repo_replacements(
                repository, arguments.write_replacements
            )
        findings: list[str] = []
        if arguments.tree or arguments.all:
            findings.extend(scan_tree(repository))
        if arguments.history or arguments.all:
            findings.extend(scan_history(repository))
    except Exception:
        print("error: repository audit could not complete safely", file=sys.stderr)
        return 2

    for finding in sorted(set(findings)):
        print(finding)
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
