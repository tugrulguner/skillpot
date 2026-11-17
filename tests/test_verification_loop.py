import json
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/check_project_skills.py"


class VerificationLoopContractTests(unittest.TestCase):
    def test_complete_original_bundle_and_flat_metadata_pass(self):
        bundle = ROOT / "skills/verification-loop"
        command = [sys.executable, str(SCRIPT), "--root", str(ROOT)]
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for required in ("provenance.md", "compatibility.md",
                         "assets/verification-report.md", "assets/verification-checklist.md",
                         "assets/example-input.md", "assets/project-verification-recipe.md",
                         "assets/reliability-rule-candidate.md"):
            self.assertTrue((bundle / required).is_file(), required)
        text = (bundle / "SKILL.md").read_text()
        metadata = runpy.run_path(str(SCRIPT))["check_entrypoint"](bundle, "verification-loop")[0]
        self.assertEqual(metadata["license"], "MIT")
        self.assertTrue(all(isinstance(v, str) for v in metadata["metadata"].values()))
        self.assertIn("assets/verification-report.md", text)
        self.assertIn("assets/verification-checklist.md", text)

    def test_article_workflow_modes_and_reusable_resources(self):
        bundle = ROOT / "skills/verification-loop"
        procedure = (bundle / "SKILL.md").read_text()
        guide = (ROOT / "docs/verification-loop-first-use.md").read_text()
        for phrase in ("Authorized verification", "Project recipe setup", "existing authorization",
                       "discover", "diff trigger", "non-trigger", "owner approval"):
            self.assertIn(phrase.lower(), (procedure + guide).lower())
        for resource in ("project-verification-recipe.md", "reliability-rule-candidate.md"):
            self.assertIn("](assets/" + resource + ")", procedure)
            self.assertTrue((bundle / "assets" / resource).is_file())
        self.assertIn("## Bounded authorized verification", guide)
        self.assertIn("## Optional project recipe setup", guide)

    def test_description_over_limit_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "SKILL.md").write_text("---\nname: verification-loop\ndescription: " + "x" * 61 +
                "\nlicense: MIT\nmetadata:\n  version: '0.1.0'\n---\n\nBody.\n")
            _, errors = runpy.run_path(str(SCRIPT))["check_entrypoint"](root, "verification-loop")
            self.assertIn("verification-loop: invalid portable frontmatter", errors)

    def test_non_string_metadata_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "SKILL.md").write_text("---\nname: verification-loop\ndescription: Verify a code change\n"
                "license: MIT\nmetadata:\n  version: 1\n---\n\nBody.\n")
            _, errors = runpy.run_path(str(SCRIPT))["check_entrypoint"](root, "verification-loop")
            self.assertIn("verification-loop: metadata must contain only string values", errors)

    def test_missing_linked_resource_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            (directory / "SKILL.md").write_text("---\nname: verification-loop\n"
                "description: Verify a code change\nlicense: MIT\n---\n\n[missing](absent.md)\n")
            errors = runpy.run_path(str(SCRIPT))["check_resources"](directory, "verification-loop")
            self.assertEqual(errors, ["verification-loop/SKILL.md: missing resource: absent.md"])

    def test_procedure_contract_safety_and_result_states(self):
        text = (ROOT / "skills/verification-loop/SKILL.md").read_text()
        for phrase in ("inspection and a proposed verification plan", "explicit scope and permission",
                       "Never delete, weaken, skip, mask, or bypass", "At most three repair rounds",
                       "BLOCKED", "NOT RUN", "STALE", "Change-impact", "Bug-repro",
                       "Release-verification", "Example-regression-check"):
            self.assertIn(phrase.lower(), text.lower())
        self.assertIn("criteria, fixtures and checks are unchanged from the base", text)

    def test_input_only_bundle_and_standalone_links(self):
        import shutil

        bundle = ROOT / "skills/verification-loop"
        checker = runpy.run_path(str(SCRIPT))
        with tempfile.TemporaryDirectory() as temp:
            installed = Path(temp) / "verification-loop"
            shutil.copytree(bundle, installed)
            self.assertEqual(checker["check_resources"](installed, "verification-loop"), [])
            self.assertFalse((installed / "examples").exists())
            self.assertFalse((installed / "expected").exists())
            self.assertFalse(list(installed.rglob("*.py")))
            text = (installed / "SKILL.md").read_text()
            for link in ("assets/verification-report.md", "assets/verification-checklist.md",
                         "assets/example-input.md", "provenance.md", "compatibility.md"):
                self.assertIn("](" + link + ")", text)
            (installed / "assets/example-input.md").unlink()
            self.assertTrue(checker["check_resources"](installed, "verification-loop"))

    def test_distribution_record_binds_complete_bundle(self):
        import hashlib

        record = json.loads((ROOT / "evaluations/verification-loop/distribution-002/summary.json").read_text())
        bundle = ROOT / "skills/verification-loop"
        actual = {p.relative_to(bundle).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in bundle.rglob("*") if p.is_file()}
        self.assertEqual(record["source_files"], actual)
        self.assertEqual(record["files_verified"], len(actual))
        self.assertTrue(record["lock_ref_verified"])
        self.assertTrue(record["sibling_preserved"])
        self.assertTrue(record["selected_removal_verified"])
        self.assertFalse(record["client_or_model_launched"])
        guide = (ROOT / "docs/verification-loop-first-use.md").read_text()
        self.assertIn("/tree/" + record["pin"] + " --skill verification-loop", guide)
        self.assertNotIn("<FULL_COMMIT>", guide)

    def test_historical_distribution_record_is_preserved(self):
        import hashlib

        old = ROOT / "evaluations/verification-loop/distribution-001/summary.json"
        self.assertEqual(hashlib.sha256(old.read_bytes()).hexdigest(),
                         "f94e8b208101782d3e9e04de3de6b80698f3c05f09f93b0e2e2b61d7f0cfeadc")
        record = json.loads(old.read_text())
        self.assertEqual(record["pin"], "a483d6c2d7207f2ffb66b5c9b2bb712c6efcdec7")
        self.assertEqual(record["files_verified"], len(record["source_files"]))
        self.assertEqual(record["files_verified"], 6)

    def test_discovery_counts_and_historical_collection_count(self):
        count = sum(1 for _ in (ROOT / "skills").glob("*/SKILL.md"))
        self.assertEqual(count, 17)
        readme = (ROOT / "README.md").read_text()
        self.assertIn("seventeen workflows", readme)
        self.assertIn("ten-skill published collection", readme)
        source_catalog = json.loads((ROOT / "catalog/modepot-sources.json").read_text())
        self.assertEqual(len(source_catalog["skills"]), 7)


if __name__ == "__main__":
    unittest.main()
