"""Offline contract checks for the original change-impact skill."""
from pathlib import Path
import re
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "change-impact"


class ChangeImpactBundleTests(unittest.TestCase):
    def test_bundle_and_required_resources_exist(self):
        required = [
            "SKILL.md",
            "assets/impact-template.md",
            "assets/verification-template.md",
            "assets/review-checklist.md",
            "provenance.md",
            "compatibility.md",
        ]
        for item in required:
            with self.subTest(item=item):
                self.assertTrue((SKILL / item).is_file(), f"missing {item}")

    def test_portable_metadata_and_concise_entrypoint(self):
        text = (SKILL / "SKILL.md").read_text()
        self.assertTrue(text.startswith("---\n"))
        lines = text.splitlines()
        closing = lines.index("---", 1)
        frontmatter = "\n".join(lines[1:closing])
        body = "\n".join(lines[closing + 1:])
        parsed = yaml.safe_load(frontmatter)
        self.assertEqual(parsed["name"], "change-impact")
        self.assertEqual(parsed["metadata"], {"version": "0.1.0", "status": "unreleased"})
        self.assertTrue(all(isinstance(v, str) for v in parsed["metadata"].values()))
        self.assertTrue(body.strip())
        self.assertLessEqual(len(body.splitlines()), 150)
        self.assertIn("name: change-impact", frontmatter)
        description = re.search(r"^description: (.+)$", frontmatter, re.M)
        self.assertIsNotNone(description)
        value = description.group(1).strip().strip("'\"")
        self.assertLessEqual(len(value), 60)
        self.assertNotIn("\n", value)
        self.assertRegex(frontmatter, r"(?m)^license: MIT$")
        self.assertRegex(frontmatter, r'(?m)^  version: "0\.1\.0"$')
        for resource in ("impact-template.md", "verification-template.md", "review-checklist.md"):
            self.assertIn(f"assets/{resource}", body)

    def test_procedure_covers_safety_and_contract(self):
        text = (SKILL / "SKILL.md").read_text().lower()
        for term in ("counter-trigger", "readiness", "security review", "potential", "unknown", "not run", "base", "head", "symlink", "outside", "exactly two reports", "no tests by default"):
            with self.subTest(term=term):
                self.assertIn(term, text)

    def test_pinned_inspection_is_safe_and_outputs_are_reopened(self):
        text = (SKILL / "SKILL.md").read_text()
        for term in ["--no-ext-diff", "--no-textconv", "Reopen both", "changes during", "read budget"]:
            self.assertIn(term, text)
        template = (SKILL / "assets/verification-template.md").read_text()
        self.assertIn("## Checks", template)

    def test_preserves_siblings_and_no_fixture_leak(self):
        self.assertEqual(len(list((ROOT / "skills").glob("*/SKILL.md"))), 13)
        bundle = "\n".join(p.read_text() for p in SKILL.rglob("*.md"))
        self.assertNotIn("/Users/", bundle)
        self.assertNotIn("private fixture", bundle.lower())


if __name__ == "__main__":
    unittest.main()
