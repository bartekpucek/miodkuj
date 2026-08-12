import unittest
from pathlib import Path


README = (Path(__file__).resolve().parents[1] / "README.md").read_text(encoding="utf-8")


class ReadmeInstallationTests(unittest.TestCase):
    def test_platform_chooser_is_before_installation_details(self):
        chooser = README.index("## Wybierz platformę")
        self.assertLess(chooser, README.index("## ChatGPT"))
        for label in ("ChatGPT", "Claude.ai", "Claude Code", "Codex"):
            self.assertIn(label, README[chooser:README.index("## ChatGPT")])

    def test_chatgpt_has_complete_click_path_and_direct_download(self):
        self.assertIn("releases/latest/download/miodkuj.skill", README)
        self.assertIn(
            "**Plugins** → **Skills** → **Create** → **Upload from your computer**",
            README,
        )
        self.assertIn("ChatGPT sprawdzi plik", README)

    def test_claude_ai_has_complete_click_path(self):
        self.assertIn("**Settings** → **Capabilities**", README)
        self.assertIn("**Customize** → **Skills**", README)
        self.assertIn("wykonywanie kodu", README)

    def test_claude_code_marketplace_is_default(self):
        self.assertIn("/plugin marketplace add bartekpucek/miodkuj", README)
        self.assertIn("/plugin install miodkuj@miodkuj", README)
        self.assertIn("/reload-plugins", README)
        self.assertIn("/miodkuj:miodkuj", README)
        self.assertIn("krótkie `/miodkuj`", README)

    def test_codex_marketplace_is_default(self):
        self.assertIn("codex plugin marketplace add bartekpucek/miodkuj", README)
        self.assertIn("codex plugin add miodkuj@miodkuj", README)
        self.assertIn("nowe zadanie", README.casefold())
        self.assertIn("`$miodkuj`", README)

    def test_default_routes_do_not_require_a_clone(self):
        default_part = README[: README.index("### Instalacja ręczna")]
        self.assertNotIn("git clone", default_part)
