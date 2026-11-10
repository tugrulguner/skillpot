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

    def check(self, entries=None, catalog_override=None, catalog_text=None):
        record = {"schema_version": 1, "skills": [self.entry] if entries is None else entries}
        if catalog_override is not None:
            record = catalog_override
        (self.root / "catalog/modepot-sources.json").write_text(
            json.dumps(record) if catalog_text is None else catalog_text)
        return self.run_cli()

    def run_cli(self):
        return subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root)],
                              capture_output=True, text=True, timeout=10)

    def test_changed_upstream_reference_is_rejected(self):
        (self.skill / "references/upstream.md").write_text("changed guide\n")
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("hash", result.stdout + result.stderr)

    def test_missing_closing_frontmatter_delimiter_is_rejected(self):
        path = self.skill / "SKILL.md"
        path.write_text(path.read_text().split("\n---\n", 1)[0] + "\n")
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("frontmatter", result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_empty_instruction_body_is_rejected(self):
        path = self.skill / "SKILL.md"
        header = path.read_text().split("\n---\n", 1)[0]
        for suffix in ("\n---", "\n---\n", "\n---\n \t\n"):
            with self.subTest(suffix=suffix):
                path.write_text(header + suffix)
                result = self.check()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("instruction body", result.stdout + result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_original_bundle_outside_import_catalog_is_validated(self):
        original = self.root / "skills/original"
        original.mkdir()
        (original / "SKILL.md").write_text(
            '---\nname: original\ndescription: Inspect original inputs.\n'
            'license: MIT\n---\n')
        for name in ("provenance.md", "compatibility.md"):
            (original / name).write_text("Original work, source checks only.\n")
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("original", result.stdout)
        self.assertIn("instruction body", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_malformed_or_nonmapping_frontmatter_reports_a_diagnostic(self):
        path = self.skill / "SKILL.md"
        for header in ("[unfinished", "scalar", "- list item", "null"):
            with self.subTest(header=header):
                path.write_text("---\n" + header + "\n---\n# Body\n")
                result = self.check()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("frontmatter", result.stdout)
                self.assertNotIn("Traceback", result.stderr)

    def test_duplicate_frontmatter_keys_are_rejected(self):
        path = self.skill / "SKILL.md"
        original = path.read_text()
        mutants = (
            original.replace("name: sample", "name: wrong\nname: sample"),
            original.replace('status: "experimental"', 'status: "hidden"\n  status: "experimental"'),
        )
        for text in mutants:
            with self.subTest(text=text):
                path.write_text(text)
                result = self.check()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("duplicate", result.stdout)
                self.assertNotIn("Traceback", result.stderr)

    def test_bundle_symlinks_are_rejected_before_reading_targets(self):
        for relative in ("SKILL.md", "references/upstream.md", "provenance.md"):
            with self.subTest(path=relative):
                path = self.skill / relative
                original = path.read_bytes()
                outside = self.root / ("outside-" + relative.replace("/", "_"))
                outside.write_bytes(original)
                path.unlink()
                path.symlink_to(outside)
                result = self.check()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("symlink", result.stdout)
                self.assertNotIn("Traceback", result.stderr)
                path.unlink()
                path.write_bytes(original)

    def test_missing_bundle_resources_report_diagnostics(self):
        for relative in ("SKILL.md", "provenance.md", "compatibility.md", "references/upstream.md"):
            with self.subTest(path=relative):
                path = self.skill / relative
                original = path.read_bytes()
                path.unlink()
                try:
                    result = self.check()
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(relative, result.stdout)
                    self.assertNotIn("Traceback", result.stderr)
                finally:
                    path.write_bytes(original)

    def test_local_resource_links_must_survive_standalone_installation(self):
        path = self.skill / "SKILL.md"
        original = path.read_text()
        (self.root / "outside.md").write_text("Available only in the source checkout.\n")
        for link, message in (("../../outside.md", "escapes bundle"),
                              ("references/missing.md", "missing resource")):
            with self.subTest(link=link):
                path.write_text(original + "\n[required](" + link + ")\n")
                result = self.check()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(message, result.stdout)
                self.assertNotIn("Traceback", result.stderr)

    def test_missing_catalogued_bundle_cannot_pass(self):
        self.skill.rename(self.root / "removed-sample")
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing bundle", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_portable_name_length_limit_has_a_valid_boundary_control(self):
        for size in (64, 65):
            name = "a" * size
            directory = self.root / "skills" / name
            directory.mkdir()
            (directory / "SKILL.md").write_text(
                '---\nname: ' + name + '\ndescription: Inspect a sample.\n---\n# Body\n')
            for resource in ("provenance.md", "compatibility.md"):
                (directory / resource).write_text("Fixture only.\n")
            result = self.check()
            if size == 64:
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            else:
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("name", result.stdout)

    def test_portable_optional_fields_reject_host_extensions_and_wrong_types(self):
        path = self.skill / "SKILL.md"
        original = path.read_text()
        for extra in ("version: 1", "platforms: [linux]", "compatibility: {}", "allowed-tools: [Read]"):
            with self.subTest(extra=extra):
                path.write_text(original.replace("name: sample", "name: sample\n" + extra))
                result = self.check()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("frontmatter", result.stdout)
                self.assertNotIn("Traceback", result.stderr)
        path.write_text(original.replace("name: sample", 'name: sample\ncompatibility: "Trusted input only"\nallowed-tools: "Read"'))
        self.assertEqual(self.check().returncode, 0)

    def test_original_bundle_optional_license_must_be_a_string(self):
        directory = self.root / "skills/original"
        directory.mkdir()
        (directory / "SKILL.md").write_text(
            '---\nname: original\ndescription: Inspect a sample.\nlicense: []\n---\n# Body\n')
        for resource in ("provenance.md", "compatibility.md"):
            (directory / resource).write_text("Fixture only.\n")
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("frontmatter license", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_text_fields_reject_blank_descriptions_and_overlong_compatibility(self):
        path = self.skill / "SKILL.md"
        original = path.read_text()
        variants = (
            original.replace("description: Use a sample task.", 'description: "   "'),
            original.replace("name: sample", "name: sample\ncompatibility: " + "a" * 501),
        )
        for text in variants:
            with self.subTest(text=text):
                path.write_text(text)
                result = self.check()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("frontmatter", result.stdout)
                self.assertNotIn("Traceback", result.stderr)
        path.write_text(original.replace("name: sample", "name: sample\ncompatibility: " + "a" * 500))
        self.assertEqual(self.check().returncode, 0)

    def test_unreadable_utf8_is_a_bounded_resource_diagnostic(self):
        for relative in ("SKILL.md", "compatibility.md"):
            with self.subTest(path=relative):
                path = self.skill / relative
                original = path.read_bytes()
                path.write_bytes(b"\xff")
                try:
                    result = self.check()
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("cannot read", result.stdout)
                    self.assertIn(relative, result.stdout)
                    self.assertNotIn("Traceback", result.stderr)
                finally:
                    path.write_bytes(original)

    def test_catalogue_requires_unique_bundle_names(self):
        result = self.check(entries=[self.entry, dict(self.entry)])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate catalogue", result.stdout)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(self.check().returncode, 0)

    def test_malformed_catalogue_shapes_return_bounded_diagnostics(self):
        variants = [[], {"schema_version": True, "skills": []},
                    {"schema_version": 1, "skills": "wrong"}]
        variants += [{"schema_version": 1, "skills": [row]} for row in
                     [None, 42, {}, {**self.entry, "name": ["sample"]},
                      {**self.entry, "upstream_revision": 123}]]
        for record in variants:
            with self.subTest(record=record):
                result = self.check(catalog_override=record)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("catalogue", result.stdout)
                self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(self.check().returncode, 0)

    def test_invalid_json_unreadable_catalogue_and_source_link_are_diagnostics(self):
        for text in ("{", "null"):
            with self.subTest(text=text):
                result = self.check(catalog_text=text)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("catalogue", result.stdout)
                self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(self.check().returncode, 0)
        path = self.root / "catalog/modepot-sources.json"
        original = path.read_bytes()
        path.write_bytes(b"\xff")
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("catalogue", result.stdout)
        self.assertNotIn("Traceback", result.stderr)
        path.write_bytes(original)
        outside = self.root / "outside-catalogue.json"
        path.rename(outside)
        path.symlink_to(outside)
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("catalogue symlink", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

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
