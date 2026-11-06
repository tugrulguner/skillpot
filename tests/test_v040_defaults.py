"""Current post-publication defaults, distinct from immutable release history."""
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
RELEASE = "79284b3faa928dc556a9032aa9dbeb059b4ee915"
V040_RELEASE = "3624eaaf2aa6c870e1dad6190ac3466e4e378f35"


class V040DefaultsTests(unittest.TestCase):
    def test_readme_selects_published_ten_skill_release(self):
        text = (ROOT / "README.md").read_text()
        self.assertIn("git clone --branch v0.4.1 --depth 1", text)
        self.assertIn("Published v0.4.1 contains ten skills", text)
        self.assertIn("discussions/43", text)
        self.assertNotIn("not included in published v0.3.0", text)

    def test_readme_clone_failure_cannot_continue_to_copy(self):
        text = (ROOT / "README.md").read_text()
        block = re.search(r"<summary>Advanced:.*?</summary>.*?```sh\n(.*?)\n```", text, re.S)
        self.assertIsNotNone(block)
        assert block is not None
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            (project / "skillpot-source").mkdir()
            (project / "skillpot-source/owner").write_text("UNCHANGED")
            (project / "skills/intpot-python").mkdir(parents=True)
            (project / "skills/intpot-python/SKILL.md").write_text("WRONG SOURCE")
            destination = project / "project-skills"
            script = block[1].replace("https://github.com/tugrulguner/skillpot.git", "nonexistent-local-remote")
            script = script.replace("/absolute/owned-project/.claude/skills", str(destination))
            run = subprocess.run(["sh", "-c", script], cwd=project, env=os.environ.copy(),
                                 capture_output=True, text=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertFalse(destination.exists())
            self.assertEqual((project / "skillpot-source/owner").read_text(), "UNCHANGED")

    def test_all_first_use_source_selections_share_release_commit(self):
        text = (ROOT / "docs/quickstart.md").read_text()
        for directory in ["skillpot-source", "skillpot-actions-source", "skillpot-decision-source"]:
            self.assertIn(f"git -C {directory} checkout --detach {RELEASE}", text)
        for old in ["b4dabf93e7e4a85a55d947a05eb2989f035a58c1",
                    "8a07fb954694cae186a59893bcbc3c0c579dee1e",
                    "4ca53963cafc8a9a3965808c485dc8c6ad502a66"]:
            self.assertNotIn(old, text)
        self.assertNotIn("not included in published v0.3.0", text)

    def test_original_workflow_source_labels_match_verified_publication(self):
        for name, version in [("decision-brief", "0.1.1"), ("document-actions", "0.1.2")]:
            text = (ROOT / f"skills/{name}/SKILL.md").read_text()
            self.assertIn('status: "published"', text)
            self.assertIn(f'version: "{version}"', text)
            self.assertIn("v0.4.1", (ROOT / f"skills/{name}/compatibility.md").read_text())
        self.assertIn("experimental", (ROOT / "skills/repository-readiness/SKILL.md").read_text())

    def test_publication_record_keeps_exact_identity_and_public_parity(self):
        text = (ROOT / "docs/releases/v0.4.0.md").read_text()
        self.assertIn("**Published:**", text)
        self.assertIn(V040_RELEASE, text)
        self.assertIn("269", text)
        self.assertIn("5ae45d1c0359adf297c822704a1c8c1b608a6ffb58ce9c1542701edeba5a24c4", text)
        self.assertIn("c1f4f9992b9635bfdadf60134c925d97f3240645d9594639fc44b75472feca1b", text)
        self.assertIn("historical", text)

    def test_current_discovery_publishes_both_new_workflows(self):
        for filename in ["catalog/README.md", "website/src/content/docs/index.mdx", "website/public/llms.txt"]:
            text = (ROOT / filename).read_text()
            for name in ["decision-brief", "document-actions"]:
                self.assertIn(name, text)
            self.assertIn("v0.4.1", text)
            self.assertNotIn("not included in published v0.3.0", text)
            self.assertNotIn("reviewed, unreleased", text)


if __name__ == "__main__":
    unittest.main()
