"""Exercise the exact documented offline copy recipes, not a host client."""
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DocumentActionsFirstUseTests(unittest.TestCase):
    def section(self):
        text = (ROOT / "docs/quickstart.md").read_text()
        self.assertIn("## Try document-actions from pinned source", text)
        return text.split("## Try document-actions from pinned source", 1)[1].split("\n## ", 1)[0]

    def run_copy(self, project, index):
        recipes = re.findall(r"(?ms)^\(\n  set -eu\n.*?^\)", self.section())
        self.assertEqual(len(recipes), 2)
        return subprocess.run(["sh", "-c", recipes[index]], cwd=ROOT,
                              env={**os.environ, "PROJECT": str(project),
                                   "SKILL_ROOT": str(project / "skills")},
                              capture_output=True, text=True)

    def test_complete_package_packet_and_fresh_output(self):
        with tempfile.TemporaryDirectory(prefix="document actions ") as temp:
            project = Path(temp)
            (project / "skills/other-skill").mkdir(parents=True)
            (project / "skills/other-skill/SKILL.md").write_text("OWNER")
            for index in [0, 1]:
                result = self.run_copy(project, index)
                self.assertEqual(result.returncode, 0, result.stderr)
            fingerprint = lambda path: {p.relative_to(path).as_posix(): p.read_bytes()
                                        for p in path.rglob("*") if p.is_file()}
            self.assertEqual(fingerprint(project / "skills/document-actions"),
                             fingerprint(ROOT / "skills/document-actions"))
            self.assertEqual(fingerprint(project / "document-actions-input"),
                             fingerprint(ROOT / "examples/document-actions/inputs"))
            self.assertEqual(list((project / "document-actions-output").iterdir()), [])
            self.assertEqual((project / "skills/other-skill/SKILL.md").read_text(), "OWNER")

    def test_existing_selected_destinations_are_refused(self):
        for kind in ["file", "directory", "symlink"]:
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temp:
                project = Path(temp)
                (project / "skills").mkdir()
                destination = project / "skills/document-actions"
                outside = project / "other-owned-directory"
                outside.mkdir()
                (outside / "sentinel").write_text("UNCHANGED")
                if kind == "file":
                    destination.write_text("LOCAL")
                elif kind == "directory":
                    destination.mkdir()
                    (destination / "SKILL.md").write_text("LOCAL")
                else:
                    destination.symlink_to(outside, target_is_directory=True)
                self.assertNotEqual(self.run_copy(project, 0).returncode, 0)
                self.assertEqual(list(p.name for p in outside.iterdir()), ["sentinel"])
                self.assertEqual((outside / "sentinel").read_text(), "UNCHANGED")
                if kind == "file":
                    self.assertEqual(destination.read_text(), "LOCAL")
                elif kind == "directory":
                    self.assertEqual((destination / "SKILL.md").read_text(), "LOCAL")
                    self.assertEqual(list(p.name for p in destination.iterdir()), ["SKILL.md"])
                else:
                    self.assertTrue(destination.is_symlink())

    def test_existing_output_remains_untouched(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            output = project / "document-actions-output"
            output.mkdir()
            (output / "actions.md").write_text("OWNER")
            self.assertNotEqual(self.run_copy(project, 1).returncode, 0)
            self.assertEqual((output / "actions.md").read_text(), "OWNER")
            self.assertEqual(list(p.name for p in output.iterdir()), ["actions.md"])

    def test_real_source_pin_and_safe_clone_chain(self):
        section = self.section()
        self.assertRegex(section, r"checkout --detach [0-9a-f]{40} &&")
        match = re.search(r"```sh\n(git clone .*?)\n```", section, re.DOTALL)
        self.assertIsNotNone(match)
        assert match is not None
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "skillpot-actions-source"
            source.mkdir()
            (source / "owner.txt").write_text("OWNER")
            result = subprocess.run(["sh", "-c", match[1]], cwd=temp,
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("not a git repository", result.stderr)
            self.assertEqual((source / "owner.txt").read_text(), "OWNER")


if __name__ == "__main__":
    unittest.main()
