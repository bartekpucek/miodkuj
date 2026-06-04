# Stop Slop PL

Stop Slop PL is an open-source Polish writing skill for removing AI-sounding, bureaucratic, generic, or over-polished prose while preserving facts, meaning, and register.

It ships in two interchangeable forms from one repository:

- a **Claude / Claude Code** skill (installable as a plugin or uploaded to claude.ai), and
- a **Codex / ChatGPT** skill (`$polish-anti-slop`).

Both share the same Polish content, so the two versions never drift.

## What It Does

- Rewrites Polish text by default; returns the revised text first.
- Keeps facts, numbers, names, links, citations, quotes, code, and legal references intact.
- Removes common Polish slop: officialese, nominalizations, passive and impersonal fog, genitive chains, fake importance, formulaic contrasts, generic endings, and chatbot residue.
- Adapts to register: plain public Polish, marketing, technical docs, academic/scientific, legal/official, social/newsletter/opinion.
- Can provide an audit, before/after, strict cleanup, plain-Polish simplification, academic cleanup, legal/official cleanup, or voice matching when asked.

It does **not** promise AI-detector evasion, "undetectable" text, academic laundering, or impersonation.

## Repo Layout

```text
.claude-plugin/
  plugin.json          # Claude Code plugin manifest (loads the Claude skill)
  marketplace.json     # lets users add this repo as a plugin marketplace
shared/
  references/          # single source of truth for the Polish content
skills/
  claude/
    polish-anti-slop/  # Claude / Claude Code skill (references synced from shared/)
      SKILL.md
      references/
  codex/
    polish-anti-slop/  # Codex / ChatGPT skill
      SKILL.md
      agents/openai.yaml
      references/
scripts/
  build.sh             # sync shared/references into both skills; build the .skill bundle
  validate.sh          # validate both skills
  validate_skill.py    # portable SKILL.md validator (stdlib only)
docs/
  research-summary.md
  test-scenarios.md
```

## Install for Claude Code

Add the repository as a plugin marketplace, then install the plugin:

```text
/plugin marketplace add bartekpucek/stop-slop-PL
/plugin install stop-slop-pl@stop-slop-pl
```

The skill then triggers automatically on Polish editing requests, or you can call it directly as `/stop-slop-pl:polish-anti-slop`.

## Install for Claude.ai

You can either download the prebuilt bundle or build it yourself.

**Option A — download (no terminal needed):** grab `polish-anti-slop.skill` from the [latest release](https://github.com/bartekpucek/stop-slop-PL/releases/latest), then upload it in **Settings → Capabilities → Skills**.

**Option B — build it yourself:** build the bundle and upload it in **Settings → Capabilities → Skills**:

```bash
./scripts/build.sh
# produces dist/polish-anti-slop.skill
```

## Install for Codex or ChatGPT

Copy or symlink the Codex skill folder into the skills directory your Codex setup uses:

```bash
mkdir -p ~/.codex/skills
ln -s "$(pwd)/skills/codex/polish-anti-slop" ~/.codex/skills/polish-anti-slop
```

Some setups also load personal skills from `~/.agents/skills`:

```bash
mkdir -p ~/.agents/skills
ln -s "$(pwd)/skills/codex/polish-anti-slop" ~/.agents/skills/polish-anti-slop
```

Restart or reload the agent environment so the skill metadata is discovered.

## Usage

```text
Odslopuj ten tekst po polsku, zachowaj sens i fakty:
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

Default behavior: return the revised Polish text first. Diagnostics appear only when requested or when they prevent a risky edit. For audit only, ask for `tylko audyt`.

## Development

The Polish content lives once in `shared/references/`. Edit it there, then sync it into both skill targets and rebuild the bundle:

```bash
./scripts/build.sh      # sync references + build dist/polish-anti-slop.skill
./scripts/validate.sh   # validate both skills
```

Manual pressure tests live in [docs/test-scenarios.md](docs/test-scenarios.md).

## Sources

This skill is based on a source-level audit of anti-slop and humanizer skills plus Polish plain-language, readability, stylometry, and Polish LLM research. See [docs/research-summary.md](docs/research-summary.md) and [references/sources.md](skills/claude/polish-anti-slop/references/sources.md).

## License

MIT. See [LICENSE](LICENSE).
