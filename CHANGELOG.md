# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/), and this project adheres to
[Semantic Versioning](https://semver.org/).

## [2.1.1] - 2026-09-14

### Added

- Contextual guidance for translated word choices, with Edinburgh and accommodation examples and preservation of appropriate technical, figurative, and residence uses ([#2](https://github.com/bartekpucek/miodkuj/issues/2), [#3](https://github.com/bartekpucek/miodkuj/issues/3)).
- Seven manual behavioral scenarios covering Polish-only editing, comparison with an English original, appropriate uses, audit mode, temporary accommodation, residence, and remaining in place.

### Fixed

- Older before/after examples that added unsupported actors, findings, product features, performance claims, or conditions.
- Translation guidance now distinguishes a trip's main focus from an accommodation base, preserves day-trip constraints, and does not equate travelling without driving with excluding car passengers.
- Edit mode returns already-clear text without an unsolicited confirmation note.

## [2.1.0] - 2026-08-12

### Added

- Claude Code and Codex marketplace installation from the public repository.
- Step-by-step ChatGPT and Claude.ai installation instructions.
- Public-repository privacy validation and history cleanup.

### Changed

- All distribution routes now use the one canonical runtime at `plugins/miodkuj/skills/miodkuj/`.
- Documented the invocation difference between `/miodkuj:miodkuj` in Claude Code marketplace installs, `/miodkuj` in manual Claude Code installs, and `$miodkuj` in Codex.

## [2.0.0] - 2026-08-11

### Changed

- Renamed the project and skill to Miodkuj.
- Consolidated Claude, ChatGPT, and Codex distribution into one portable Agent Skill.
- Changed direct invocation to `/miodkuj` in Claude Code and `$miodkuj` in Codex.
- Rewrote installation and usage documentation around the supported platform behavior.

### Removed

- Claude plugin and marketplace packaging, which forced a namespaced slash command.
- Platform-specific duplicate skill directories and the previous project identifiers.

## [1.1.0] - 2026-08-11

### Changed

- Replaced rewrite-first behavior with the minimum effective edit.
- Inferred voice from every applicable draft and treated a supplied voice sample as stronger evidence.
- Added explicit edit, audit, and embedded/file output modes.
- Replaced the numerical quality score with a binary fidelity, voice, register, and mode evaluation.
- Made audit mode quote named patterns without guessing AI authorship.

### Added

- Eight cluster-sensitive Polish pattern families with false-positive guards: faux insight, interpretive metadiscourse, colon reveals, negative listing, synonym cycling, fake-profound endings, formatting slop, and second-hand text protection.
- Portability and specificity checks that ground edits in source material without inventing evidence.
- Nineteen behavioral scenarios, including clean-text and intentional-rhetoric negative controls.
- Repository-level validation for reference synchronization, metadata versions, Codex UI metadata, and the built skill bundle.

### Removed

- The uncalibrated 70-point quality score.
- Research-source material from the runtime skill context; sources now live in `docs/sources.md`.

## [1.0.0] - 2026-06-04

Initial public release.

### Added
- Polish-language anti-slop writing skill that rewrites AI-sounding, bureaucratic,
  generic, or translated-from-English Polish prose into natural, register-appropriate
  text while preserving facts, numbers, citations, and meaning.
- A pre-2.0 layout with two delivery targets built from a single source.
- Shared Polish reference content in `shared/references/`: slop patterns, register
  rules, plain-Polish guide, voice calibration, scoring/severity, before/after
  examples, and sources.
- `scripts/build.sh` (sync references into the pre-2.0 targets + bundle the `.skill`),
  `scripts/validate.sh`, and a stdlib-only `scripts/validate_skill.py`.
- Pre-2.0 plugin and marketplace manifests, MIT license, and documentation
  (`README.md`, `docs/research-summary.md`, `docs/test-scenarios.md`).
- CI workflow that validates the pre-2.0 targets and guards against reference drift.

[2.1.1]: https://github.com/bartekpucek/miodkuj/compare/v2.1.0...v2.1.1
[2.1.0]: https://github.com/bartekpucek/miodkuj/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/bartekpucek/miodkuj/compare/v1.1.0...v2.0.0
[1.1.0]: https://github.com/bartekpucek/miodkuj/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/bartekpucek/miodkuj/releases/tag/v1.0.0
