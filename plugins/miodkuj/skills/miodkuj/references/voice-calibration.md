# Polish Voice Calibration

Use this for every personal, marketing, newsletter, social, or opinion edit. Infer a working voice profile from the draft itself. If the user supplies a separate writing sample, treat it as stronger evidence of voice than the draft being repaired.

## Fingerprint The Draft

Choose three to five signals that most distinguish this writer. Do not regularize the text before identifying them.

Look for:

- pronouns and address: `ja`, `my`, `ty`, `Pan`, `Pani`, `Państwo`,
- sentence length and tolerance for fragments,
- paragraph length,
- punctuation habits,
- directness or softness,
- formality,
- use of slang, idioms, or regional flavor,
- first-person opinions,
- favorite connectors,
- appetite for examples,
- level of warmth or bluntness,
- useful repetition and favorite terms,
- fragments, asides, self-corrections, and digressions,
- mixed feelings or unresolved tension,
- profanity or deliberate informality,
- stable domain vocabulary,
- intentional punctuation, including dashes, ellipses, parentheses, or sentence fragments.

## Separate Voice Sample

- Use a supplied sample to distinguish the writer's habits from defects in the draft.
- Match only traits supported by the sample; do not copy its subject matter, facts, jokes, or opinions.
- Preserve roughly the sample's punctuation and rhythm when they do not conflict with an explicit user constraint.
- Let fidelity, legal force, scientific uncertainty, and protected spans outrank voice matching.

## Rewrite Rules

- Match the sample before generic anti-slop preferences.
- Preserve the user's stance and degree of certainty.
- Keep the same relationship with the reader.
- Remove AI residue without polishing away the person's edge.
- Do not add slang unless the sample uses it.
- Do not add jokes, vulnerability, or attitude that the sample does not support.
- Preserve intentional roughness if it makes the voice recognizable.
- Keep useful repetition when it creates emphasis, cohesion, or a recognizable verbal habit.
- Keep fragments, asides, self-corrections, mixed feelings, profanity, and domain language when they are clear and characteristic.
- Do not make every paragraph equally tidy or force the same sentence pattern throughout the piece.

## Quick Voice Labels

Use labels internally, not necessarily in output:

- `krótko i twardo`: short, blunt, little connective tissue.
- `ciepło i prosto`: direct but friendly, good for public communication.
- `ekspercko bez patosu`: confident, precise, no inflated authority.
- `urzędowo jasno`: formal enough for institutions, readable for citizens.
- `akademicko ostrożnie`: precise, hedged where evidence requires it.
- `newsletterowo`: specific, conversational, a little uneven.

## Integrity Check

After rewriting, ask:

- Would this person actually write this sentence?
- Did I keep their level of formality?
- Did I preserve their rhythm?
- Did I remove too much texture?
- Did I add new claims or examples?
