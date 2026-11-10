"""Bounded physical-placement checks for one preserved real report and its repair."""
import hashlib
import json
from pathlib import Path
import re
import unittest
import zipfile

CORPUS = Path(__file__).resolve().parents[1] / "evaluations/skill-quality"
EXPECTED = "Outstanding actions and requirements"
HEADING = "### A3 — Send the revised access matrix to Mara"


def placement_errors(text):
    """Only this captured template-shaped record, not a general Markdown validator."""
    sections = list(re.finditer(r"(?m)^## (.+)$", text))
    if sum(section[1] == EXPECTED for section in sections) != 1:
        return ["missing or duplicate outstanding section"]
    records = list(re.finditer(r"(?m)^" + re.escape(HEADING) + r"$", text))
    if len(records) != 1:
        return ["missing or duplicate assigned record"]
    record = records[0]
    containing = next((section[1] for section in reversed(sections) if section.start() < record.start()), None)
    return [] if containing == EXPECTED else ["assigned record in wrong containing section"]


class SkillQualityPlacementTests(unittest.TestCase):
    def setUp(self):
        self.raw = CORPUS / "initial/doc-actions-handoff-001-attempt-2"
        self.fixed = CORPUS / "assisted/doc-actions-attempt-2"

    def test_real_original_fails_and_labeled_assisted_placement_passes(self):
        receipt = json.loads((self.fixed / "correction-receipt.json").read_text())
        with zipfile.ZipFile(CORPUS / "reports-exact.zip") as archive:
            raw = archive.read("initial/doc-actions-handoff-001-attempt-2/actions.md")
            fixed = archive.read("assisted/doc-actions-attempt-2/actions.md")
        self.assertEqual(hashlib.sha256(raw).hexdigest(), receipt["raw_actions_sha256"])
        self.assertEqual(hashlib.sha256(fixed).hexdigest(), receipt["corrected_actions_sha256"])
        self.assertEqual(placement_errors(raw.decode()), ["assigned record in wrong containing section"])
        self.assertEqual(placement_errors(fixed.decode()), [])
        self.assertEqual((self.raw / "questions.md").read_bytes(), (self.fixed / "questions.md").read_bytes())
        # Exact record body survives; only physical position changed.
        block = raw[raw.index(HEADING.encode()):raw.index(b"## Coverage and checks")]
        self.assertEqual(fixed.count(block), 1)
        self.assertEqual(raw.replace(block, b""), fixed.replace(block, b""))

    def test_same_fields_under_every_wrong_heading_are_rejected(self):
        text = (self.fixed / "actions.md").read_text()
        start = text.index(HEADING)
        end = text.index("## Proposals", start)
        block = text[start:end]
        without = text[:start] + text[end:]
        headings = ["Proposals — not outstanding commitments", "Historical items — not outstanding work",
                    "Unresolved items", "Coverage and checks"]
        for heading in headings:
            with self.subTest(containing=heading):
                at = without.index("## " + heading) + len("## " + heading)
                mutant = without[:at] + "\n\n" + block + without[at:]
                self.assertEqual(placement_errors(mutant), ["assigned record in wrong containing section"])
        self.assertTrue(placement_errors(text.replace("## " + EXPECTED, "## Other")))
        self.assertTrue(placement_errors(text + "\n## " + EXPECTED + "\n"))
        self.assertTrue(placement_errors(text + "\n" + block))
        self.assertEqual(placement_errors(text), [])
