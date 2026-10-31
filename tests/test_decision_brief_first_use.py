"""Execute documented copy steps in owned fixtures, not a client or installer."""
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DecisionBriefFirstUseTests(unittest.TestCase):
    def run_recipe(self, skill_root):
        text = (ROOT / "docs/quickstart.md").read_text()
        marker = "## Try decision-brief from reviewed source"
        self.assertIn(marker, text, "source-only first-use instructions missing")
        section = text.split(marker, 1)[1].split("\n## ", 1)[0]
        match = re.search(r"(?ms)^\(\n  set -eu\n.*?^\)", section)
        self.assertIsNotNone(match, "copy recipe must be complete and fail closed")
        assert match is not None
        return subprocess.run(["sh", "-c", match.group()], cwd=ROOT,
                              env={**os.environ, "SKILL_ROOT": str(skill_root)},
                              capture_output=True, text=True)

    def test_complete_bundle_and_sibling_preservation(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "project-skills"
            target.mkdir()
            sibling = target / "other-skill"
            sibling.mkdir()
            (sibling / "SKILL.md").write_text("SIBLING")
            result = self.run_recipe(target)
            self.assertEqual(result.returncode, 0, result.stderr)
            source = ROOT / "skills/decision-brief"
            expected = {p.relative_to(source).as_posix(): p.read_bytes()
                        for p in source.rglob("*") if p.is_file()}
            installed = target / "decision-brief"
            actual = {p.relative_to(installed).as_posix(): p.read_bytes()
                      for p in installed.rglob("*") if p.is_file()}
            self.assertEqual(actual, expected)
            self.assertEqual((sibling / "SKILL.md").read_text(), "SIBLING")
            self.assertEqual({p.name for p in target.iterdir()}, {"other-skill", "decision-brief"})

    def test_existing_file_directory_and_symlink_are_refused(self):
        for kind in ["file", "directory", "symlink"]:
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temp:
                target = Path(temp) / "skills"
                target.mkdir()
                destination = target / "decision-brief"
                outside = Path(temp) / "other-owned-directory"
                outside.mkdir()
                (outside / "sentinel").write_text("UNCHANGED")
                if kind == "file":
                    destination.write_text("LOCAL EDITS")
                elif kind == "directory":
                    destination.mkdir()
                    (destination / "SKILL.md").write_text("LOCAL EDITS")
                else:
                    destination.symlink_to(outside, target_is_directory=True)
                self.assertNotEqual(self.run_recipe(target).returncode, 0)
                self.assertEqual((outside / "sentinel").read_text(), "UNCHANGED")
                self.assertEqual([p.name for p in outside.iterdir()], ["sentinel"])
                if kind == "file":
                    self.assertEqual(destination.read_text(), "LOCAL EDITS")
                elif kind == "directory":
                    self.assertEqual((destination / "SKILL.md").read_text(), "LOCAL EDITS")
                    self.assertEqual([p.name for p in destination.iterdir()], ["SKILL.md"])
                else:
                    self.assertTrue(destination.is_symlink())

    def packet_recipe(self, project):
        text = (ROOT / "docs/quickstart.md").read_text().split("## Try decision-brief from reviewed source", 1)[1]
        blocks = re.findall(r"(?ms)^\(\n  set -eu\n.*?^\)", text)
        self.assertEqual(len(blocks), 2)
        return subprocess.run(["sh", "-c", blocks[1]], cwd=ROOT,
                              env={**os.environ, "PROJECT": str(project)},
                              capture_output=True, text=True)

    def test_only_task_sources_and_notices_are_prepared(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            result = self.packet_recipe(project)
            self.assertEqual(result.returncode, 0, result.stderr)
            packet = project / "decision-brief-example"
            expected = {"task.md", "sources.json", "NOTICE.md", "LICENSE-PYTHON.txt"}
            self.assertEqual({p.name for p in packet.iterdir()}, expected)
            for name in expected:
                self.assertEqual((packet / name).read_bytes(),
                                 (ROOT / "examples/decision-brief" / name).read_bytes())
            self.assertEqual(list((project / "decision-brief-output").iterdir()), [])

    def test_existing_output_is_not_modified(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            output = project / "decision-brief-output"
            output.mkdir()
            (output / "brief.md").write_text("OWNER DOCUMENT")
            result = self.packet_recipe(project)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual((output / "brief.md").read_text(), "OWNER DOCUMENT")
            self.assertEqual([p.name for p in output.iterdir()], ["brief.md"])

    def test_clone_refuses_existing_source_before_checkout(self):
        text = (ROOT / "docs/quickstart.md").read_text().split("## Try decision-brief from reviewed source", 1)[1]
        block = re.search(r"```sh\n(git clone .*?)\n```", text, re.DOTALL)
        self.assertIsNotNone(block)
        assert block is not None
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "skillpot-decision-source"
            source.mkdir()
            (source / "owner.txt").write_text("OWNER FILE")
            result = subprocess.run(["sh", "-c", block[1]], cwd=temp,
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("not a git repository", result.stderr)
            self.assertEqual((source / "owner.txt").read_text(), "OWNER FILE")

    def test_pin_prompt_and_release_boundaries_are_explicit(self):
        text = (ROOT / "docs/quickstart.md").read_text()
        self.assertIn("git -C skillpot-decision-source checkout --detach 4ca53963cafc8a9a3965808c485dc8c6ad502a66", text)
        self.assertIn("b4dabf93e7e4a85a55d947a05eb2989f035a58c1", text)
        self.assertIn("not included in published v0.3.0", text)
        self.assertIn("decision-brief-example/task.md", text)
        self.assertIn("decision-brief-example/sources.json", text)
        self.assertIn("decision-brief-output/brief.md", text)
        self.assertIn("decision-brief-output/evidence.md", text)


if __name__ == "__main__":
    unittest.main()
