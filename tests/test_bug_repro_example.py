"""Exercise the public fictional scripts; no real product/model is invoked."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/bug-repro"


class BugReproExampleTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory(prefix="bug-repro-case-")
        self.addCleanup(self.workspace.cleanup)
        self.cwd = Path(self.workspace.name)

    def run_case(self, script, *args):
        return subprocess.run([sys.executable, "-I", "-B", str(EXAMPLE / script), *map(str, args)],
                              cwd=self.cwd, capture_output=True, text=True, timeout=10,
                              env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})

    def test_original_reduced_and_nontrigger_are_actual_same_symptom(self):
        for size, expected_code, status in [(3, 1, "Reproduced"), (1, 1, "Reproduced"), (0, 0, "Not reproduced")]:
            with self.subTest(size=size):
                result = self.run_case("reproduce.py", "--items", size)
                self.assertEqual(result.returncode, expected_code, result.stderr)
                record = json.loads(result.stdout)
                self.assertEqual(record["status"], status)
                self.assertEqual(record["items"], size)
                self.assertEqual(record["target_sha256"], hashlib.sha256((EXAMPLE / "buggy.py").read_bytes()).hexdigest())

    def test_legitimate_controls_and_authored_contrast(self):
        for args in [("--limit", "1"), ("--limit", "none"), ("--target", EXAMPLE / "known-good-control.py")]:
            result = self.run_case("reproduce.py", *args)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["status"], "Not reproduced")

    def test_regression_fails_only_intended_contract_and_passes_controls(self):
        bad = self.run_case("regression.py")
        self.assertEqual(bad.returncode, 1)
        self.assertIn("FAIL: test_zero_limit", bad.stderr)
        self.assertIn("AssertionError", bad.stderr)
        self.assertIn("failures=1", bad.stderr)
        self.assertNotIn("ERROR:", bad.stderr)
        good = self.run_case("regression.py", "--target", EXAMPLE / "known-good-control.py")
        self.assertEqual(good.returncode, 0, good.stderr)
        self.assertIn("Ran 4 tests", good.stderr)
        for case in ["positive", "none", "empty"]:
            result = self.run_case("regression.py", "--case", case)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_missing_raising_and_different_failures_do_not_confirm_report(self):
        missing = self.run_case("reproduce.py", "--target", self.cwd / "missing.py")
        self.assertEqual(missing.returncode, 2)
        self.assertTrue(missing.stdout.lstrip().startswith("{"), "setup errors need structured classification")
        self.assertEqual(json.loads(missing.stdout)["status"], "Blocked")
        target = self.cwd / "raising.py"
        target.write_text("def page(items, limit): raise RuntimeError('unrelated failure')\n")
        raised = self.run_case("reproduce.py", "--target", target)
        self.assertEqual(raised.returncode, 2)
        self.assertEqual(json.loads(raised.stdout)["status"], "Blocked")
        target.write_text("def page(items, limit): return ['unrelated']\n")
        other = self.run_case("reproduce.py", "--target", target)
        self.assertEqual(other.returncode, 3)
        self.assertEqual(json.loads(other.stdout)["status"], "Different failure")
        failed_setup = self.run_case("regression.py", "--target", self.cwd / "missing.py")
        self.assertEqual(failed_setup.returncode, 2)
        self.assertNotIn("AssertionError", failed_setup.stderr)

    def test_public_receipts_bind_exact_scripts_and_reduction_records(self):
        manifest = json.loads((EXAMPLE / "receipts/manifest.json").read_text())
        self.assertIn("source_files", manifest, "receipts must bind final artifact identities")
        self.assertEqual(set(manifest["source_files"]), {"buggy.py", "known-good-control.py", "reproduce.py", "regression.py"})
        for name, digest in manifest["source_files"].items():
            self.assertEqual(hashlib.sha256((EXAMPLE / name).read_bytes()).hexdigest(), digest)
        for name in ["original", "minimal", "empty", "positive", "none", "good_control", "regression_bug", "regression_good", "missing_target"]:
            self.assertIn(name, manifest["cases"])
        for name, metadata in manifest["cases"].items():
            raw = (EXAMPLE / "receipts/cases" / (name + ".json")).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), metadata["public_sha256"])
            text = raw.decode()
            self.assertNotRegex(text, r"/(?:Users|home)/")
            receipt = json.loads(raw)
            for field in ["argv", "cwd", "exit_code", "stdout", "stderr", "timeout_seconds"]:
                self.assertIn(field, receipt)
            self.assertEqual(receipt["exit_code"], metadata["expected_exit"])
            self.assertEqual(receipt["status"], "completed")
        self.assertIn("redaction", manifest)


if __name__ == "__main__":
    unittest.main()
