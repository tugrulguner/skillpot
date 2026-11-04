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
        self.assertEqual(meta["metadata"], {"version": "0.1.2", "maintainer": "tugrulguner", "status": "unreleased"})
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

    def test_review_retains_known_historical_fields(self):
        skill = (PACKAGE / "SKILL.md").read_text()
        template = (PACKAGE / "assets/actions-template.md").read_text()
        self.assertIn("Preserve known owners in historical items", skill)
        self.assertIn("named possessive", skill)
        checklist = (PACKAGE / "assets/review-checklist.md").read_text()
        self.assertIn("possessive phrase", checklist)
        historical = template.split("## Historical items", 1)[1].split("## Unresolved items", 1)[0]
        for field in ["- Owner:", "- Due text (verbatim):", "- Reported completion/cancellation time:"]:
            self.assertIn(field, historical)

    def test_status_conflict_has_one_canonical_record(self):
        skill = (PACKAGE / "SKILL.md").read_text()
        template = (PACKAGE / "assets/actions-template.md").read_text()
        self.assertIn("one canonical record per underlying item", skill)
        self.assertIn("not a second historical or outstanding record", skill)
        self.assertIn("Place this item only here", template)

    def test_status_and_approval_role_are_field_level_and_explicit(self):
        skill = (PACKAGE / "SKILL.md").read_text().lower()
        template = (PACKAGE / "assets/actions-template.md").read_text().lower()
        checklist = (PACKAGE / "assets/review-checklist.md").read_text().lower()
        self.assertIn("no completion report means status is", skill)
        self.assertIn("use `incomplete` only when the", skill)
        self.assertIn("approval role:", template)
        self.assertIn("approver (named person):", template)
        self.assertIn("an approver/proposer is not an", skill)
        self.assertIn("source-known approval role", checklist)
        self.assertIn("unnamed individual `unknown`", checklist)
        self.assertIn("do not infer", checklist)

    def test_refusal_requests_new_location_and_checklist_is_linked(self):
        skill = (PACKAGE / "SKILL.md").read_text()
        self.assertIn("name the colliding targets and request a fresh approved location", skill)
        self.assertIn("assets/review-checklist.md", skill)
        self.assertTrue((PACKAGE / "assets/review-checklist.md").is_file())

    def test_requirement_cannot_be_replaced_by_question_or_coverage_note(self):
        skill = (PACKAGE / "SKILL.md").read_text()
        template = (PACKAGE / "assets/actions-template.md").read_text()
        self.assertIn("A question or coverage note is not a substitute", skill)
        self.assertIn("Conflicting owners or deadlines alone do not change", skill)
        self.assertIn("Source-item map:", template)
        self.assertIn("questions cannot replace a record", template)

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
