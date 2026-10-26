"""Catalogue integrity checks, not product/agent performance qualification."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/check_project_skills.py"


class ProjectCatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "catalog").mkdir()
        self.skill = self.root / "skills/sample"
        (self.skill / "references").mkdir(parents=True)
        (self.skill / "SKILL.md").write_text(
            '---\nname: sample\ndescription: Use a sample task.\nlicense: MIT\n'
            'metadata:\n  status: "experimental"\n---\n# Sample\n'
            '[guide](references/upstream.md) [license](references/LICENSE.md)\n')
        (self.skill / "references/upstream.md").write_text("fixture guide\n")
        for rel in ("LICENSE", "references/LICENSE.md"):
            (self.skill / rel).write_text("fixture permission notice\n")
        for rel in ("provenance.md", "compatibility.md"):
            (self.skill / rel).write_text("Fixture status only.\n")
        self.entry = {"name": "sample", "directory": "skills/sample", "kind": "consumer",
                      "upstream_repository": "example/project", "upstream_revision": "a" * 40,
                      "upstream_path": "skills/sample.md", "license": "MIT",
                      "upstream_sha256": self.hash("references/upstream.md"),
                      "license_sha256": self.hash("LICENSE")}

    def hash(self, rel):
        return hashlib.sha256((self.skill / rel).read_bytes()).hexdigest()

    def check(self):
        (self.root / "catalog/modepot-sources.json").write_text(
            json.dumps({"schema_version": 1, "skills": [self.entry]}))
        return subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root)],
                              capture_output=True, text=True, timeout=10)

    def test_changed_upstream_reference_is_rejected(self):
        (self.skill / "references/upstream.md").write_text("changed guide\n")
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("hash", result.stdout + result.stderr)

    def test_valid_fixture_passes(self):
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_or_changed_license_is_rejected(self):
        for rel in ("LICENSE", "references/LICENSE.md"):
            with self.subTest(path=rel):
                original = (self.skill / rel).read_text()
                (self.skill / rel).write_text("incorrect license")
                result = self.check()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("license", result.stdout.lower() + result.stderr.lower())
                (self.skill / rel).write_text(original)

    def test_nested_metadata_is_not_portable(self):
        path = self.skill / "SKILL.md"
        path.write_text(path.read_text().replace('status: "experimental"', 'host:\n    nested: true'))
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("metadata", result.stdout + result.stderr)

    def test_bad_revision_is_not_normalized(self):
        self.entry["upstream_revision"] = "not-a-revision"
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("revision", result.stdout + result.stderr)

    def test_unsafe_directory_is_rejected_before_read(self):
        self.entry["directory"] = "../outside"
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("directory", result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_entrypoint_identity_and_trigger_are_checked(self):
        path = self.skill / "SKILL.md"
        original = path.read_text()
        for bad in (original.replace("name: sample", "name: other"),
                    original.replace("Use a sample task.", "")):
            path.write_text(bad)
            result = self.check()
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("frontmatter", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
