# Miodkuj 2.1.1: bounded behavioral check

Date: 2026-09-14.

Compared the published 2.1.0 runtime at commit `e6300cbe3c910c1677bbc44d64bca1670b7800e6` with the final 2.1.1 candidate. Each version was read by a fresh Codex subagent using `gpt-5.6-sol` with high reasoning effort. The evaluators received the skill and 12 shared input requests; the candidate also received a thirteenth case checking the implementation subject in a voice-match edit. Neither evaluator received target responses or findings from the other run. They returned actual edits and audits, which were reviewed against the source and requested mode.

## Evidence

- [Inputs](cases.json)
- [Published-version responses](codex-baseline.json)
- [Candidate responses](codex-candidate.json)

The response files include hashes of the runtime files used in each run. The bilingual Edinburgh case uses the source pair supplied in issue #2. The complete accommodation, residence, and remaining-in-place cases are synthetic; issue #3 contains only truncated fragments.

## Reviewed results

| Case | 2.1.0 | 2.1.1 | Invariant checked |
| --- | --- | --- | --- |
| `travel_polish` | Fail | Pass | Name the main focus without inventing an accommodation or excursion base. |
| `travel_bilingual` | Fail | Pass | Preserve countryside, day trips, practical feasibility, and travel without driving; invent no base. |
| `preserve_physics` | Pass | Pass | Leave the precise physical term and clear sentence unchanged. |
| `preserve_figurative` | Pass | Pass | Preserve the appropriate analytical metaphor. |
| `audit_context` | Fail | Pass | Give contextual severity and supported directions, without rewriting or suggesting unprovided logistics. |
| `temporary_stay` | Pass | Pass | Use wording appropriate to weekend accommodation; preserve the location and duration. |
| `preserve_residence` | Pass | Pass | Preserve `zamieszkaj` in the explicit residence context. |
| `stay_remaining` | Pass | Pass | Express remaining in place until Anna arrives, without implying accommodation. |
| `generic_fidelity` | Pass | Pass | Remove the stock opening without inventing actors or applications. |
| `analysis_fidelity` | Pass | Pass | Simplify the sentence without adding counts, actors, systems, or performance measures. |
| `unsupported_synthesis` | Pass | Pass | Preserve only the supplied attributed claim; invent no research findings. |
| `preserve_opinions` | Pass | Pass | Do not turn unspecified opinions into conversations or consultations. |
| `voice_implementation` | Not run | Pass | Preserve implementation as the subject and the possibility of improvement, without inventing features or conditions. |

All 13 candidate responses satisfied the reviewed invariants in this run. The published version failed three of the 12 shared cases by introducing an unsupported base or omitting source constraints. The temporary-accommodation correction already worked in this baseline, so this run does not establish that the new guidance fixed issue #3's original occurrence. The additional voice-match case checks the final correction to an older example; it has no baseline comparison.

## Limits

This is one sample per case and version, with 12 baseline cases and 13 candidate cases processed in their respective evaluator's context. It checks the loaded instructions, not automatic skill discovery or independent fresh-session behavior for every case. Outputs are evaluated for meaning and mode, not exact match to one preferred sentence. The original reporters did not provide full prompts, model identifiers, or skill-loading evidence, so these checks are not a reproduction of their complete sessions. They establish no general reliability rate or cross-model improvement.
