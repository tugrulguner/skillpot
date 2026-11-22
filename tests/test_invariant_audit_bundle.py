"""Portable invariant-audit bundle contract and input-only parity checks."""
import hashlib
import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "skills/invariant-audit"
PRACTICE = BUNDLE / "assets/practice"
SOURCE = ROOT / "examples/invariant-audit/source"
SECTIONS = (
    "Guarantee, scope and failure model",
    "Evidence inventory and identity/provenance",
    "Source enforcement map",
    "Expected outcomes and counterexamples",
    "Findings: source-only and executed observations",
    "Proposed negative tests and healthy controls",
    "Limits and prioritized permission-aware handoff",
)


def parse_entrypoint(text):
    match = re.fullmatch(r"---\n(.*?)\n---\n(.+)", text, re.DOTALL)
    if not match:
        raise AssertionError("portable frontmatter/body boundary malformed")
    return yaml.safe_load(match.group(1)), match.group(2)


class InvariantAuditBundleTests(unittest.TestCase):
    def test_frontmatter_and_bundle_resources_are_portable(self):
        text = (BUNDLE / "SKILL.md").read_text()
        metadata, body = parse_entrypoint(text)
        self.assertEqual(set(metadata), {"name", "description", "license", "metadata"})
        self.assertEqual(metadata["name"], "invariant-audit")
        self.assertLessEqual(len(metadata["description"]), 60)
        self.assertEqual(metadata["license"], "MIT")
        self.assertEqual(metadata["metadata"], {"version": "0.1.0"})
        self.assertTrue(all(isinstance(k, str) and isinstance(v, str)
                            for k, v in metadata["metadata"].items()))
        self.assertTrue(body.strip())
        links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
        self.assertGreaterEqual(len(links), 4)
        for link in links:
            target = (BUNDLE / link).resolve()
            self.assertTrue(target.is_relative_to(BUNDLE.resolve()), link)
            self.assertTrue(target.is_file(), link)
        for required in ("provenance.md", "compatibility.md"):
            self.assertTrue((BUNDLE / required).is_file())

    def test_report_contract_has_seven_meaningful_sections(self):
        text = (BUNDLE / "assets/report-template.md").read_text()
        headings = re.findall(r"^## [1-7]\. (.+)$", text, re.M)
        self.assertEqual(headings, list(SECTIONS))
        for term in ("Declared identity", "Independently read identity", "unavailable",
                     "exact source/evidence", "authorized", "healthy control", "permission"):
            self.assertIn(term.lower(), text.lower())
        body = (BUNDLE / "SKILL.md").read_text()
        for term in ("Unknown/missing identities", "snapshots alone do not prove continuity",
                     "ancestor symlinks", "Preserve partial output", "Reuse existing authorization"):
            self.assertIn(term, body)

    def test_practice_is_input_only_and_byte_identical_to_proposal_assets(self):
        readme = (PRACTICE / "README.md").read_text().lower()
        for forbidden in ("expected report", "oracle", "expected verdict", "acceptance answer"):
            self.assertIn(forbidden, readme)
        for forbidden in ("expected/", "cases.json", "verdict"):
            self.assertNotIn(forbidden, " ".join(p.relative_to(PRACTICE).as_posix()
                                                  for p in PRACTICE.rglob("*")))
        names = ("baseline.txt", "candidate.txt", "checker.txt")
        actual = {p.name for p in (PRACTICE / "source").glob("*.txt")}
        self.assertEqual(actual, set(names))
        for name in names:
            original = (SOURCE / name).read_bytes()
            copied = (PRACTICE / "source" / name).read_bytes()
            self.assertEqual(hashlib.sha256(copied).digest(), hashlib.sha256(original).digest())
        provenance = (BUNDLE / "provenance.md").read_text()
        self.assertIn("6d5655ae2efd05fab3046df44c2b3f2a6f67bbb3", provenance)
        self.assertIn("not real incidents", provenance.lower())
        self.assertIn("commented defects", readme)


if __name__ == "__main__":
    unittest.main()
