"""Release-preparation/source-copy checks, not tag publication or model trials."""
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "docs/releases/v0.4.0.md"


class V040PreparationTests(unittest.TestCase):
    def recipe(self):
        blocks = re.findall(r"(?ms)^\(\n  set -eu\n.*?^\)", NOTES.read_text())
        self.assertEqual(len(blocks), 1)
        return blocks[0]

    def copy(self, project, name="document-actions"):
        return subprocess.run(["sh", "-c", self.recipe()], cwd=ROOT,
                              env={**os.environ, "PROJECT": str(project), "SKILL": name,
                                   "SKILL_ROOT": str(project / "skills")},
                              capture_output=True, text=True)

    def test_preparation_history_and_published_defaults_are_distinct(self):
        text = NOTES.read_text()
        self.assertIn("Not published", text)
        self.assertIn("only after the tag and public archives exist", text)
        self.assertIn("Do not rerun", text)
        self.assertIn("2b8040fece04dc159a44e72e909e376f5d0583a3", text)
        self.assertIn("git clone --branch v0.4.0", (ROOT / "README.md").read_text())
        self.assertIn("checkout --detach 3624eaaf2aa6c870e1dad6190ac3466e4e378f35",
                      (ROOT / "docs/quickstart.md").read_text())
        current = (ROOT / "skills/document-actions/SKILL.md").read_text()
        self.assertIn('status: "unreleased"', current)
        self.assertIn('version: "0.1.2"', current)
        self.assertIn("Published version `0.1.1`", (ROOT / "skills/document-actions/compatibility.md").read_text())

    def test_contents_and_limits_cover_complete_collection(self):
        names = sorted(p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md"))
        self.assertEqual(len(names), 10)
        text = NOTES.read_text()
        self.assertIn("ten skills", text)
        for name in names:
            self.assertIn(f"`{name}`", text)
        for token in ["0.1.1", "assisted", "supplementary", "not a runtime", "v0.3.0"]:
            self.assertIn(token, text)

    def test_freshness_inventory_covers_each_retained_package(self):
        catalog = json.loads((ROOT / "catalog/modepot-sources.json").read_text())["skills"]
        audit = json.loads((ROOT / "docs/releases/v0.4.0-freshness.json").read_text())
        packages = {row["name"]: row for row in audit["packages"]}
        self.assertEqual(len(packages), len(audit["packages"]))
        self.assertEqual(set(packages), {row["name"] for row in catalog})
        self.assertEqual(set(audit["repositories"]), {row["upstream_repository"] for row in catalog})
        for row in catalog:
            record = packages[row["name"]]
            self.assertEqual(record["pinned"]["revision"], row["upstream_revision"])
            self.assertEqual(record["pinned"]["guide_sha256"], row["upstream_sha256"])
            self.assertEqual(record["pinned"]["license_sha256"], row["license_sha256"])
            repo = audit["repositories"][row["upstream_repository"]]
            self.assertEqual(record["main"]["revision"], repo["default_commit"])
            self.assertEqual(record["release"]["revision"], repo["release_commit"])
            for state in ["pinned", "main", "release"]:
                self.assertRegex(record[state]["revision"], r"^[0-9a-f]{40}$")
                for field in ["guide_sha256", "license_sha256"]:
                    self.assertRegex(record[state][field], r"^[0-9a-f]{64}$")

    def test_every_complete_selected_package_and_sibling_preserved(self):
        fingerprint = lambda path: {p.relative_to(path).as_posix(): p.read_bytes()
                                    for p in path.rglob("*") if p.is_file()}
        with tempfile.TemporaryDirectory(prefix="v040 project ") as temp:
            project = Path(temp)
            (project / "skills/sibling").mkdir(parents=True)
            (project / "skills/sibling/owner").write_text("UNCHANGED")
            for source in sorted((ROOT / "skills").iterdir()):
                if not (source / "SKILL.md").is_file():
                    continue
                with self.subTest(skill=source.name):
                    result = self.copy(project, source.name)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(fingerprint(source), fingerprint(project / "skills" / source.name))
            self.assertEqual((project / "skills/sibling/owner").read_text(), "UNCHANGED")

    def test_existing_selected_file_directory_and_links_are_refused(self):
        for kind in ["file", "directory", "live-symlink", "dangling-symlink"]:
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temp:
                project = Path(temp)
                (project / "skills").mkdir()
                destination = project / "skills/document-actions"
                target = project / "target"
                if kind != "dangling-symlink":
                    target.mkdir()
                    (target / "owner").write_text("UNCHANGED")
                if kind == "file":
                    destination.write_text("LOCAL")
                elif kind == "directory":
                    destination.mkdir()
                    (destination / "owner").write_text("LOCAL")
                else:
                    destination.symlink_to(target, target_is_directory=True)
                result = self.copy(project)
                self.assertNotEqual(result.returncode, 0)
                if kind == "file":
                    self.assertEqual(destination.read_text(), "LOCAL")
                elif kind == "directory":
                    self.assertEqual(list(p.name for p in destination.iterdir()), ["owner"])
                    self.assertEqual((destination / "owner").read_text(), "LOCAL")
                else:
                    self.assertTrue(destination.is_symlink())
                    self.assertEqual(destination.readlink(), target)
                if kind == "dangling-symlink":
                    self.assertFalse(target.exists())
                else:
                    self.assertEqual((target / "owner").read_text(), "UNCHANGED")


if __name__ == "__main__":
    unittest.main()
