import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "2.1.1"
REPOSITORY = "https://github.com/bartekpucek/miodkuj"


def load_json(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class MarketplaceContractTests(unittest.TestCase):
    def test_claude_plugin_points_to_canonical_skill(self):
        plugin = load_json(Path(".claude-plugin/plugin.json"))
        self.assertEqual(plugin["name"], "miodkuj")
        self.assertEqual(plugin["version"], VERSION)
        self.assertEqual(plugin["repository"], REPOSITORY)
        self.assertEqual(
            plugin["skills"], ["./plugins/miodkuj/skills/miodkuj"]
        )

    def test_claude_marketplace_installs_root_plugin(self):
        marketplace = load_json(Path(".claude-plugin/marketplace.json"))
        self.assertEqual(marketplace["name"], "miodkuj")
        self.assertEqual(len(marketplace["plugins"]), 1)
        entry = marketplace["plugins"][0]
        self.assertEqual(entry["name"], "miodkuj")
        self.assertEqual(entry["source"], "./")
        self.assertEqual(entry["version"], VERSION)

    def test_codex_plugin_points_to_canonical_skills_directory(self):
        plugin = load_json(Path("plugins/miodkuj/.codex-plugin/plugin.json"))
        self.assertEqual(plugin["name"], "miodkuj")
        self.assertEqual(plugin["version"], VERSION)
        self.assertEqual(plugin["repository"], REPOSITORY)
        self.assertEqual(plugin["skills"], "./skills/")
        self.assertEqual(plugin["interface"]["displayName"], "Miodkuj")

    def test_codex_marketplace_installs_payload_plugin(self):
        marketplace = load_json(Path(".agents/plugins/marketplace.json"))
        self.assertEqual(marketplace["name"], "miodkuj")
        self.assertEqual(marketplace["interface"]["displayName"], "Miodkuj")
        self.assertEqual(len(marketplace["plugins"]), 1)
        entry = marketplace["plugins"][0]
        self.assertEqual(entry["name"], "miodkuj")
        self.assertEqual(
            entry["source"],
            {"source": "local", "path": "./plugins/miodkuj"},
        )
        self.assertEqual(entry["policy"], {
            "installation": "AVAILABLE",
            "authentication": "ON_INSTALL",
        })
        self.assertEqual(entry["category"], "Writing")
