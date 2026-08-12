import importlib.util
import io
import stat
import subprocess
import sys
import tempfile
import unittest
import zipfile
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_public_repo.py"
SPEC = importlib.util.spec_from_file_location("audit_public_repo", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

INTERNAL_ACRONYM = "".join(("T", "T", "C"))
INTERNAL_NAME = " ".join(("Target", "Creators"))
INTERNAL_PATH = "." + "super" + "powers"
INTERNAL_PATHS = (
    INTERNAL_PATH + "/notes.md",
    "/".join(("docs", "super" + "powers", "notes.md")),
    "/".join(("notes", "s" + "dd", "notes.md")),
    "/".join(("review" + "-" + "package", "notes.md")),
)
PRIVATE_EMAIL = "private" + "@" + "example.invalid"
LOCAL_USER = "example" + "-" + "person"
LOCAL_PATH = "/" + "/".join(("Users", LOCAL_USER, "private-project"))
LINUX_PATH = "/" + "/".join(("home", LOCAL_USER, "private-project"))
WINDOWS_PATH = "C:" + "\\" + "\\".join(("Users", LOCAL_USER, "private-project"))
PUBLIC_EMAIL = "65296954+bartekpucek" + "@" + "users.noreply.github.com"


class PublicRepoAuditTests(unittest.TestCase):
    def init_repo(self, root: Path) -> None:
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(
            ["git", "config", "user.name", "Public Author"],
            cwd=root,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.email", PUBLIC_EMAIL],
            cwd=root,
            check=True,
        )

    def commit_all(self, root: Path, message: str = "fixture") -> str:
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", message], cwd=root, check=True)
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

    def write_archive(self, root: Path, name: str, contents: bytes) -> Path:
        archive = root / "dist" / name
        archive.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
            bundle.writestr("miodkuj/references/private.md", contents)
        return archive

    def test_tree_scan_catches_tracked_internal_planning_path(self):
        """Catches scanners that inspect contents but skip tracked path names."""
        for internal_path in INTERNAL_PATHS:
            with self.subTest(internal_path=Path(internal_path).name):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    target = root / internal_path
                    target.parent.mkdir(parents=True)
                    target.write_text("public\n", encoding="utf-8")
                    self.init_repo(root)
                    subprocess.run(["git", "add", "."], cwd=root, check=True)

                    findings = MODULE.scan_tree(root)
                    rendered = "\n".join(findings)

                    self.assertIn("internal path", rendered)
                    self.assertNotIn(internal_path, rendered)

    def test_tree_scan_catches_absolute_home_path_without_disclosing_it(self):
        """Catches missing tracked-file scans and unredacted finding output."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(LOCAL_PATH, encoding="utf-8")
            self.init_repo(root)
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            blob = subprocess.run(
                ["git", "rev-parse", ":README.md"],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()

            findings = MODULE.scan_tree(root)
            rendered = "\n".join(findings)

            self.assertIn("absolute home path", rendered)
            self.assertIn(blob, rendered)
            self.assertNotIn(LOCAL_PATH, rendered)
            self.assertNotIn(LOCAL_USER, rendered)

    def test_scan_bytes_catches_each_absolute_home_style_without_disclosure(self):
        """Catches a regex that supports only one operating-system home style."""
        for local_path in (LOCAL_PATH, LINUX_PATH, WINDOWS_PATH):
            with self.subTest(local_path=local_path[:2]):
                findings = MODULE.scan_bytes("README.md", local_path.encode())
                rendered = "\n".join(findings)

                self.assertIn("absolute home path", rendered)
                self.assertNotIn(local_path, rendered)
                self.assertNotIn(LOCAL_USER, rendered)

    def test_scan_bytes_catches_internal_organization_identifiers(self):
        """Catches an identifier rule that protects only one internal spelling."""
        for identifier in (INTERNAL_ACRONYM, INTERNAL_NAME):
            with self.subTest(length=len(identifier)):
                findings = MODULE.scan_bytes("README.md", identifier.encode())
                rendered = "\n".join(findings)

                self.assertIn("internal identifier", rendered)
                self.assertNotIn(identifier, rendered)

    def test_history_scan_catches_removed_private_email_metadata(self):
        """Catches history scans that inspect blobs but omit commit metadata."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            (root / "README.md").write_text("private fixture\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.email=" + PRIVATE_EMAIL,
                    "commit",
                    "-qm",
                    "private fixture",
                ],
                cwd=root,
                check=True,
            )
            commit = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()

            findings = MODULE.scan_history(root)
            rendered = "\n".join(findings)

            self.assertIn("private email metadata", rendered)
            self.assertIn(commit, rendered)
            self.assertNotIn(PRIVATE_EMAIL, rendered)

    def test_history_scan_catches_internal_identifier_in_removed_blob(self):
        """Catches history scans that inspect only the current tracked tree."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            (root / "README.md").write_text(INTERNAL_ACRONYM, encoding="utf-8")
            self.commit_all(root, "private fixture")
            private_blob = subprocess.run(
                ["git", "rev-parse", "HEAD:README.md"],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            (root / "README.md").write_text("public\n", encoding="utf-8")
            subprocess.run(
                ["git", "commit", "-am", "public", "-q"],
                cwd=root,
                check=True,
            )

            findings = MODULE.scan_history(root)
            rendered = "\n".join(findings)

            self.assertIn("internal identifier", rendered)
            self.assertIn(private_blob, rendered)
            self.assertIn("README.md", rendered)
            self.assertNotIn(INTERNAL_ACRONYM, rendered)

    def test_tree_scan_reads_packaged_secret_like_text_from_miodkuj_archive(self):
        """Catches scanners that skip the generated sole-runtime archive."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            archive = self.write_archive(
                root, "miodkuj.skill", INTERNAL_ACRONYM.encode()
            )
            blob = subprocess.run(
                ["git", "hash-object", str(archive)],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()

            findings = MODULE.scan_tree(root)
            rendered = "\n".join(findings)

            self.assertIn("internal identifier", rendered)
            self.assertIn("dist/miodkuj.skill", rendered)
            self.assertIn(blob, rendered)
            self.assertNotIn(INTERNAL_ACRONYM, rendered)

    def test_history_scan_reads_removed_packaged_secret_like_text(self):
        """Catches history scans that treat compressed archive blobs as plain text."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            archive = self.write_archive(
                root, "miodkuj.skill", INTERNAL_ACRONYM.encode()
            )
            self.commit_all(root, "private archive")
            blob = subprocess.run(
                ["git", "rev-parse", "HEAD:dist/miodkuj.skill"],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            archive.unlink()
            subprocess.run(["git", "add", "-u"], cwd=root, check=True)
            subprocess.run(
                ["git", "commit", "-qm", "remove private archive"],
                cwd=root,
                check=True,
            )

            findings = MODULE.scan_history(root)
            rendered = "\n".join(findings)

            self.assertIn("internal identifier", rendered)
            self.assertIn(blob, rendered)
            self.assertIn("dist/miodkuj.skill", rendered)
            self.assertNotIn(INTERNAL_ACRONYM, rendered)

    def test_history_preserves_every_special_path_for_one_archive_blob(self):
        """Catches quoted-path parsing and blob-only association deduplication."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            first = self.write_archive(
                root, "zażółć [one].skill", INTERNAL_ACRONYM.encode()
            )
            second = root / "dist" / "zażółć [two].skill"
            second.write_bytes(first.read_bytes())
            self.commit_all(root, "private archive paths")
            blob = subprocess.run(
                ["git", "rev-parse", "HEAD:" + first.relative_to(root).as_posix()],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            first.unlink()
            second.unlink()
            subprocess.run(["git", "add", "-u"], cwd=root, check=True)
            subprocess.run(
                ["git", "commit", "-qm", "remove archive paths"],
                cwd=root,
                check=True,
            )

            findings = MODULE.scan_history(root)
            matching = [
                item
                for item in findings
                if "internal identifier" in item and blob in item
            ]
            rendered = "\n".join(matching)

            self.assertIn(first.relative_to(root).as_posix(), rendered)
            self.assertIn(second.relative_to(root).as_posix(), rendered)
            self.assertEqual(len(matching), 2, matching)
            self.assertNotIn(INTERNAL_ACRONYM, rendered)

    def test_tree_scan_rejects_unexpected_skill_artifact(self):
        """Catches archive allow lists that accept arbitrary dist bundles."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            archive = self.write_archive(root, "legacy.skill", b"public")
            blob = subprocess.run(
                ["git", "hash-object", str(archive)],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()

            findings = MODULE.scan_tree(root)
            rendered = "\n".join(findings)

            self.assertIn("unexpected skill artifact", rendered)
            self.assertIn(blob, rendered)

    def test_tree_scan_fails_closed_when_expected_archive_cannot_be_read(self):
        """Catches generated archive read errors being silently skipped."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            archive = root / "dist" / "miodkuj.skill"
            archive.mkdir(parents=True)

            with self.assertRaises(MODULE.AuditError):
                MODULE.scan_tree(root)

    def test_history_scans_annotated_tag_identity_metadata_and_message(self):
        """Catches history scans that discard reachable annotated tag objects."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            (root / "README.md").write_text("public\n", encoding="utf-8")
            self.commit_all(root, "public fixture")
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.name=" + INTERNAL_NAME,
                    "-c",
                    "user.email=" + PRIVATE_EMAIL,
                    "tag",
                    "-am",
                    LOCAL_PATH,
                    "private-tag",
                ],
                cwd=root,
                check=True,
            )
            tag_object = subprocess.run(
                ["git", "rev-parse", "private-tag^{tag}"],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()

            findings = MODULE.scan_history(root)
            matching = [item for item in findings if tag_object in item]
            rendered = "\n".join(matching)

            self.assertIn("private email metadata", rendered)
            self.assertIn("internal identifier", rendered)
            self.assertIn("absolute home path", rendered)
            self.assertNotIn(PRIVATE_EMAIL, rendered)
            self.assertNotIn(INTERNAL_NAME, rendered)
            self.assertNotIn(LOCAL_PATH, rendered)
            self.assertNotIn(LOCAL_USER, rendered)

    def test_cli_redacts_unexpected_archive_exception_without_traceback(self):
        """Catches archive exceptions escaping the generic CLI error boundary."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            self.write_archive(root, "miodkuj.skill", b"public")
            stdout = io.StringIO()
            stderr = io.StringIO()

            try:
                with mock.patch.object(
                    MODULE.zipfile,
                    "ZipFile",
                    side_effect=LookupError(LOCAL_PATH),
                ):
                    with redirect_stdout(stdout), redirect_stderr(stderr):
                        result = MODULE.main(["--tree"], root=root)
            except Exception as exc:
                self.fail(type(exc).__name__ + " escaped the CLI boundary")

            rendered = stdout.getvalue() + stderr.getvalue()

            self.assertEqual(result, 2)
            self.assertEqual(
                stderr.getvalue(),
                "error: repository audit could not complete safely\n",
            )
            self.assertEqual(stdout.getvalue(), "")
            self.assertNotIn("Traceback", rendered)
            self.assertNotIn(str(root), rendered)
            self.assertNotIn(LOCAL_PATH, rendered)
            self.assertNotIn(LOCAL_USER, rendered)

    def test_public_attribution_is_allowed(self):
        """Catches over-broad identity and email rules that block attribution."""
        text = (
            "Bartek Pucek https://github.com/bartekpucek/miodkuj " + PUBLIC_EMAIL
        ).encode()

        self.assertEqual(MODULE.scan_bytes("LICENSE", text), [])

    def test_generic_polish_business_words_are_allowed(self):
        """Catches an over-broad heuristic that suppresses ordinary Polish."""
        text = " ".join(("klient", "zespół", "firma")).encode()

        self.assertEqual(MODULE.scan_bytes("README.md", text), [])

    def test_scanner_and_privacy_tests_do_not_trigger_their_own_rules(self):
        """Catches forbidden fixture literals accidentally shipped by the gate."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            source_files = (
                Path("scripts") / SCRIPT.name,
                Path("tests") / Path(__file__).name,
            )
            for relative in source_files:
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                source = SCRIPT if relative.parts[0] == "scripts" else Path(__file__)
                target.write_bytes(source.read_bytes())
            subprocess.run(["git", "add", "."], cwd=root, check=True)

            findings = MODULE.scan_tree(root)

            self.assertEqual(findings, [])

    def test_replacements_are_exact_and_written_outside_repo_with_private_mode(self):
        """Catches regex exports, in-repository secret files, and loose permissions."""
        with tempfile.TemporaryDirectory() as tmp:
            outer = Path(tmp)
            root = outer / "repo"
            root.mkdir()
            self.init_repo(root)
            (root / "README.md").write_text(
                INTERNAL_ACRONYM + " " + LOCAL_PATH,
                encoding="utf-8",
            )
            internal_file = root / INTERNAL_PATH / "notes.md"
            internal_file.parent.mkdir()
            internal_file.write_text("public\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.email=" + PRIVATE_EMAIL,
                    "commit",
                    "-qm",
                    "private fixture",
                ],
                cwd=root,
                check=True,
            )
            output = outer / "private-replacements.txt"

            MODULE.write_filter_repo_replacements(root, output)

            lines = output.read_text(encoding="utf-8").splitlines()
            expected = {
                "literal:" + INTERNAL_ACRONYM + "==>[REDACTED]",
                "literal:" + INTERNAL_PATH + "/notes.md==>[REDACTED]",
                "literal:" + LOCAL_PATH + "==>[REDACTED]",
                "literal:" + PRIVATE_EMAIL + "==>[REDACTED]",
            }
            self.assertEqual(set(lines), expected)
            self.assertEqual(stat.S_IMODE(output.stat().st_mode), 0o600)

    def test_replacements_reject_output_inside_repository(self):
        """Catches accidental publication of the exact replacement literals."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            output = root / "private-replacements.txt"

            with self.assertRaises(ValueError):
                MODULE.write_filter_repo_replacements(root, output)

            self.assertFalse(output.exists())

    def test_tree_cli_returns_failure_and_prints_only_redacted_findings(self):
        """Catches a CLI that reports success or prints the matched secret."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            (root / "README.md").write_text(LOCAL_PATH, encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)

            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--tree"],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 1, result)
            self.assertIn("absolute home path", result.stdout)
            self.assertNotIn(LOCAL_PATH, result.stdout + result.stderr)
            self.assertNotIn(LOCAL_USER, result.stdout + result.stderr)

    def test_all_cli_accepts_a_clean_repository(self):
        """Catches an --all mode that omits or misroutes one scan mode."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            (root / "README.md").write_text("public\n", encoding="utf-8")
            self.commit_all(root, "public fixture")

            with redirect_stdout(io.StringIO()) as stdout:
                result = MODULE.main(["--all"], root=root)

            self.assertEqual(result, 0, stdout.getvalue())
            self.assertEqual(stdout.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
