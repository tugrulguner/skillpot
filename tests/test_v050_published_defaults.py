"""Current v0.5.0 selection and immutable public-distribution evidence."""
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
COMMIT = "044213fd00343e94b4d389c3ca2c0f2909feb79f"


class V050PublicationTests(unittest.TestCase):
    def test_every_published_bundle_matches_the_public_tag_install_record(self):
        record = json.loads((ROOT / "docs/releases/v0.5.0-distribution.json").read_text())
        summary = record["summary"]
        self.assertEqual(summary["source_commit"], COMMIT)
        self.assertEqual(summary["tag"], "v0.5.0")
        self.assertEqual(summary["passed"], 17)
        self.assertEqual(summary["unique_names"], 17)
        names = [row["name"] for row in record["skills"]]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(set(names), {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")})
        count = 0
        for row in record["skills"]:
            directory = ROOT / "skills" / row["name"]
            actual = {p.relative_to(directory).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in directory.rglob("*") if p.is_file()}
            self.assertEqual(actual, row["source_files"], row["name"])
            count += len(actual)
            for field in ("passed", "selected_only", "lock_ref_verified",
                          "selected_removal_verified", "sibling_preserved"):
                self.assertIs(row[field], True, (row["name"], field))
            self.assertIs(row["placement"]["agent_is_symlink"], False)
        self.assertEqual(count, 113)
        self.assertEqual(summary["bundle_files"], count)

    def test_all_active_first_use_selections_use_the_published_revision(self):
        for name in ("claim-check", "change-impact", "bug-repro", "incident-triage",
                     "benchmark-audit", "experiment-design", "verification-loop"):
            text = (ROOT / "docs" / (name + "-first-use.md")).read_text()
            command = re.search(r"```sh\n([^\n]+)\n```", text)
            self.assertIsNotNone(command)
            assert command is not None
            self.assertEqual(command[1], "npx skills@1.7.6 add https://github.com/tugrulguner/skillpot/tree/"
                             + COMMIT + " --skill " + name)
            self.assertIn("construction-time publication labels", text)

    def test_release_record_preserves_preparation_and_public_archive_identities(self):
        text = (ROOT / "docs/releases/v0.5.0.md").read_text()
        self.assertLess(text.index("**Published:**"), text.index("**Not published.**"))
        for value in (COMMIT, "726e18899c2d51cec2bac12293e0a4d83a9a9f9ca05b2601007238a99939e386",
                      "9d1300616e820fcb6b2f180443cb6076ccd18e039a381bc494c02b859fd19ff4"):
            self.assertIn(value, text)
        self.assertIn("v0.4.1", text)


if __name__ == "__main__":
    unittest.main()
