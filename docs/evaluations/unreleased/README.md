# Unreleased changes: behavioural check

Date: 2026-11-14.

Compared the released skill at tag `v2.1.1` with the working tree, which holds the pattern rework, the legal-register sentence, the rule that leaves business and IT vocabulary alone, and the trimmed pattern file. Both were run with `scripts/behavior_eval.py`: 41 cases sent to the Claude Code CLI (`claude -p`) with the whole skill inlined, no user settings, no MCP servers and no tools.

## Evidence

- [Cases and checks](../../../tests/behavior/cases.json)
- Model alias `sonnet`, two runs per case: [v2.1.1](claude-baseline.json), [working tree](claude-candidate.json)
- Model alias `haiku`, one run per case: [v2.1.1](claude-baseline-haiku.json), [working tree](claude-candidate-haiku.json)

Each response file records the CLI version, the model alias, and a hash of every skill file that was loaded.

## Sonnet, two runs per case

Cases passing both runs:

| Kind | Cases | v2.1.1 | Working tree |
| --- | --- | --- | --- |
| Clean text that must come back unchanged | 10 | 6 | 10 |
| Clean sentences next to slop | 8 | 1 | 6 |
| Protected spans, legal, academic, voice, translated words | 14 | 14 | 14 |
| Text that must change | 7 | 6 | 7 |
| Audit (read by hand, not auto-graded) | 2 | n/a | n/a |

What v2.1.1 got wrong:

- **Clean sentences next to slop.** A legitimate edit to one sentence came with changes to clean neighbours: `Ustalono, że` dropped, `W przypadku wycieku` and `W ramach przeglądu` swapped for synonyms, standard Polish dashes removed, a contrast between two stated facts recast with `ale`.
- **Business wording.** `rozwiązanie dedykowane dla firm`, `adresuje problem`, `na koniec dnia`, `finalnie` and `eskalujemy` were replaced in every run. `dedykowany zespół` became `osobny` or `wyznaczony zespół`, which changes the meaning.
- **One clean impersonal text** (`Ustalono, że… Przyjęto…`) was rewritten in both runs.

What the working tree still gets wrong:

- `mixed-reporting-verb` failed both runs. `Założono, że do końca roku obsłuży 60% zgłoszeń` came back as `Plan zakłada, że…` once and with an added subject (`platforma`) once. Over eight separate runs it passed four.
- `s27-clean-next-to-slop` failed one run of two (`W przypadku wycieku` became `W razie wycieku`). Over eight separate runs it passed eight.

## Cases measured with more runs

Two-run results hide cases that fail one time in five. These were measured separately during the work, so they are not all in the saved files:

| Case | v2.1.1 | Working tree |
| --- | --- | --- |
| Scenario 15, legal duty keeps `Przedsiębiorca` | 14 of 16 | 16 of 16 |
| Scenario 29, `W ramach przeglądu wymieniono…` kept verbatim | 0 of 4 | 4 of 8 |
| Longer three-paragraph mixed text | 0 of 4 | 8 of 8 |
| Synonym cycling, with sameness stated in the request | not run | 8 of 8 |

Scenario 29 is the weakest of the reworked cases. After the first two sentences are merged, the model often avoids repeating `przegląd` and writes `W jego trakcie wymieniono`.

## Haiku, one run per case

| Version | Automatic cases failing, of 39 |
| --- | --- |
| v2.1.1 | 17 |
| Working tree | 15 |

On this model and in this setup, both versions rewrite clean text they should leave alone, including most of the verbatim cases. One run per case cannot separate the two versions. It does show that the skill's "leave it alone" behaviour depends heavily on the model.

## Size of the skill

| | v2.1.1 | Working tree | Change |
| --- | --- | --- | --- |
| `SKILL.md`, `eval.md`, `polish-patterns.md` (read on nearly every use) | 26,344 bytes | 27,049 bytes | +2.7% |
| Whole skill folder | 42,420 bytes | 43,268 bytes | +2.0% |

The pattern file lost its contents list and three before/after pairs that `examples.md` repeats. Those three rules were then run eight times each on a copy of the skill with `examples.md` deleted, and held.

## Limits

- One platform. Nothing here covers Codex, ChatGPT or Claude.ai.
- The skill is inlined in full and the model has no tools. Real sessions load reference files selectively, so this measures the instructions, not skill discovery or which files get read.
- The checks are string checks. They catch a changed or missing sentence, not a subtly worse one. The two audit cases are printed for reading instead of graded.
- Five checks were loosened during the work because they failed correct output: a sentence-initial `Retry policy`, a straight closing quote after a preserved quotation, removed wording quoted inside an editor's note, a shortened first sentence where the request said to shorten, and `aż przyjedzie Anna` for `do przyjazdu Anny`.
- Scenarios 28–30 encode editorial preferences (dashes, `w ramach`, the kept connector). A different preference would change those checks, not the fidelity ones.
