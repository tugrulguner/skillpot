"""Released-source refresh checks, not runtime or agent-performance evidence."""
from pathlib import Path
import hashlib
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
DEXPOT_RELEASE = "a670e626cf73e1c4b21e0529294a87f1aa83e74f"
DEXPOT_GUIDE = "064792cb9897483af66fa1199cbcf4be97cc3e26417533dbb87a36e471a3fa0d"


class PublishedGuideRefreshTests(unittest.TestCase):
    def test_dexpot_released_reference_and_entrypoint_share_supported_path_contract(self):
        catalog = json.loads((ROOT / "catalog/modepot-sources.json").read_text())
        row = next(p for p in catalog["skills"] if p["name"] == "dexpot")
        self.assertEqual(row["upstream_revision"], DEXPOT_RELEASE)
        reference = (ROOT / "skills/dexpot/references/upstream.md").read_bytes()
        self.assertEqual(hashlib.sha256(reference).hexdigest(), DEXPOT_GUIDE)
        self.assertEqual(row["upstream_sha256"], DEXPOT_GUIDE)
        entry = (ROOT / "skills/dexpot/SKILL.md").read_text()
        for token in [DEXPOT_RELEASE, 'version: "0.3.0"', 'Dexpot 0.8.1+',
                      '`str`, `int`, unannotated parameters, and `Any`',
                      '`TypeError`', 'registration', 'Body/response schema support']:
            self.assertIn(token, entry)
        self.assertNotIn('Typed input sources (unreleased)', reference.decode())


    def test_refresh_has_explicit_collection_and_runtime_boundaries(self):
        note = ROOT / "docs/published-upstream-refresh.md"
        self.assertTrue(note.is_file(), "scoped refresh record missing")
        text = note.read_text()
        for token in ["Dexpot v0.8.1", "0.3.0", DEXPOT_RELEASE,
                      "not included in published SkillPot v0.4.1", "No product runtime",
                      "nine other bundles", "typed query/header/cookie"]:
            self.assertIn(token, text)
        compatibility = (ROOT / "skills/dexpot/compatibility.md").read_text()
        self.assertIn("Dexpot v0.8.1", compatibility)
        self.assertIn("0.3.0", compatibility)
        self.assertIn("not included in published SkillPot v0.4.1", compatibility)
        self.assertIn("0.7.1", compatibility)  # Retain original runtime-evidence identity.


    def test_audit_retains_old_catalog_and_selects_only_one_published_contract(self):
        path = ROOT / "docs/published-upstream-refresh.json"
        self.assertTrue(path.is_file(), "complete scoped audit inventory missing")
        audit = json.loads(path.read_text())
        before = {p["name"]: p for p in audit["catalog_before_refresh"]["skills"]}
        after = {p["name"]: p for p in json.loads((ROOT / "catalog/modepot-sources.json").read_text())["skills"]}
        self.assertEqual(set(before), set(after))
        self.assertEqual(audit["catalogue_package_count"], 7)
        self.assertEqual(audit["unique_repository_count"], 4)
        self.assertEqual(audit["snapshot_count"], 21)
        self.assertEqual(audit["failures"], [])
        self.assertEqual([name for name in before if before[name] != after[name]], ["dexpot"])
        self.assertEqual(before["dexpot"]["upstream_revision"], "409df5b68a2386bd04e1f2cf0f057773142e0759")
        self.assertEqual(after["dexpot"]["upstream_revision"], DEXPOT_RELEASE)
        identities = set()
        for package in audit["packages"]:
            self.assertEqual(len(package["snapshots"]), 3)
            self.assertEqual({s["label"] for s in package["snapshots"]}, {"held_pin", "latest_release", "main"})
            self.assertEqual(package["held_pin"], before[package["name"]]["upstream_revision"])
            for snapshot in package["snapshots"]:
                self.assertRegex(snapshot["ref"], r"^[0-9a-f]{40}$")
                self.assertIn('/' + snapshot["ref"] + '/', snapshot["guide_url"])
                self.assertIn('/' + snapshot["ref"] + '/', snapshot["license_url"])
                self.assertRegex(snapshot["guide_sha256"], r"^[0-9a-f]{64}$")
                self.assertEqual(snapshot["license_sha256"], before[package["name"]]["license_sha256"])
                for field in ["path", "license_path"]:
                    identities.add((package["repository"], package[field], snapshot["ref"]))
        self.assertEqual(len(identities), audit["unique_cached_blob_count"])


if __name__ == "__main__":
    unittest.main()
