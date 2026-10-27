"""Real subprocess regressions for the skill's evidence recorder."""
from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/repository-readiness/scripts/record_check.py"


class RecordCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.repo = self.base / "target"
        self.repo.mkdir()

    def invoke(self, output, code, *, cwd=None, timeout="5"):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--repo", str(self.repo),
             "--output", str(output), "--timeout", timeout, "--",
             sys.executable, "-c", code],
            cwd=cwd or self.base, capture_output=True, text=True, timeout=10,
        )

    def test_refuses_output_inside_target_before_launch(self):
        marker = self.base / "launched"
        result = self.invoke(self.repo / "commands.json",
                             f"from pathlib import Path; Path({str(marker)!r}).touch()")
        self.assertIn("outside", result.stderr)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(marker.exists())
        self.assertEqual(list(self.repo.iterdir()), [])

    def test_records_actual_failure_without_reconstructing_output(self):
        output = self.base / "check.json"
        code = ("import os,sys,json; from pathlib import Path; "
                f"assert os.getcwd()=={str(self.repo)!r}; "
                f"assert json.loads(Path({str(output)!r}).read_text())['status']=='running'; "
                "print('real stdout café'); print('real stderr',file=sys.stderr); "
                "assert os.environ['PYTHONDONTWRITEBYTECODE']=='1'; sys.exit(7)")
        result = self.invoke(output, code, cwd=self.repo)
        self.assertEqual(result.returncode, 7, result.stderr)
        record = json.loads(output.read_text())
        self.assertEqual(record["argv"], [sys.executable, "-c", code])
        self.assertEqual(record["cwd"], ".")
        self.assertEqual(record["status"], "failed")
        self.assertEqual(record["exit_code"], 7)
        self.assertEqual(record["stdout"], "real stdout café\n")
        self.assertEqual(record["stderr"], "real stderr\n")
        self.assertEqual(list(self.repo.iterdir()), [])

    def test_existing_evidence_is_never_overwritten_or_executed(self):
        output = self.base / "prior.json"
        output.write_text("original evidence")
        marker = self.base / "launched"
        result = self.invoke(output, f"from pathlib import Path; Path({str(marker)!r}).touch()")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(output.read_text(), "original evidence")
        self.assertFalse(marker.exists())

    def test_relative_output_is_rejected_before_launch(self):
        result = self.invoke("relative.json", "print('must not run')")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.base / "relative.json").exists())

    def test_deadline_must_be_finite_positive_and_bounded(self):
        for value in ("0", "-1", "nan", "inf", "61"):
            with self.subTest(value=value):
                output = self.base / (value + ".json")
                result = self.invoke(output, "print('must not run')", timeout=value)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(output.exists())

    def test_timeout_retains_partial_output_and_is_not_success(self):
        output = self.base / "timeout.json"
        result = self.invoke(output, "import time; print('before timeout',flush=True); time.sleep(5)", timeout="0.2")
        self.assertEqual(result.returncode, 124, result.stderr)
        record = json.loads(output.read_text())
        self.assertEqual(record["status"], "timed_out")
        self.assertIsNone(record["exit_code"])
        self.assertEqual(record["stdout"], "before timeout\n")

    def test_missing_executable_is_recorded_as_launch_failure(self):
        output = self.base / "missing.json"
        command = str(self.base / "missing-executable")
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--repo", str(self.repo),
             "--output", str(output), "--", command],
            cwd=self.base, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 127, result.stderr)
        record = json.loads(output.read_text())
        self.assertEqual(record["status"], "launch_failed")
        self.assertIsNone(record["exit_code"])
        self.assertIn("missing-executable", record["stderr"])

    def test_symlink_into_target_cannot_bypass_output_boundary(self):
        alias = self.base / "alias"
        alias.symlink_to(self.repo, target_is_directory=True)
        result = self.invoke(alias / "commands.json", "print('must not run')")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(self.repo.iterdir()), [])

    def test_pass_records_actual_success(self):
        output = self.base / "passed.json"
        result = self.invoke(output, "print('actual success')")
        self.assertEqual(result.returncode, 0, result.stderr)
        record = json.loads(output.read_text())
        self.assertEqual(record["status"], "passed")
        self.assertEqual(record["exit_code"], 0)
        self.assertEqual(record["stdout"], "actual success\n")

    def test_invalid_repo_or_missing_command_creates_no_record(self):
        for name, repo, command in (
            ("relative-repo", "target", [sys.executable, "-c", "print('must not run')"]),
            ("missing-repo", str(self.base / "absent"), [sys.executable, "-c", "pass"]),
            ("no-command", str(self.repo), []),
        ):
            with self.subTest(name=name):
                output = self.base / (name + ".json")
                result = subprocess.run(
                    [sys.executable, str(SCRIPT), "--repo", repo,
                     "--output", str(output), "--", *command],
                    cwd=self.base, capture_output=True, text=True, timeout=10)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(output.exists())

    def test_existing_dangling_output_symlink_is_not_followed(self):
        destination = self.base / "uncreated.json"
        alias = self.base / "evidence-link.json"
        alias.symlink_to(destination)
        result = self.invoke(alias, "print('must not run')")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(destination.exists())
        self.assertTrue(alias.is_symlink())


if __name__ == "__main__":
    unittest.main()
