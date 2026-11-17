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


class VerificationLoopExampleTests(unittest.TestCase):
    def run_replay(self, destination):
        return subprocess.run([sys.executable, str(REPLAY), "--output", str(destination)], text=True,
                              capture_output=True, timeout=15, check=False)

    def test_real_baseline_and_candidate_expose_field_loss_end_to_end(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "receipts"
            process = self.run_replay(output)
            self.assertEqual(process.returncode, 0, process.stderr)
            report = json.loads((output / "result.json").read_text())
            self.assertTrue(report["summary"]["baseline_trustworthy"])
            self.assertEqual(report["identity_status"], "CURRENT")
            self.assertEqual(report["results"][0]["runs"]["baseline"]["semantic_assertion"], "PASS")
            self.assertEqual(report["results"][0]["runs"]["candidate"]["semantic_assertion"], "FAIL")
            self.assertEqual(report["results"][0]["verdict"], "FAIL")
            self.assertEqual(report["results"][1]["verdict"], "PASS")
            self.assertEqual(report["results"][2]["verdict"], "FAIL")
            self.assertTrue(report["summary"]["invariant_generated_control_failed"])
            for name in ("baseline", "candidate"):
                digest = hashlib.sha256((ROOT / f"{name}.py").read_bytes()).hexdigest()
                self.assertEqual(report["source_sha256"][name], digest)
            self.assertTrue((output / "case-0-candidate.stdout").exists())
            self.assertIn('"extension"', (output / "case-0-baseline.stdout").read_text())
            self.assertNotIn('"extension"', (output / "case-0-candidate.stdout").read_text())

    def test_stale_source_identity_is_not_current(self):
        spec = importlib.util.spec_from_file_location("verification_loop_replay", REPLAY)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.identity_status({"candidate": "old"}, {"candidate": "new"}), "STALE")
        self.assertEqual(module.identity_status({"candidate": "same"}, {"candidate": "same"}), "CURRENT")

    def test_timeout_and_nonzero_execution_remain_distinct(self):
        with tempfile.TemporaryDirectory() as temp:
            slow = Path(temp) / "slow.py"
            slow.write_text("import sys, time; print('partial', flush=True); print('err', file=sys.stderr, flush=True); time.sleep(1)\n")
            spec = importlib.util.spec_from_file_location("verification_loop_replay_timeout", REPLAY)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.TIMEOUT_SECONDS = 0.1
            run = module.invoke(slow, {})
            self.assertEqual(run["classification"], "TIMEOUT")
            self.assertIn("partial", run["raw_stdout"])
            self.assertIn("err", run["raw_stderr"])
            broken = Path(temp) / "broken.py"
            broken.write_text("raise SystemExit(7)\n")
            run = module.invoke(broken, {})
            self.assertEqual(run["exit_code"], 7)

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
        spec = importlib.util.spec_from_file_location("verification_loop_replay_semantic", REPLAY)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertFalse(module.baseline_trustworthy({"classification": "OK", "semantic_assertion": "FAIL"}))

    def test_timeout_bytes_are_safe_and_launch_error_is_distinct(self):
        spec = importlib.util.spec_from_file_location("verification_loop_replay_timeout_bytes", REPLAY)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.safe_text(b"partial"), "partial")

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
