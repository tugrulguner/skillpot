"""Offline source/fixture checks; not an incident-response model evaluation."""
import copy
import hashlib
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "examples/incident-triage"
SELECTED = [8, 11, 18, 19, 169, 171, 172, 174, 176, 178, 180, 182, 184]


def validate_fixture(manifest, excerpt, incident, timeline):
    """Check THIS authored packet's bindings/fields, not arbitrary triage semantics."""
    if manifest.get("source_run_head") != "b4d8f6020ca5b9646f68f5dfd915b61bb6e30db7":
        return False
    if manifest.get("selected_original_line_ids") != SELECTED:
        return False
    if hashlib.sha256(excerpt.encode()).hexdigest() != manifest["excerpt_sha256"]:
        return False
    rows = excerpt.splitlines()
    if len(rows) != len(SELECTED):
        return False
    by_id = dict(zip(SELECTED, rows))
    if not by_id[171].endswith("Z OK") or "Ran 147 tests" not in by_id[169]:
        return False
    for field in ["- Customer impact: Unknown.", "- Resolution: Not assessed."]:
        prefix = field.split(":", 1)[0] + ":"
        if [line for line in incident.splitlines() if line.startswith(prefix)] != [field]:
            return False
    template = (ROOT / "skills/incident-triage/assets/timeline-template.md").read_text()
    expected_header = "| ID | Source ID/locator | Timestamp as recorded | Precision/timezone/clock | Kind: event, collection, notification | Event or bounded interval | Ordering relation / uncertainty |"
    if expected_header not in timeline.splitlines() or expected_header not in template.splitlines():
        return False
    expected_rows = {
        "log-command": ("2026-11-06T22:37:02.7377903Z", "event"),
        "log-version": ("2026-11-06T22:37:02.7501011Z", "event"),
        "log-pass-docs": ("2026-11-06T22:37:04.7277690Z", "event"),
        "log-pass-integrity": ("2026-11-06T22:37:04.7641399Z", "event"),
        "log-tests-summary": ("2026-11-06T22:37:06.8379918Z", "event"),
        "log-tests-ok": ("2026-11-06T22:37:06.8380110Z", "event"),
        "log-whitespace-1": ("2026-11-06T22:37:06.8490429Z", "event"),
        "log-whitespace-2": ("2026-11-06T22:37:06.8490958Z", "event"),
        "log-whitespace-3": ("2026-11-06T22:37:06.8491438Z", "event"),
        "log-whitespace-4": ("2026-11-06T22:37:06.8491962Z", "event"),
        "log-whitespace-5": ("2026-11-06T22:37:06.8492479Z", "event"),
        "log-whitespace-6": ("2026-11-06T22:37:06.8492829Z", "event"),
        "log-exit": ("2026-11-06T22:37:06.8507649Z", "event"),
    }
    cited = []
    for row in timeline.splitlines():
        if not row.startswith("| ") or row.startswith("| ID ") or row.startswith("|---"):
            continue
        cells = [cell.strip() for cell in row.split("|")[1:-1]]
        if len(cells) != 7 or cells[0] not in expected_rows:
            return False
        if cells[2] != expected_rows[cells[0]][0] or cells[4] != expected_rows[cells[0]][1]:
            return False
        ids = [int(n) for n in re.findall(r"\d+", cells[1])]
        if not ids or any(n not in by_id for n in ids):
            return False
        locator = re.search(r"original line (\d+)", cells[1])
        if locator is None or cells[1] != f"`sources/ci-excerpt.log`, original line {ids[0]}":
            return False
        source_time = re.search(r"\d{4}-\d\d-\d\dT[\d:.]+Z", by_id[ids[0]])
        if source_time is None or source_time.group() != cells[2]:
            return False
        if ("7 fractional digits" not in cells[3] or "recorded Z" not in cells[3]
                or "clock accuracy unknown" not in cells[3].lower() or not cells[6].strip()):
            return False
        predecessor = SELECTED[SELECTED.index(ids[0]) - 1] if SELECTED.index(ids[0]) else None
        if predecessor is None:
            if "selected log" not in cells[6]:
                return False
        elif f"After original line {predecessor}" not in cells[6]:
            return False
        cited.extend(ids)
    return sorted(cited) == SELECTED and len(expected_rows) == 13


class IncidentTriageExampleTests(unittest.TestCase):
    def test_public_inputs_have_bound_source_identity_without_private_dependencies(self):
        manifest = json.loads((CASE / "manifest.json").read_text())
        excerpt = (CASE / "sources/ci-excerpt.log").read_bytes()
        self.assertEqual(hashlib.sha256(excerpt).hexdigest(), manifest["excerpt_sha256"])
        self.assertEqual(manifest["selected_original_line_ids"], SELECTED)
        self.assertRegex(manifest["full_original_sha256"], r"^[a-f0-9]{64}$")
        self.assertEqual(set(manifest["input_files"]), {"sources/case.md", "sources/ci-excerpt.log", "sources/source-lines.json"})
        for name, digest in manifest["input_files"].items():
            self.assertEqual(hashlib.sha256((CASE / name).read_bytes()).hexdigest(), digest)
        snapshots = json.loads((CASE / "sources/source-lines.json").read_text())["files"]
        self.assertEqual({s["path"] for s in snapshots}, {"examples/change-impact/change.diff", "skills/change-impact/assets/example-input.md"})
        for snapshot in snapshots:
            self.assertEqual(snapshot["revision"], manifest["source_run_head"])
            self.assertRegex(snapshot["git_blob"], r"^[a-f0-9]{40}$")
            self.assertRegex(snapshot["sha256"], r"^[a-f0-9]{64}$")
            self.assertEqual(len(snapshot["selected_lines"]), 3)
            self.assertEqual(set(snapshot["selected_lines"].values()), {" "})
        self.assertNotRegex(Path(__file__).read_text(), r"/(?:Users|home)/[A-Za-z]")

    def test_two_reports_are_self_contained_and_bounded(self):
        incident = (CASE / "incident.md").read_text()
        timeline = (CASE / "timeline.md").read_text()
        self.assertIn("## Hypotheses", incident)
        self.assertIn("Next checks", incident)
        for text in [incident.lower(), timeline.lower()]:
            self.assertIn("unknown", text)
            self.assertIn("not assessed", text)
        self.assertIn("no customer impact", incident.lower())
        self.assertIn("semantic-model proof", incident.lower())
        self.assertIn("No original CI", (CASE / "README.md").read_text())

    def test_timeline_fields_reject_substring_kinds_foreign_sources_and_invented_accuracy(self):
        manifest = json.loads((CASE / "manifest.json").read_text())
        excerpt = (CASE / "sources/ci-excerpt.log").read_text()
        incident = (CASE / "incident.md").read_text()
        timeline = (CASE / "timeline.md").read_text()
        self.assertTrue(validate_fixture(manifest, excerpt, incident, timeline))
        for bad in (timeline.replace("| event |", "| not-event |", 1),
                    timeline.replace("`sources/ci-excerpt.log`", "`sources/other.log`", 1),
                    timeline.replace("clock accuracy unknown", "clock accuracy verified", 1),
                    timeline.replace("recorded Z", "recorded +01:00", 1)):
            with self.subTest(timeline=bad):
                self.assertFalse(validate_fixture(manifest, excerpt, incident, bad))

    def test_complete_header_matches_the_actual_installed_template(self):
        manifest = json.loads((CASE / "manifest.json").read_text())
        excerpt = (CASE / "sources/ci-excerpt.log").read_text()
        incident = (CASE / "incident.md").read_text()
        timeline = (CASE / "timeline.md").read_text()
        template = (ROOT / "skills/incident-triage/assets/timeline-template.md").read_text()
        self.assertTrue(validate_fixture(manifest, excerpt, incident, timeline))
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "skills/incident-triage/assets/timeline-template.md"
            target.parent.mkdir(parents=True)
            target.write_text(template.replace("Precision/timezone/clock", "Clock"))
            with patch.dict(globals(), {"ROOT": Path(directory)}):
                self.assertFalse(validate_fixture(manifest, excerpt, incident, timeline))

    def test_authored_fixture_validator_rejects_the_declared_mutations(self):
        self.assertTrue(callable(globals().get("validate_fixture")), "fixture controls must actually execute, not merely name countercases")
        manifest = json.loads((CASE / "manifest.json").read_text())
        excerpt = (CASE / "sources/ci-excerpt.log").read_text()
        incident = (CASE / "incident.md").read_text()
        timeline = (CASE / "timeline.md").read_text()
        self.assertTrue(validate_fixture(manifest, excerpt, incident, timeline))
        wrong_revision = copy.deepcopy(manifest)
        wrong_revision["source_run_head"] = "0" * 40
        mutants = {
            "wrong_revision": (wrong_revision, excerpt, incident, timeline),
            "missing_contradiction": (manifest, "\n".join(l for l in excerpt.splitlines() if not l.endswith("Z OK")) + "\n", incident, timeline),
            "wrong_timeline_timestamp": (manifest, excerpt, incident, timeline.replace("2026-11-06T22:37:06.8380110Z", "2026-11-07T22:37:06.8380110Z")),
            "wrong_locator": (manifest, excerpt, incident, timeline.replace("original line 171", "original line 170")),
            "false_production_impact": (manifest, excerpt, incident.replace("- Customer impact: Unknown.", "- Customer impact: Confirmed outage."), timeline),
            "false_fixed_from_retry": (manifest, excerpt, incident.replace("- Resolution: Not assessed.", "- Resolution: Fixed by retry."), timeline),
        }
        self.assertEqual(set(mutants), set(manifest["authored_countercases"]))
        for name, inputs in mutants.items():
            with self.subTest(name=name):
                self.assertFalse(validate_fixture(*inputs), name)
        self.assertFalse(validate_fixture(manifest, excerpt, incident, timeline.replace("| event |", "| collection |", 1)))
        self.assertFalse(validate_fixture(manifest, excerpt, incident, timeline.replace("Timestamp precision: 7 fractional digits", "Timestamp precision: milliseconds", 1)))
        self.assertFalse(validate_fixture(manifest, excerpt, incident, timeline.replace("After original line 169", "After original line 168", 1)))
        self.assertTrue(validate_fixture(manifest, excerpt, incident, timeline.replace("clock accuracy unknown", "clock accuracy unknown (not measured)", 1)))


if __name__ == "__main__":
    unittest.main()
