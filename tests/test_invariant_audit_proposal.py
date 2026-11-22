"""Fixed authored-packet consistency, not target execution or report grading."""
import copy
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "examples/invariant-audit"
ROLES = ("baseline", "candidate", "checker")
CASE_IDS = {
    "healthy-control", "baseline-deleted", "baseline-directory-read-error",
    "checker-changed", "source-changed", "both-unavailable", "missing-coverage",
    "changed-between-snapshots", "unknown-at-both-snapshots", "malformed-checker",
    "read-error-with-retained-value",
}


def expected_snapshot(case):
    """Independent statement of this toy domain's guarantee, not snippet execution."""
    if case.get("read_errors"):
        return "NOT_CURRENT"
    pairs = [(case.get("captured", {}).get(role), case.get("actual", {}).get(role))
             for role in ROLES]
    if not all(isinstance(value, str) and bool(value.strip())
               for pair in pairs for value in pair):
        return "NOT_CURRENT"
    return "CURRENT" if all(before == after for before, after in pairs) else "NOT_CURRENT"


def expected_case(case):
    if "initial" in case:
        snapshots = {"captured": case["initial"], "actual": case.get("final", {}),
                     "read_errors": case.get("read_errors", [])}
        if expected_snapshot(snapshots) != "CURRENT":
            return "NOT_CURRENT"
        # No continuous observation was supplied, regardless of equal endpoints.
        if case.get("continuity_observed") is not False:
            return "UNSUPPORTED_FIXTURE"
        return "CONTINUITY_UNPROVEN"
    return expected_snapshot(case)


def packet_matches(packet, report):
    cases = packet.get("cases", [])
    ids = [case["id"] for case in cases]
    if len(ids) != len(CASE_IDS) or set(ids) != CASE_IDS:
        return False
    if any(case["expected"] != expected_case(case) for case in cases):
        return False
    rows = re.findall(r"^\| ([a-z][a-z-]+) \| ([A-Z_]+) \|", report, re.M)
    return (len(rows) == len(cases) and len({key for key, _ in rows}) == len(cases)
            and dict(rows) == {case["id"]: expected_case(case) for case in cases})


class InvariantAuditProposalTests(unittest.TestCase):
    def setUp(self):
        self.packet = json.loads((PACKET / "inputs/cases.json").read_text())
        self.report = (PACKET / "expected/invariant-audit.md").read_text()

    def test_authored_control_and_complete_independent_ledger(self):
        self.assertTrue(packet_matches(self.packet, self.report))
        rows = {case["id"]: case for case in self.packet["cases"]}
        self.assertEqual(expected_case(rows["healthy-control"]), "CURRENT")
        self.assertEqual(expected_case(rows["unknown-at-both-snapshots"]), "NOT_CURRENT")
        self.assertEqual(expected_case(rows["read-error-with-retained-value"]), "NOT_CURRENT")

    def test_each_changed_expectation_and_each_ledger_verdict_is_rejected(self):
        for index, case in enumerate(self.packet["cases"]):
            with self.subTest(case=case["id"]):
                changed = copy.deepcopy(self.packet)
                wrong = "NOT_CURRENT" if case["expected"] == "CURRENT" else "CURRENT"
                changed["cases"][index]["expected"] = wrong
                self.assertFalse(packet_matches(changed, self.report))
                wrong_report = self.report.replace(
                    f"| {case['id']} | {case['expected']} |",
                    f"| {case['id']} | {wrong} |")
                self.assertNotEqual(wrong_report, self.report)
                self.assertFalse(packet_matches(self.packet, wrong_report))

    def test_omission_duplicate_and_orphan_are_rejected(self):
        for case in self.packet["cases"]:
            row = next(line for line in self.report.splitlines()
                       if line.startswith(f"| {case['id']} |"))
            for mutated in (self.report.replace(row + "\n", ""),
                            self.report + "\n" + row,
                            self.report.replace(row, row.replace(case["id"], "orphan-case"))):
                self.assertFalse(packet_matches(self.packet, mutated))
        missing = copy.deepcopy(self.packet)
        missing["cases"].pop()
        self.assertFalse(packet_matches(missing, self.report))

    def test_identity_boundary_mutations_retain_healthy_control(self):
        healthy = next(case for case in self.packet["cases"] if case["id"] == "healthy-control")
        for role in ROLES:
            for value in (None, False, 0, "", "  ", [], {}, "different-id"):
                changed = copy.deepcopy(healthy)
                changed["actual"][role] = value
                self.assertEqual(expected_snapshot(changed), "NOT_CURRENT")
            for value in (None, False, "", "  "):
                changed = copy.deepcopy(healthy)
                changed["captured"][role] = changed["actual"][role] = value
                self.assertEqual(expected_snapshot(changed), "NOT_CURRENT")
        self.assertEqual(expected_snapshot(healthy), "CURRENT")

    def test_verifier_controls_transfer_and_source_only_scope(self):
        quality = self.packet["verifier_quality_cases"]
        self.assertEqual({case["id"] for case in quality}, {"wrong-reason", "control-failure"})
        self.assertTrue(all(case["expected"] == "REJECT_AS_INVALID_VERIFIER_RESULT" for case in quality))
        transfer = self.packet["transfer_case"]
        self.assertIn("original bytes remain unchanged", transfer["independent_expected"])
        self.assertIn("truncates", transfer["counterexample"])
        self.assertIn("Executed against target: **none**", self.report)
        self.assertEqual(len(re.findall(r"^## [1-7]\. ", self.report, re.M)), 7)
        self.assertTrue(all((PACKET / "source" / name).is_file()
                            for name in ("baseline.txt", "candidate.txt", "checker.txt")))


if __name__ == "__main__":
    unittest.main()
