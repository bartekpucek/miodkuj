---
name: polish-anti-slop
description: Use when Polish prose sounds AI-generated, over-formal, generic, bureaucratic, or translated from English; also when asked to popraw styl, napisz po ludzku, napisz prościej, uprość, uprość do prostego języka, usuń slop, or when the text brzmi jak ChatGPT or brzmi sztucznie. Matches a Polish voice or register when a sample is given.
---

# Polish Anti Slop

## Core Rule

Improve Polish prose so it sounds natural, specific, and appropriate to its genre. Rewrite first by default. Preserve meaning, facts, names, numbers, links, citations, quotes, code, legal references, and user constraints.

Never promise detector evasion, "undetectable" writing, academic laundering, impersonation, or fact invention.

## Default Output

- If the user asks to rewrite, popraw styl, napisz po ludzku, uprość, usuń slop, make natural, or remove AI style: return the revised Polish text first.
- Add short notes only when requested or when a constraint/risk matters.
- If the user asks for audit only: do not rewrite.
- If the user gives a voice sample: match it before applying generic preferences.

## Workflow

1. Identify genre and audience: public/plain Polish, marketing, technical docs, academic/scientific, legal/official, or social/opinion.
2. Protect exact spans: code, commands, URLs, markdown links, quotes, citations, tables, numbers, dates, legal references, product/API names.
3. Scan for Polish slop: chatbot residue, officialese, nominalizations, passive/impersonal fog, genitive chains, inflated importance, formulaic structures, generic endings.
4. Rewrite paragraph by paragraph. Prefer actors, verbs, concrete stakes, and natural Polish order.
5. Run a second pass: what still sounds generated, bureaucratic, translated, too balanced, or too generic?
6. Run an integrity pass: no changed facts, no invented proof, no lost caveats, no broken protected spans.

## Reference Navigation

- For Polish pattern lists and rewrites, read `references/polish-patterns.md`.
- For register-specific behavior and exceptions, read `references/registers.md`.
- For public-facing simplification, read `references/plain-polish.md`.
- For voice matching from a Polish sample, read `references/voice-calibration.md`.
- For severity and internal scoring, read `references/scoring.md`.
- For before/after patterns, read `references/examples.md`.
- For research and upstream sources, read `references/sources.md`.

## Quick Decisions

| Situation | Default |
| --- | --- |
| User says "popraw styl" / "usuń slop" | Rewrite first |
| User says "tylko audyt" | Audit only |
| Public/citizen text | Plain Polish, direct address, action first |
| Marketing | Replace adjectives with proof or concrete benefit |
| Technical docs | Keep terms/code exact, cut filler |
| Academic text | Preserve hedging, data, citations, and valid passive |
| Legal/official text | Clarify explanatory parts; keep the obligated party and formal register; preserve legal force |
| Voice sample supplied | Match sample over generic naturalness |

## Common Mistakes

- Do not flatten every text into casual Polish. Register matters.
- Do not remove passive/impersonal forms when they are conventional or precise.
- Do not replace official legal terms with loose paraphrases.
- Do not add examples, data, dates, sources, or claims that the user did not provide.
- Do not treat one word like `kluczowy` or `ważny` as proof of AI style. Act on clusters and weak writing.
