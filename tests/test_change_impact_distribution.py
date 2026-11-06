"""Current-source discovery and installer contracts; not task efficacy tests."""
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ChangeImpactDistributionTests(unittest.TestCase):
    def test_separate_immutable_one_skill_install_and_complete_resources(self):
        guide = ROOT / "docs/change-impact-first-use.md"
        self.assertTrue(guide.is_file(), "new skill needs one-command first-use guidance")
        text = guide.read_text()
        command = re.search(r"```sh\n([^\n]+)\n```", text)
        self.assertIsNotNone(command)
        assert command is not None
        self.assertRegex(command[1], r"^npx skills@1\.7\.6 add https://github\.com/tugrulguner/skillpot/tree/[0-9a-f]{40} --skill change-impact$")
        self.assertNotIn("--all", command[1])
        self.assertIn("not included in published SkillPot v0.4.1", text)
        self.assertIn("assets/example-input.md", text)
        self.assertIn("not native activation", text)
        for name in ["impact.md", "verification.md", "Not run", "fresh", "offline"]:
            self.assertIn(name, text)

    def test_public_distribution_manifest_matches_exact_bundle_and_source_pin(self):
        path = ROOT / "docs/change-impact-distribution.json"
        self.assertTrue(path.is_file(), "real public installer record is required")
        record = json.loads(path.read_text())
        package = ROOT / "skills/change-impact"
        actual = {p.relative_to(package).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in package.rglob("*") if p.is_file()}
        self.assertEqual(actual, record["source_files"])
        self.assertEqual(len(actual), record["files_verified"])
        self.assertEqual(len(actual), 7)
        self.assertIn("/tree/" + record["source_commit"] + " --skill change-impact",
                      (ROOT / "docs/change-impact-first-use.md").read_text())
        for field in ["lock_ref_verified", "selected_removal_verified", "sibling_preserved", "no_global_install"]:
            self.assertTrue(record[field])
        self.assertFalse(record["client_or_model_launched"])
        self.assertEqual(set(record["agents"]), {"claude-code", "cursor", "codex", "hermes-agent"})

    def test_current_source_twelve_stable_ten_and_new_task_discoverable(self):
        expected = {row["name"] for row in json.loads((ROOT / "catalog/modepot-sources.json").read_text())["skills"]}
        expected |= {"repository-readiness", "decision-brief", "document-actions", "claim-check", "change-impact"}
        actual = {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}
        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), 12)
        for name in ["README.md", "catalog/README.md", "website/src/content/docs/index.mdx", "website/public/llms.txt"]:
            text = (ROOT / name).read_text()
            for value in ["change-impact", "change-impact-first-use.md", "impact.md", "verification.md"]:
                self.assertIn(value, text, name)
        self.assertIn("Published v0.4.1 contains ten skills", (ROOT / "README.md").read_text())


if __name__ == "__main__":
    unittest.main()
