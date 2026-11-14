# Unreleased pattern rework: behavioural check

Date: 2026-11-14.

Compared the released 2.1.1 skill (`--ref HEAD` at the time of the run) with the reworked pattern file and legal-register sentence in the working tree. Both were run with `scripts/behavior_eval.py --samples 2`: 30 cases, two runs each, sent to the Claude Code CLI (`claude -p`, model alias `sonnet`) with the whole skill inlined, no user settings, no MCP servers and no tools.

## Evidence

- [Cases and checks](../../../tests/behavior/cases.json)
- [Released-version responses](claude-baseline.json)
- [Reworked-version responses](claude-candidate.json)

Each response file records the CLI version, the model alias, and a hash of every skill file that was loaded.

## Results

| Kind | Cases | 2.1.1 passing both runs | Reworked passing both runs |
| --- | --- | --- | --- |
| Clean text that must come back unchanged | 7 | 7 | 7 |
| Clean sentences next to slop | 6 | 1 | 6 |
| Protected spans, legal, academic, voice | 9 | 9 | 9 |
| Text that must change | 6 | 6 | 6 |
| Audit (read by hand, not auto-graded) | 2 | n/a | n/a |

The released version failed five mixed cases in both runs. In each, a legitimate edit to one sentence was accompanied by changes to clean neighbouring sentences:

- `Ustalono, że w 2025 r. firma zgłosiła…` lost `Ustalono, że`, and `Założono, że…` became `Zakładamy, że…` or `ma obsłużyć`. Both change who holds the claim or how certain it is.
- `W przypadku wycieku` became `Jeśli dojdzie do wycieku` or `W razie wycieku`; `W ramach przeglądu wymieniono` became `Podczas przeglądu wymieniono` or `Wymieniono w nim`.
- `drudzy — z biura` and `Decyzja — to sprawa zespołu` lost their dashes.
- `Z jednej strony… z drugiej strony…` between two stated facts was recast with `ale`.

The last three groups are editorial calls encoded in scenarios 27–30. The first group is a fidelity matter.

## Scenario 15, measured separately

The legal-duty case (`Uprość wyjaśnienie dla przedsiębiorcy`) is unstable and two runs do not show it. Sixteen runs each:

| Version | Kept `Przedsiębiorca` as the subject |
| --- | --- |
| 2.1.1 | 14 of 16 |
| Reworked patterns, before the register sentence | 11 of 16 |
| Reworked patterns with the register sentence | 16 of 16 |

## Limits

- One model alias on one platform. Nothing here covers Codex, ChatGPT or Claude.ai.
- The skill is inlined in full. Real sessions load reference files selectively, so this measures the instructions, not skill discovery or which files get read.
- Two runs per case. A case that fails one time in ten will usually pass; scenario 15 is the example.
- The checks are string checks. They catch a changed or missing sentence, not a subtly worse one, and the two audit cases are printed for reading instead of graded.
- Three checks were loosened after the first run because they failed correct output: a sentence-initial `Retry policy`, a straight closing quote after a preserved quotation, and removed wording quoted inside an editor's note.
