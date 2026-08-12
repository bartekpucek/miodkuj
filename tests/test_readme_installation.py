import re
import unittest
from pathlib import Path


README = (Path(__file__).resolve().parents[1] / "README.md").read_text(encoding="utf-8")
DOWNLOAD_URL = (
    "https://github.com/bartekpucek/miodkuj/"
    "releases/latest/download/miodkuj.skill"
)
FIRST_USE = "`Użyj Miodkuj, aby poprawić ten tekst: …`"


def markdown_section(markdown: str, heading: str) -> str:
    heading_line = f"{heading}\n"
    start = markdown.index(heading_line)
    body_start = start + len(heading_line)
    level = len(heading) - len(heading.lstrip("#"))
    next_heading = re.search(rf"(?m)^#{{1,{level}}} ", markdown[body_start:])
    end = len(markdown) if next_heading is None else body_start + next_heading.start()
    return markdown[start:end]


def fenced_commands(section: str, language: str) -> tuple[str, ...]:
    opening = f"```{language}\n"
    start = section.index(opening) + len(opening)
    end = section.index("\n```", start)
    return tuple(section[start:end].splitlines())


CHATGPT = markdown_section(README, "## ChatGPT")
CLAUDE_AI = markdown_section(README, "## Claude.ai")
CLAUDE_CODE = markdown_section(README, "## Claude Code")
CLAUDE_MANUAL_HEADING = "### Instalacja ręczna z krótkim `/miodkuj`"
CLAUDE_DEFAULT = CLAUDE_CODE[: CLAUDE_CODE.index(CLAUDE_MANUAL_HEADING)]
CLAUDE_MANUAL = markdown_section(README, CLAUDE_MANUAL_HEADING)
CODEX = markdown_section(README, "## Codex")


class ReadmeInstallationTests(unittest.TestCase):
    def test_platform_chooser_is_before_installation_details(self):
        chooser = README.index("## Wybierz platformę")
        self.assertLess(chooser, README.index("## ChatGPT"))
        for label in ("ChatGPT", "Claude.ai", "Claude Code", "Codex"):
            self.assertIn(label, README[chooser : README.index("## ChatGPT")])

    def test_chatgpt_has_complete_installation_and_caveats(self):
        self.assertIn(DOWNLOAD_URL, CHATGPT)
        self.assertIn(
            "**Plugins** → **Skills** → **Create** → **Upload from your computer**",
            CHATGPT,
        )
        self.assertIn("ChatGPT sprawdzi plik", CHATGPT)
        self.assertIn("https://chatgpt.com/skills", CHATGPT)
        self.assertIn(FIRST_USE, CHATGPT)
        self.assertIn("Business, Enterprise, Healthcare i Edu", CHATGPT)
        self.assertIn("Na kontach Enterprise i Edu administrator", CHATGPT)
        self.assertIn("korzystać ze Skills i przesyłać pliki", CHATGPT)
        self.assertIn(
            "sprawdź plan i ustawienia administratora",
            CHATGPT,
        )
        self.assertIn(
            "https://help.openai.com/en/articles/20001066-skills-in-chatgpt",
            CHATGPT,
        )
        self.assertIn("ChatGPT może też wybrać Miodkuj automatycznie", CHATGPT)
        self.assertIn("Nie używaj tutaj polecenia slash", CHATGPT)

    def test_claude_ai_has_complete_installation_and_caveats(self):
        self.assertIn(DOWNLOAD_URL, CLAUDE_AI)
        self.assertIn("planu Free, Pro lub Max", CLAUDE_AI)
        self.assertIn("**Settings** → **Capabilities**", CLAUDE_AI)
        self.assertIn("wykonywanie kodu i tworzenie plików", CLAUDE_AI)
        self.assertIn("planie Team lub Enterprise", CLAUDE_AI)
        self.assertIn("właściciel organizacji musi sprawdzić", CLAUDE_AI)
        self.assertIn("**Organization settings** → **Skills**", CLAUDE_AI)
        self.assertIn(
            "czy włączone są **Code execution and file creation** oraz **Skills**",
            CLAUDE_AI,
        )
        self.assertIn("**Customize** → **Skills**", CLAUDE_AI)
        self.assertIn("skill jest włączony", CLAUDE_AI)
        self.assertIn(FIRST_USE, CLAUDE_AI)
        self.assertIn(
            "https://support.claude.com/en/articles/12512180-use-skills-in-claude",
            CLAUDE_AI,
        )
        self.assertIn("Claude.ai może wybrać Miodkuj automatycznie", CLAUDE_AI)
        self.assertIn("Nie używaj tutaj polecenia slash", CLAUDE_AI)

    def test_claude_code_marketplace_is_default(self):
        self.assertEqual(
            fenced_commands(CLAUDE_DEFAULT, "text"),
            (
                "/plugin marketplace add bartekpucek/miodkuj",
                "/plugin install miodkuj@miodkuj",
                "/reload-plugins",
            ),
        )
        self.assertIn("`/miodkuj:miodkuj`", CLAUDE_DEFAULT)
        self.assertIn("Claude Code dopisuje nazwę pluginu", CLAUDE_DEFAULT)
        self.assertIn("nie daje krótkiego `/miodkuj`", CLAUDE_DEFAULT)
        self.assertIn("https://code.claude.com/docs/en/discover-plugins", CLAUDE_DEFAULT)

    def test_claude_manual_installation_is_explicit_and_scoped(self):
        self.assertIn("Potrzebujesz programu Git", CLAUDE_MANUAL)
        commands = fenced_commands(CLAUDE_MANUAL, "bash")
        self.assertEqual(
            commands,
            (
                'miodkuj_tmp="$(mktemp -d)"',
                "git clone --depth 1 https://github.com/bartekpucek/miodkuj.git "
                '"$miodkuj_tmp"',
                "mkdir -p ~/.claude/skills",
                'cp -R "$miodkuj_tmp/skills/miodkuj" ~/.claude/skills/miodkuj',
                'rm -rf "$miodkuj_tmp"',
            ),
        )
        self.assertEqual(commands[-1], 'rm -rf "$miodkuj_tmp"')
        self.assertIn("kopiują z niego tylko folder `skills/miodkuj`", CLAUDE_MANUAL)
        self.assertIn("Po instalacji użyj `/miodkuj`", CLAUDE_MANUAL)
        self.assertIn("https://code.claude.com/docs/en/slash-commands", CLAUDE_MANUAL)

    def test_codex_marketplace_is_default(self):
        self.assertEqual(
            fenced_commands(CODEX, "bash"),
            (
                "codex plugin marketplace add bartekpucek/miodkuj",
                "codex plugin add miodkuj@miodkuj",
            ),
        )
        self.assertIn("nowe zadanie", CODEX.casefold())
        self.assertIn("`$miodkuj`", CODEX)
        self.assertIn("Codex może też wybrać skill automatycznie", CODEX)

    def test_no_default_route_requires_a_clone(self):
        default_routes = {
            "ChatGPT": CHATGPT,
            "Claude.ai": CLAUDE_AI,
            "Claude Code": CLAUDE_DEFAULT,
            "Codex": CODEX,
        }
        for platform, section in default_routes.items():
            with self.subTest(platform=platform):
                self.assertNotIn("git clone", section)
