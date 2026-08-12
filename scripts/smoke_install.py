#!/usr/bin/env python3
"""Smoke-test Miodkuj installation without touching user configuration."""

import argparse
import os
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path
from typing import Sequence


EXPECTED_BUNDLE_ENTRIES = frozenset(
    {
        "miodkuj/SKILL.md",
        "miodkuj/agents/openai.yaml",
        "miodkuj/references/eval.md",
        "miodkuj/references/examples.md",
        "miodkuj/references/plain-polish.md",
        "miodkuj/references/polish-patterns.md",
        "miodkuj/references/registers.md",
        "miodkuj/references/voice-calibration.md",
    }
)
RUNTIME = Path("plugins/miodkuj/skills/miodkuj")


def isolated_environment(home: Path) -> dict[str, str]:
    """Return a process environment rooted in an isolated temporary home."""
    (home / ".claude").mkdir(parents=True, exist_ok=True)
    (home / ".codex").mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update(
        HOME=str(home),
        CLAUDE_CONFIG_DIR=str(home / ".claude"),
        CODEX_HOME=str(home / ".codex"),
    )
    return env


def claude_commands(repo: Path) -> list[list[str]]:
    """Return the native Claude Code local-marketplace installation plan."""
    return [
        ["claude", "plugin", "validate", str(repo)],
        ["claude", "plugin", "marketplace", "add", str(repo)],
        ["claude", "plugin", "install", "miodkuj@miodkuj"],
    ]


def codex_commands(repo: Path) -> list[list[str]]:
    """Return the native Codex local-marketplace installation plan."""
    return [
        ["codex", "plugin", "marketplace", "add", str(repo), "--json"],
        ["codex", "plugin", "add", "miodkuj@miodkuj", "--json"],
    ]


def verify_bundle(bundle: Path, runtime: Path | None = None) -> None:
    """Require exactly eight unique canonical file records and their contents."""
    with zipfile.ZipFile(bundle) as archive:
        records = archive.infolist()
        directory_entries = sorted(
            info.filename for info in records if info.is_dir()
        )
        if directory_entries:
            raise RuntimeError(
                "skill bundle must not contain directory entries; "
                f"found {directory_entries}"
            )
        names = [info.filename for info in records]
        duplicate_names = sorted(
            {name for name in names if names.count(name) > 1}
        )
        if duplicate_names:
            raise RuntimeError(
                "skill bundle must not contain a duplicate ZIP record; "
                f"found {duplicate_names}"
            )
        if len(records) != len(EXPECTED_BUNDLE_ENTRIES):
            raise RuntimeError(
                "skill bundle must contain exactly eight ZIP records; "
                f"found {len(records)}: {sorted(names)}"
            )
        if set(names) != EXPECTED_BUNDLE_ENTRIES:
            raise RuntimeError(
                "skill bundle must contain the exact canonical record names; "
                f"found {sorted(names)}"
            )
        if runtime is not None:
            for record in records:
                relative = Path(record.filename).relative_to("miodkuj")
                if archive.read(record) != (runtime / relative).read_bytes():
                    raise RuntimeError(
                        f"skill bundle content differs: {record.filename}"
                    )


def verify_installed_cache(home: Path, platform: str) -> Path:
    """Require one cached Miodkuj runtime with the canonical frontmatter name."""
    cache = home / f".{platform}" / "plugins" / "cache"
    installed = sorted(cache.rglob("skills/miodkuj/SKILL.md")) if cache.is_dir() else []
    if len(installed) != 1:
        raise RuntimeError(
            f"expected exactly one installed {platform} cache skill; found {installed}"
        )
    contents = installed[0].read_text(encoding="utf-8")
    frontmatter = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", contents, re.DOTALL)
    if frontmatter is None or not re.search(
        r"(?m)^name:\s*miodkuj\s*$", frontmatter.group(1)
    ):
        raise RuntimeError(f"installed cache has the wrong skill name: {installed[0]}")
    return installed[0]


def _tree_bytes(root: Path) -> dict[Path, bytes]:
    return {
        path.relative_to(root): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def install_standalone(repo: Path, home: Path, platform: str) -> None:
    """Copy the canonical runtime into isolated standalone skill directories."""
    platforms = ("claude", "codex") if platform == "all" else (platform,)
    source = repo / RUNTIME
    expected = _tree_bytes(source)
    for target_platform in platforms:
        destination = home / f".{target_platform}" / "skills" / "miodkuj"
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, destination)
        if _tree_bytes(destination) != expected:
            raise RuntimeError(
                f"standalone {target_platform} skill differs from canonical runtime"
            )


def run_command(
    command: Sequence[str], cwd: Path, env: dict[str, str]
) -> subprocess.CompletedProcess[str]:
    """Run one smoke-test command and retain both output streams on failure."""
    try:
        return subprocess.run(
            list(command),
            cwd=cwd,
            env=env,
            text=True,
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError as error:
        rendered = " ".join(command)
        raise RuntimeError(
            f"command failed with exit code {error.returncode}: {rendered}\n"
            f"stdout:\n{error.stdout or ''}\n"
            f"stderr:\n{error.stderr or ''}"
        ) from error
    except OSError as error:
        rendered = " ".join(command)
        raise RuntimeError(f"could not run command: {rendered}: {error}") from error


def apply_tracked_worktree_snapshot(
    repo: Path, clone: Path, env: dict[str, str]
) -> None:
    """Reproduce tracked, uncommitted source changes in the temporary clone."""
    patch = run_command(["git", "diff", "--binary", "HEAD"], repo, env).stdout
    if not patch:
        return
    patch_path = clone / ".smoke-worktree.patch"
    patch_path.write_text(patch, encoding="utf-8")
    run_command(["git", "apply", "--index", str(patch_path)], clone, env)
    patch_path.unlink()
    run_command(
        [
            "git",
            "-c",
            "user.name=Miodkuj Smoke Test",
            "-c",
            "[REDACTED]",
            "commit",
            "-m",
            "test snapshot",
        ],
        clone,
        env,
    )


def smoke_install(
    repo: Path,
    platform: str,
    env: dict[str, str],
    *,
    structural_only: bool = False,
) -> None:
    """Verify native and standalone installs from an isolated clean clone."""
    if platform not in {"claude", "codex", "all"}:
        raise ValueError(f"unsupported platform: {platform}")

    with (
        tempfile.TemporaryDirectory(prefix="miodkuj-smoke-home-") as home_tmp,
        tempfile.TemporaryDirectory(prefix="miodkuj-smoke-clone-") as clone_tmp,
    ):
        home = Path(home_tmp)
        clone = Path(clone_tmp) / "repo"
        run_env = dict(env)
        isolated = isolated_environment(home)
        for key in ("HOME", "CLAUDE_CONFIG_DIR", "CODEX_HOME"):
            run_env[key] = isolated[key]

        run_command(
            ["git", "clone", "--no-local", str(repo.resolve()), str(clone)],
            Path(clone_tmp),
            run_env,
        )
        apply_tracked_worktree_snapshot(repo, clone, run_env)
        run_command(["bash", "scripts/build.sh"], clone, run_env)
        verify_bundle(clone / "dist" / "miodkuj.skill", clone / RUNTIME)

        if not structural_only:
            platforms = ("claude", "codex") if platform == "all" else (platform,)
            for target_platform in platforms:
                commands = (
                    claude_commands(clone)
                    if target_platform == "claude"
                    else codex_commands(clone)
                )
                for command in commands:
                    run_command(command, clone, run_env)
                verify_installed_cache(home, target_platform)

        install_standalone(clone, home, platform)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Test Miodkuj installation from a clean clone and temporary home."
    )
    parser.add_argument(
        "--platform", choices=("claude", "codex", "all"), default="all"
    )
    parser.add_argument(
        "--structural-only",
        action="store_true",
        help="check clone, standalone, and bundle contracts without host CLIs",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    try:
        smoke_install(
            root,
            args.platform,
            os.environ.copy(),
            structural_only=args.structural_only,
        )
    except (RuntimeError, ValueError, OSError, zipfile.BadZipFile) as error:
        print(f"error: {error}")
        return 1
    mode = "structural" if args.structural_only else "native"
    print(f"{mode} installation smoke test passed: {args.platform}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
