"""Assisted correction regressions; never relabel the original model attempts."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "evaluations/workflow-fields"
CORRECTIONS = RECORD / "corrections-001"


class FieldConsistencyCorrectionsTests(unittest.TestCase):
    def read_corrected(self, case, name):
        path = CORRECTIONS / "cases" / case / "output" / name
        self.assertTrue(path.is_file(), f"missing assisted correction: {path.relative_to(CORRECTIONS)}")
        return path.read_text()

    def test_confirmation_time_is_not_a_proven_failed_completion_gate(self):
        brief = self.read_corrected("01-archive-decision", "brief.md")
        rows = [line for line in brief.splitlines() if line.startswith("|") and "volunteer" in line.lower()]
        self.assertEqual(len(rows), 1)
        self.assertIn("unknown", rows[0].lower())
        self.assertNotRegex(rows[0].lower(), r"fail[^|]*(deadline|timing)")
        evidence = self.read_corrected("01-archive-decision", "evidence.md")
        self.assertNotIn("stated confirmation timing fails", evidence)
        original = (RECORD / "followup-001/cases/01-archive-decision/output/brief.md").read_text()
        self.assertIn("fail deadline", original)

    def test_inspection_note_has_the_correct_sentence_locator(self):
        evidence = self.read_corrected("02-reading-room-decision", "evidence.md")
        claim = next(line for line in evidence.splitlines() if line.startswith("| C4 |"))
        locator = claim.split("|")[5].strip()
        self.assertIn("B4, second sentence", locator)
        self.assertIn("inspection-note", locator.lower())
        self.assertIn("two steps", claim.lower())
        self.assertNotIn("third", locator.lower())
        original = (RECORD / "followup-001/cases/02-reading-room-decision/output/evidence.md").read_text()
        self.assertIn("B4, third sentence", original)

    def test_frame_and_criteria_claims_resolve_to_the_corrected_ledger(self):
        for case in ["01-archive-decision", "02-reading-room-decision"]:
            with self.subTest(case=case):
                brief = self.read_corrected(case, "brief.md")
                evidence = self.read_corrected(case, "evidence.md")
                registered = set(re.findall(r"^\| ([CAKU]\d+) \|", evidence, re.M))
                for field in ["Decision owner", "Intended reader", "Purchasing / approval authority",
                              "Hard constraints (gates)", "Preferences (trade-offs)"]:
                    line = next(line for line in brief.splitlines() if f"**{field}:**" in line)
                    ids = set(re.findall(r"\b[CAKU]\d+\b", line))
                    self.assertTrue(ids, f"{case}: {field} needs a stable ledger claim")
                    self.assertLessEqual(ids, registered)

    def test_role_locators_match_the_actual_source_sentences(self):
        source = (RECORD / "followup-001/cases/02-reading-room-decision/input/evidence.md").read_text()
        paragraph = next(line[4:] for line in source.splitlines() if line.startswith("B1. "))
        sentences = re.split(r"(?<=\.)\s+", paragraph)
        self.assertEqual(len(sentences), 3)
        evidence = self.read_corrected("02-reading-room-decision", "evidence.md")
        for claim_id, ordinal, subject in [("C9", "first", "Rafi"),
                                           ("C10", "second", "Sera"),
                                           ("U3", "third", "authority")]:
            line = next(line for line in evidence.splitlines() if line.startswith(f"| {claim_id} |"))
            self.assertIn(f"B1, {ordinal} sentence", line)
            self.assertIn(subject, line)
        self.assertNotIn("B4 has two sentences", evidence)

    def test_manifest_preserves_originals_and_fingerprints_corrected_copies(self):
        import hashlib
        import json
        manifest = json.loads((CORRECTIONS / "manifest.json").read_text())
        self.assertEqual(set(manifest["cases"]), {"01-archive-decision", "02-reading-room-decision"})
        for case in manifest["cases"].values():
            for group, base in [("originals", ROOT), ("corrected", CORRECTIONS)]:
                for name, record in case[group].items():
                    self.assertEqual(hashlib.sha256((base / name).read_bytes()).hexdigest(), record["sha256"], name)

    def test_assisted_corrections_are_not_claimed_as_new_model_attempts(self):
        readme = CORRECTIONS / "README.md"
        self.assertTrue(readme.is_file())
        text = readme.read_text().lower()
        self.assertIn("assisted", text)
        self.assertRegex(text, r"not (?:a )?fresh")
        self.assertIn("oracle", text)
        self.assertRegex(text, r"\b(?:unchanged|untouched)\b")


if __name__ == "__main__":
    unittest.main()
