import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "examples/experiment-design-proposal"


def planned_rows():
    """This fixture's fixed schedule, not a general experiment planner."""
    rows = []

    def add(stage, profile, phase, block, slot, artifact, seconds):
        rows.append({"id": f"P{len(rows) + 1:03d}", "stage": stage,
                     "profile": profile, "phase": phase, "block": block,
                     "slot": slot, "artifact_role": artifact, "seconds": seconds})

    for slot, artifact in (("A", "control"), ("B", "candidate")):
        add("closed_loop_capacity", "item", "smoke", 0, slot, artifact, 1)
    for stage in ("closed_loop_capacity", "scheduled_arrival"):
        for profile in ("item", "large_nested"):
            for slot in "AB":
                add(stage, profile, "calibration", 0, slot, "control", 30)
            for block, order in enumerate(("AB", "BA", "BA", "AB"), 1):
                for slot in order:
                    add(stage, profile, "comparison", block, slot,
                        "control" if slot == "A" else "candidate", 30)
    return rows


def matrix_and_rules_match(design, report):
    rows = design.get("matrix", [])
    if rows != planned_rows():
        return False
    table_rows = [line for line in report.splitlines() if re.match(r"\| P\d{3} \|", line)]
    expected = ["| " + " | ".join(str(row[key]) for key in (
        "id", "stage", "profile", "phase", "block", "slot", "artifact_role", "seconds")) + " |"
        for row in rows]
    if table_rows != expected:
        return False
    rules = design.get("analysis_rules", {})
    return all((
        rules.get("item_goodput") == {"each_pair_gt": 1.0, "median_ge": 1.05},
        rules.get("large_nested_goodput") == {"each_pair_ge": 0.95},
        rules.get("item_adjusted_closed_loop_p99") == {"median_pair_ratio_le": 1.10},
        rules.get("large_nested_adjusted_closed_loop_p99") == {"each_pair_ratio_le": 1.10},
        rules.get("aa_drift_limit") is None,
        rules.get("positive_control_definition") is None,
        rules.get("negative_control_definition") is None,
    ))


def coherent(design, report):
    stages, profiles = design.get("stages", []), design.get("profiles", [])
    orders = design.get("paired_order_sequence", [])
    n = len(stages) * len(profiles) * design.get("paired_blocks_per_stage_profile", 0) * 2
    sections = re.findall(r"^## (.+)$", report, re.M)
    return all((
        stages == ["closed_loop_capacity", "scheduled_arrival"],
        profiles == ["item", "large_nested"],
        matrix_and_rules_match(design, report),
        n == design.get("regular_cells"),
        design.get("regular_cells", 0) + design.get("aa_cells", 0) == design.get("total_timed_cells"),
        design.get("aa_cells") == design.get("aa_pairs") * 2,
        design.get("timed_seconds_total") == design.get("total_timed_cells") * design.get("timed_seconds_per_cell"),
        design.get("smoke_seconds_total") == design.get("smoke_cells") * design.get("smoke_seconds_per_cell"),
        design.get("measured_seconds_including_smoke") == design.get("timed_seconds_total", 0) + design.get("smoke_seconds_total", 0),
        orders.count("AB") == orders.count("BA") == 2,
        "not randomized" in design.get("order_claim", ""),
        design.get("resource_scope", {}).get("historical_ft_limits_scope", "").startswith("DUT/server"),
        "not authorized" in report.lower(),
        "scheduled-arrival" in report.lower(),
        sections == design.get("report", {}).get("sections"),
        "post-result threshold changes" in report.lower(),
    ))


class ExperimentDesignPacketTests(unittest.TestCase):
    def test_packet_exists_and_provenance_is_byte_bound(self):
        for relative in ("README.md", "provenance.json", "acceptance.json", "sources/linux-screen.json", "sources/DEXPOT-LICENSE", "expected/experiment.md", "expected/design.json"):
            self.assertTrue((PACKET / relative).is_file(), relative)
        provenance = json.loads((PACKET / "provenance.json").read_text())
        self.assertEqual(provenance["capture_origin"]["commit"], "1b0ae953b56a439661861c8f8ec9bf5375e8e5a6")
        self.assertEqual(provenance["upstream"]["commit"], "798c449fd1337404c388abb2a177c0302ba35fc0")
        for entry in provenance["files"]:
            data = (PACKET / entry["local_path"]).read_bytes()
            self.assertEqual(len(data), entry["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"])
            blob = b"blob " + str(len(data)).encode() + b"\0" + data
            self.assertEqual(hashlib.sha1(blob).hexdigest(), entry["git_blob_sha1"])

    def test_complete_selected_source_and_evidence_limits(self):
        record = json.loads((PACKET / "sources/linux-screen.json").read_bytes())
        self.assertEqual(record["evaluation"]["expected_trials"], record["evaluation"]["collected_trials"])
        self.assertEqual(len(record["trials"]), record["evaluation"]["collected_trials"])
        self.assertEqual({t["cell"]["id"] for t in record["trials"]}, {c["id"] for c in record["plan"]["cells"]})
        self.assertTrue(any(t["metrics"].get("timeout_errors", 0) for t in record["trials"]))
        self.assertTrue(any(not t.get("comparison_valid", False) for t in record["trials"]))
        gaps = " ".join(json.loads((PACKET / "provenance.json").read_text())["evidence_gaps"]).lower()
        for term in ("raw", "wheel", "source-reported", "driver"):
            self.assertIn(term, gaps)

    def test_matrix_metadata_and_arithmetic(self):
        d = json.loads((PACKET / "expected/design.json").read_text())
        self.assertEqual(d["regular_cells"], 32)
        self.assertEqual(d["aa_cells"], 8)
        self.assertEqual(d["total_timed_cells"], 40)
        self.assertEqual(d["timed_seconds_total"], 1200)
        self.assertEqual(d["measured_seconds_including_smoke"], 1202)
        self.assertTrue(coherent(d, (PACKET / "expected/experiment.md").read_text()))

    def test_output_contract_is_exact(self):
        d = json.loads((PACKET / "expected/design.json").read_text())
        text = (PACKET / d["report"]["path"]).read_text()
        headings = re.findall(r"^## (.+)$", text, re.M)
        self.assertEqual(headings, d["report"]["sections"])
        self.assertEqual(len(headings), 8)

    def test_acceptance_cases_are_declared(self):
        acceptance = json.loads((PACKET / "acceptance.json").read_text())
        ids = {case["id"] for case in acceptance["cases"]}
        self.assertTrue({"missing_identity", "aa_drift", "negative_control_not_detected", "observed_candidate_error", "valid_loss", "capacity_win_without_scheduled_arrivals", "preflight_clean_no_candidate_observations", "threshold_revision_after_data", "unauthorized_run"} <= ids)

    def test_scope_and_destination_guards_are_explicit(self):
        text = (ROOT / "docs/experiment-design-proposal.md").read_text()
        for phrase in ("read budget", "outside all evidence roots", "exclusive creation"):
            self.assertIn(phrase, text)

    def test_changed_profile_or_stage_cannot_match_the_unchanged_report(self):
        d = json.loads((PACKET / "expected/design.json").read_text())
        report = (PACKET / "expected/experiment.md").read_text()
        for field in ("profiles", "stages"):
            bad = json.loads(json.dumps(d))
            bad[field][1] = "unmatched_payload_or_mode"
            with self.subTest(field=field):
                self.assertFalse(coherent(bad, report))

    def test_bounded_adversarial_mutations_reject(self):
        d = json.loads((PACKET / "expected/design.json").read_text())
        baseline = (PACKET / "expected/experiment.md").read_text()
        self.assertTrue(coherent(d, baseline))
        variants = []
        bad = json.loads(json.dumps(d)); bad["regular_cells"] = 31; variants.append((bad, baseline))
        bad = json.loads(json.dumps(d)); bad["paired_order_sequence"] = ["AB", "BA", "AB", "AB"]; variants.append((bad, baseline))
        bad = json.loads(json.dumps(d)); bad["aa_cells"] = 6; variants.append((bad, baseline))
        bad = json.loads(json.dumps(d)); bad["timed_seconds_total"] += 1; variants.append((bad, baseline))
        bad = json.loads(json.dumps(d)); bad["stages"].append("closed_loop_capacity"); variants.append((bad, baseline))
        variants.append((d, re.sub("scheduled-arrival", "closed-loop", baseline, flags=re.I)))
        variants.append((d, baseline.replace("not authorized", "authorized", 1)))
        variants.append((d, baseline.replace("post-result threshold changes", "threshold revisions", 1)))
        for field in ("id", "profile", "artifact_role", "seconds"):
            bad = json.loads(json.dumps(d))
            bad["matrix"][2][field] = "wrong_or_duplicate"
            variants.append((bad, baseline))
        bad = json.loads(json.dumps(d)); bad["matrix"].pop(2); variants.append((bad, baseline))
        bad = json.loads(json.dumps(d)); bad["analysis_rules"]["large_nested_goodput"]["each_pair_ge"] = 0.90; variants.append((bad, baseline))
        table_row = next(line for line in baseline.splitlines() if line.startswith("| P003 |"))
        variants.append((d, baseline.replace(table_row, "")))
        for index, (mutant, report) in enumerate(variants):
            with self.subTest(mutation=index):
                self.assertFalse(coherent(mutant, report))


if __name__ == "__main__":
    unittest.main()
