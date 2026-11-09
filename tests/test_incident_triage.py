"""Offline source-contract checks for the incident-triage skill."""
from pathlib import Path
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills" / "incident-triage"
REQUIRED = (
    "SKILL.md", "assets/incident-template.md", "assets/timeline-template.md",
    "assets/review-checklist.md", "provenance.md", "compatibility.md",
)


class IncidentTriageTests(unittest.TestCase):
    def test_metadata_and_required_resources_are_available(self):
        for relative in REQUIRED:
            self.assertTrue((PACKAGE / relative).is_file(), relative)
        text = (PACKAGE / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        lines = text.splitlines()
        closing = lines.index("---", 1)
        metadata = yaml.safe_load("\n".join(lines[1:closing]))
        self.assertEqual(metadata["name"], "incident-triage")
        self.assertEqual(metadata["metadata"]["version"], "0.1.0")
        self.assertEqual(metadata["metadata"], {"version": "0.1.0", "status": "unreleased"})
        self.assertTrue(all(isinstance(v, str) for v in metadata["metadata"].values()))
        self.assertLessEqual(len(metadata["description"]), 60)
        self.assertTrue("\n".join(lines[closing + 1:]).strip())
        self.assertLessEqual(len(lines), 150)
        for relative in REQUIRED[1:]:
            self.assertIn(relative, text)

    def test_installed_practice_packet_contains_inputs_not_authored_answers(self):
        path = PACKAGE / "assets/example-input.md"
        self.assertTrue(path.is_file(), "standalone practice inputs are required")
        text = path.read_text()
        for name in ["case.md", "ci-excerpt.log", "source-lines.json"]:
            self.assertIn((ROOT / "examples/incident-triage/sources" / name).read_text(), text)
        self.assertNotIn("## Evidence-supported finding", text)
        self.assertNotIn("authored_countercases", text)
        self.assertIn("assets/example-input.md", (PACKAGE / "SKILL.md").read_text())

    def test_portable_fields_and_checkout_identity_are_not_misrepresented(self):
        text = (PACKAGE / "SKILL.md").read_text()
        closing = text.splitlines().index("---", 1)
        data = yaml.safe_load("\n".join(text.splitlines()[1:closing]))
        self.assertLessEqual(set(data), {"name", "description", "license", "metadata", "compatibility", "allowed-tools"})
        self.assertNotIn("a synthetic merge is not an actual checkout", text)

    def test_procedure_covers_evidence_permissions_and_honest_timeline(self):
        if not (PACKAGE / "SKILL.md").is_file():
            self.skipTest("skill entry point not created yet")
        text = (PACKAGE / "SKILL.md").read_text(encoding="utf-8").lower()
        for phrase in (
            "exactly `incident.md` and `timeline.md`", "fresh external", "dangling symlink",
            "read-only", "read budget", "source roots", "untrusted", "synthetic merge",
            "not reproduced", "incomplete", "blocked", "timezone", "partial ordering",
            "do not export raw logs by default", "explicit commands", "never automatically retry",
            "do not use for performance investigation", "bug-repro", "full postmortems",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)
        for path in ("assets/incident-template.md", "assets/timeline-template.md", "assets/review-checklist.md"):
            self.assertIn(path, text)


if __name__ == "__main__":
    unittest.main()
