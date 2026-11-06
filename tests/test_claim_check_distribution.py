"""Offline checks for documented automated distribution, not model behavior."""
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PIN = "4139aff1dd8127fc4c9bb3916a4bc5e3fd5cd23c"


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

    def test_current_source_preserves_prior_bundle_and_adds_change_impact(self):
        imported = json.loads((ROOT / "catalog/modepot-sources.json").read_text())["skills"]
        expected = {row["name"] for row in imported} | {
            "repository-readiness", "decision-brief", "document-actions", "claim-check", "change-impact"}
        actual = {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}
        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), 12)
        self.assertIn("Published v0.4.1 contains ten skills", (ROOT / "README.md").read_text())

    def test_public_replay_manifest_binds_every_installed_file(self):
        path = ROOT / "docs/claim-check-distribution.json"
        self.assertTrue(path.is_file(), "public installer verification record missing")
        record = json.loads(path.read_text())
        self.assertEqual(record["source_commit"], PIN)
        package = ROOT / "skills/claim-check"
        actual = {p.relative_to(package).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in package.rglob("*") if p.is_file()}
        self.assertEqual(actual, record["source_files"])
        self.assertEqual(len(actual), 8)
        self.assertEqual(set(record["agents"]), {"claude-code", "cursor", "codex", "hermes-agent"})
        self.assertTrue(record["lock_ref_verified"])
        self.assertTrue(record["selected_removal_verified"])
        self.assertFalse(record["client_or_model_launched"])


if __name__ == "__main__":
    unittest.main()
