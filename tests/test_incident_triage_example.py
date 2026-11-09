"""Offline source/fixture checks; not an incident-response model evaluation."""
import copy
import hashlib
import json
from pathlib import Path
import re
import unittest

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
    cited = []
    for row in timeline.splitlines():
        if not row.startswith("| 2026-"):
            continue
        cells = [cell.strip() for cell in row.split("|")[1:-1]]
        if len(cells) != 3:
            return False
        ids = [int(n) for n in re.findall(r"\d+", cells[2])]
        if not ids or any(n not in by_id for n in ids):
            return False
        actual = re.findall(r"\d{4}-\d\d-\d\dT[\d:.]+Z", cells[0])
        source_times = [re.search(r"\d{4}-\d\d-\d\dT[\d:.]+Z", by_id[n]) for n in ids]
        if any(match is None for match in source_times):
            return False
        expected = [match.group() for match in source_times if match is not None]
        if actual != ([expected[0]] if len(ids) == 1 else [expected[0], expected[-1]]):
            return False
        cited.extend(ids)
    return sorted(cited) == SELECTED


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
            "wrong_locator": (manifest, excerpt, incident, timeline.replace("Original line 171", "Original line 170")),
            "false_production_impact": (manifest, excerpt, incident.replace("- Customer impact: Unknown.", "- Customer impact: Confirmed outage."), timeline),
            "false_fixed_from_retry": (manifest, excerpt, incident.replace("- Resolution: Not assessed.", "- Resolution: Fixed by retry."), timeline),
        }
        self.assertEqual(set(mutants), set(manifest["authored_countercases"]))
        for name, inputs in mutants.items():
            with self.subTest(name=name):
                self.assertFalse(validate_fixture(*inputs), name)


if __name__ == "__main__":
    unittest.main()
