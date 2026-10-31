"""Offline worked-example integrity, not agent behavior or decision quality."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/decision-brief"


class DecisionBriefExampleTests(unittest.TestCase):
    def run_checker(self, root):
        self.assertTrue((EXAMPLE / "verify.py").is_file(), "portable example verifier is missing")
        return subprocess.run([sys.executable, str(EXAMPLE / "verify.py"), "--root", str(root)],
                              capture_output=True, text=True)

    def test_published_example_is_offline_and_inspectable(self):
        result = self.run_checker(EXAMPLE)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["kind"], "offline-example-integrity")
        self.assertFalse(report["network_used"])
        self.assertEqual(report["failure_cases"], 4)

    def test_unknown_claim_reference_is_rejected(self):
        self.assertTrue(EXAMPLE.is_dir(), "worked example is missing")
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "example"
            shutil.copytree(EXAMPLE, target)
            path = target / "brief.md"
            path.write_text(path.read_text().replace("[C1]", "[C999]"))
            result = self.run_checker(target)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unknown claim", result.stdout)

    def test_changed_excerpt_is_rejected(self):
        self.assertTrue(EXAMPLE.is_dir(), "worked example is missing")
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "example"
            shutil.copytree(EXAMPLE, target)
            path = target / "sources.json"
            data = json.loads(path.read_text())
            data["sources"][0]["excerpt"] += " forged addition"
            path.write_text(json.dumps(data))
            result = self.run_checker(target)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("excerpt hash mismatch", result.stdout)


if __name__ == "__main__":
    unittest.main()
