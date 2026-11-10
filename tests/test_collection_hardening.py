"""Current-source distribution regressions; not agent-task accuracy tests."""
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PIN = "66bad57a0a42a4aec2c5d54feee1df8fb242e166"


class CollectionHardeningTests(unittest.TestCase):
    def test_current_source_matrix_binds_every_bundle_and_verified_install_boundary(self):
        path = ROOT / "docs/skill-hardening-distribution.json"
        self.assertTrue(path.is_file(), "real public installer matrix is required")
        record = json.loads(path.read_text())
        self.assertEqual(record["source_commit"], PIN)
        self.assertEqual(record["installer"], "skills@1.7.6")
        self.assertEqual(set(record["agents"]), {"claude-code", "cursor", "codex", "hermes-agent"})
        self.assertFalse(record["client_or_model_launched"])
        names = {p.name for p in (ROOT / "skills").iterdir() if p.is_dir()}
        self.assertEqual({row["name"] for row in record["skills"]}, names)
        self.assertEqual(len(record["skills"]), len(names))
        for row in record["skills"]:
            with self.subTest(name=row["name"]):
                package = ROOT / "skills" / row["name"]
                actual = {p.relative_to(package).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in package.rglob("*") if p.is_file()}
                self.assertEqual(row["source_files"], actual)
                self.assertEqual(row["files_verified"], len(actual))
                for field in ("selected_only", "lock_ref_verified", "project_links_verified",
                              "standalone_resource_links_verified", "sibling_preserved",
                              "selected_removal_verified", "no_global_install"):
                    self.assertIs(row[field], True, field)

    def test_reader_facing_current_source_defaults_select_the_verified_bytes(self):
        expected = "npx skills@1.7.6 add https://github.com/tugrulguner/skillpot/tree/" + PIN + " --skill claim-check"
        for relative in ("website/src/content/docs/index.mdx", "catalog/README.md", "website/public/llms.txt"):
            with self.subTest(path=relative):
                self.assertIn(expected, (ROOT / relative).read_text())
        self.assertIn("[claim-check](skills/claim-check/SKILL.md) 0.1.1", (ROOT / "README.md").read_text())

    def test_current_hardening_guide_selects_one_explicit_pinned_bundle(self):
        path = ROOT / "docs/skill-hardening.md"
        self.assertTrue(path.is_file(), "current-source guide is required")
        text = path.read_text()
        command = re.search(r"```sh\n(.*?)\n```", text, re.S)
        self.assertIsNotNone(command)
        assert command is not None
        self.assertEqual(command[1], "npx skills@1.7.6 add https://github.com/tugrulguner/skillpot/tree/" + PIN + " --skill claim-check")
        for token in ("fourteen", "v0.4.1", "ten", "user edits", "native", "model", "skill-hardening-distribution.json"):
            self.assertIn(token, " ".join(text.split()))
        self.assertNotIn("--all", command[1])
        self.assertNotIn("--global", command[1])


if __name__ == "__main__":
    unittest.main()
