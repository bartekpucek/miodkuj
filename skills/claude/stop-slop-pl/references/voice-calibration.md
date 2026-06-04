# Polish Voice Calibration

Use this when the user supplies a writing sample or asks to match a voice.

## Fingerprint The Sample

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
- level of warmth or bluntness.

## Rewrite Rules

- Match the sample before generic anti-slop preferences.
- Preserve the user's stance and degree of certainty.
- Keep the same relationship with the reader.
- Remove AI residue without polishing away the person's edge.
- Do not add slang unless the sample uses it.
- Do not add jokes, vulnerability, or attitude that the sample does not support.
- Preserve intentional roughness if it makes the voice recognizable.

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
