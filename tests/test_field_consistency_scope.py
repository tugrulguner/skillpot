"""Source corrections must not silently change published installation defaults."""
from pathlib import Path
import hashlib
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
RELEASE = "3624eaaf2aa6c870e1dad6190ac3466e4e378f35"


class FieldConsistencyScopeTests(unittest.TestCase):
    def test_current_corrections_are_separate_from_the_published_snapshot(self):
        note = ROOT / "docs/field-consistency.md"
        self.assertTrue(note.is_file(), "current-source patch boundary note is missing")
        text = note.read_text()
        for required in ["0.1.1", "0.1.2", "v0.4.0", RELEASE,
                         "unreleased", "not a controlled comparison"]:
            self.assertIn(required, text)
        self.assertIn("docs/field-consistency.md", (ROOT / "README.md").read_text())
        self.assertIn("../docs/field-consistency.md", (ROOT / "catalog/README.md").read_text())

    def test_observation_record_keeps_exact_artifact_hashes_and_scope(self):
        record = ROOT / "evaluations/workflow-fields/followup-001"
        manifest = json.loads((record / "manifest.json").read_text())
        self.assertEqual(manifest["candidate_commit"], "6a3d6950a40e2fc6bec236741b59085e02486f8a")
        self.assertEqual(len(manifest["attempts"]), 4)
        attempts = {row["case"]: row for row in manifest["attempts"]}
        self.assertEqual(attempts["03-garden-actions"]["visible_tool_error_previews"], 1,
                         "preserve the recovered missing-path write failure")
        for name, digest in manifest["copied_file_sha256"].items():
            self.assertEqual(hashlib.sha256((record / name).read_bytes()).hexdigest(), digest, name)
        actual = {p.relative_to(record).as_posix() for p in record.rglob("*") if p.is_file()}
        self.assertEqual(actual, set(manifest["copied_file_sha256"]) | {"manifest.json"})
        self.assertEqual(len(list(record.glob("cases/*/output/*.md"))), 8)
        self.assertFalse(list(record.rglob("*.log")), "private runner logs must not be published")

    def test_stable_installation_still_selects_the_published_snapshot(self):
        self.assertIn("git clone --branch v0.4.0 --depth 1",
                      (ROOT / "README.md").read_text())
        setup = (ROOT / "docs/quickstart.md").read_text()
        for directory in ["skillpot-source", "skillpot-actions-source", "skillpot-decision-source"]:
            self.assertIn(f"git -C {directory} checkout --detach {RELEASE}", setup)


if __name__ == "__main__":
    unittest.main()
