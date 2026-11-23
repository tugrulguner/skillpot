"""Preparation-only source/distribution integrity, not task efficacy or publication."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = "d91297f4d388a5c98a069e70dc3d7e7ea752479f"
FLAGS = ("passed", "selected_only", "lock_ref_verified", "list_verified",
         "selected_removal_verified", "sibling_preserved")


class V060PreparationTests(unittest.TestCase):
    def test_complete_nineteen_selection_receipt_matches_every_current_bundle(self):
        record = json.loads((ROOT / "docs/releases/v0.6.0-distribution.json").read_text())
        self.assertEqual(record["source_commit"], BASE)
        self.assertEqual(record["schema_version"], 1)
        self.assertIs(record["passed"], True)
        bundles = {p.parent.name: p.parent for p in (ROOT / "skills").glob("*/SKILL.md")}
        self.assertEqual(len(bundles), 19)
        self.assertEqual(set(record["skills"]), set(bundles))
        total = 0
        for name, directory in bundles.items():
            row = record["skills"][name]
            self.assertEqual(row["source_commit"], BASE)
            self.assertEqual(row["skill"], name)
            actual = {p.relative_to(directory).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in directory.rglob("*") if p.is_file()}
            self.assertEqual(row["source_files"], actual, name)
            self.assertEqual(row["installed_files"], actual, name)
            for flag in FLAGS:
                self.assertIs(row[flag], True, (name, flag))
            self.assertEqual(set(row["lock"]["skills"]), {name})
            entry = row["lock"]["skills"][name]
            self.assertEqual(entry["ref"], BASE)
            self.assertEqual(entry["source"], "tugrulguner/skillpot")
            self.assertEqual(entry["skillPath"], f"skills/{name}/SKILL.md")
            self.assertEqual(row["node"], "v22.23.4")
            self.assertEqual(row["installer"], "1.7.6")
            total += len(actual)
        self.assertEqual(total, 133)
        self.assertEqual(record["bundle_files"], total)
        self.assertNotIn("/Users/", json.dumps(record))

    def test_public_freshness_record_is_complete_pinned_and_private_path_free(self):
        record = json.loads((ROOT / "docs/releases/v0.6.0-freshness.json").read_text())
        catalogue = json.loads((ROOT / "catalog/modepot-sources.json").read_text())
        expected = {r["name"]: r for r in catalogue["skills"]}
        rows = record["package_records"]
        self.assertEqual(record["repository_commit"], BASE)
        self.assertEqual(record["package_count"], 7)
        self.assertEqual(len(rows), 7)
        self.assertEqual({r["name"] for r in rows}, set(expected))
        self.assertEqual(len(record["repositories"]), 4)
        self.assertIs(record["runtime_or_product_trials"], False)
        for row in rows:
            held = expected[row["name"]]
            self.assertEqual(row["held_revision"], held["upstream_revision"])
            self.assertEqual(row["held_fetched_sha256"], held["upstream_sha256"])
            self.assertEqual(row["held_catalog_guide_sha256"], held["upstream_sha256"])
            self.assertEqual(row["fresh_default_license_sha256"], held["license_sha256"])
            self.assertEqual(row["latest_release_license_sha256"], held["license_sha256"])
            self.assertIs(row["unchanged_from_v050_freshness_review"], True)
            for key in ("held_revision", "fresh_default_commit", "fresh_latest_release_commit"):
                self.assertRegex(row[key], r"^[0-9a-f]{40}$")
            for key in ("fresh_default_guide_sha256", "latest_release_guide_sha256"):
                self.assertRegex(row[key], r"^[0-9a-f]{64}$")
            root = "https://github.com/" + row["repository"]
            self.assertEqual(row["fresh_default_guide_url"],
                             root + "/blob/" + row["fresh_default_commit"] + "/" + row["path"])
            self.assertEqual(row["latest_release_guide_url"],
                             root + "/blob/" + row["fresh_latest_release_commit"] + "/" + row["path"])
            self.assertTrue(row["classification"].strip())
        comparison = record["prior_v050_comparison"]
        self.assertEqual(comparison["byte_comparisons"], 28)
        for key in ("same_default_commits", "same_latest_release_commits",
                    "same_held_default_release_guide_and_default_notice_bytes"):
            self.assertIs(comparison[key], True)
        self.assertNotIn("/Users/", json.dumps(record))

    def test_proposal_is_conditional_and_preserves_published_default(self):
        text = (ROOT / "docs/releases/v0.6.0.md").read_text()
        for phrase in ("**Not published.**", "invariant-audit 0.1.0",
                       "performance-investigation 0.1.0", "nineteen skills / 133 bundle files",
                       "Preparation merge and publication require separate approval.",
                       "tree/v0.6.0 --skill performance-investigation",
                       "Older-command warning", "not native loading"):
            self.assertIn(phrase, text)
        readme = (ROOT / "README.md").read_text()
        self.assertIn("Published v0.5.0 contains seventeen skills", readme)
        self.assertNotIn("tree/v0.6.0", readme)
        self.assertNotIn("checkout v0.6.0", (ROOT / "docs/quickstart.md").read_text())


if __name__ == "__main__":
    unittest.main()
