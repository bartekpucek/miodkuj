# Stop Slop PL

Stop Slop PL is an open-source Polish writing skill for removing AI-sounding, bureaucratic, generic, or over-polished prose while preserving facts, meaning, and register.

The v1 package contains a Codex/ChatGPT skill named `$polish-anti-slop`. A Claude/Claude Code version can be added later without changing the repo layout.

## What It Does

- Rewrites Polish text by default.
- Keeps facts, numbers, names, links, citations, quotes, code, and legal references intact.
- Removes common Polish slop patterns: officialese, nominalizations, passive and impersonal fog, genitive chains, fake importance, formulaic contrasts, generic endings, and chatbot residue.
- Adapts to register: plain public Polish, marketing, technical docs, academic/scientific, legal/official, social/newsletter/opinion.
- Can provide an audit, before/after, strict cleanup, plain Polish simplification, academic cleanup, legal/official cleanup, or voice matching when asked.

It does not promise AI-detector evasion, "undetectable" text, academic laundering, or impersonation.

## Repo Layout

```text
skills/
  codex/
    polish-anti-slop/
      SKILL.md
      agents/openai.yaml
      references/
docs/
  research-summary.md
  test-scenarios.md
```

## Install for Codex or ChatGPT Skill Workflows

Copy or symlink the skill folder into the skills directory used by your Codex setup.

Common local targets:

```bash
mkdir -p ~/.codex/skills
ln -s [REDACTED] ~/.codex/skills/polish-anti-slop
```

Some Codex setups also load personal skills from:

```bash
mkdir -p ~/.agents/skills
ln -s [REDACTED] ~/.agents/skills/polish-anti-slop
```

After installing, restart or reload the agent environment so the skill metadata is discovered.

## Usage

Examples:

```text
Use $polish-anti-slop to odslopuj ten tekst po polsku:
W celu dokonania zgłoszenia należy wypełnić niniejszy formularz.
```

```text
Zhumanizuj po polsku ten fragment, bez zmiany faktów:
...
```

```text
Usuń AI-owy styl i urzędowe lanie wody. Pokaż też krótką listę zmian:
...
```

Default behavior: return the revised Polish text first. Diagnostics appear only when requested or when they prevent a risky edit.

## Validation

Validate the skill metadata:

```bash
python3 [REDACTED] [REDACTED]
```

Manual pressure tests live in [docs/test-scenarios.md](docs/test-scenarios.md).

## Sources

This skill is based on a source-level audit of anti-slop and humanizer skills plus Polish plain-language, readability, stylometry, and Polish LLM research. See [docs/research-summary.md](docs/research-summary.md) and [skills/codex/polish-anti-slop/references/sources.md](skills/codex/polish-anti-slop/references/sources.md).

## License

MIT.
