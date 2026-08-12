import importlib.util
import os
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "plugins" / "miodkuj" / "skills" / "miodkuj"
SPEC = importlib.util.spec_from_file_location(
    "smoke_install", ROOT / "scripts" / "smoke_install.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SmokeInstallTests(unittest.TestCase):
    def test_claude_command_plan_uses_local_marketplace(self):
        commands = MODULE.claude_commands(Path("/tmp/public-clone"))
        self.assertEqual(commands, [
            ["claude", "plugin", "validate", "/tmp/public-clone"],
            ["claude", "plugin", "marketplace", "add", "/tmp/public-clone"],
            ["claude", "plugin", "install", "miodkuj@miodkuj"],
        ])

    def test_codex_command_plan_uses_local_marketplace(self):
        commands = MODULE.codex_commands(Path("/tmp/public-clone"))
        self.assertEqual(commands, [
            ["codex", "plugin", "marketplace", "add", "/tmp/public-clone", "--json"],
            ["codex", "plugin", "add", "miodkuj@miodkuj", "--json"],
        ])

    def test_isolated_environment_does_not_inherit_user_plugin_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = MODULE.isolated_environment(Path(tmp))
        self.assertEqual(env["HOME"], tmp)
        self.assertEqual(env["CLAUDE_CONFIG_DIR"], str(Path(tmp) / ".claude"))
        self.assertEqual(env["CODEX_HOME"], str(Path(tmp) / ".codex"))

    def test_isolated_environment_prepares_cli_config_roots(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            MODULE.isolated_environment(home)

            self.assertTrue((home / ".claude").is_dir())
            self.assertTrue((home / ".codex").is_dir())

    def test_bundle_rejects_a_ninth_entry(self):
        entries = {
            "miodkuj/SKILL.md",
            "miodkuj/agents/openai.yaml",
            "miodkuj/references/eval.md",
            "miodkuj/references/examples.md",
            "miodkuj/references/plain-polish.md",
            "miodkuj/references/polish-patterns.md",
            "miodkuj/references/registers.md",
            "miodkuj/references/voice-calibration.md",
            "miodkuj/references/unexpected.md",
        }
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp) / "miodkuj.skill"
            with zipfile.ZipFile(bundle, "w") as archive:
                for entry in entries:
                    archive.writestr(entry, b"fixture")

            with self.assertRaisesRegex(RuntimeError, "exactly eight canonical entries"):
                MODULE.verify_bundle(bundle)

    def test_installed_cache_requires_one_named_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache = Path(tmp) / ".claude" / "plugins" / "cache"
            skill = cache / "miodkuj" / "miodkuj" / "2.1.0" / "skills" / "miodkuj" / "SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("---\nname: miodkuj\ndescription: Fixture\n---\n", encoding="utf-8")

            MODULE.verify_installed_cache(Path(tmp), "claude")

            duplicate = cache / "other" / "skills" / "miodkuj" / "SKILL.md"
            duplicate.parent.mkdir(parents=True)
            shutil.copy2(skill, duplicate)
            with self.assertRaisesRegex(RuntimeError, "exactly one installed"):
                MODULE.verify_installed_cache(Path(tmp), "claude")

    def test_standalone_copy_matches_canonical_runtime(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            MODULE.install_standalone(ROOT, home, "all")

            expected = {
                path.relative_to(RUNTIME): path.read_bytes()
                for path in RUNTIME.rglob("*")
                if path.is_file()
            }
            for platform in ("claude", "codex"):
                installed = home / f".{platform}" / "skills" / "miodkuj"
                actual = {
                    path.relative_to(installed): path.read_bytes()
                    for path in installed.rglob("*")
                    if path.is_file()
                }
                self.assertEqual(actual, expected)

    def test_command_failure_reports_captured_output(self):
        with self.assertRaises(RuntimeError) as caught:
            MODULE.run_command(
                [
                    sys.executable,
                    "-c",
                    "import sys; print('visible stdout'); "
                    "print('visible stderr', file=sys.stderr); sys.exit(7)",
                ],
                ROOT,
                os.environ.copy(),
            )

        message = str(caught.exception)
        self.assertIn("visible stdout", message)
        self.assertIn("visible stderr", message)
        self.assertIn("exit code 7", message)

    def test_structural_smoke_uses_a_clean_clone_without_native_clis(self):
        env = os.environ.copy()
        env["PATH"] = "/usr/bin:/bin"

        MODULE.smoke_install(ROOT, "all", env, structural_only=True)
