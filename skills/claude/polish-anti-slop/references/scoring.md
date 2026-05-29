# Scoring And Severity

Use scoring internally. Show it only when the user asks for an audit, diagnostics, or before/after analysis.

## Red, Yellow, Green

Red issues:

- chatbot residue,
- fabricated or unsupported facts,
- broken register,
- obvious boilerplate intros or endings,
- generic "AI essay" structure,
- protected spans changed.

Yellow issues:

- repeated officialese,
- inflated adjectives without proof,
- nominalization clusters,
- repeated passive or impersonal fog,
- formulaic contrast structures,
- generic nouns replacing concrete actors.

Green issues:

- one-off weak words,
- slightly too even rhythm,
- mild abstraction,
- small missed opportunities for directness.

## Internal Score

Score 0 to 10:

- `Bezpośredniość`: statements over announcements.
- `Konkret`: actors, examples, facts, constraints.
- `Naturalność polszczyzny`: idiomatic Polish, not translated English or officialese.
- `Rytm`: sentence and paragraph variation without theatrics.
- `Rejestr`: matches genre and audience.
- `Gęstość`: every sentence earns its place.
- `Wierność`: facts and nuance preserved.

Thresholds:

- 60 to 70: publishable.
- 48 to 59: acceptable but needs another pass.
- below 48: rewrite again.

## Audit Output Format

When diagnostics are requested, keep them short:

```text
Najważniejsze zmiany:
- Usunąłem urzędowe nominalizacje.
- Zamieniłem bierne formy na aktora i czasownik.
- Zachowałem liczby, cytaty i linki.
```

For audit only:

```text
Audyt:
- Red: ...
- Yellow: ...
- Green: ...
```

Do not bury the revised text under long explanation unless the user asks for critique.
