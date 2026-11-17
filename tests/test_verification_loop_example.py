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
            self.assertTrue(summary["named_controls_match_expected"])
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

    def test_boolean_corruption_cannot_pass_contract_or_differential(self):
        import shutil

        corrupt = ("import json,sys\n"
                   "def corrupt(v):\n"
                   "    if type(v) is bool: return int(v)\n"
                   "    if type(v) is list: return [corrupt(x) for x in v]\n"
                   "    if type(v) is dict: return {k:corrupt(x) for k,x in v.items()}\n"
                   "    return v\n"
                   "json.dump(corrupt(json.load(sys.stdin)),sys.stdout)\n")
        for wrong_baseline in (False, True):
            with self.subTest(wrong_baseline=wrong_baseline), tempfile.TemporaryDirectory() as temp:
                base = Path(temp).resolve()
                target = base / "target" / "examples" / "verification-loop"
                shutil.copytree(ROOT, target)
                (target / "candidate.py").write_text(corrupt)
                if wrong_baseline:
                    (target / "baseline.py").write_text(corrupt)
                output = base / "receipts"
                subprocess.run([sys.executable, str(target / "replay.py"), "--output", str(output)],
                               text=True, capture_output=True, timeout=30, check=False)
                report = json.loads((output / "result.json").read_text())
                minimal = report["results"][1]
                self.assertEqual(minimal["runs"]["candidate"]["semantic_assertion"], "FAIL")
                self.assertEqual(report["summary"]["baseline_trustworthy"], not wrong_baseline)
                self.assertEqual(minimal["differential_equal"], wrong_baseline)
                self.assertNotEqual(minimal["verdict"], "PASS")
                # Nested booleans must also differ from numeric output.
                for case in report["results"][2:]:
                    self.assertEqual(case["runs"]["candidate"]["semantic_assertion"], "FAIL")

    def test_failed_or_unavailable_legitimate_control_fails_replay(self):
        import shutil

        variants = {
            "always-loss": "import json,sys\njson.load(sys.stdin)\njson.dump({},sys.stdout)\n",
            "minimal-execution-error": (
                "import json,sys\nv=json.load(sys.stdin)\n"
                "if v['id']=='minimal': raise SystemExit(7)\n"
                "json.dump({k:v[k] for k in ('id','name','enabled')},sys.stdout)\n"),
        }
        for label, code in variants.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temp:
                base = Path(temp).resolve()
                target = base / "target" / "examples" / "verification-loop"
                shutil.copytree(ROOT, target)
                (target / "candidate.py").write_text(code)
                output = base / "receipts"
                process = subprocess.run([sys.executable, str(target / "replay.py"), "--output", str(output)],
                                         text=True, capture_output=True, timeout=30, check=False)
                report = json.loads((output / "result.json").read_text())
                self.assertTrue(report["summary"]["baseline_trustworthy"])
                self.assertTrue(report["summary"]["candidate_detected_regression"])
                self.assertNotEqual(report["results"][1]["verdict"], "PASS")
                self.assertNotEqual(process.returncode, 0)

    def test_json_comparison_preserves_nested_types_and_legitimate_formatting(self):
        module = load_replay()
        left = module.normalized('{"snow":"雪", "nested":[false, {"zero":0,"nil":null}]}')
        reordered = module.normalized('{"nested": [false,{"nil":null,"zero":0}], "snow":"雪"}')
        self.assertTrue(module.json_equal(left, reordered))
        for changed in (
            {"snow": "雪", "nested": [0, {"zero": 0, "nil": None}]},
            {"snow": "雪", "nested": [False, {"zero": False, "nil": None}]},
            {"snow": "雪", "nested": [False]},
            {"snow": "雪", "nested": [False, {"zero": 0, "nil": None}, None]},
        ):
            self.assertFalse(module.json_equal(left, changed))
        self.assertFalse(module.json_equal(True, 1))
        self.assertFalse(module.json_equal(0, False))
        self.assertFalse(module.json_equal([], {}))

    def test_invalid_utf8_streams_retain_exact_receipts_and_report(self):
        import base64
        import shutil

        for stream in ("stdout", "stderr"):
            with self.subTest(stream=stream), tempfile.TemporaryDirectory() as temp:
                root = Path(temp).resolve()
                target = root / "target" / "examples" / "verification-loop"
                shutil.copytree(ROOT, target)
                bad = b"\xff\x00\r\n"
                if stream == "stdout":
                    code = "import sys\nsys.stdout.buffer.write(bytes([255,0,13,10]))\n"
                else:
                    code = ((ROOT / "candidate.py").read_text() +
                            "\nsys.stderr.buffer.write(bytes([255,0,13,10]))\n")
                (target / "candidate.py").write_text(code)
                output = root / "receipts"
                process = subprocess.run([sys.executable, str(target / "replay.py"), "--output", str(output)],
                                         text=True, capture_output=True, timeout=30, check=False)
                self.assertTrue((output / "result.json").is_file(), process.stderr)
                self.assertTrue((output / "verification.md").is_file())
                report = json.loads((output / "result.json").read_text())
                self.assertEqual(process.returncode, 1 if stream == "stdout" else 0)
                self.assertEqual(report["identity_status"], "CURRENT")
                for case in report["results"]:
                    run = case["runs"]["candidate"]
                    self.assertEqual(run["classification"], "INVALID_OUTPUT" if stream == "stdout" else "OK")
                    if stream == "stdout":
                        self.assertIn("decode_error", run)
                    self.assertEqual(base64.b64decode(run[stream + "_base64"]), bad)
                    for name in ("baseline", "candidate"):
                        for channel in ("stdout", "stderr"):
                            receipt = output / f"case-{case['case_index']}-{name}.{channel}"
                            self.assertEqual(receipt.read_bytes(), base64.b64decode(case["runs"][name][channel + "_base64"]))
                self.assertEqual(len(list(output.glob("*.stdout"))) + len(list(output.glob("*.stderr"))), 104)

    def test_escaped_surrogate_output_does_not_break_report_encoding(self):
        import shutil

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            target = root / "target" / "examples" / "verification-loop"
            shutil.copytree(ROOT, target)
            (target / "candidate.py").write_text(
                "import json,sys\nv=json.load(sys.stdin)\nv['name']=chr(0xd800)\njson.dump(v,sys.stdout)\n")
            output = root / "receipts"
            process = subprocess.run([sys.executable, str(target / "replay.py"), "--output", str(output)],
                                     text=True, capture_output=True, timeout=30, check=False)
            self.assertTrue((output / "result.json").is_file(), process.stderr)
            self.assertTrue((output / "verification.md").is_file())
            self.assertEqual(process.returncode, 1)
            report = json.loads((output / "result.json").read_text())
            self.assertEqual(report["results"][1]["verdict"], "FAIL")
            self.assertEqual(report["results"][1]["runs"]["candidate"]["normalized"]["name"], chr(0xd800))
            self.assertEqual(len(list(output.glob("*.stdout"))) + len(list(output.glob("*.stderr"))), 104)

    def test_timeout_and_nonzero_capture_preserve_binary_streams(self):
        import base64

        module = load_replay()
        setattr(module, "TIMEOUT_SECONDS", 0.1)
        with tempfile.TemporaryDirectory() as temp:
            for tail, expected in (("import time; time.sleep(1)", "TIMEOUT"),
                                   ("raise SystemExit(7)", "SETUP_OR_EXECUTION_ERROR")):
                target = Path(temp) / "binary.py"
                target.write_text("import sys\nsys.stdout.buffer.write(bytes([255,13,10])); sys.stdout.buffer.flush()\n"
                                  "sys.stderr.buffer.write(bytes([254,0])); sys.stderr.buffer.flush()\n" + tail + "\n")
                run = module.invoke(target, {})
                self.assertEqual(run["classification"], expected)
                self.assertEqual(base64.b64decode(run["stdout_base64"]), b"\xff\r\n")
                self.assertEqual(base64.b64decode(run["stderr_base64"]), b"\xfe\x00")
                json.dumps(run)  # Structured receipts must remain serializable.

    def test_unavailable_source_identity_retains_execution_evidence(self):
        import base64
        import shutil

        for condition in ("deleted", "directory", "missing-initial", "directory-initial"):
            with self.subTest(condition=condition), tempfile.TemporaryDirectory() as temp:
                root = Path(temp).resolve()
                target = root / "target" / "examples" / "verification-loop"
                shutil.copytree(ROOT, target)
                candidate = target / "candidate.py"
                if condition.endswith("initial"):
                    candidate.unlink()
                    if condition == "directory-initial":
                        candidate.mkdir()
                else:
                    action = "p.unlink()\n" + ("p.mkdir()\n" if condition == "directory" else "")
                    candidate.write_text("import json,sys\nfrom pathlib import Path\n"
                                         "v=json.load(sys.stdin)\np=Path(__file__)\n" + action +
                                         "json.dump({k:v[k] for k in ('id','name','enabled')},sys.stdout)\n")
                output = root / "receipts"
                process = subprocess.run([sys.executable, str(target / "replay.py"), "--output", str(output)],
                                         text=True, capture_output=True, timeout=30, check=False)
                self.assertTrue((output / "result.json").is_file(), process.stderr)
                self.assertTrue((output / "verification.md").is_file())
                self.assertNotEqual(process.returncode, 0)
                self.assertNotIn("Traceback", process.stderr)
                report = json.loads((output / "result.json").read_text())
                self.assertEqual(report["identity_status"], "STALE")
                self.assertIsNone(report["post_execution_sha256"]["candidate"])
                self.assertIn("candidate", report["post_execution_identity_errors"])
                self.assertEqual("candidate" in report["initial_identity_errors"], condition.endswith("initial"))
                for case in report["results"]:
                    self.assertEqual(case["verdict"], "NO_CURRENT_VERDICT_STALE_SOURCE")
                    for name in ("baseline", "candidate"):
                        for channel in ("stdout", "stderr"):
                            path = output / f"case-{case['case_index']}-{name}.{channel}"
                            self.assertEqual(path.read_bytes(), base64.b64decode(case["runs"][name][channel + "_base64"]))
                self.assertEqual(len(list(output.glob("*.stdout"))) + len(list(output.glob("*.stderr"))), 104)

    def test_readable_source_change_stays_stale_with_receipts(self):
        import shutil

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            target = root / "target" / "examples" / "verification-loop"
            shutil.copytree(ROOT, target)
            original = (ROOT / "candidate.py").read_text()
            (target / "candidate.py").write_text(
                "from pathlib import Path\np=Path(__file__)\np.write_text(p.read_text()+'\\n')\n" + original)
            output = root / "receipts"
            process = subprocess.run([sys.executable, str(target / "replay.py"), "--output", str(output)],
                                     text=True, capture_output=True, timeout=30, check=False)
            self.assertEqual(process.returncode, 1, process.stderr)
            report = json.loads((output / "result.json").read_text())
            self.assertEqual(report["identity_status"], "STALE")
            self.assertEqual(report["initial_identity_errors"], {})
            self.assertEqual(report["post_execution_identity_errors"], {})
            self.assertNotEqual(report["source_sha256"]["candidate"], report["post_execution_sha256"]["candidate"])
            self.assertTrue(all(case["verdict"] == "NO_CURRENT_VERDICT_STALE_SOURCE" for case in report["results"]))
            self.assertEqual(len(list(output.glob("*.stdout"))) + len(list(output.glob("*.stderr"))), 104)

    def test_parser_depth_limits_retain_reports_and_candidate_bytes(self):
        import base64
        import shutil

        for depth, expected in ((16, "OK"), (900, "OUTPUT_LIMIT"), (2000, "OUTPUT_LIMIT")):
            with self.subTest(depth=depth), tempfile.TemporaryDirectory() as temp:
                root = Path(temp).resolve()
                target = root / "target" / "examples" / "verification-loop"
                shutil.copytree(ROOT, target)
                payload = '{"value":' + '[' * depth + '0' + ']' * depth + '}'
                (target / "candidate.py").write_text("import sys\nsys.stdout.write(" + repr(payload) + ")\n")
                output = root / "receipts"
                process = subprocess.run([sys.executable, str(target / "replay.py"), "--output", str(output)],
                                         text=True, capture_output=True, timeout=30, check=False)
                self.assertTrue((output / "verification.md").is_file(), process.stderr)
                report = json.loads((output / "result.json").read_text())
                self.assertEqual(process.returncode, 1)
                self.assertNotIn("Traceback", process.stderr)
                for case in report["results"]:
                    run = case["runs"]["candidate"]
                    self.assertEqual(run["classification"], expected)
                    self.assertEqual(base64.b64decode(run["stdout_base64"]), payload.encode())
                    self.assertEqual((output / f"case-{case['case_index']}-candidate.stdout").read_bytes(), payload.encode())
                    if expected == "OUTPUT_LIMIT":
                        self.assertNotIn("normalized", run)
                self.assertEqual(len(list(output.glob("*.stdout"))) + len(list(output.glob("*.stderr"))), 104)

    def test_checker_changes_invalidate_current_identity(self):
        import shutil

        for action in ("append", "delete"):
            with self.subTest(action=action), tempfile.TemporaryDirectory() as temp:
                root = Path(temp).resolve()
                target = root / "target" / "examples" / "verification-loop"
                shutil.copytree(ROOT, target)
                checker = target / "replay.py"
                checker_before = hashlib.sha256(checker.read_bytes()).hexdigest()
                mutation = ("p.write_bytes(p.read_bytes()+b'\\n# changed checker\\n')\n" if action == "append"
                            else "if p.exists(): p.unlink()\n")
                (target / "candidate.py").write_text(
                    "from pathlib import Path\np=Path(__file__).with_name('replay.py')\n" + mutation +
                    (ROOT / "candidate.py").read_text())
                output = root / "receipts"
                process = subprocess.run([sys.executable, str(checker), "--output", str(output)],
                                         text=True, capture_output=True, timeout=30, check=False)
                self.assertEqual(process.returncode, 1, process.stderr)
                self.assertTrue((output / "verification.md").is_file())
                report = json.loads((output / "result.json").read_text())
                self.assertEqual(report["identity_status"], "STALE")
                self.assertEqual(report["source_sha256"]["checker"], checker_before)
                self.assertTrue(report["summary"]["named_controls_match_expected"])
                self.assertTrue(all(case["verdict"] == "NO_CURRENT_VERDICT_STALE_SOURCE" for case in report["results"]))
                self.assertEqual("checker" in report["post_execution_identity_errors"], action == "delete")
                self.assertEqual(len(list(output.glob("*.stdout"))) + len(list(output.glob("*.stderr"))), 104)

    def test_parser_depth_boundary_preserves_legitimate_output(self):
        module = load_replay()
        before = sys.getrecursionlimit()
        accepted = '{"value":' + '[' * 63 + '"braces { [ \\\"quote\\\" ] }"' + ']' * 63 + '}'
        self.assertIsInstance(module.normalized(accepted), dict)
        rejected = '{"value":' + '[' * 64 + '0' + ']' * 64 + '}'
        with self.assertRaises(module.OutputLimitError):
            module.normalized(rejected)
        self.assertEqual(sys.getrecursionlimit(), before)

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
