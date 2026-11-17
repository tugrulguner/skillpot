import hashlib
import re
import unittest
from pathlib import Path

from scripts.check_project_skills import check_entrypoint, check_resources

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "skills/experiment-design"
FIXTURE_HASHES = {
    "examples/experiment-design-proposal/README.md": "17b4b97b917be2a94614bab73954e772910e877f3bda2fd2acd033af65f374cc",
    "examples/experiment-design-proposal/expected/experiment.md": "97647f6e89a9c90f761c42c2cce789d8efdb35f1e7ab4c1a968ba6228486490a",
    "examples/experiment-design-proposal/expected/design.json": "adbda2eaf4ac0c3647242c52dce6de7b0ea737a095523e1abda3416faed3e09c",
    "tests/test_experiment_design_proposal.py": "20380c6e9b3785c5e4da2bc4f01d8e401ff67aecf97861631a57eee1d2e4faa8",
}
HEADINGS = [
    "Question and decision", "Evidence and assumptions", "Hypotheses and falsifiers",
    "Design, controls and invariants", "Trial matrix and measurements",
    "Budgets and permissions", "Analysis and decision rules", "Freeze and execution handoff",
]


class ExperimentDesignBundleTests(unittest.TestCase):
    def test_portable_frontmatter_and_resources(self):
        metadata, errors = check_entrypoint(BUNDLE, "experiment-design")
        self.assertEqual(errors, [])
        self.assertIsNotNone(metadata)
        assert metadata is not None
        self.assertLessEqual(len(metadata["description"]), 60)
        self.assertEqual(metadata["license"], "MIT")
        self.assertTrue(all(isinstance(key, str) and isinstance(value, str)
                            for key, value in metadata["metadata"].items()))
        self.assertEqual(check_resources(BUNDLE, "experiment-design"), [])
        for relative in ("provenance.md", "compatibility.md", "assets/report-template.md",
                         "assets/checklist.md", "assets/practice-input.md"):
            self.assertTrue((BUNDLE / relative).is_file(), relative)

    def test_standalone_resources_and_metadata_negative_controls(self):
        import shutil
        import tempfile

        with tempfile.TemporaryDirectory() as temp:
            installed = Path(temp) / "experiment-design"
            shutil.copytree(BUNDLE, installed)
            self.assertEqual(check_resources(installed, "experiment-design"), [])
            entry = installed / "SKILL.md"
            original = entry.read_text()
            entry.write_text(original.replace('version: "0.1.0"', 'version: 1'))
            self.assertTrue(check_entrypoint(installed, "experiment-design")[1])
            entry.write_text(original)
            self.assertEqual(check_entrypoint(installed, "experiment-design")[1], [])
            (installed / "assets/report-template.md").unlink()
            self.assertTrue(check_resources(installed, "experiment-design"))

    def test_output_contract_and_caused_design_content(self):
        text = (BUNDLE / "assets/report-template.md").read_text()
        self.assertEqual(re.findall(r"^## (.+)$", text, re.M), HEADINGS)
        procedure = (BUNDLE / "SKILL.md").read_text().lower()
        for phrase in ("discriminating observation", "falsifier", "cheaper adequate",
                       "experimental unit", "analysis unit", "independent repetitions",
                       "failure consequence", "no new experiment", "not executed",
                       "design-changing unknowns", "exclusive", "dangling symlinks",
                       "no optional stopping"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, procedure)

    def test_practice_is_input_only_and_oracle_is_not_installed(self):
        text = (BUNDLE / "assets/practice-input.md").read_text().lower()
        self.assertIn("no expected report or answer oracle", text)
        self.assertIn("no experiment was run", text)
        self.assertFalse(any("expected" in path.name.lower() or "oracle" in path.name.lower()
                             for path in BUNDLE.rglob("*")))
        provenance = (BUNDLE / "provenance.md").read_text()
        self.assertIn("0b637dc", provenance)
        self.assertIn("expected report and integrity oracle are deliberately excluded", provenance)

    def test_accepted_retrospective_fixture_preserved_byte_for_byte(self):
        for relative, expected in FIXTURE_HASHES.items():
            with self.subTest(path=relative):
                self.assertEqual(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(), expected)

    def test_first_use_does_not_silently_pin_an_old_or_stable_release(self):
        guide = (ROOT / "docs/experiment-design-first-use.md").read_text()
        import json
        record = json.loads((ROOT / "evaluations/experiment-design/distribution-001/summary.json").read_text())
        self.assertIn("/tree/" + record["pin"] + " --skill experiment-design", guide)
        self.assertNotIn("SOURCE_COMMIT", guide)
        actual = {p.relative_to(BUNDLE).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in BUNDLE.rglob("*") if p.is_file()}
        self.assertEqual(record["source_files"], actual)
        self.assertEqual(record["files_verified"], len(actual))
        for flag in ("lock_ref_verified", "sibling_preserved", "selected_removal_verified"):
            self.assertTrue(record[flag])
        self.assertFalse(record["client_or_model_launched"])
        self.assertIn("absent from published SkillPot v0.4.1", guide)
        self.assertIn("--skill experiment-design", guide)
        self.assertIn("permission-aware", guide)
        discovery = (ROOT / "website/public/llms.txt").read_text()
        self.assertIn("seventeen bundles", discovery)
        self.assertIn("experiment-design-first-use.md", discovery)
        self.assertIn("seven unreleased working artifacts", discovery)


if __name__ == "__main__":
    unittest.main()
