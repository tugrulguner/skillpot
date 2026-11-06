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
        self.assertEqual([c["id"] for c in claims], [f"C{i}" for i in range(1, 13)])
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

    def assert_coverage(self, fixture):
        claims = {c["id"]: c for c in fixture["claims"]}
        exclusions = {e["id"]: e for e in fixture["exclusions"]}
        draft_ids = {line.split(']')[0][1:] for line in
                     (EXAMPLE / "draft.md").read_text().splitlines() if line.startswith('[D')}
        self.assertEqual(set(fixture["coverage"]), draft_ids)
        mapped = []
        for paragraph, ids in fixture["coverage"].items():
            self.assertTrue(ids)
            for identifier in ids:
                self.assertIn(identifier, claims.keys() | exclusions.keys())
                record = claims[identifier] if identifier in claims else exclusions[identifier]
                self.assertEqual(record.get("draft_locator", record.get("locator")), paragraph)
                mapped.append(identifier)
        self.assertEqual(sorted(mapped), sorted(claims.keys() | exclusions.keys()))
        d5 = [claims[i]["proposition"] for i in fixture["coverage"]["D5"]]
        self.assertEqual(set(d5), {"An audit was performed", "The audit was independent",
                                  "The audit reported a positive security conclusion",
                                  "The system is secure"})

    def test_explicit_coverage_reconciles_draft_and_audit_facets(self):
        fixture = json.loads((EXAMPLE / "expected-claims.json").read_text())
        self.assert_coverage(fixture)
        import copy
        for mutation in ["omission", "duplicate", "wrong-paragraph", "missing-paragraph"]:
            bad = copy.deepcopy(fixture)
            if mutation == "omission":
                bad["coverage"]["D5"].remove("C12")
            elif mutation == "duplicate":
                bad["coverage"]["D5"].append("C7")
            elif mutation == "wrong-paragraph":
                bad["coverage"]["D5"].remove("C12")
                bad["coverage"]["D6"].append("C12")
            else:
                del bad["coverage"]["D5"]
            with self.subTest(mutation=mutation), self.assertRaises(AssertionError):
                self.assert_coverage(bad)

    def test_proposal_remains_a_historical_record_after_implementation(self):
        proposal = (ROOT / "docs/claim-check-proposal.md").read_text()
        self.assertIn("**Status: proposed, not an installable skill or published collection addition.**", proposal)
        self.assertIn("before implementing a portable", proposal)
        self.assertIn("Missing support is not proof of falsehood", proposal)
        self.assertIn("dangling symlink", proposal)
        self.assertIn("No wholesale rewrite", proposal)
        self.assertTrue((ROOT / "skills/claim-check/SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
