"""Source-contract checks for the portable bug-repro skill."""
from pathlib import Path
import re
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "bug-repro"


class BugReproSkillTests(unittest.TestCase):
    def test_standalone_skill_metadata_and_linked_resources(self):
        text = (SKILL / "SKILL.md").read_text()
        self.assertTrue(text.startswith("---\n"))
        match = re.search(r"\n---\n", text[4:])
        self.assertIsNotNone(match)
        assert match is not None
        frontmatter = text[4:4 + match.start()]
        parsed = yaml.safe_load(frontmatter)
        self.assertEqual(parsed["name"], "bug-repro")
        self.assertEqual(parsed["metadata"], {"version": "0.1.0", "status": "unreleased"})
        self.assertTrue(all(isinstance(v, str) for v in parsed["metadata"].values()))
        description = re.search(r"^description:\s*(.+)$", frontmatter, re.M).group(1).strip('"\'')
        self.assertLessEqual(len(description), 60)
        self.assertIn("0.1.0", frontmatter)
        self.assertIn("status: unreleased", frontmatter)
        self.assertTrue(text[4 + match.end():].strip())
        for name in ("repro-template.md", "reduction-log-template.md", "review-checklist.md"):
            self.assertTrue((SKILL / "assets" / name).is_file(), name)
            self.assertIn(name, text)
        for name in ("provenance.md", "compatibility.md"):
            self.assertTrue((SKILL / name).is_file(), name)
            self.assertIn(name, text)

    def test_practice_input_is_self_contained_without_expected_answers(self):
        path = SKILL / "assets/example-input.md"
        self.assertTrue(path.is_file(), "practice needs installed inputs")
        text = path.read_text()
        for name in ["bug-report.md", "buggy.py"]:
            source = (ROOT / "examples/bug-repro" / name).read_text()
            self.assertIn(source, text)
        self.assertNotIn("regression_bug.json", text)
        self.assertNotIn("# Reproduction report:", text)
        self.assertIn("assets/example-input.md", (SKILL / "SKILL.md").read_text())

    def test_one_report_name_and_non_circular_baseline_setup(self):
        text = (SKILL / "SKILL.md").read_text()
        self.assertIn("`repro.md`", text)
        self.assertNotIn("minimumrepro.md", text)
        self.assertIn("baseline probe", text)
        self.assertIn("`reproduce.py`", text)
        self.assertIn("`test_regression.py`", text)
        self.assertIn("reopen", text.lower())
        template = (SKILL / "assets/repro-template.md").read_text()
        self.assertIn("`repro.md`", template)

    def test_procedure_preserves_safety_and_evidence_contract(self):
        text = (SKILL / "SKILL.md").read_text().lower()
        for phrase in (
            "fresh external", "dangling symlink", "preserve", "not reproduced", "blocked",
            "known-bug", "negative control", "exact final", "input hash", "explicit permission",
            "target source", "privacy", "incomplete candidate", "source equivalence",
        ):
            self.assertIn(phrase, text, phrase)
        self.assertIn("do not use for", text)
        self.assertLessEqual(len((SKILL / "SKILL.md").read_text().splitlines()), 150)


if __name__ == "__main__":
    unittest.main()
