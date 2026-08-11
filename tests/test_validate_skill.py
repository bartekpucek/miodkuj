import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_skill", ROOT / "scripts" / "validate_skill.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ValidateSkillTests(unittest.TestCase):
    def write_skill(self, root: Path, description: str) -> Path:
        skill = root / "miodkuj"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            f"---\nname: miodkuj\ndescription: {description}\n---\n\n# Miodkuj\n",
            encoding="utf-8",
        )
        return skill

    def validate_silently(self, skill: Path) -> bool:
        with redirect_stdout(io.StringIO()):
            return MODULE.validate(skill)

    def test_portable_description_allows_200_characters(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = self.write_skill(Path(tmp), "x" * 200)

            self.assertTrue(self.validate_silently(skill))

    def test_portable_description_rejects_201_characters(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = self.write_skill(Path(tmp), "x" * 201)

            self.assertFalse(self.validate_silently(skill))


if __name__ == "__main__":
    unittest.main()
