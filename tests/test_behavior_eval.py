import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "behavior_eval", ROOT / "scripts" / "behavior_eval.py"
)
behavior_eval = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(behavior_eval)


def source_text(case: dict) -> str:
    """The text a user pasted: everything after the instruction line."""
    return case["prompt"].split("\n", 1)[1]


class CaseFileTests(unittest.TestCase):
    def setUp(self):
        self.cases = behavior_eval.load_cases()

    def test_case_file_loads_with_unique_ids_and_known_checks(self):
        self.assertGreaterEqual(len(self.cases), 25)

    def test_every_kind_is_covered(self):
        self.assertEqual(
            {case["kind"] for case in self.cases}, behavior_eval.KINDS
        )

    def test_returning_the_input_unchanged_fails_every_slop_case(self):
        for case in self.cases:
            if case["kind"] in ("mixed", "must_change"):
                verdict, _ = behavior_eval.grade(case, source_text(case))
                self.assertEqual(verdict, "FAIL", case["id"])

    def test_returning_the_input_unchanged_passes_every_verbatim_case(self):
        for case in self.cases:
            if "equals" in case["checks"]:
                verdict, reasons = behavior_eval.grade(case, source_text(case))
                self.assertEqual(verdict, "PASS", (case["id"], reasons))

    def test_an_empty_response_passes_nothing(self):
        for case in self.cases:
            if case.get("manual"):
                continue
            needs_text = {"equals", "contains", "contains_ci"} & set(case["checks"])
            if needs_text:
                verdict, _ = behavior_eval.grade(case, "")
                self.assertEqual(verdict, "FAIL", case["id"])


class GradeTests(unittest.TestCase):
    def case(self, **checks):
        return {"id": "t", "kind": "clean", "prompt": "x\ny", "checks": checks}

    def test_verbatim_text_passes_and_a_synonym_swap_fails(self):
        case = self.case(equals="W ramach umowy producent wymienia baterię.")
        self.assertEqual(
            behavior_eval.grade(case, "W ramach umowy producent wymienia baterię.")[0],
            "PASS",
        )
        self.assertEqual(
            behavior_eval.grade(case, "Zgodnie z umową producent wymienia baterię.")[0],
            "FAIL",
        )

    def test_a_note_after_the_edit_does_not_break_a_verbatim_check(self):
        case = self.case(equals="Zdanie bez zmian.")
        response = "Zdanie bez zmian.\n\nUwaga: nic nie wymagało poprawy."
        self.assertEqual(behavior_eval.grade(case, response)[0], "PASS")

    def test_removed_wording_quoted_in_a_note_is_not_counted_as_present(self):
        case = self.case(excludes=["Warto zauważyć"])
        response = "Kupiono trzy serwery.\n\nUwaga: usunąłem „Warto zauważyć”."
        self.assertEqual(behavior_eval.grade(case, response)[0], "PASS")

    def test_note_after_a_multi_paragraph_edit_is_ignored_too(self):
        case = self.case(excludes=["ogromny potencjał"])
        case["scope"] = "full"
        response = (
            "Projekt ruszył 3 marca.\n\nZarząd zdecyduje 30 kwietnia.\n\n"
            "Uwaga: usunąłem zdanie „rozwiązanie ma ogromny potencjał”."
        )
        self.assertEqual(behavior_eval.grade(case, response)[0], "PASS")
        kept = "Projekt ruszył 3 marca.\n\nRozwiązanie ma ogromny potencjał."
        self.assertEqual(behavior_eval.grade(case, kept)[0], "FAIL")

    def test_wording_left_in_the_edit_fails(self):
        case = self.case(excludes_ci=["w dniu dzisiejszym"])
        verdict, reasons = behavior_eval.grade(
            case, "W dniu dzisiejszym kupiono trzy serwery."
        )
        self.assertEqual(verdict, "FAIL")
        self.assertIn("still present: w dniu dzisiejszym", reasons)

    def test_non_breaking_spaces_do_not_fail_a_required_string(self):
        case = self.case(contains=["180 000 zł"])
        self.assertEqual(
            behavior_eval.grade(case, "Budżet wyniósł 180 000 zł.")[0], "PASS"
        )

    def test_dash_limit_counts_only_the_edit(self):
        case = self.case(max_count={"—": 2})
        self.assertEqual(behavior_eval.grade(case, "a — b — c")[0], "PASS")
        self.assertEqual(behavior_eval.grade(case, "a — b — c — d")[0], "FAIL")

    def test_manual_case_is_reported_for_reading_not_as_a_pass(self):
        case = self.case(contains=["dowód"])
        case["manual"] = True
        self.assertEqual(behavior_eval.grade(case, "Cytuję dowód.")[0], "MANUAL")
        self.assertEqual(behavior_eval.grade(case, "Brak cytatu.")[0], "FAIL")


class RunnerTests(unittest.TestCase):
    def test_system_prompt_inlines_the_skill_and_all_six_references(self):
        prompt = behavior_eval.build_system_prompt(ROOT / behavior_eval.RUNTIME)
        self.assertEqual(prompt.count("=== "), 7)
        self.assertIn("=== SKILL.md ===", prompt)
        self.assertIn("=== references/polish-patterns.md ===", prompt)

    def test_command_loads_no_user_settings_servers_or_tools(self):
        command = behavior_eval.claude_command("Popraw styl", Path("s.txt"), "sonnet")
        self.assertEqual(command[command.index("--setting-sources") + 1], "project")
        self.assertIn("--strict-mcp-config", command)
        self.assertEqual(command[command.index("--tools") + 1], "")
        self.assertIn("--no-session-persistence", command)

    def test_regrade_applies_current_checks_to_saved_responses(self):
        cases = [
            {"id": "t", "kind": "must_change", "prompt": "x\ny",
             "checks": {"excludes": ["niniejszy"]}}
        ]
        saved = [{"id": "t", "runs": [{"response": "Wypełnij niniejszy formularz."}]}]
        result = behavior_eval.regrade(cases, saved)
        self.assertEqual(result[0]["runs"][0]["verdict"], "FAIL")

    def test_result_metadata_carries_hashes_not_paths(self):
        hashes = behavior_eval.skill_hashes(ROOT / behavior_eval.RUNTIME)
        self.assertEqual(len(hashes), 7)
        self.assertTrue(all("/" not in name or name.startswith("references/")
                            for name in hashes))


if __name__ == "__main__":
    unittest.main()
