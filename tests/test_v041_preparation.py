"""v0.4.1 preparation is not publication or stable-default promotion."""
from pathlib import Path
import os
import json
import re
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "docs/releases/v0.4.1.md"
BASE = "e3ba0893f2ae03587206c4ee8d15c5187c29ebea"
RELEASE = "79284b3faa928dc556a9032aa9dbeb059b4ee915"


class V041PreparationTests(unittest.TestCase):
    def test_preparation_keeps_publication_and_evidence_boundaries(self):
        self.assertTrue(NOTES.is_file(), "v0.4.1 preparation notes missing")
        text = NOTES.read_text()
        for phrase in ["Not published", "v0.4.1", "0.1.1", "0.1.2", BASE,
                       "ten skills", "assisted", "not a controlled comparison",
                       "only after the tag and public archives exist", "Do not rerun"]:
            self.assertIn(phrase, text)
        self.assertIn("git clone --branch v0.4.1", (ROOT / "README.md").read_text())
        setup = (ROOT / "docs/quickstart.md").read_text()
        self.assertIn(RELEASE, setup)
        self.assertIn("v0.4.1", setup)
        for name in ["decision-brief", "document-actions"]:
            self.assertIn('status: "published"', (ROOT / "skills" / name / "SKILL.md").read_text())

    def test_freshness_record_covers_all_retained_guides_and_notices(self):
        path = ROOT / "docs/releases/v0.4.1-freshness.json"
        self.assertTrue(path.is_file(), "fresh v0.4.1 inventory missing")
        audit = json.loads(path.read_text())
        self.assertEqual(audit["failures"], [])
        # Compare the frozen release inventory with its recorded pre-refresh catalogue,
        # not the newer current-source Dexpot selection. All identity checks remain.
        catalog = json.loads((ROOT / "docs/published-upstream-refresh.json").read_text())["catalog_before_refresh"]["skills"]
        packages = {row["name"]: row for row in audit["packages"]}
        self.assertEqual(len(packages), len(audit["packages"]))
        self.assertEqual(set(packages), {row["name"] for row in catalog})
        self.assertEqual(set(audit["repositories"]), {row["upstream_repository"] for row in catalog})
        for row in catalog:
            package = packages[row["name"]]
            self.assertEqual(package["pin"]["commit"], row["upstream_revision"])
            self.assertEqual(package["pin"]["sha256"], row["upstream_sha256"])
            self.assertEqual(package["pin"]["notice"]["sha256"], row["license_sha256"])
            repo = audit["repositories"][row["upstream_repository"]]
            self.assertEqual(package["main"]["commit"], repo["default_commit"])
            self.assertEqual(package["release"]["commit"], repo["release_commit"])
            for key in ["pin", "main", "release"]:
                self.assertRegex(package[key]["commit"], r"^[0-9a-f]{40}$")
                self.assertRegex(package[key]["sha256"], r"^[0-9a-f]{64}$")
                self.assertRegex(package[key]["notice"]["sha256"], r"^[0-9a-f]{64}$")

    def copy_recipe(self, project, skill):
        match = re.search(r"# Copy the complete selected bundle\.\n(.*?)\n\)", NOTES.read_text(), re.S)
        self.assertIsNotNone(match)
        assert match is not None
        script = '( set -eu; test -d "$PROJECT"\n' + match[1] + '\n)'
        return subprocess.run(["sh", "-c", script], cwd=ROOT,
                              env={**os.environ, "PROJECT": str(project), "SKILL": skill,
                                   "SKILL_ROOT": str(project / "project skills")},
                              capture_output=True, text=True)

    def test_complete_ten_bundle_copy_and_sibling_preservation(self):
        fingerprint = lambda p: {f.relative_to(p).as_posix(): f.read_bytes()
                                  for f in p.rglob("*") if f.is_file()}
        with tempfile.TemporaryDirectory(prefix="v041 owned project ") as directory:
            project = Path(directory)
            root = project / "project skills"
            (root / "sibling").mkdir(parents=True)
            (root / "sibling/owner").write_text("UNCHANGED")
            skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
            self.assertEqual(len(skills), 10)
            for entry in skills:
                with self.subTest(skill=entry.parent.name):
                    result = self.copy_recipe(project, entry.parent.name)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(fingerprint(root / entry.parent.name), fingerprint(entry.parent))
            self.assertEqual((root / "sibling/owner").read_text(), "UNCHANGED")

    def test_copy_refuses_existing_files_directories_and_both_symlink_kinds(self):
        for kind in ["file", "directory", "live-symlink", "dangling-symlink"]:
            with self.subTest(kind=kind), tempfile.TemporaryDirectory(prefix="v041 collision ") as directory:
                project = Path(directory)
                root = project / "project skills"
                root.mkdir()
                target = root / "decision-brief"
                outside = project / "owned outside"
                if kind != "dangling-symlink":
                    outside.mkdir()
                    (outside / "owner").write_text("UNCHANGED")
                if kind == "file":
                    target.write_text("LOCAL EDITS")
                elif kind == "directory":
                    target.mkdir()
                    (target / "owner").write_text("LOCAL EDITS")
                else:
                    target.symlink_to(outside, target_is_directory=True)
                self.assertNotEqual(self.copy_recipe(project, "decision-brief").returncode, 0)
                if kind == "file":
                    self.assertEqual(target.read_text(), "LOCAL EDITS")
                elif kind == "directory":
                    self.assertEqual({p.name for p in target.iterdir()}, {"owner"})
                    self.assertEqual((target / "owner").read_text(), "LOCAL EDITS")
                else:
                    self.assertTrue(target.is_symlink())
                    self.assertEqual(target.readlink(), outside)
                if kind == "dangling-symlink":
                    self.assertFalse(outside.exists())
                else:
                    self.assertEqual({p.name for p in outside.iterdir()}, {"owner"})
                    self.assertEqual((outside / "owner").read_text(), "UNCHANGED")

    def test_future_release_clone_failure_cannot_copy_a_decoy(self):
        self.assertTrue(NOTES.is_file(), "v0.4.1 preparation notes missing")
        block = re.search(r"```sh\n(.*?)\n```", NOTES.read_text(), re.S)
        self.assertIsNotNone(block)
        assert block is not None
        with tempfile.TemporaryDirectory(prefix="v041 clone guard ") as directory:
            project = Path(directory)
            (project / "owned").mkdir()
            (project / "skills/decision-brief").mkdir(parents=True)
            (project / "skills/decision-brief/SKILL.md").write_text("DECOY")
            script = block[1].replace("/absolute/owned-project", str(project / "owned"))
            script = script.replace("https://github.com/tugrulguner/skillpot.git", "absent-local-remote")
            result = subprocess.run(["sh", "-c", script], cwd=project, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((project / "owned/.claude/skills/decision-brief").exists())
            self.assertEqual((project / "skills/decision-brief/SKILL.md").read_text(), "DECOY")


if __name__ == "__main__":
    unittest.main()
