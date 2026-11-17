# Unreleased changes: behavioural check

Date: 2026-11-14.

Compared the released skill at tag `v2.1.1` with the working tree, which holds the pattern rework, the legal-register sentence, the rule that leaves business and IT vocabulary alone, the trimmed pattern file, and a per-sentence rule in `SKILL.md`. Both were run with `scripts/behavior_eval.py`: 41 cases sent to the Claude Code CLI (`claude -p`) with the whole skill inlined, no user settings, no MCP servers and no tools.

## Evidence

- [Cases and checks](../../../tests/behavior/cases.json)
- Model alias `sonnet`, two runs per case: [v2.1.1](claude-baseline.json), [working tree](claude-candidate.json)
- Model alias `haiku`, three runs per case: [v2.1.1](claude-baseline-haiku.json), [working tree](claude-candidate-haiku.json)

Each response file records the CLI version, the model alias, and a hash of every skill file that was loaded. The two audit cases are printed for reading and are left out of the counts below.

## Runs passing

| Kind | Sonnet v2.1.1 | Sonnet now | Haiku v2.1.1 | Haiku now |
| --- | --- | --- | --- | --- |
| Clean text that must come back unchanged | 12/20 | 20/20 | 10/30 | 17/30 |
| Clean sentences next to slop | 3/16 | 16/16 | 4/24 | 11/24 |
| Protected spans, legal, academic, voice, translated words | 28/28 | 28/28 | 23/42 | 30/42 |
| Text that must change | 13/14 | 14/14 | 17/21 | 20/21 |
| All automatic cases | 56/78 | 78/78 | 54/117 | 78/117 |

What v2.1.1 gets wrong on Sonnet:

- **Clean sentences next to slop.** A legitimate edit to one sentence came with changes to clean neighbours: `Ustalono, że` dropped, `W przypadku wycieku` and `W ramach przeglądu` swapped for synonyms, standard Polish dashes removed, a contrast between two stated facts recast with `ale`.
- **Business wording.** `rozwiązanie dedykowane dla firm`, `adresuje problem`, `na koniec dnia`, `finalnie` and `eskalujemy` were replaced in every run. `dedykowany zespół` became `osobny` or `wyznaczony zespół`, which changes the meaning.
- **A clean impersonal text** (`Ustalono, że… Przyjęto…`) was rewritten in both runs.

Haiku rewrites far more readily on both versions. It changes sentences where no rule applies (`drudzy — z biura` to `a inni z biura`) and sometimes changes the meaning while doing so (`W przypadku tego preparatu` to `W tym przypadku`; `adresuje problem` to `eliminuje`). The working tree improves every group on Haiku but leaves it well short of Sonnet.

## The per-sentence rule

The largest single gain came from seven lines added near the top of `SKILL.md`. In edit mode the model sorts each sentence silently: it rewrites a sentence with cut-on-sight wording or another defect it can name from the pattern file, and copies every other sentence character for character. The skill already said this in workflow step 5, but the weaker model did not act on it there.

A first version, which said a sentence changes only if the model can name and quote its defect, overshot on Haiku: it returned the README's headline example (`W celu dokonania zgłoszenia należy wypełnić niniejszy formularz…`) unchanged in two of three runs, and once listed the defects in a note while leaving the text as it was. The final wording names the cut-on-sight wording as always rewritten and asks for the sorting to happen silently.

Measured with and without the rule, on the same build otherwise:

| Case or group | Without the rule | With the rule |
| --- | --- | --- |
| Sonnet, scenario 29, `W ramach przeglądu wymieniono…` kept | 3 of 8 | 8 of 8 |
| Sonnet, `Założono, że…` kept | 6 of 8 | 8 of 8 |
| Sonnet, scenario 27, clean sentences next to slop | 8 of 8 | 8 of 8 |
| Haiku, clean text left alone | 9 of 30 | 15 of 30 |
| Haiku, mixed text, clean parts kept | 5 of 24 | 8 of 24 |
| Haiku, slop that must change | 13 of 21 | 20 of 21 |

A one-line control prompt with no skill at all left Haiku's clean text intact in 4 of 30 runs and its mixed text in 1 of 24.

## Cases measured with more runs

| Case | v2.1.1 | Working tree |
| --- | --- | --- |
| Scenario 15, legal duty keeps `Przedsiębiorca` (Sonnet) | 14 of 16 | 16 of 16, measured before the per-sentence rule |
| Longer three-paragraph mixed text (Sonnet) | 0 of 4 | 8 of 8, measured before the per-sentence rule |

## Size of the skill

| | v2.1.1 | Working tree | Change |
| --- | --- | --- | --- |
| `SKILL.md`, `eval.md`, `polish-patterns.md` (read on nearly every use) | 26,344 bytes | 27,358 bytes | +3.8% |
| Whole skill folder | 42,420 bytes | 43,577 bytes | +2.7% |

The pattern file lost its contents list and three before/after pairs that `examples.md` repeats. Those three rules were then run eight times each on a copy of the skill with `examples.md` deleted, and held.

## Limits

- One platform. Nothing here covers Codex, ChatGPT or Claude.ai.
- The skill is inlined in full and the model has no tools. Real sessions load reference files selectively, so this measures the instructions, not skill discovery or which files get read.
- Two or three runs per case. A case that fails one time in five can pass both runs.
- The checks are string checks. They catch a changed or missing sentence, not a subtly worse one.
- Five checks were loosened during the work because they failed correct output: a sentence-initial `Retry policy`, a straight closing quote after a preserved quotation, removed wording quoted inside an editor's note, a shortened first sentence where the request said to shorten, and `aż przyjedzie Anna` for `do przyjazdu Anny`.
- Scenarios 28–30 encode editorial preferences (dashes, `w ramach`, the kept connector). A different preference would change those checks, not the fidelity ones.
