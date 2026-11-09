"""Bug-repro distribution/discovery checks, not agent performance claims."""
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BugReproDistributionTests(unittest.TestCase):
    def test_first_use_selects_one_immutable_bundle_with_explicit_execution_scope(self):
        path = ROOT / "docs/bug-repro-first-use.md"
        self.assertTrue(path.is_file(), "one-command installation guide required")
        text = path.read_text()
        first = re.search(r"```sh\n([^\n]+)\n```", text)
        self.assertIsNotNone(first)
        assert first is not None
        self.assertRegex(first[1], r"^npx skills@1\.7\.6 add https://github\.com/tugrulguner/skillpot/tree/[0-9a-f]{40} --skill bug-repro$")
        for value in ["not included in published SkillPot v0.4.1", "assets/example-input.md", "explicit", "fresh", "Not reproduced", "Blocked"]:
            self.assertIn(value, text)
        self.assertNotIn("--all", first[1])

    def test_current_source_fourteen_and_stable_ten_remain_separate(self):
        imported = json.loads((ROOT / "catalog/modepot-sources.json").read_text())["skills"]
        names = {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}
        self.assertEqual(names, {row["name"] for row in imported} | {
            "repository-readiness", "decision-brief", "document-actions", "claim-check", "change-impact", "bug-repro", "incident-triage"})
        self.assertEqual(len(names), 14)
        for file in ["README.md", "catalog/README.md", "website/src/content/docs/index.mdx", "website/public/llms.txt"]:
            text = (ROOT / file).read_text()
            self.assertIn("bug-repro", text, file)
            self.assertIn("bug-repro-first-use.md", text, file)
        self.assertIn("Published v0.4.1 contains ten skills", (ROOT / "README.md").read_text())

    def test_public_installer_manifest_binds_the_complete_selected_bundle(self):
        path = ROOT / "docs/bug-repro-distribution.json"
        self.assertTrue(path.is_file(), "actual public installer record required")
        report = json.loads(path.read_text())
        package = ROOT / "skills/bug-repro"
        actual = {p.relative_to(package).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in package.rglob("*") if p.is_file()}
        self.assertEqual(actual, report["source_files"])
        self.assertEqual(len(actual), report["files_verified"])
        self.assertIn("/tree/" + report["source_commit"] + " --skill bug-repro",
                      (ROOT / "docs/bug-repro-first-use.md").read_text())
        for key in ["lock_ref_verified", "sibling_preserved", "selected_removal_verified", "no_global_install"]:
            self.assertTrue(report[key])
        self.assertFalse(report["client_or_model_launched"])
        self.assertEqual(set(report["agents"]), {"claude-code", "cursor", "codex", "hermes-agent"})


if __name__ == "__main__":
    unittest.main()
