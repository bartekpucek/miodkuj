import importlib.util
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = Path("skills/miodkuj")
BUNDLE = Path("dist/miodkuj.skill")
LEGACY_SLUG = "-".join(("stop", "slop", "PL"))
LEGACY_DISPLAY = " ".join(("Stop", "Slop", "PL"))
SPEC = importlib.util.spec_from_file_location(
    "validate_repo", ROOT / "scripts" / "validate_repo.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ValidateRepoTests(unittest.TestCase):
    def copy_repository(self, destination: Path) -> Path:
        copy = destination / "repo"
        shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git"))
        return copy

    def test_current_repository_passes(self):
        self.assertEqual(MODULE.validate_repo(ROOT), [])

    def test_reference_drift_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            target = copy / SKILL / "references" / "examples.md"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("drift\n", encoding="utf-8")

            errors = MODULE.validate_repo(copy)

            self.assertTrue(any("reference drift" in error for error in errors), errors)

    def test_missing_runtime_file_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            (copy / SKILL / "SKILL.md").unlink(missing_ok=True)

            errors = MODULE.validate_repo(copy)

            self.assertIn(f"missing runtime file: {SKILL / 'SKILL.md'}", errors)

    def test_obsolete_plugin_manifest_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            manifest = copy / ".claude-plugin" / "plugin.json"
            manifest.parent.mkdir(parents=True, exist_ok=True)
            manifest.write_text("{}", encoding="utf-8")

            errors = MODULE.validate_repo(copy)

            self.assertIn("obsolete plugin manifest: .claude-plugin/plugin.json", errors)

    def test_platform_specific_runtime_copy_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            duplicate = copy / "skills" / "claude" / "miodkuj" / "SKILL.md"
            duplicate.parent.mkdir(parents=True, exist_ok=True)
            duplicate.write_text("# Miodkuj\n", encoding="utf-8")

            errors = MODULE.validate_repo(copy)

            self.assertIn("platform-specific runtime copy: skills/claude", errors)

    def test_legacy_identifier_in_path_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            path = copy / "docs" / f"{LEGACY_SLUG}.md"
            path.write_text("# Migrated\n", encoding="utf-8")

            errors = MODULE.validate_repo(copy)

            self.assertIn(f"legacy identifier in path: docs/{LEGACY_SLUG}.md", errors)

    def test_legacy_display_name_in_text_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            target = copy / "docs" / "identity.md"
            target.write_text(f"# Miodkuj\n\n{LEGACY_DISPLAY}\n", encoding="utf-8")

            errors = MODULE.validate_repo(copy)

            self.assertIn("legacy display name in text: docs/identity.md", errors)

    def test_missing_release_changelog_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            (copy / "CHANGELOG.md").write_text("# Changelog\n", encoding="utf-8")

            errors = MODULE.validate_repo(copy)

            self.assertIn("changelog missing version 2.0.0", errors)

    def test_invalid_codex_metadata_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            metadata = copy / SKILL / "agents" / "openai.yaml"
            metadata.parent.mkdir(parents=True, exist_ok=True)
            metadata.write_text(
                'interface:\n  display_name: "Miodkuj"\n  default_prompt: "Edit."\n',
                encoding="utf-8",
            )

            errors = MODULE.validate_repo(copy)

            self.assertIn("Codex default_prompt must mention $miodkuj", errors)

    def test_missing_bundle_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            (copy / BUNDLE).unlink(missing_ok=True)

            errors = MODULE.validate_repo(copy)

            self.assertIn(f"missing {BUNDLE}", errors)

    def test_corrupt_bundle_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            bundle = copy / BUNDLE
            bundle.parent.mkdir(parents=True, exist_ok=True)
            bundle.write_bytes(b"not a zip archive")

            errors = MODULE.validate_repo(copy)

            self.assertTrue(any("invalid skill bundle" in error for error in errors), errors)

    def test_bundle_with_wrong_root_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            bundle = copy / BUNDLE
            bundle.parent.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(bundle, "w") as archive:
                archive.writestr("wrong-root/SKILL.md", "# Miodkuj\n")

            errors = MODULE.validate_repo(copy)

            self.assertIn("built skill artifact differs from skills/miodkuj", errors)

    def test_bundle_with_drifted_content_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            bundle = copy / BUNDLE
            bundle.parent.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(bundle, "w") as archive:
                archive.writestr("miodkuj/SKILL.md", "# Altered\n")

            errors = MODULE.validate_repo(copy)

            self.assertIn("built skill artifact differs from skills/miodkuj", errors)


if __name__ == "__main__":
    unittest.main()
