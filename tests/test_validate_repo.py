import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = Path("plugins/miodkuj/skills/miodkuj")
CODEX_PLUGIN = Path("plugins/miodkuj/.codex-plugin/plugin.json")
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

    def test_internal_planning_tree_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            internal = copy / "docs" / ("super" + "powers") / "plan.md"
            internal.parent.mkdir(parents=True, exist_ok=True)
            internal.write_text("internal\n", encoding="utf-8")
            subprocess.run(["git", "init", "-q"], cwd=copy, check=True)
            subprocess.run(["git", "add", "."], cwd=copy, check=True)

            errors = MODULE.validate_repo(copy)

            self.assertTrue(any("internal path" in error for error in errors), errors)

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

    def test_missing_claude_marketplace_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            (copy / ".claude-plugin" / "marketplace.json").unlink()

            errors = MODULE.validate_repo(copy)

            self.assertIn(
                "missing installation manifest: .claude-plugin/marketplace.json",
                errors,
            )

    def test_manifest_version_drift_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            path = copy / CODEX_PLUGIN
            manifest = json.loads(path.read_text(encoding="utf-8"))
            manifest["version"] = "9.9.9"
            path.write_text(json.dumps(manifest), encoding="utf-8")

            errors = MODULE.validate_repo(copy)

            self.assertIn(
                f"installation manifest version drift: {CODEX_PLUGIN}",
                errors,
            )

    def test_claude_plugin_skill_path_drift_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            path = copy / ".claude-plugin" / "plugin.json"
            manifest = json.loads(path.read_text(encoding="utf-8"))
            manifest["skills"] = ["./skills/retired"]
            path.write_text(json.dumps(manifest), encoding="utf-8")

            errors = MODULE.validate_repo(copy)

            self.assertIn(
                "installation manifest contract drift: .claude-plugin/plugin.json: skills",
                errors,
            )

    def test_claude_marketplace_source_drift_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            path = copy / ".claude-plugin" / "marketplace.json"
            manifest = json.loads(path.read_text(encoding="utf-8"))
            manifest["plugins"][0]["source"] = "./retired"
            path.write_text(json.dumps(manifest), encoding="utf-8")

            errors = MODULE.validate_repo(copy)

            self.assertIn(
                "installation manifest contract drift: .claude-plugin/marketplace.json: "
                "plugins[0].source",
                errors,
            )

    def test_codex_plugin_skill_path_drift_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            path = copy / CODEX_PLUGIN
            manifest = json.loads(path.read_text(encoding="utf-8"))
            manifest["skills"] = "./retired/"
            path.write_text(json.dumps(manifest), encoding="utf-8")

            errors = MODULE.validate_repo(copy)

            self.assertIn(
                f"installation manifest contract drift: {CODEX_PLUGIN}: skills",
                errors,
            )

    def test_codex_marketplace_source_drift_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            path = copy / ".agents" / "plugins" / "marketplace.json"
            manifest = json.loads(path.read_text(encoding="utf-8"))
            manifest["plugins"][0]["source"]["path"] = "./retired"
            path.write_text(json.dumps(manifest), encoding="utf-8")

            errors = MODULE.validate_repo(copy)

            self.assertIn(
                "installation manifest contract drift: .agents/plugins/marketplace.json: "
                "plugins[0].source",
                errors,
            )

    def test_codex_marketplace_policy_drift_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            path = copy / ".agents" / "plugins" / "marketplace.json"
            manifest = json.loads(path.read_text(encoding="utf-8"))
            manifest["plugins"][0]["policy"]["installation"] = "DISABLED"
            path.write_text(json.dumps(manifest), encoding="utf-8")

            errors = MODULE.validate_repo(copy)

            self.assertIn(
                "installation manifest contract drift: .agents/plugins/marketplace.json: "
                "plugins[0].policy",
                errors,
            )

    def test_invalid_installation_manifest_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            path = copy / CODEX_PLUGIN
            path.write_text("not JSON", encoding="utf-8")

            errors = MODULE.validate_repo(copy)

            self.assertTrue(
                any(
                    error.startswith("invalid installation manifest: ")
                    and f"{CODEX_PLUGIN}:" in error
                    for error in errors
                ),
                errors,
            )

    def test_unexpected_skill_bundle_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            extra = copy / "dist" / "retired.skill"
            extra.write_bytes(b"obsolete")

            errors = MODULE.validate_repo(copy)

            self.assertIn("unexpected distribution artifact: dist/retired.skill", errors)

    def test_platform_specific_runtime_copy_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            duplicate = copy / "skills" / "miodkuj" / "SKILL.md"
            duplicate.parent.mkdir(parents=True, exist_ok=True)
            duplicate.write_text("# Miodkuj\n", encoding="utf-8")

            errors = MODULE.validate_repo(copy)

            self.assertIn("unexpected runtime folder: skills/miodkuj", errors)

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

    def test_lowercase_legacy_identifier_in_path_and_text_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            lowercase_slug = LEGACY_SLUG.casefold()
            target = copy / "docs" / f"{lowercase_slug}.md"
            target.write_text(LEGACY_DISPLAY.casefold(), encoding="utf-8")

            errors = MODULE.validate_repo(copy)

            self.assertIn(
                f"legacy identifier in path: docs/{lowercase_slug}.md", errors
            )
            self.assertIn(
                f"legacy display name in text: docs/{lowercase_slug}.md", errors
            )

    def test_tracked_internal_planning_file_is_scanned(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            internal_directory = "." + "super" + "powers"
            target = root / internal_directory / "tracked.md"
            target.parent.mkdir(parents=True)
            target.write_text(LEGACY_DISPLAY, encoding="utf-8")
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(
                ["git", "add", target.relative_to(root).as_posix()],
                cwd=root,
                check=True,
            )

            errors = []
            MODULE.validate_identity(root, errors)

            self.assertIn(
                f"legacy display name in text: {internal_directory}/tracked.md", errors
            )

    def test_internal_planning_artifact_is_scanned_without_git(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            internal_directory = "." + "super" + "powers"
            workflow_directory = "s" + "dd"
            target = copy / internal_directory / workflow_directory / "review.diff"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(LEGACY_DISPLAY, encoding="utf-8")

            errors = MODULE.validate_repo(copy)

            self.assertIn(
                "legacy display name in text: "
                f"{internal_directory}/{workflow_directory}/review.diff",
                errors,
            )

    def test_utf8_decodable_binary_content_is_not_scanned(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            target = copy / "docs" / "binary.dat"
            target.write_bytes(b"\x00" + LEGACY_DISPLAY.encode("utf-8"))

            errors = MODULE.validate_repo(copy)

            self.assertNotIn("legacy display name in text: docs/binary.dat", errors)

    def test_missing_release_changelog_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            (copy / "CHANGELOG.md").write_text("# Changelog\n", encoding="utf-8")

            errors = MODULE.validate_repo(copy)

            self.assertIn("changelog missing version 2.1.1", errors)

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

            self.assertIn(
                "Codex interface.default_prompt must exactly invoke $miodkuj with the approved prompt",
                errors,
            )

    def test_misnested_codex_metadata_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            metadata = copy / SKILL / "agents" / "openai.yaml"
            metadata.write_text(
                'interface:\n  display_name: "Miodkuj"\n'
                '  short_description: "Polszczyzna bez sztucznego tonu"\n'
                'default_prompt: "Use $miodkuj"\n'
                "policy:\n  allow_implicit_invocation: true\n",
                encoding="utf-8",
            )

            errors = MODULE.validate_repo(copy)

            self.assertTrue(
                any("invalid Codex metadata" in error for error in errors), errors
            )

    def test_duplicate_codex_metadata_key_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            metadata = copy / SKILL / "agents" / "openai.yaml"
            contents = metadata.read_text(encoding="utf-8")
            metadata.write_text(
                contents.replace(
                    '  display_name: "Miodkuj"\n',
                    '  display_name: "Miodkuj"\n  display_name: "Miodkuj"\n',
                ),
                encoding="utf-8",
            )

            errors = MODULE.validate_repo(copy)

            self.assertIn(
                "invalid Codex metadata: duplicate key interface.display_name", errors
            )

    def test_implicit_invocation_requires_boolean_true(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            metadata = copy / SKILL / "agents" / "openai.yaml"
            metadata.write_text(
                metadata.read_text(encoding="utf-8").replace(
                    "allow_implicit_invocation: true",
                    'allow_implicit_invocation: "true"',
                ),
                encoding="utf-8",
            )

            errors = MODULE.validate_repo(copy)

            self.assertIn(
                "Codex policy.allow_implicit_invocation must be boolean true", errors
            )

    def test_unknown_malformed_codex_metadata_key_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            metadata = copy / SKILL / "agents" / "openai.yaml"
            metadata.write_text(
                metadata.read_text(encoding="utf-8").replace(
                    "policy:\n", "  malformed: [\npolicy:\n"
                ),
                encoding="utf-8",
            )

            errors = MODULE.validate_repo(copy)

            self.assertIn(
                "invalid Codex metadata: unsupported key interface.malformed", errors
            )

    def test_unsupported_codex_metadata_scalar_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            metadata = copy / SKILL / "agents" / "openai.yaml"
            metadata.write_text(
                metadata.read_text(encoding="utf-8").replace(
                    'display_name: "Miodkuj"', "display_name: ["
                ),
                encoding="utf-8",
            )

            errors = MODULE.validate_repo(copy)

            self.assertTrue(
                any("unsupported scalar syntax" in error for error in errors), errors
            )

    def test_unknown_codex_metadata_section_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            metadata = copy / SKILL / "agents" / "openai.yaml"
            metadata.write_text(
                metadata.read_text(encoding="utf-8")
                + 'unknown:\n  value: "not allowed"\n',
                encoding="utf-8",
            )

            errors = MODULE.validate_repo(copy)

            self.assertIn(
                "invalid Codex metadata: unsupported top-level key unknown", errors
            )

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

            self.assertIn(f"built skill artifact differs from {SKILL}", errors)

    def test_bundle_with_drifted_content_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = self.copy_repository(Path(tmp))
            bundle = copy / BUNDLE
            bundle.parent.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(bundle, "w") as archive:
                archive.writestr("miodkuj/SKILL.md", "# Altered\n")

            errors = MODULE.validate_repo(copy)

            self.assertIn(f"built skill artifact differs from {SKILL}", errors)


if __name__ == "__main__":
    unittest.main()
