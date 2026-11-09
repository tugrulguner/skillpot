"""Distribution/discovery checks for incident-triage, not agent efficacy."""
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class IncidentTriageDistributionTests(unittest.TestCase):
    def test_current_source_discovery_explains_the_distinct_triage_task(self):
        for name in ["README.md", "catalog/README.md", "website/src/content/docs/index.mdx", "website/public/llms.txt"]:
            text = (ROOT / name).read_text()
            for token in ["incident-triage", "incident-triage-first-use.md", "incident.md", "timeline.md"]:
                self.assertIn(token, text, name)
        self.assertIn("fourteen current-source bundles", (ROOT / "catalog/README.md").read_text())
        self.assertIn("Published v0.4.1 contains ten skills", (ROOT / "README.md").read_text())

    def test_public_installer_manifest_binds_all_selected_files_and_pin(self):
        path = ROOT / "docs/incident-triage-distribution.json"
        self.assertTrue(path.is_file(), "public installer verification record is required")
        record = json.loads(path.read_text())
        package = ROOT / "skills/incident-triage"
        actual = {p.relative_to(package).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in package.rglob("*") if p.is_file()}
        self.assertEqual(actual, record["source_files"])
        self.assertEqual(len(actual), record["files_verified"])
        guide = (ROOT / "docs/incident-triage-first-use.md").read_text()
        first = re.search(r"```sh\n([^\n]+)\n```", guide)
        self.assertIsNotNone(first)
        assert first is not None
        self.assertRegex(first[1], r"^npx skills@1\.7\.6 add https://github\.com/tugrulguner/skillpot/tree/[a-f0-9]{40} --skill incident-triage$")
        self.assertIn(record["source_commit"], first[1])
        self.assertEqual(set(record["agents"]), {"claude-code", "cursor", "codex", "hermes-agent"})
        for field in ["lock_ref_verified", "sibling_preserved", "selected_removal_verified", "no_global_install"]:
            self.assertTrue(record[field])
        self.assertFalse(record["client_or_model_launched"])

    def test_first_use_has_bounded_read_only_task_and_two_reports(self):
        path = ROOT / "docs/incident-triage-first-use.md"
        self.assertTrue(path.is_file(), "selected-skill first-use guide is missing")
        text = path.read_text()
        for token in ["--skill incident-triage", "incident.md", "timeline.md",
                      "not included in published SkillPot v0.4.1", "read-only", "fresh",
                      "assets/example-input.md", "No production", "unknown"]:
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
