"""Portable performance-investigation bundle and practice-source contract."""
import hashlib
import json
import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "skills/performance-investigation"
PRACTICE = BUNDLE / "assets/practice"
SOURCE = ROOT / "examples/performance-investigation/sources"
SECTIONS = (
    "Symptom, scope and decision",
    "Evidence and execution identity",
    "Comparison validity and observations",
    "Competing explanations",
    "Checks performed and proposed",
    "Diagnosis and limits",
    "Prioritized handoff",
)
FILES = {"linux-screen.json", "candidate-scalar-response.py.txt", "DEXPOT-LICENSE"}


def parse_entrypoint(text):
    match = re.fullmatch(r"---\n(.*?)\n---\n(.+)", text, re.DOTALL)
    if not match:
        raise AssertionError("portable frontmatter/body boundary malformed")
    return yaml.safe_load(match.group(1)), match.group(2)


class PerformanceInvestigationBundleTests(unittest.TestCase):
    def test_flat_portable_metadata_and_all_resources_resolve_standalone(self):
        text = (BUNDLE / "SKILL.md").read_text()
        metadata, body = parse_entrypoint(text)
        self.assertEqual(set(metadata), {"name", "description", "license", "metadata"})
        self.assertEqual(metadata["name"], "performance-investigation")
        self.assertLessEqual(len(metadata["description"]), 60)
        self.assertEqual(metadata["license"], "MIT")
        self.assertEqual(metadata["metadata"], {"version": "0.1.0"})
        self.assertTrue(all(isinstance(k, str) and isinstance(v, str)
                            for k, v in metadata["metadata"].items()))
        self.assertTrue(body.strip())
        for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            target = (BUNDLE / link).resolve()
            self.assertTrue(target.is_relative_to(BUNDLE.resolve()), link)
            self.assertTrue(target.is_file(), link)
        for path in ("provenance.md", "compatibility.md", "assets/report-template.md",
                     "assets/checklist.md", "assets/practice/README.md",
                     "assets/practice/request.md", "assets/practice/provenance.json"):
            self.assertTrue((BUNDLE / path).is_file(), path)

    def test_exact_seven_section_output_contract_and_core_rules(self):
        template = (BUNDLE / "assets/report-template.md").read_text()
        self.assertEqual(tuple(re.findall(r"^## [1-7]\. (.+)$", template, re.M)), SECTIONS)
        body = (BUNDLE / "SKILL.md").read_text().lower()
        for phrase in ("actual runtime bytes", "source map is not a timing profile",
                       "endpoint flag as continuous state", "preserve every planned/observed row",
                       "do not subtract percentiles", "unknown cause is valid",
                       "bounded diagnostic authorization already granted", "dangling symlinks",
                       "preserve partial results"):
            self.assertIn(phrase, body)
        checklist = (BUNDLE / "assets/checklist.md").read_text().lower()
        self.assertIn("invalid rows", checklist)
        self.assertIn("healthy control", checklist)

    def test_practice_contains_only_input_files_with_exact_source_parity(self):
        self.assertEqual({p.name for p in (PRACTICE / "sources").iterdir()}, FILES)
        self.assertEqual({p.name for p in PRACTICE.iterdir()},
                         {"README.md", "request.md", "provenance.json", "sources"})
        for name in FILES:
            self.assertEqual((PRACTICE / "sources" / name).read_bytes(),
                             (SOURCE / name).read_bytes(), name)
        self.assertEqual((PRACTICE / "request.md").read_bytes(),
                         (ROOT / "examples/performance-investigation/request.md").read_bytes())
        self.assertEqual((PRACTICE / "provenance.json").read_bytes(),
                         (ROOT / "examples/performance-investigation/provenance.json").read_bytes())
        provenance = json.loads((PRACTICE / "provenance.json").read_text())
        for item in provenance["files"]:
            content = (PRACTICE / item["local_path"]).read_bytes()
            self.assertEqual(len(content), item["bytes"])
            self.assertEqual(hashlib.sha256(content).hexdigest(), item["file_sha256"])
        readme = (PRACTICE / "README.md").read_text().lower()
        for phrase in ("input-only", "fresh", "external", "source-summary raw streams",
                       "wheel bytes", "cause as unknown"):
            self.assertIn(phrase, readme)
        names = {p.relative_to(PRACTICE).as_posix().lower() for p in PRACTICE.rglob("*")}
        self.assertFalse(any("expected" in n or "acceptance" in n or "oracle" in n for n in names))
        self.assertNotIn("expected/investigation.md", " ".join(names))
        self.assertIn("complete upstream MIT `LICENSE` notice", (BUNDLE / "provenance.md").read_text())

    def test_current_public_selection_has_exact_complete_hashes_and_strict_receipts(self):
        record = json.loads((ROOT / "docs/performance-investigation-distribution.json").read_text())
        pin = "ca4246d4c2eabdb22da5d75af7adafbc230d06c2"
        self.assertEqual(record["source_commit"], pin)
        self.assertEqual(record["skill"], "performance-investigation")
        expected_names = {"SKILL.md", "provenance.md", "compatibility.md",
                          "assets/report-template.md", "assets/checklist.md",
                          "assets/practice/README.md", "assets/practice/request.md",
                          "assets/practice/provenance.json"} | {
                              "assets/practice/sources/" + name for name in FILES}
        actual = {p.relative_to(BUNDLE).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in BUNDLE.rglob("*") if p.is_file()}
        self.assertEqual(set(actual), expected_names)
        self.assertEqual(len(actual), 11)
        self.assertEqual(record["bundle_files"], 11)
        self.assertEqual(actual, record["source_files"])
        self.assertEqual(actual, record["installed_files"])
        for flag in ("passed", "selected_only", "lock_ref_verified", "list_verified",
                     "selected_removal_verified", "sibling_preserved"):
            self.assertIs(record[flag], True, flag)
        self.assertEqual(set(record["lock"]["skills"]), {"performance-investigation"})
        entry = record["lock"]["skills"]["performance-investigation"]
        self.assertEqual(entry["ref"], pin)
        self.assertEqual(entry["source"], "tugrulguner/skillpot")
        self.assertEqual(entry["skillPath"], "skills/performance-investigation/SKILL.md")
        guide = (ROOT / "docs/performance-investigation-first-use.md").read_text()
        self.assertIn("tree/" + pin + " --skill performance-investigation", guide)
        self.assertNotIn("SOURCE_PIN_PENDING", guide)
        self.assertNotIn("tree/v0.5.0 --skill performance-investigation", guide)
        self.assertNotIn("/Users/", json.dumps(record))

    def test_h1_contrast_has_competing_predictions_and_ambiguity(self):
        text = (BUNDLE / "assets/checklist.md").read_text().lower()
        for phrase in ("projection-on/off ablation", "artifact and contract", "healthy response/error",
                       "track projection-on", "track run position", "observer-off control",
                       "null alternative", "no stable difference", "remain ambiguous",
                       "not an implemented toggle", "an invented timing receipt"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
