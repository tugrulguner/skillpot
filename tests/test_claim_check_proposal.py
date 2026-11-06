"""Consistency of authored proposal fixtures, not agent correctness evidence."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/claim-check-proposal"


class ClaimCheckProposalTests(unittest.TestCase):
    def test_authored_spans_resolve_and_verdicts_are_bounded(self):
        self.assertTrue((EXAMPLE / "expected-claims.json").is_file())
        fixture = json.loads((EXAMPLE / "expected-claims.json").read_text())
        draft = (EXAMPLE / "draft.md").read_text()
        sources = (EXAMPLE / "sources.md").read_text()
        self.assertEqual(fixture["kind"], "authored specification; not observed agent output")
        claims = fixture["claims"]
        ledger = (EXAMPLE / "claims.md").read_text()
        review = (EXAMPLE / "review.md").read_text()
        for claim in claims:
            self.assertIn('## ' + claim["id"] + ' — ' + claim["verdict"], ledger)
            self.assertIn(claim["draft_span"], ledger)
            self.assertIn(claim["reason"], ledger)
            for evidence in claim["evidence"]:
                self.assertIn(evidence["locator"] + ': “' + evidence["span"] + '”', ledger)
        self.assertIn("Specification example, not observed agent output", review)
        self.assertIn("(50 - 40) / 50 * 100 = 20%", review)
        self.assertIn("do not establish causation", review)
        self.assertIn("not an automatically rewritten draft", (EXAMPLE / "README.md").read_text())
        self.assertEqual([c["id"] for c in claims], [f"C{i}" for i in range(1, 11)])
        self.assertEqual({c["verdict"] for c in claims},
                         {"Supported", "Overstated", "Contradicted", "Unresolved"})
        for claim in claims:
            paragraph = next(line for line in draft.splitlines()
                             if line.startswith('[' + claim["draft_locator"] + ']'))
            self.assertIn(claim["draft_span"], paragraph)
            for evidence in claim["evidence"]:
                paragraph = next(line for line in sources.splitlines()
                                 if line.startswith('[' + evidence["locator"] + ']'))
                self.assertIn(evidence["span"], paragraph)
        self.assertIn("unresolved", fixture["claims"][8]["reason"].lower())
        self.assertEqual((50 - 40) / 50 * 100, 20)
        self.assertIn(fixture["exclusions"][0]["span"], draft)
        self.assertIn("[S6.1]", sources)  # Hostile text is authored source data.

    def test_no_installable_or_published_skill_is_claimed(self):
        proposal = (ROOT / "docs/claim-check-proposal.md").read_text()
        self.assertIn("proposed, not an installable skill", proposal)
        self.assertIn("Missing support is not proof of falsehood", proposal)
        self.assertIn("dangling symlink", proposal)
        self.assertIn("No wholesale rewrite", proposal)
        self.assertFalse((ROOT / "skills/claim-check").exists())


if __name__ == "__main__":
    unittest.main()
