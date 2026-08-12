---
name: miodkuj
description: Use for AI-generated/over-formal/generic/bureaucratic/translated Polish; brzmi jak ChatGPT, brzmi sztucznie, popraw styl, napisz po ludzku, napisz prościej, uprość, usuń slop, miodkuj. Edit/audit.
---

# Miodkuj

## Core Rule

Make the minimum effective edit. Preserve the writer's point, recognizable voice, structure, and useful irregularities while removing Polish AI-writing patterns, bureaucratic fog, translation residue, repetition, and unclear passages.

Preserve meaning, facts, qualifications, names, numbers, dates, links, citations, quotations, code, legal references, product names, and user constraints. Never invent specificity or promise detector evasion, "undetectable" writing, academic laundering, or impersonation.

## Modes

- **Edit mode:** Default for pasted text. Return the revised Polish text first. Add a short change note only when requested or when a material constraint or evidence gap needs explanation. If the source already passes the quality gate, return it unchanged; do not replace correct wording merely to show an edit.
- **Audit mode:** When the user asks for an audit, scan, or diagnosis without rewriting, name each material pattern, quote the relevant source fragment, assign red/yellow/green severity, and suggest the direction of a fix. Do not rewrite and do not claim that AI wrote the text. Do not manufacture a finding when the supplied text establishes no material problem; say so, and use green findings where useful. Treat missing surrounding context as conditional rather than as a red defect unless the supplied text itself materially blocks understanding.
- **Embedded or file mode:** When another task uses this skill or the user points to a file, run the full process internally and return or write only the final text the parent task requires. Preserve frontmatter, code blocks, tables, and link targets unless the user explicitly asks to edit them.

If the user has not supplied text or a file, ask for it. Ask about audience or purpose only when the answer would materially change the edit and cannot be inferred from context.

## Workflow

1. Read the complete source before editing. Identify its job, audience, and register.
2. Infer three to five voice signals from the source: vocabulary, cadence, formality, directness, punctuation, humor, uncertainty, asides, fragments, or digressions. If the user supplies a separate voice sample, treat it as stronger evidence.
3. Protect exact spans: code, commands, URLs, Markdown links, quotations, citations, tables, numbers, dates, legal references, product/API names, and required terminology.
4. Scan for clusters of Polish slop and weak writing. Do not treat a single word or construction as proof of a problem.
5. Before changing a passage, identify the material defect internally. If there is none, copy the passage verbatim. Preserve useful repetition, roughness, mixed feelings, self-corrections, domain language, and uneven rhythm when they belong to the writer.
6. Run a second pass for generated cadence, bureaucratic or translated phrasing, generic claims, and over-regular structure.
7. Run `references/eval.md`. If a check fails, revise once before returning the result.

## Specificity Ladder

When a generic claim needs grounding:

1. Use a fact, mechanism, example, constraint, consequence, or judgment already present in the source.
2. Recombine source information into a more direct statement without increasing certainty.
3. Make the unsupported claim smaller or remove it.
4. If the missing detail blocks a useful rewrite, flag the gap or ask for the information.

Never invent a number, example, customer, source, mechanism, consequence, affected workflow, performance claim, comparison, or opinion to make prose sound human. A plausible inference is still new information: removing a slogan does not authorize replacing it with an inferred explanation. If the source gives no support, end on the preceding supported statement or flag the gap.

## Portability Test

If a sentence could move unchanged to another company, ministry, product, project, or person, it is probably filler. Cut it, ground it in available source material, or make the claim smaller.

Do not apply this test mechanically to definitions, legal formulas, standard warnings, or necessary procedural language.

## Reference Navigation

- For Polish slop patterns and their false-positive guards, read `references/polish-patterns.md`.
- For the final pass/fail quality gate, read `references/eval.md` on every edit or audit.
- For genre-specific behavior and exceptions, read `references/registers.md`.
- For public-facing, instructional, civic, UX, or broad-audience text, read `references/plain-polish.md`.
- For every personal, marketing, newsletter, or opinion edit, read `references/voice-calibration.md`.
- For ambiguous transformations or useful Polish before/after models, read `references/examples.md`.

## Quick Decisions

| Situation | Default |
| --- | --- |
| `popraw styl`, `usuń slop`, `napisz po ludzku` | Edit minimally and return the text first |
| `tylko audyt`, `wskaż problemy` | Audit only; quote evidence and do not rewrite |
| Public or citizen text | Use plain Polish, direct address, and action first |
| Marketing | Replace unsupported adjectives with source-grounded benefit or a smaller claim |
| Technical documentation | Preserve terms and code; remove filler and hidden steps |
| Academic text | Preserve hedging, data, citations, and valid passive forms |
| Legal or official text | Preserve the obligated party, legal force, definitions, and formal register |
| Voice sample supplied | Match the sample over generic preferences when fidelity remains intact |

## Common Mistakes

- Do not flatten every text into casual, clipped, or uniformly polished Polish.
- Do not infer AI authorship from stylistic patterns. Describe the writing that is present.
- Do not remove passive or impersonal forms when they are conventional or precise.
- Do not replace official legal or technical terms with loose paraphrases.
- Do not regularize intentional fragments, repetition, punctuation, or digressions merely for consistency.
- Do not add examples, data, dates, sources, opinions, or claims the user did not provide.
- Do not treat one use of `kluczowy`, a triad, a contrast, or an em dash as proof of slop. Judge function and clusters.
- Do not use the em dash as a default connector. Preserve or use it only when the source or supplied voice supports it and it clearly works better than a comma, colon, full stop, or parentheses.
