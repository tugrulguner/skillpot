"""Fixed retrospective packet integrity, not a diagnostic engine or report grader."""
import copy
import hashlib
import json
import math
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "examples/performance-investigation"
SOURCE_COMMIT = "798c449fd1337404c388abb2a177c0302ba35fc0"
CANDIDATE = "92e8561aa96f7e799279b89c9c9453834f9e0cda"
CONTROL = "e703edf18d1526ebc2a91398f18c9e808e5cf5aa"
CELL_IDS = {"smoke-control", "smoke-candidate", "item-1-control", "item-1-candidate",
            "item-2-candidate", "item-2-control", "fallback-control", "fallback-candidate"}
SECTIONS = (
    "Symptom, scope and decision", "Evidence and execution identity",
    "Comparison validity and observations", "Competing explanations",
    "Checks performed and proposed", "Diagnosis and limits", "Prioritized handoff",
)


def fixed_observations_match(source, expected):
    """Bind the selected authored observation; no causal inference or target execution."""
    trials = source["trials"]
    ids = [row["cell"]["id"] for row in trials]
    if len(ids) != 8 or set(ids) != CELL_IDS:
        return False
    if (source["measured_source"] != CANDIDATE
            or source["plan"]["candidate_commit"] != CANDIDATE
            or source["plan"]["control_commit"] != CONTROL):
        return False
    rows = {row["cell"]["id"]: row for row in trials}
    pair = [rows["item-2-" + side] for side in ("candidate", "control")]
    rates = []
    events = []
    for row, side in zip(pair, ("candidate", "control")):
        cell = row["cell"]
        if tuple(cell[key] for key in ("phase", "pair", "profile", "platform", "runtime",
                                       "kind", "duration_s", "connections", "side")) != (
                "screen", "item-2", "item", "linux", "ft", "capacity", 30, 16, side):
            return False
        if any(row[key] is not True for key in (
                "accuracy_pass", "transport_pass", "runtime_pass", "activation_pass",
                "source_unchanged", "comparison_valid")):
            return False
        wheel = row["source"]["wheel"]
        if (not isinstance(wheel, str) or not re.fullmatch(r"[a-f0-9]{64}", wheel)
                or wheel != source["plan"][side + "_wheel_sha256"]):
            return False
        metrics = row["metrics"]
        if (any(metrics[k] != 0 for k in ("bad", "connect_errors", "read_errors",
                                          "write_errors", "timeout_errors"))
                or metrics["requests"] != metrics["good"] or metrics["duration_us"] <= 0):
            return False
        rate = metrics["good"] * 1_000_000 / metrics["duration_us"]
        if not math.isclose(rate, row["goodput_rps"], rel_tol=1e-12):
            return False
        rates.append(rate)
        lifecycle = row["lifecycle"]
        if lifecycle["valid"] is not True or lifecycle["errors"]:
            return False
        if [e["phase"] for e in lifecycle["events"]] != ["startup", "after_workload"]:
            return False
        events.extend(lifecycle["events"])
    ratios = {"goodput_ratio": rates[0] / rates[1],
              "p99_ratio": pair[0]["metrics"]["p99_us"] / pair[1]["metrics"]["p99_us"]}
    if not all(math.isclose(value, expected[key], rel_tol=1e-12)
               for key, value in ratios.items()):
        return False
    invalid = {row["cell"]["id"]: row["metrics"]["timeout_errors"]
               for row in trials if row["comparison_valid"] is False}
    if invalid != expected["invalid_cells"] or source["evaluation"]["screen_pass"] is not False:
        return False
    endpoint_disposition = ("CONTRADICTED_AT_RECORDED_ENDPOINTS" if all(
        e["gil_enabled"] is False and e["free_threaded_build"] is True for e in events)
        else "UNRESOLVED")
    return expected["hypotheses"] == {
        "H1": "UNRESOLVED", "H2": "UNRESOLVED", "H3": "UNRESOLVED",
        "H4": endpoint_disposition,
    }


def section_text(report, number):
    matches = list(re.finditer(rf"^## {number}\. [^\n]+\n", report, re.M))
    if len(matches) != 1:
        return ""
    rest = report[matches[0].end():]
    return re.split(r"^## ", rest, maxsplit=1, flags=re.M)[0]


def fixed_report_rows_match(source, expected, report):
    """Bounded row meaning/placement checks, independent of the whole-report seal."""
    hypothesis_rows = [line for line in section_text(report, 4).splitlines()
                       if re.match(r"^\| H[1-4] \|", line)]
    cells = [[value.strip() for value in row.strip("|").split("|")]
             for row in hypothesis_rows]
    if (len(cells) != 4 or any(len(row) != 6 for row in cells)
            or {row[0]: row[-1] for row in cells} != expected["hypotheses"]):
        return False
    for row in hypothesis_rows:
        for pointer in re.findall(r"`(/[^`]+)`", row):
            current = source
            try:
                for part in pointer.lstrip("/").split("/"):
                    current = current[int(part)] if isinstance(current, list) else current[part]
            except (KeyError, IndexError, ValueError, TypeError):
                return False
    rows = [line for line in section_text(report, 3).splitlines()
            if any(line.startswith("| " + key + " |") for key in CELL_IDS)]
    if len(rows) != 8:
        return False
    seen = set()
    by_id = {row["cell"]["id"]: row for row in source["trials"]}
    for line in rows:
        values = [value.strip() for value in line.strip("|").split("|")]
        if len(values) != 6 or values[0] in seen:
            return False
        seen.add(values[0])
        original = by_id[values[0]]
        if (float(values[3].replace(",", "")) != round(original["goodput_rps"], 3)
                or float(values[4].replace(",", "")) != original["metrics"]["p99_us"]):
            return False
    return seen == CELL_IDS


class PerformanceInvestigationProposalTests(unittest.TestCase):
    def setUp(self):
        self.source = json.loads((PACKET / "sources/linux-screen.json").read_text())
        self.expected = json.loads((PACKET / "acceptance.json").read_text())
        self.report = (PACKET / "expected/investigation.md").read_text()

    def test_immutable_public_sources_not_missing_raw_artifacts(self):
        provenance = json.loads((PACKET / "provenance.json").read_text())
        self.assertEqual(provenance["source_commit"], SOURCE_COMMIT)
        self.assertEqual(len(provenance["files"]), 3)
        for entry in provenance["files"]:
            data = (PACKET / entry["local_path"]).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["file_sha256"])
            self.assertEqual(len(data), entry["bytes"])
            commit = entry.get("source_commit", SOURCE_COMMIT)
            self.assertRegex(commit, r"^[a-f0-9]{40}$")
            self.assertIn("/blob/" + commit + "/", entry["url"])
        original = ROOT / "examples/benchmark-audit-proposal/sources"
        for name in ("linux-screen.json", "DEXPOT-LICENSE"):
            self.assertEqual((PACKET / "sources" / name).read_bytes(), (original / name).read_bytes())
        notice = (PACKET / "sources/DEXPOT-LICENSE").read_text()
        self.assertIn("Permission is hereby granted", notice)
        self.assertIn('THE SOFTWARE IS PROVIDED "AS IS"', notice)
        self.assertIn("original per-trial client streams", provenance["source_status"])
        self.assertEqual({p.name for p in (PACKET / "sources").iterdir()},
                         {"linux-screen.json", "DEXPOT-LICENSE", "candidate-scalar-response.py.txt"})

    def test_healthy_record_and_recomputed_observation(self):
        self.assertTrue(fixed_observations_match(self.source, self.expected))
        self.assertLess(self.expected["goodput_ratio"], 1)
        self.assertGreater(self.expected["p99_ratio"], 1)
        self.assertEqual(self.expected["cause"], "UNRESOLVED")
        self.assertFalse(self.expected["target_executed"])
        self.assertFalse(self.expected["raw_streams_supplied"])

    def test_metadata_identity_error_and_ratio_mutations_are_rejected(self):
        candidate = next(i for i, row in enumerate(self.source["trials"])
                         if row["cell"]["id"] == "item-2-candidate")
        mutations = (
            ("cell", "profile", "different-workload"),
            ("cell", "connections", 32), ("cell", "duration_s", 1),
            ("source", "wheel", None), ("source", "wheel", "0" * 64),
            ("metrics", "timeout_errors", 1), ("metrics", "bad", 1),
            ("metrics", "duration_us", 0), ("metrics", "p99_us", 1),
        )
        for section, key, value in mutations:
            changed = copy.deepcopy(self.source)
            changed["trials"][candidate][section][key] = value
            with self.subTest(section=section, key=key):
                self.assertFalse(fixed_observations_match(changed, self.expected))
        for key in ("accuracy_pass", "runtime_pass", "activation_pass", "comparison_valid"):
            changed = copy.deepcopy(self.source)
            changed["trials"][candidate][key] = False
            self.assertFalse(fixed_observations_match(changed, self.expected))
        for key in ("goodput_ratio", "p99_ratio"):
            changed = copy.deepcopy(self.expected)
            changed[key] = 1.5
            self.assertFalse(fixed_observations_match(self.source, changed))
        self.assertTrue(fixed_observations_match(self.source, self.expected))

    def test_omitted_adverse_cells_and_causal_promotions_are_rejected(self):
        for index in range(8):
            changed = copy.deepcopy(self.source)
            changed["trials"].pop(index)
            self.assertFalse(fixed_observations_match(changed, self.expected))
        for key in ("H1", "H2", "H3", "H4"):
            changed = copy.deepcopy(self.expected)
            changed["hypotheses"][key] = "PROVEN_CAUSE"
            self.assertFalse(fixed_observations_match(self.source, changed))
        changed = copy.deepcopy(self.source)
        changed["trials"].append(copy.deepcopy(changed["trials"][0]))
        self.assertFalse(fixed_observations_match(changed, self.expected))
        changed = copy.deepcopy(self.source)
        next(row for row in changed["trials"] if row["cell"]["id"] == "item-2-candidate")[
            "lifecycle"]["events"][0]["gil_enabled"] = True
        self.assertFalse(fixed_observations_match(changed, self.expected))

    def test_report_rows_and_each_wrong_section_are_checked_without_identity_seal(self):
        self.assertTrue(fixed_report_rows_match(self.source, self.expected, self.report))
        bounded_rows = section_text(self.report, 3) + section_text(self.report, 4)
        rows = [line for line in bounded_rows.splitlines()
                if re.match(r"^\| H[1-4] \|", line)
                or any(line.startswith("| " + key + " |") for key in CELL_IDS)]
        self.assertEqual(len(rows), 12)
        for row in rows:
            original_section = 4 if row.startswith("| H") else 3
            without = self.report.replace(row + "\n", "", 1)
            self.assertFalse(fixed_report_rows_match(self.source, self.expected, without))
            duplicated = self.report.replace(row, row + "\n" + row, 1)
            self.assertFalse(fixed_report_rows_match(self.source, self.expected, duplicated))
            for destination in range(1, 8):
                if destination == original_section:
                    continue
                moved = re.sub(rf"(^## {destination}\. [^\n]+\n)",
                               lambda match: match[0] + row + "\n", without,
                               count=1, flags=re.M)
                with self.subTest(row=row.split("|")[1], destination=destination):
                    self.assertFalse(fixed_report_rows_match(self.source, self.expected, moved))
        wrong_pointer = self.report.replace("/events/1/gil_enabled", "/events/9/gil_enabled")
        self.assertNotEqual(wrong_pointer, self.report)
        self.assertFalse(fixed_report_rows_match(self.source, self.expected, wrong_pointer))
        wrong_number = self.report.replace("| 86,634.965 | 891 |", "| 99,999.999 | 891 |")
        self.assertNotEqual(wrong_number, self.report)
        self.assertFalse(fixed_report_rows_match(self.source, self.expected, wrong_number))
        self.assertTrue(fixed_report_rows_match(self.source, self.expected, self.report))

    def test_reviewed_report_identity_and_seven_section_contract(self):
        # A frozen reviewed artifact is an identity seal, not semantic report grading.
        self.assertEqual(hashlib.sha256(self.report.encode()).hexdigest(),
                         self.expected["reviewed_report_sha256"])
        self.assertEqual(re.findall(r"^## [1-7]\. (.+)$", self.report, re.M), list(SECTIONS))
        for phrase in ("cause is unresolved", "proposed", "startup", "after_workload"):
            self.assertIn(phrase, self.report.lower())
        cases = {case["id"] for case in self.expected["acceptance_cases"]}
        self.assertEqual(cases, {"recorded-slowdown", "competing-explanations", "invalid-comparison",
                                "missing-identity", "measurement-boundary", "healthy-control-failure",
                                "permission-budget", "source-is-not-profile"})


if __name__ == "__main__":
    unittest.main()
