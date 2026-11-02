import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills" / "document-actions"


class DocumentActionsContractTests(unittest.TestCase):
    def test_frontmatter_is_portable_and_has_flat_metadata(self):
        text = (PACKAGE / "SKILL.md").read_text()
        match = re.fullmatch(r"---\n(.*?)\n---\n(.+)", text, re.DOTALL)
        self.assertIsNotNone(match)
        assert match is not None
        meta = yaml.safe_load(match[1])
        self.assertEqual(meta["name"], "document-actions")
        self.assertLessEqual(len(meta["description"]), 60)
        self.assertTrue(meta["description"].endswith("."))
        self.assertIn("compatibility", meta)
        self.assertEqual(meta["metadata"], {"version": "0.1.0", "maintainer": "tugrulguner", "status": "unreleased"})
        self.assertTrue(match[2].strip())

    def test_procedure_covers_extraction_categories_and_safety_contract(self):
        text = (PACKAGE / "SKILL.md").read_text().lower()
        required = (
            "assigned action", "unassigned requirement", "proposal", "completed", "cancelled",
            "acceptance", "condition", "unknown", "conflicting", "source citation",
            "partial", "actions.md", "questions.md", "untrusted", "existing",
            "symlink", "no date normalization", "external", "install",
        )
        for phrase in required:
            self.assertIn(phrase, text, phrase)
        self.assertIn("questions.md", text)

    def test_self_contained_templates_provenance_compatibility(self):
        for name in ("assets/actions-template.md", "assets/questions-template.md", "provenance.md", "compatibility.md"):
            self.assertTrue((PACKAGE / name).is_file(), name)
        skill = (PACKAGE / "SKILL.md").read_text()
        self.assertIn("actions-template.md", skill)
        self.assertIn("questions-template.md", skill)
        provenance = (PACKAGE / "provenance.md").read_text()
        self.assertIn("github/awesome-copilot", provenance)
        self.assertIn("googleworkspace/cli", provenance)
        self.assertIn("microsoft/skills", provenance)
        self.assertIn("No text, template, or code is copied or adapted", provenance)
        compatibility = (PACKAGE / "compatibility.md").read_text().lower()
        self.assertIn("offline", compatibility)
        self.assertIn("not established", compatibility)

    def test_template_separates_categories_assignment_and_acceptance(self):
        template = (PACKAGE / "assets/actions-template.md").read_text()
        sections = ["## Outstanding actions and requirements", "## Proposals", "## Historical items", "## Unresolved items"]
        positions = [template.index(section) for section in sections]
        self.assertEqual(positions, sorted(positions))
        for field in ["Assignment:", "Acceptance:", "Due text (verbatim):", "Source citation"]:
            self.assertIn(field, template)
        questions = (PACKAGE / "assets/questions-template.md").read_text()
        self.assertIn("Why it matters:", questions)
        self.assertIn("None identified within the supplied", questions)

    def test_package_local_markdown_links_resolve(self):
        self.assertTrue((PACKAGE / "SKILL.md").is_file())
        for md in PACKAGE.rglob("*.md"):
            for target in re.findall(r"\[[^]]*\]\(([^)]+)\)", md.read_text()):
                if "://" not in target and not target.startswith("#"):
                    destination = (md.parent / target.split("#", 1)[0]).resolve()
                    if PACKAGE.resolve() in destination.parents or destination == PACKAGE.resolve():
                        self.assertTrue(destination.is_file(), f"{md}: {target}")


if __name__ == "__main__":
    unittest.main()
