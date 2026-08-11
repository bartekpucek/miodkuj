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
    def test_current_repository_passes(self):
        self.assertEqual(MODULE.validate_repo(ROOT), [])

    def test_reference_drift_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "repo"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git"))
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


if __name__ == "__main__":
    unittest.main()
