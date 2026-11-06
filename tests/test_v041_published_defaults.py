"""Postpublication v0.4.1 defaults distinguish live source from archive."""
import unittest
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMIT = "79284b3faa928dc556a9032aa9dbeb059b4ee915"


class PublishedDefaultsTests(unittest.TestCase):
    def test_stable_checkout_and_workflow_guides_select_published_commit(self):
        sources = [ROOT / "README.md", ROOT / "docs/quickstart.md",
                   ROOT / "docs/project-skill-installation.md"]
        for path in sources:
            text = path.read_text()
            self.assertIn(COMMIT, text, str(path))
            self.assertNotIn("3624eaaf2aa6c870e1dad6190ac3466e4e378f35", text, str(path))

    def test_workflow_versions_are_published_and_current_source_not_mislabelled_unreleased(self):
        expectations = {"decision-brief": "0.1.1", "document-actions": "0.1.2"}
        for name, version in expectations.items():
            meta = (ROOT / f"skills/{name}/SKILL.md").read_text()
            self.assertIn(f'version: "{version}"', meta)
            self.assertNotIn('status: "unreleased"', meta)
            self.assertIn("v0.4.1", (ROOT / f"skills/{name}/compatibility.md").read_text())

    def test_publication_record_leads_with_archive_identity_and_historical_preparation(self):
        text = (ROOT / "docs/releases/v0.4.1.md").read_text()
        self.assertLess(text.index("**Published:**"), text.index("**Not published.**"))
        self.assertIn("ed653603b5dcdb764ee21c231566395177e0c4b577e8e6be9e5c3467c9157b79", text)
        self.assertIn("7c349755f5d031989b9dd7cc7d86450b25c51a633f60b450f89cd36319130a45", text)

    def test_website_names_live_excerpt_and_stable_release_separately(self):
        excerpt = (ROOT / "website/src/components/SkillExcerpt.astro").read_text()
        self.assertIn("current source", excerpt)
        self.assertIn("v0.4.1", excerpt)
        home = (ROOT / "website/src/content/docs/index.mdx").read_text()
        self.assertIn("npx skills@1.7.6 add https://github.com/tugrulguner/skillpot/tree/4139aff1dd8127fc4c9bb3916a4bc5e3fd5cd23c --skill claim-check", home)
        self.assertIn("releases/tag/v0.4.1", home)

    def test_publication_labels_do_not_change_released_instruction_bodies(self):
        # Frozen from the approved v0.4.1 commit, excluding YAML frontmatter only.
        expected = {
            "decision-brief": "b73497d11e7c7479a87a556852b85e42ec6d44ad26e420fde2f64fdcf3139e18",
            "document-actions": "e3f216bb9199575d95bd0ce26865b8abc9cfc30e359da69e719f9bffcff4d14d",
        }
        for name, digest in expected.items():
            body = (ROOT / f"skills/{name}/SKILL.md").read_bytes().split(b"---\n", 2)[2]
            self.assertEqual(hashlib.sha256(body).hexdigest(), digest, name)

    def test_current_discovery_retains_correct_versions_count_and_discussion(self):
        readme = (ROOT / "README.md").read_text()
        self.assertIn("discussions/43", readme)
        self.assertNotIn("discussions/34", readme)
        setup = (ROOT / "docs/quickstart.md").read_text()
        self.assertIn("`decision-brief` version 0.1.1", setup)
        self.assertIn("`document-actions` version 0.1.2", setup)
        home = (ROOT / "website/src/content/docs/index.mdx").read_text()
        self.assertIn("Published v0.4.1 has ten skills", home)
        self.assertNotIn("published collection has eight skills", home)
        for name, version in [("decision-brief", "0.1.1"), ("document-actions", "0.1.2")]:
            compatibility = (ROOT / f"skills/{name}/compatibility.md").read_text()
            self.assertIn(f"version `{version}`", compatibility)
            self.assertNotIn("not included in that release", compatibility)
        note = (ROOT / "docs/field-consistency.md").read_text()
        self.assertIn("included in published collection **v0.4.1**", note)
        self.assertNotIn("These are unreleased source patches", note)


if __name__ == "__main__":
    unittest.main()
