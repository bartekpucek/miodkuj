import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
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
            target = (
                copy
                / "skills"
                / "codex"
                / "stop-slop-pl"
                / "references"
                / "examples.md"
            )
            target.write_text(
                target.read_text(encoding="utf-8") + "\ndrift\n", encoding="utf-8"
            )
            errors = MODULE.validate_repo(copy)
            self.assertTrue(
                any("reference drift" in error for error in errors), errors
            )

    def test_malformed_manifest_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            (copy / ".claude-plugin/plugin.json").write_text("{", encoding="utf-8")

            errors = MODULE.validate_repo(copy)

            self.assertTrue(any("invalid JSON" in error for error in errors), errors)

    def test_missing_manifest_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            (copy / ".claude-plugin/plugin.json").unlink()

            errors = MODULE.validate_repo(copy)

            self.assertTrue(any("missing manifest" in error for error in errors), errors)

    def test_invalid_manifest_structure_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            (copy / ".claude-plugin/marketplace.json").write_text(
                "{}", encoding="utf-8"
            )

            errors = MODULE.validate_repo(copy)

            self.assertTrue(
                any("invalid manifest structure" in error for error in errors), errors
            )

    def test_missing_bundle_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            (copy / "dist/stop-slop-pl.skill").unlink()

            errors = MODULE.validate_repo(copy)

            self.assertIn("missing dist/stop-slop-pl.skill", errors)

    def test_corrupt_bundle_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            (copy / "dist/stop-slop-pl.skill").write_bytes(b"not a zip archive")

            errors = MODULE.validate_repo(copy)

            self.assertTrue(any("invalid skill bundle" in error for error in errors), errors)

    def test_version_mismatch_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            marketplace = copy / ".claude-plugin/marketplace.json"
            marketplace.write_text(
                marketplace.read_text(encoding="utf-8").replace(
                    '"version": "1.1.0"', '"version": "9.9.9"', 1
                ),
                encoding="utf-8",
            )

            errors = MODULE.validate_repo(copy)

            self.assertTrue(any("version mismatch" in error for error in errors), errors)

    def test_invalid_codex_metadata_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            metadata = copy / "skills/codex/stop-slop-pl/agents/openai.yaml"
            metadata.write_text(
                metadata.read_text(encoding="utf-8").replace("$stop-slop-pl", "skill"),
                encoding="utf-8",
            )

            errors = MODULE.validate_repo(copy)

            self.assertIn("Codex default_prompt must mention $stop-slop-pl", errors)


if __name__ == "__main__":
    unittest.main()
