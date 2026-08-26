import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PackagingTests(unittest.TestCase):
    def read_json(self, relative_path: str) -> dict:
        return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))

    def test_platform_manifest_versions_match(self) -> None:
        codex = self.read_json("plugins/forms-responder/.codex-plugin/plugin.json")
        claude = self.read_json("plugins/forms-responder/.claude-plugin/plugin.json")
        gemini = self.read_json("gemini-extension.json")
        marketplace = self.read_json(".claude-plugin/marketplace.json")

        base_version = codex["version"].split("+", 1)[0]
        self.assertEqual(base_version, claude["version"])
        self.assertEqual(base_version, gemini["version"])
        self.assertEqual(base_version, marketplace["plugins"][0]["version"])
        self.assertEqual("forms-responder", codex["name"])
        self.assertEqual("forms-responder", claude["name"])
        self.assertEqual("forms-responder", gemini["name"])

    def test_generated_skill_packages_have_no_drift(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/sync_skill_packages.py"), "check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
