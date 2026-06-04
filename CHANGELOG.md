# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/), and this project adheres to
[Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-06-04

Initial public release.

### Added
- Polish-language anti-slop writing skill that rewrites AI-sounding, bureaucratic,
  generic, or translated-from-English Polish prose into natural, register-appropriate
  text while preserving facts, numbers, citations, and meaning.
- Two interchangeable delivery targets built from a single source: a Claude /
  Claude Code skill and a Codex / ChatGPT skill (`$polish-anti-slop`).
- Shared Polish reference content in `shared/references/`: slop patterns, register
  rules, plain-Polish guide, voice calibration, scoring/severity, before/after
  examples, and sources.
- `scripts/build.sh` (sync references into both targets + bundle the `.skill`),
  `scripts/validate.sh`, and a stdlib-only `scripts/validate_skill.py`.
- Claude Code plugin and marketplace manifests, MIT license, and documentation
  (`README.md`, `docs/research-summary.md`, `docs/test-scenarios.md`).
- CI workflow that validates both skill targets and guards against reference drift.

[1.0.0]: https://github.com/bartekpucek/stop-slop-PL/releases/tag/v1.0.0
