import hashlib
import json
import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills" / "decision-brief"


class DecisionBriefContractTests(unittest.TestCase):
    def test_recorded_tasks_preserve_artifacts_and_tested_procedure(self):
        record = ROOT / "evaluations/decision-brief/offline-tasks-001"
        self.assertTrue((record / "manifest.json").is_file(), "observed task record is missing")
        manifest = json.loads((record / "manifest.json").read_text())
        self.assertEqual(manifest["candidate_revision"], "9227a9310728a4919ce012bc3f24850c6d2e721e")
        self.assertEqual({case["id"] for case in manifest["cases"]}, {"normal", "missing", "collision"})
        self.assertEqual(len(manifest["cases"]), 3)
        for path, digest in manifest["archived_files"].items():
            self.assertEqual(hashlib.sha256((record / path).read_bytes()).hexdigest(), digest, path)
        body = (PACKAGE / "SKILL.md").read_text().split("\n---\n", 1)[1]
        self.assertEqual(hashlib.sha256(body.encode()).hexdigest(), manifest["procedure_body_sha256"])
        for path, digest in manifest["unchanged_resources"].items():
            self.assertEqual(hashlib.sha256((PACKAGE / path).read_bytes()).hexdigest(), digest, path)

    def test_frontmatter_has_short_trigger_and_flat_metadata(self):
        text = (PACKAGE / "SKILL.md").read_text()
        match = re.fullmatch(r"---\n(.*?)\n---\n(.+)", text, re.DOTALL)
        self.assertIsNotNone(match)
        assert match is not None
        self.assertTrue(match[2].strip())
        metadata = yaml.safe_load(match[1])
        self.assertLessEqual(len(metadata["description"]), 60)
        self.assertTrue(metadata["description"].endswith("."))
        self.assertTrue(all(isinstance(k, str) and isinstance(v, str)
                            for k, v in metadata["metadata"].items()))

    def test_complete_portable_bundle_and_required_contract(self):
        entry = PACKAGE / "SKILL.md"
        self.assertTrue(entry.is_file(), "decision-brief entry point is missing")
        text = entry.read_text()
        for phrase in ("brief.md", "evidence.md", "hard constraints", "preferences", "reversal", "defer", "offline", "untrusted", "overwrite", "professional advice"):
            self.assertIn(phrase, text.lower(), phrase)
        for name in ("provenance.md", "compatibility.md", "assets/brief-template.md", "assets/evidence-template.md"):
            self.assertTrue((PACKAGE / name).is_file(), name)
        self.assertIn("](LICENSE)", text)
        self.assertIn("](LICENSES/github-spec-kit-MIT.txt)", text)
        self.assertIn("provenance.md", text)
        self.assertIn("compatibility.md", text)

    def test_metadata_and_source_notice_are_portable_and_pinned(self):
        text = (PACKAGE / "SKILL.md").read_text()
        self.assertIn("name: decision-brief", text)
        self.assertIn('version: "0.1.0"', text)
        self.assertIn('maintainer: "tugrulguner"', text)
        self.assertIn('status: "unreleased"', text)
        self.assertNotIn("metadata:\n  hermes:", text)
        provenance = (PACKAGE / "provenance.md").read_text()
        self.assertIn("7370e592f3cd9c06e5b698983957e227c75b30e2", provenance)
        self.assertIn("206a0386d20b3eed4c087a4d9de247a3e7b2b59348bf3c801fc74f63ca2726a5", provenance)
        notice = (PACKAGE / "LICENSES" / "github-spec-kit-MIT.txt").read_text()
        notice_bytes = (PACKAGE / "LICENSES" / "github-spec-kit-MIT.txt").read_bytes()
        self.assertIn(hashlib.sha256(notice_bytes).hexdigest(), provenance)
        self.assertEqual((PACKAGE / "LICENSE").read_bytes(), (ROOT / "LICENSE").read_bytes())
        self.assertIn("Copyright GitHub, Inc.", notice)
        self.assertIn('THE SOFTWARE IS PROVIDED "AS IS"', notice)

    def test_package_local_markdown_links_resolve(self):
        for md in PACKAGE.rglob("*.md"):
            for target in re.findall(r"\[[^]]*\]\(([^)]+)\)", md.read_text()):
                if "://" not in target and not target.startswith("#"):
                    destination = (md.parent / target.split("#", 1)[0]).resolve()
                    if PACKAGE.resolve() in destination.parents or destination == PACKAGE.resolve():
                        self.assertTrue(destination.is_file(), f"{md}: {target}")


if __name__ == "__main__":
    unittest.main()
