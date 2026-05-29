# Research Summary

Stop Slop PL adapts anti-AI-slop writing patterns to Polish instead of translating English banned-word lists.

## What The External Skills Agree On

The strongest anti-slop skills, including `hardikpandya/stop-slop`, `blader/humanizer`, `slopbuster`, `de-slop`, and `deslopify`, share a few core ideas:

- Pattern lists help, but rewriting happens at paragraph level.
- Meaning, facts, numbers, citations, links, and quoted text must be preserved.
- Banned words are weak signals unless they cluster.
- Voice and register matter more than generic "humanization."
- A second audit pass catches residue left by the first rewrite.
- Genre exceptions prevent overcorrection.
- Detector-evasion claims should be avoided.

## Polish Adaptation

Polish slop often shows up as:

- officialese: `niniejszy`, `celem`, `w ramach`, `w zakresie`,
- nominalizations: `dokonanie`, `wdrożenie`, `przeprowadzenie`, `realizacja działań`,
- passive and impersonal forms: `zostało wykonane`, `dokonano`, `ustalono`, `należy`,
- genitive chains: `w przypadku braku możliwości uruchomienia pojazdu`,
- inflated importance: `kluczowy`, `fundamentalny`, `kompleksowy`, `przełomowy`,
- formulaic structures: `nie tylko X, ale także Y`, `z jednej strony... z drugiej strony...`,
- generic endings: `podsumowując`, `przyszłość pokaże`, `warto śledzić rozwój sytuacji`.

The skill uses Gov.pl plain-language guidance and Jasnopis-style readability signals: short public-facing sentences, actors and verbs, direct reader perspective, fewer noun chains, less passive voice, fewer participles, and less abstract vocabulary.

## Polish LLM Context

PLLuM and Bielik show why Polish-specific instructions matter. They are useful references for Polish language capability and prompt style, but they do not remove the need for editorial guardrails. The skill therefore treats Polish LLMs as possible helpers, not sources of truth.

## Boundary

Stop Slop PL improves clarity, specificity, register fit, and voice. It does not claim to bypass AI detectors or make text "undetectable."
