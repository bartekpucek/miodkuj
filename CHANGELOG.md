# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/), and this project adheres to
[Semantic Versioning](https://semver.org/).

## [2.0.0] - 2026-08-11

### Changed

- Consolidated the runtime into the portable `miodkuj` skill and release bundle.
- Kept generated runtime references synchronized from `shared/references/`.

### Removed

- Platform-specific runtime copies and Claude plugin manifests.

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
- Two interchangeable delivery targets built from a single source: a Claude /
  Claude Code skill and a Codex / ChatGPT skill (`$stop-slop-pl`).
- Shared Polish reference content in `shared/references/`: slop patterns, register
  rules, plain-Polish guide, voice calibration, scoring/severity, before/after
  examples, and sources.
- `scripts/build.sh` (sync references into both targets + bundle the `.skill`),
  `scripts/validate.sh`, and a stdlib-only `scripts/validate_skill.py`.
- Claude Code plugin and marketplace manifests, MIT license, and documentation
  (`README.md`, `docs/research-summary.md`, `docs/test-scenarios.md`).
- CI workflow that validates both skill targets and guards against reference drift.

[1.1.0]: https://github.com/bartekpucek/stop-slop-PL/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/bartekpucek/stop-slop-PL/releases/tag/v1.0.0
