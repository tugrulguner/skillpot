import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1] / "examples" / "verification-loop"
REPLAY = ROOT / "replay.py"


def load_replay(name="verification_loop_replay_test"):
    spec = importlib.util.spec_from_file_location(name, REPLAY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class VerificationLoopExampleTests(unittest.TestCase):
    def run_replay(self, destination):
        return subprocess.run([sys.executable, str(REPLAY), "--output", str(destination)], text=True,
                              capture_output=True, timeout=30, check=False)

    def test_generated_cases_are_seed_reproducible_varied_and_bounded(self):
        module = load_replay()
        first = module.generated_records(1234, 24)
        self.assertEqual(first, module.generated_records(1234, 24))
        self.assertNotEqual(first, module.generated_records(1235, 24))
        self.assertEqual(len({json.dumps(record, sort_keys=True) for record in first}), 24)
        self.assertTrue(any("" in record.values() for record in first))
        self.assertTrue(any("雪" in json.dumps(record, ensure_ascii=False) for record in first))
        self.assertTrue(any(0 in record.values() for record in first))
        self.assertTrue(any(False in record.values() for record in first))
        self.assertTrue(any(None in record.values() for record in first))
        self.assertTrue(any(isinstance(value, (dict, list)) for record in first for value in record.values()))
        self.assertTrue(any(len(record) > 3 for record in first))
        with self.assertRaises(ValueError):
            module.generated_records(1, 129)

    def test_real_baseline_candidate_and_per_case_receipts_end_to_end(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp).resolve() / "receipts"
            process = self.run_replay(output)
            self.assertEqual(process.returncode, 0, process.stderr)
            report = json.loads((output / "result.json").read_text())
            summary = report["summary"]
            self.assertTrue(summary["baseline_trustworthy"])
            self.assertEqual(report["identity_status"], "CURRENT")
            self.assertEqual(report["generator"]["seed"], 20261117)
            self.assertEqual(summary["generated_cases"], 24)
            self.assertEqual(summary["cases"], 26)
            self.assertIsNotNone(summary["generated_counterexample_case_index"])
            self.assertTrue(summary["candidate_detected_regression"])
            self.assertEqual(report["results"][0]["verdict"], "FAIL")
            self.assertEqual(report["results"][1]["verdict"], "PASS")
            generated = report["results"][2:]
            self.assertTrue(all(case["case_kind"] == "generated-invariant" for case in generated))
            self.assertTrue(all(case["runs"]["baseline"]["semantic_assertion"] == "PASS" for case in generated))
            counter = next(case for case in generated if case["case_index"] == summary["generated_counterexample_case_index"])
            self.assertEqual(counter["runs"]["candidate"]["semantic_assertion"], "FAIL")
            self.assertFalse(counter["differential_equal"])
            self.assertEqual(counter["verdict"], "FAIL")
            for name in ("baseline", "candidate"):
                digest = hashlib.sha256((ROOT / f"{name}.py").read_bytes()).hexdigest()
                self.assertEqual(report["source_sha256"][name], digest)
            for case in report["results"]:
                for name in ("baseline", "candidate"):
                    self.assertTrue((output / f"case-{case['case_index']}-{name}.stdout").is_file())
                    self.assertTrue((output / f"case-{case['case_index']}-{name}.stderr").is_file())
            self.assertIn("not proof", (output / "verification.md").read_text())

    def test_stale_source_identity_is_not_current(self):
        module = load_replay()
        self.assertEqual(module.identity_status({"candidate": "old"}, {"candidate": "new"}), "STALE")
        self.assertEqual(module.identity_status({"candidate": "same"}, {"candidate": "same"}), "CURRENT")

    def test_timeout_and_nonzero_execution_remain_distinct(self):
        with tempfile.TemporaryDirectory() as temp:
            slow = Path(temp) / "slow.py"
            slow.write_text("import sys, time; print('partial', flush=True); print('err', file=sys.stderr, flush=True); time.sleep(1)\n")
            module = load_replay("verification_loop_replay_timeout")
            module.TIMEOUT_SECONDS = 0.1
            run = module.invoke(slow, {})
            self.assertEqual(run["classification"], "TIMEOUT")
            self.assertIn("partial", run["raw_stdout"])
            self.assertIn("err", run["raw_stderr"])
            broken = Path(temp) / "broken.py"
            broken.write_text("raise SystemExit(7)\n")
            run = module.invoke(broken, {})
            self.assertEqual(run["exit_code"], 7)
            self.assertEqual(run["classification"], "SETUP_OR_EXECUTION_ERROR")

    def test_ancestor_symlink_cannot_redirect_output(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            target = root / "target"
            (target / "nested").mkdir(parents=True)
            link = root / "alias"
            link.symlink_to(target, target_is_directory=True)
            process = self.run_replay(link / "nested" / "evidence")
            self.assertNotEqual(process.returncode, 0)
            self.assertFalse((target / "nested" / "evidence").exists())

    def test_existing_destination_is_preserved_and_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "already-there"
            output.mkdir()
            sentinel = output / "keep.txt"
            sentinel.write_text("preserve me")
            process = self.run_replay(output)
            self.assertNotEqual(process.returncode, 0)
            self.assertEqual(sentinel.read_text(), "preserve me")

    def test_symlink_destination_is_refused_without_touching_target(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "target"
            target.mkdir()
            sentinel = target / "keep.txt"
            sentinel.write_text("preserve me")
            link = Path(temp) / "link"
            link.symlink_to(target, target_is_directory=True)
            process = self.run_replay(link)
            self.assertNotEqual(process.returncode, 0)
            self.assertEqual(sentinel.read_text(), "preserve me")

    def test_wrong_valid_baseline_is_not_trusted_or_passed(self):
        module = load_replay("verification_loop_replay_semantic")
        self.assertFalse(module.baseline_trustworthy({"classification": "OK", "semantic_assertion": "FAIL"}))

    def test_timeout_bytes_are_safe_and_launch_error_is_distinct(self):
        module = load_replay("verification_loop_replay_timeout_bytes")
        self.assertEqual(module.safe_text(b"partial"), "partial")
        interpreter = module.sys.executable
        try:
            module.sys.executable = "/definitely/missing/python-interpreter"
            run = module.invoke(REPLAY, {})
        finally:
            module.sys.executable = interpreter
        self.assertEqual(run["classification"], "LAUNCH_ERROR")

    def test_missing_parent_and_symlink_parent_are_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            self.assertNotEqual(self.run_replay(base / "missing" / "receipts").returncode, 0)
            (base / "real").mkdir()
            (base / "parent").symlink_to(base / "real", target_is_directory=True)
            self.assertNotEqual(self.run_replay(base / "parent" / "receipts").returncode, 0)

    def test_dangling_destination_symlink_is_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            link = Path(temp) / "dangling"
            link.symlink_to(Path(temp) / "absent")
            self.assertNotEqual(self.run_replay(link).returncode, 0)


if __name__ == "__main__":
    unittest.main()
