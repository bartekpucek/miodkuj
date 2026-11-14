#!/usr/bin/env python3
"""Run Miodkuj on fixed Polish inputs and check the responses automatically.

The cases live in tests/behavior/cases.json. Each case is a user request plus
checks on the response: text that must come back verbatim, strings that must
survive, strings that must be gone. A live run sends every case to the Claude
Code CLI with the skill's files loaded and no user settings, plugins or tools,
so it measures the loaded instructions, not skill discovery.

Nothing here ships to users: the skill bundle contains only the skill folder.

Usage:
  python3 scripts/behavior_eval.py                      # working tree, 1 sample
  python3 scripts/behavior_eval.py --samples 3 --out results.json
  python3 scripts/behavior_eval.py --ref v2.1.1         # a released version
  python3 scripts/behavior_eval.py --grade results.json # regrade, no model calls
"""

import argparse
import datetime
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "tests" / "behavior" / "cases.json"
RUNTIME = Path("plugins/miodkuj/skills/miodkuj")
KINDS = {"clean", "mixed", "protected", "must_change", "audit"}
CHECK_KEYS = {
    "equals",
    "contains",
    "contains_ci",
    "excludes",
    "excludes_ci",
    "max_count",
}
PREAMBLE = (
    "One skill is installed in this session: Miodkuj. It applies to every "
    "request here. Follow its SKILL.md exactly. The reference files it names "
    "are reproduced below; treat each as already read. Reply only with what "
    "the skill says the user should see."
)


def load_cases(path: Path = CASES_PATH) -> list[dict]:
    """Load and validate the case file."""
    cases = json.loads(path.read_text(encoding="utf-8"))["cases"]
    seen: set[str] = set()
    for case in cases:
        case_id = case["id"]
        if case_id in seen:
            raise ValueError(f"duplicate case id: {case_id}")
        seen.add(case_id)
        if case["kind"] not in KINDS:
            raise ValueError(f"{case_id}: unknown kind {case['kind']}")
        unknown = set(case.get("checks", {})) - CHECK_KEYS
        if unknown:
            raise ValueError(f"{case_id}: unknown checks {sorted(unknown)}")
        if not case.get("manual") and not case.get("checks"):
            raise ValueError(f"{case_id}: an automatic case needs a check")
    return cases


def normalize(text: str) -> str:
    """Make non-breaking and repeated spaces irrelevant to a comparison."""
    text = text.replace(" ", " ").replace(" ", " ")
    return re.sub(r"[ \t]+", " ", text).strip()


NOTE_START = re.compile(
    r"(?i)^[*_>\s]*(uwag|notatk|nota\b|zmian|co zmieni|zmieni[łl]|usun[ąa][łl]|"
    r"zostawi[łl]|note\b|what changed)"
)


def edit_block(response: str, whole: bool = False) -> str:
    """Return the edited text without the editor's note that may follow it.

    By default that is the first paragraph. For a multi-paragraph edit
    (`whole`), it is everything before the first paragraph that opens a note.
    """
    paragraphs = re.split(r"\n\s*\n", response.strip())
    if not whole:
        return paragraphs[0]
    kept = [paragraphs[0]]
    for paragraph in paragraphs[1:]:
        if NOTE_START.match(paragraph):
            break
        kept.append(paragraph)
    return "\n\n".join(kept)


def grade(case: dict, response: str) -> tuple[str, list[str]]:
    """Return PASS, FAIL or MANUAL with the reasons for a failure."""
    checks = case.get("checks", {})
    full = normalize(response)
    whole = case.get("scope") == "full" and case.get("mode") != "audit"
    scoped = (
        full
        if case.get("mode") == "audit"
        else normalize(edit_block(response, whole=whole))
    )
    reasons: list[str] = []

    if "equals" in checks and scoped != normalize(checks["equals"]):
        reasons.append("text was changed but should come back verbatim")
    for needle in checks.get("contains", []):
        if normalize(needle) not in full:
            reasons.append(f"missing: {needle}")
    for needle in checks.get("contains_ci", []):
        if normalize(needle).casefold() not in full.casefold():
            reasons.append(f"missing: {needle}")
    for needle in checks.get("excludes", []):
        if needle in scoped:
            reasons.append(f"still present: {needle.strip()}")
    for needle in checks.get("excludes_ci", []):
        if needle.casefold() in scoped.casefold():
            reasons.append(f"still present: {needle.strip()}")
    for needle, limit in checks.get("max_count", {}).items():
        count = scoped.count(needle)
        if count > limit:
            reasons.append(f"{count} x {needle!r}, at most {limit} allowed")

    if reasons:
        return "FAIL", reasons
    return ("MANUAL" if case.get("manual") else "PASS"), []


def skill_files(skill_dir: Path) -> list[Path]:
    """Return SKILL.md followed by the reference files in a stable order."""
    return [skill_dir / "SKILL.md", *sorted((skill_dir / "references").glob("*.md"))]


def build_system_prompt(skill_dir: Path) -> str:
    """Inline the whole skill so the model needs no tools to read it."""
    parts = [PREAMBLE]
    for path in skill_files(skill_dir):
        name = path.relative_to(skill_dir).as_posix()
        parts.append(f"=== {name} ===\n{path.read_text(encoding='utf-8')}")
    return "\n\n".join(parts)


def skill_hashes(skill_dir: Path) -> dict[str, str]:
    """Hash each loaded file so a result names exactly what was tested."""
    return {
        path.relative_to(skill_dir).as_posix(): hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
        for path in skill_files(skill_dir)
    }


def export_ref(ref: str, destination: Path) -> Path:
    """Extract the skill folder as it was at a git ref."""
    archive = subprocess.run(
        ["git", "archive", ref, RUNTIME.as_posix()],
        cwd=ROOT,
        capture_output=True,
        check=True,
    )
    subprocess.run(
        ["tar", "-x", "-C", str(destination)], input=archive.stdout, check=True
    )
    return destination / RUNTIME


def claude_command(prompt: str, system_file: Path, model: str) -> list[str]:
    """One request, no user or project settings, no MCP servers, no tools."""
    return [
        "claude",
        "-p",
        prompt,
        "--append-system-prompt-file",
        str(system_file),
        "--setting-sources",
        "project",
        "--strict-mcp-config",
        "--tools",
        "",
        "--no-session-persistence",
        "--output-format",
        "json",
        "--model",
        model,
    ]


def run_claude(prompt: str, system_file: Path, model: str, timeout: int) -> dict:
    """Send one request from an empty directory and return text plus usage."""
    with tempfile.TemporaryDirectory(prefix="miodkuj-eval-") as cwd:
        try:
            done = subprocess.run(
                claude_command(prompt, system_file, model),
                cwd=cwd,
                text=True,
                capture_output=True,
                timeout=timeout,
            )
            payload = json.loads(done.stdout)
        except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as error:
            return {"error": f"{type(error).__name__}: {error}"[:300]}
    if payload.get("is_error") or "result" not in payload:
        return {"error": str(payload.get("result", "no result"))[:300]}
    usage = payload.get("usage", {})
    return {
        "response": payload["result"],
        "usage": {
            "input": usage.get("input_tokens", 0)
            + usage.get("cache_creation_input_tokens", 0)
            + usage.get("cache_read_input_tokens", 0),
            "output": usage.get("output_tokens", 0),
        },
        "cost_usd": payload.get("total_cost_usd", 0.0),
    }


def run_suite(cases, skill_dir, model, samples, workers, timeout) -> list[dict]:
    """Run every case `samples` times and grade each response."""
    with tempfile.TemporaryDirectory(prefix="miodkuj-eval-sys-") as tmp:
        system_file = Path(tmp) / "system.txt"
        system_file.write_text(build_system_prompt(skill_dir), encoding="utf-8")
        jobs = [(case, n) for case in cases for n in range(samples)]
        with ThreadPoolExecutor(max_workers=workers) as pool:
            raw = list(
                pool.map(
                    lambda job: run_claude(
                        job[0]["prompt"], system_file, model, timeout
                    ),
                    jobs,
                )
            )
    by_case: dict[str, list[dict]] = {case["id"]: [] for case in cases}
    for (case, _), run in zip(jobs, raw):
        if "error" in run:
            run.update(verdict="ERROR", reasons=[run["error"]])
        else:
            run["verdict"], run["reasons"] = grade(case, run["response"])
        by_case[case["id"]].append(run)
    return [{"id": case["id"], "runs": by_case[case["id"]]} for case in cases]


def regrade(cases, results: list[dict]) -> list[dict]:
    """Apply the current checks to responses recorded earlier."""
    by_id = {case["id"]: case for case in cases}
    for entry in results:
        case = by_id.get(entry["id"])
        for run in entry["runs"]:
            if case is None:
                run.update(verdict="ERROR", reasons=["case no longer exists"])
            elif "response" in run:
                run["verdict"], run["reasons"] = grade(case, run["response"])
    return results


def report(cases, results: list[dict], verbose: bool) -> tuple[int, int, int]:
    """Print pass counts per case and the text of every failing response."""
    kinds = {case["id"]: case["kind"] for case in cases}
    failed = errors = manual = 0
    for entry in results:
        runs = entry["runs"]
        verdicts = [run["verdict"] for run in runs]
        passed = sum(v in ("PASS", "MANUAL") for v in verdicts)
        if "ERROR" in verdicts:
            label, errors = "ERROR ", errors + 1
        elif passed < len(runs):
            label, failed = "FAIL  ", failed + 1
        elif "MANUAL" in verdicts:
            label, manual = "MANUAL", manual + 1
        else:
            label = "PASS  "
        kind = kinds.get(entry["id"], "?")
        print(f"{label} {passed}/{len(runs)}  {entry['id']}  [{kind}]")
        for run in runs:
            show = run["verdict"] in ("FAIL", "ERROR") or (
                verbose or run["verdict"] == "MANUAL"
            )
            if show:
                for reason in run.get("reasons", []):
                    print(f"         - {reason}")
                if "response" in run:
                    print("         > " + run["response"].replace("\n", "\n         > "))
    return failed, errors, manual


def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--model", default="sonnet", help="Claude model alias or id")
    parser.add_argument("--samples", type=int, default=1, help="runs per case")
    parser.add_argument("--case", action="append", help="run only this case id")
    parser.add_argument("--kind", choices=sorted(KINDS), help="run only this kind")
    parser.add_argument("--ref", help="test the skill as of this git ref")
    parser.add_argument("--skill-dir", type=Path, help="test a skill folder elsewhere")
    parser.add_argument("--out", type=Path, help="write responses and verdicts here")
    parser.add_argument("--grade", type=Path, help="regrade a saved results file")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--verbose", action="store_true", help="print every response")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    cases = load_cases()
    if args.case:
        cases = [case for case in cases if case["id"] in args.case]
    if args.kind:
        cases = [case for case in cases if case["kind"] == args.kind]
    if not cases:
        print("error: no matching cases")
        return 2

    if args.grade:
        document = json.loads(args.grade.read_text(encoding="utf-8"))
        results = regrade(load_cases(), document["cases"])
    else:
        with tempfile.TemporaryDirectory(prefix="miodkuj-eval-ref-") as tmp:
            if args.ref:
                skill_dir = export_ref(args.ref, Path(tmp))
            else:
                skill_dir = args.skill_dir or ROOT / RUNTIME
            version = subprocess.run(
                ["claude", "--version"], capture_output=True, text=True
            ).stdout.strip()
            results = run_suite(
                cases, skill_dir, args.model, args.samples, args.workers, args.timeout
            )
            document = {
                "date": datetime.date.today().isoformat(),
                "runner": f"claude -p, {version}",
                "model": args.model,
                "samples": args.samples,
                "skill": {
                    "source": args.ref
                    or ("custom folder" if args.skill_dir else "working tree"),
                    "sha256": skill_hashes(skill_dir),
                },
                "cases": results,
            }

    failed, errors, manual = report(cases, results, args.verbose)
    runs = [run for entry in results for run in entry["runs"]]
    tokens = sum(run.get("usage", {}).get("input", 0) for run in runs)
    cost = sum(run.get("cost_usd", 0.0) for run in runs)
    print(
        f"\n{len(results)} cases, {len(runs)} runs: {failed} failing, "
        f"{errors} with errors, {manual} to read by hand. "
        f"Input tokens: {tokens:,}. Reported cost: ${cost:.2f}."
    )
    if args.out:
        args.out.write_text(
            json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    if errors:
        return 2
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
