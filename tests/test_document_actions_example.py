"""Offline authored example checks; no agent extraction is evaluated."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/document-actions"


class DocumentActionsExampleTests(unittest.TestCase):
    def run_checker(self, root):
        return subprocess.run([sys.executable, str(root / "verify.py"), "--root", str(root)],
                              capture_output=True, text=True)

    def test_fictional_packet_and_expected_outputs_verify_offline(self):
        result = self.run_checker(EXAMPLE)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["kind"], "authored-document-actions-example")
        self.assertFalse(report["network_used"])
        self.assertGreaterEqual(report["item_count"], 7)

    def test_expected_records_distinguish_assignment_proposal_history_and_conflict(self):
        data = json.loads((EXAMPLE / "expected.json").read_text())
        items = {item["id"]: item for item in data["items"]}
        self.assertEqual(items["A01"]["category"], "assigned")
        self.assertEqual(items["A01"]["acceptance"], "unknown")
        self.assertEqual(items["A02"]["category"], "unassigned_requirement")
        self.assertEqual(items["A03"]["category"], "proposal")
        self.assertEqual(items["A05"]["conflicts"]["owner"], ["Mira", "Jon"])
        self.assertEqual(items["A05"]["conflicts"]["due"], ["Friday", "Monday"])
        self.assertEqual({item["id"]: item["category"] for item in data["exclusions"]},
                         {"A07": "completed_historical", "A09": "cancelled_historical"})

    def test_checker_rejects_proposal_promoted_to_assignment(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "example"
            shutil.copytree(EXAMPLE, target)
            path = target / "expected.json"
            data = json.loads(path.read_text())
            next(item for item in data["items"] if item["id"] == "A03")["category"] = "assigned"
            path.write_text(json.dumps(data))
            result = self.run_checker(target)
            self.assertNotEqual(result.returncode, 0)

    def test_checker_rejects_historical_action_inserted_into_outstanding_output(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "example"
            shutil.copytree(EXAMPLE, target)
            path = target / "actions.md"
            text = path.read_text()
            marker = "## Completed or cancelled historical items"
            path.write_text(text.replace(marker, "### A07 — Completed historical task\n\n" + marker, 1))
            result = self.run_checker(target)
            self.assertNotEqual(result.returncode, 0)

    def test_checker_rejects_silently_resolved_conflict(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "example"
            shutil.copytree(EXAMPLE, target)
            path = target / "actions.md"
            path.write_text(path.read_text().replace(
                "**Owner (conflicting):** Mira (`N06:L8`); Jon (`N07:L9`)",
                "**Owner:** Mira"))
            result = self.run_checker(target)
            self.assertNotEqual(result.returncode, 0)

    def test_checker_rejects_wrong_markdown_owner(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "example"
            shutil.copytree(EXAMPLE, target)
            path = target / "actions.md"
            path.write_text(path.read_text().replace("**Owner:** Mira", "**Owner:** Cora", 1))
            self.assertNotEqual(self.run_checker(target).returncode, 0)

    def test_checker_rejects_changed_source_claim(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "example"
            shutil.copytree(EXAMPLE, target)
            path = target / "inputs/notes.md"
            path.write_text(path.read_text().replace("Mira owns the vendor comparison", "Jon owns the vendor comparison"))
            self.assertNotEqual(self.run_checker(target).returncode, 0)

    def test_checker_rejects_proposal_promoted_in_markdown(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "example"
            shutil.copytree(EXAMPLE, target)
            path = target / "actions.md"
            path.write_text(path.read_text().replace("**Category:** Proposal", "**Category:** Assigned action"))
            self.assertNotEqual(self.run_checker(target).returncode, 0)

    def test_all_markdown_evidence_locators_resolve(self):
        import re
        notes = (EXAMPLE / "inputs/notes.md").read_text().splitlines()
        for name in ["actions.md", "questions.md"]:
            for label, number in re.findall(r"(N\d+):L(\d+)", (EXAMPLE / name).read_text()):
                self.assertTrue(notes[int(number) - 1].startswith(f"[{label}]"), (name, label, number))

    def test_every_expected_source_locator_resolves(self):
        result = self.run_checker(EXAMPLE)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads((EXAMPLE / "expected.json").read_text())
        source = (EXAMPLE / "inputs/notes.md").read_text().splitlines()
        for item in data["items"] + data["exclusions"]:
            for locator in item["source_locators"]:
                label, physical = locator.split(":L")
                line = int(physical)
                self.assertTrue(source[line - 1].startswith(f"[{label}]"))


if __name__ == "__main__":
    unittest.main()
