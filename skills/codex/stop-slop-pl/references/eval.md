# Pass/Fail Evaluation

Run this evaluation internally after every edit or audit. Do not show the checklist unless the user asks for diagnostics.

Answer every applicable check with pass or fail. If any check fails, revise once and run the failed checks again. Fidelity outranks stylistic improvement: if a conflict remains, preserve the source and briefly flag the limitation.

## Fidelity

- Does every source claim and qualification survive with the same degree of certainty?
- Did the edit avoid adding facts, examples, opinions, numbers, dates, quotations, sources, customers, mechanisms, or outcomes?
- Are names, numbers, dates, links, citations, quotations, code, legal references, product names, and required terminology exact?
- Did the edit preserve exceptions, caveats, warnings, deadlines, eligibility rules, rights, obligations, and procedural steps?

## Voice And Proportion

- Does the result preserve the writer's vocabulary, cadence, formality, directness, uncertainty, humor, asides, fragments, digressions, and useful irregularities?
- Were strong human sentences left alone unless another user constraint required a change?
- Is the amount of editing proportional to the actual slop or clarity problem?
- Did the edit avoid replacing a specific detail with a generic claim or polishing away useful friction?
- If a voice sample was supplied, does the result follow it over generic preferences where fidelity allows?

## Register And Meaning

- Does the result fit the text's job, audience, and genre?
- In legal or official text, are the obligated party, legal force, definitions, and formal requirements unchanged?
- In academic or scientific text, are data, citations, hedging, uncertainty, and causal limits unchanged?
- In technical text, are code, commands, API names, configuration keys, error messages, versions, and stable terminology unchanged?

## Slop And Clarity

- Were material clusters of chatbot residue, officialese, abstraction, inflated importance, formulaic structure, generic endings, or translated phrasing removed?
- Does each remaining sentence earn its place without forcing all paragraphs into the same shape?
- Does generic prose pass the portability test, or was it cut, grounded in source material, or made smaller?
- Does the result sound natural when read aloud without manufactured punchlines or robotic symmetry?
- Did the edit avoid mechanical synonym substitution and preserve deliberate repetition?

## Mode

### Edit Mode

- Does the response lead with the complete revised text?
- Are notes omitted unless requested or needed to explain a material risk or evidence gap?

### Audit Mode

- Does each finding name a material pattern, quote its evidence, assign severity, and suggest a direction for the fix?
- Does the response avoid rewriting the text and avoid guessing whether AI wrote it?

### Embedded Or File Mode

- Does the result contain only what the parent task or file operation requires?
- Are frontmatter, code blocks, tables, link targets, and other protected structures intact unless the user asked to edit them?

## Result

- **PASS:** Every applicable check passes.
- **REVISE:** One or more checks fail. Revise once, then rerun only the failed checks.
- **FLAG:** A fidelity conflict or missing fact prevents a safe improvement. Preserve the source and state the limitation briefly.
