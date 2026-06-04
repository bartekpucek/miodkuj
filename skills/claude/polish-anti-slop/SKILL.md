---
name: polish-anti-slop
description: Removes AI-sounding, bureaucratic, generic, or over-polished Polish prose while preserving facts, meaning, numbers, citations, and register. Use whenever Polish text sounds AI-generated, over-formal, or translated from English, or when the user asks to popraw styl, napisz po ludzku, napisz prościej, uprość, uprość do prostego języka, usuń slop, bez slopu, or says the text brzmi jak ChatGPT, brzmi sztucznie, or brzmi jak z AI. Also use for Polish marketing, technical, academic, legal/official, or newsletter text that needs to read like a person wrote it. Works on Polish text even when the user writes the request in English.
---

# Polish Anti Slop

## Core Rule

Improve Polish prose so it sounds natural, specific, and appropriate to its genre. Rewrite first by default. Preserve meaning, facts, names, numbers, links, citations, quotes, code, legal references, and user constraints.

Never promise detector evasion, "undetectable" writing, academic laundering, impersonation, or fact invention. These are out of scope; if asked, do the honest editing work and say so plainly.

## Default Output

- If the user asks to rewrite, popraw styl, napisz po ludzku, uprość, usuń slop, make natural, or remove AI style: return the revised Polish text first, nothing before it.
- Add short notes only when requested or when a constraint or risk matters (e.g., you preserved a passive form on purpose, or a claim lacked proof).
- If the user asks for audit only ("tylko audyt"): do not rewrite. List concrete issues with severity.
- If the user gives a voice sample: match it before applying generic preferences.

## Workflow

1. Identify genre and audience: public/plain Polish, marketing, technical docs, academic/scientific, legal/official, or social/opinion.
2. Protect exact spans: code, commands, URLs, markdown links, quotes, citations, tables, numbers, dates, legal references, product/API names. Reproduce them character-for-character.
3. Scan for Polish slop: chatbot residue, officialese, nominalizations, passive/impersonal fog, genitive chains, inflated importance, formulaic structures, generic endings.
4. Rewrite paragraph by paragraph. Prefer actors, verbs, concrete stakes, and natural Polish word order over noun stacks and abstraction.
5. Run a second pass: what still sounds generated, bureaucratic, translated, too balanced, or too generic?
6. Run an integrity pass: no changed facts, no invented proof, no lost caveats, no broken protected spans.

## Reference Navigation

Read these only when the situation calls for them — they live one level down in `references/`:

- Polish pattern lists and concrete rewrites: `references/polish-patterns.md`
- Register-specific behavior and exceptions: `references/registers.md`
- Public-facing simplification (prosta polszczyzna): `references/plain-polish.md`
- Voice matching from a Polish sample: `references/voice-calibration.md`
- Severity levels and internal scoring: `references/scoring.md`
- Before/after transformations: `references/examples.md`
- Research and upstream sources: `references/sources.md`

## Quick Decisions

| Situation | Default |
| --- | --- |
| User says "popraw styl" / "usuń slop" / "napisz po ludzku" | Rewrite first |
| User says "tylko audyt" | Audit only, no rewrite |
| Public/citizen text | Plain Polish, direct address, action first |
| Marketing | Replace empty adjectives with proof or a concrete benefit |
| Technical docs | Keep terms and code exact, cut filler |
| Academic text | Preserve hedging, data, citations, and valid passive |
| Legal/official text | Clarify explanatory parts; keep the obligated party and formal register; preserve legal force |
| Voice sample supplied | Match the sample over generic naturalness |

## Common Mistakes

- Do not flatten every text into casual Polish. Register matters.
- Do not remove passive or impersonal forms when they are conventional or precise (law, science, procedures).
- Do not replace official legal terms with loose paraphrases.
- Do not add examples, data, dates, sources, or claims the user did not provide.
- Do not treat one word like `kluczowy` or `ważny` as proof of AI style. Act on clusters and weak writing, not single tokens.

## License

MIT. See repository LICENSE. This skill is an independent Polish-language adaptation inspired by open anti-slop work; see `references/sources.md` for attribution.
