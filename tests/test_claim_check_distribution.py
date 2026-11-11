"""Offline checks for documented automated distribution, not model behavior."""
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PIN = "66bad57a0a42a4aec2c5d54feee1df8fb242e166"
ORIGINAL_PIN = "4139aff1dd8127fc4c9bb3916a4bc5e3fd5cd23c"


class ClaimCheckDistributionTests(unittest.TestCase):
    def test_automated_install_is_the_primary_path_and_selects_one_skill(self):
        for name in ["README.md", "docs/quickstart.md"]:
            text = (ROOT / name).read_text()
            first = re.search(r"```sh\n(.*?)\n```", text, re.S)
            self.assertIsNotNone(first)
            assert first is not None
            self.assertIn("npx skills@1.7.6 add", first[1])
            self.assertIn("/tree/v0.4.1", first[1])
            self.assertIn("--skill decision-brief", first[1])
            self.assertNotIn("git clone", first[1])
        text = (ROOT / "README.md").read_text()
        self.assertIn("Advanced: inspect and place", text)

    def test_new_skill_has_separate_pinned_install_and_bundled_inputs(self):
        text = (ROOT / "docs/claim-check-first-use.md").read_text()
        first = re.search(r"```sh\n(.*?)\n```", text, re.S)
        self.assertIsNotNone(first)
        assert first is not None
        self.assertIn("/tree/" + PIN + " --skill claim-check", first[1])
        self.assertNotRegex(first[1], r"(?m)^\s*(?:cp|mkdir|git clone)\b")
        self.assertIn("not included in published SkillPot v0.4.1", text)
        for asset in ["example-draft.md", "example-sources.md"]:
            self.assertIn("assets/" + asset, text)
        self.assertNotIn("still being integrated", text)
        self.assertNotIn("--all", first[1])

    def test_current_source_fifteen_and_stable_ten_remain_separate(self):
        imported = json.loads((ROOT / "catalog/modepot-sources.json").read_text())["skills"]
        expected = {row["name"] for row in imported} | {
            "repository-readiness", "decision-brief", "document-actions", "claim-check", "change-impact", "bug-repro", "incident-triage", "benchmark-audit"}
        actual = {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}
        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), 15)
        self.assertIn("Published v0.4.1 contains ten skills", (ROOT / "README.md").read_text())

    def test_original_public_replay_record_is_preserved_separately_from_current_matrix(self):
        path = ROOT / "docs/claim-check-distribution.json"
        self.assertTrue(path.is_file(), "original public installer record missing")
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), "3b1eefd22ed52ef53d595bd8e104d7494c0e1f7c0a768226e86dccde33cbac5a")
        record = json.loads(path.read_text())
        self.assertEqual(record["source_commit"], ORIGINAL_PIN)
        self.assertEqual(len(record["source_files"]), 8)
        # Current-byte equality is enforced for ALL bundles by test_collection_hardening.
        matrix = json.loads((ROOT / "docs/skill-hardening-distribution.json").read_text())
        self.assertEqual(matrix["source_commit"], PIN)
        self.assertEqual(len([r for r in matrix["skills"] if r["name"] == "claim-check"]), 1)
        self.assertEqual(set(record["agents"]), {"claude-code", "cursor", "codex", "hermes-agent"})
        self.assertTrue(record["lock_ref_verified"])
        self.assertTrue(record["selected_removal_verified"])
        self.assertFalse(record["client_or_model_launched"])


if __name__ == "__main__":
    unittest.main()
