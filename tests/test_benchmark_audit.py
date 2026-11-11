"""Offline source-contract checks for benchmark-audit; not task-performance tests."""
import hashlib
import json
from pathlib import Path
import re
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "skills" / "benchmark-audit"
PRACTICE = BUNDLE / "assets" / "practice"


class BenchmarkAuditSourceContract(unittest.TestCase):
    def test_bundle_metadata_and_entrypoint_contract(self):
        text = (BUNDLE / "SKILL.md").read_text()
        match = re.fullmatch(r"---\n(.*?)\n---\n(.*)", text, re.S)
        self.assertIsNotNone(match)
        meta = yaml.safe_load(match.group(1))
        self.assertEqual(set(meta), {"name", "description", "license", "metadata"})
        self.assertEqual(meta["name"], "benchmark-audit")
        self.assertLessEqual(len(meta["description"]), 60)
        self.assertEqual(meta["license"], "MIT")
        self.assertEqual(meta["metadata"], {"version": "0.1.0", "status": "unreleased"})
        self.assertLessEqual(len(text.splitlines()), 150)

    def test_required_resources_and_four_verdicts_and_scope_rules(self):
        for rel in ("provenance.md", "compatibility.md", "assets/benchmark-audit-template.md", "references/evidence-checklist.md"):
            self.assertTrue((BUNDLE / rel).is_file(), rel)
        skill = (BUNDLE / "SKILL.md").read_text()
        for phrase in ("Supported within scope", "Contradicted", "Insufficient evidence", "Not assessed", "loaded", "declared", "timeouts", "scheduled-arrival", "dangling symlink", "benchmark commands", "fresh"):
            self.assertIn(phrase.lower(), skill.lower())

    def test_output_boundary_and_read_budget_are_explicit(self):
        text = (BUNDLE / "SKILL.md").read_text()
        for phrase in ("read budget", "fresh owned external report directory",
                       "outside all evidence roots", "installed bundle", "exclusive creation"):
            self.assertIn(phrase, text)

    def test_template_has_six_required_top_level_sections(self):
        text = (BUNDLE / "assets/benchmark-audit-template.md").read_text()
        for heading in ("Scope and decision", "Evidence inventory", "Claims", "Comparison and accounting", "Calculations", "Evidence limits and next checks"):
            self.assertRegex(text, rf"(?m)^## {re.escape(heading)}$")

    def test_practice_packet_is_input_only_and_provenance_is_self_contained(self):
        for name in ("claims.md", "linux-screen.json", "DEXPOT-LICENSE", "provenance.md"):
            self.assertTrue((PRACTICE / name).is_file(), name)
        all_names = {p.name.lower() for p in PRACTICE.rglob("*") if p.is_file()}
        self.assertFalse(any("expected" in n or "acceptance" in n or "oracle" in n for n in all_names))
        manifest = json.loads((PRACTICE / "linux-screen.provenance.json").read_text())
        self.assertEqual(manifest["files"][0]["local_path"], "linux-screen.json")
        self.assertEqual(manifest["files"][0]["file_sha256"], hashlib.sha256((PRACTICE / "linux-screen.json").read_bytes()).hexdigest())
        self.assertEqual((PRACTICE / "DEXPOT-LICENSE").read_bytes(), (ROOT / "examples/benchmark-audit-proposal/sources/DEXPOT-LICENSE").read_bytes())
        self.assertEqual((PRACTICE / "linux-screen.json").read_bytes(), (ROOT / "examples/benchmark-audit-proposal/sources/linux-screen.json").read_bytes())
        self.assertIn("authored", (PRACTICE / "claims.md").read_text().lower())
        self.assertIn("raw", (PRACTICE / "provenance.md").read_text().lower())

    def test_links_are_internal_and_common_contract(self):
        for md in BUNDLE.rglob("*.md"):
            text = md.read_text()
            for dest in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
                self.assertFalse(dest.startswith(("http:", "https:")), f"non-internal link {md}: {dest}")
                if not dest.startswith("#"):
                    self.assertTrue((md.parent / dest.split("#", 1)[0]).resolve().is_file(), f"broken link {md}: {dest}")


if __name__ == "__main__":
    unittest.main()
