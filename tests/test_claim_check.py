"""Offline source-contract checks for the original claim-check bundle."""
import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills" / "claim-check"
REQUIRED = (
    "SKILL.md", "assets/review-template.md", "assets/claims-template.md",
    "assets/review-checklist.md", "provenance.md", "compatibility.md",
)


class ClaimCheckBundleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (PACKAGE / "SKILL.md").read_text(encoding="utf-8")

    def test_complete_portable_frontmatter_and_nonblank_body(self):
        lines = self.skill.splitlines()
        self.assertGreaterEqual(len(lines), 4)
        self.assertEqual(lines[0], "---")
        closing = lines.index("---", 1)
        metadata = yaml.safe_load("\n".join(lines[1:closing]))
        self.assertTrue("\n".join(lines[closing + 1:]).strip())
        self.assertEqual(metadata.get("name"), "claim-check")
        self.assertEqual(metadata.get("metadata"), {"version": "0.1.0", "status": "unreleased"})
        self.assertIsInstance(metadata.get("description"), str)
        self.assertLessEqual(len(metadata["description"]), 60)
        self.assertTrue(metadata["description"].strip())
        self.assertLessEqual(len(lines), 180)
        for key in ("version", "status"):
            self.assertIsInstance(metadata["metadata"][key], str)

    def test_required_files_and_local_links_are_self_contained(self):
        for relative in REQUIRED:
            self.assertTrue((PACKAGE / relative).is_file(), relative)
        for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", self.skill):
            self.assertFalse(re.match(r"(?:https?:|#|mailto:)", target))
            self.assertTrue((PACKAGE / target.split("#", 1)[0]).is_file(), target)

    def test_procedure_preserves_output_and_verdict_contract(self):
        text = self.skill.lower()
        for phrase in (
            "review.md", "claims.md", "exactly", "supported", "overstated",
            "contradicted", "unresolved", "source inventory", "coverage map",
            "paragraph", "exclusion", "unchecked", "independent", "reported",
            "proposition", "calculation", "offline", "confidential", "private accounts",
            "public research requires explicit permission", "partial", "dangling symlink", "live symlink",
            "do not overwrite", "publication", "do not access credentials", "hostile",
            "atomic", "counterevidence", "provenance", "cutoff",
        ):
            self.assertIn(phrase, text, phrase)
        for linked in REQUIRED[1:]:
            self.assertIn(linked, self.skill)

    def test_templates_operationalize_provenance_verdict_and_reconciliation(self):
        review = (PACKAGE / "assets/review-template.md").read_text(encoding="utf-8")
        claims = (PACKAGE / "assets/claims-template.md").read_text(encoding="utf-8")
        checklist = (PACKAGE / "assets/review-checklist.md").read_text(encoding="utf-8")
        for value in ("draft version", "cutoff", "source boundary", "coverage map",
                      "paragraph", "claim IDs", "exclusions", "unchecked"):
            self.assertIn(value.lower(), review.lower())
        for value in ("source inventory", "retrieval date", "source version",
                      "quotation", "locator", "verdict", "reason", "counterevidence",
                      "calculation", "unresolved", "minimal proposed correction/action", "limitations"):
            self.assertIn(value.lower(), claims.lower())
        for value in ("event performance", "performed", "independence", "reported finding",
                      "underlying truth", "coverage", "wrong-paragraph", "orphan", "duplicate"):
            self.assertIn(value.lower(), checklist.lower())
        self.assertNotRegex(checklist, r"\bC(?:7|8|11|12)\b", "acceptance rules must not hardcode fixture ledger")

    def test_optional_example_inputs_match_public_authored_packet(self):
        for name in ["draft", "sources"]:
            copied = PACKAGE / f"assets/example-{name}.md"
            self.assertEqual(copied.read_bytes(),
                             (ROOT / f"examples/claim-check-proposal/{name}.md").read_bytes())
            self.assertIn(f"assets/example-{name}.md", self.skill)
        self.assertFalse((PACKAGE / "assets/expected-claims.json").exists())
        self.assertNotIn("examples/claim-check-proposal/claims.md", self.skill)

    def test_original_work_uses_repository_license_and_no_false_claims(self):
        provenance = (PACKAGE / "provenance.md").read_text(encoding="utf-8")
        compatibility = (PACKAGE / "compatibility.md").read_text(encoding="utf-8").lower()
        self.assertIn("mit", provenance.lower())
        self.assertIn("original", provenance.lower())
        for text in (self.skill.lower(), provenance.lower(), compatibility):
            self.assertNotIn("published skill", text)
            self.assertNotIn("model accuracy proven", text)
            self.assertNotIn("runtime verified", text)
        self.assertIn("not established", compatibility)
        self.assertIn("offline", compatibility)


if __name__ == "__main__":
    unittest.main()
