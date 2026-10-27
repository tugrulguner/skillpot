"""Source-contract checks, not agent activation or usefulness tests."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/repository-readiness"


class RepositoryReadinessSourceTests(unittest.TestCase):
    def test_entry_point_identity_and_short_trigger(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        frontmatter, body = text[4:].split("\n---\n", 1)
        self.assertIn(f"name: {SKILL.name}\n", frontmatter)
        description = re.search(r"^description: (.+)$", frontmatter, re.MULTILINE)
        assert description is not None
        self.assertLessEqual(len(description[1]), 60)
        self.assertTrue(description[1].endswith("."))
        self.assertTrue(body.strip())

    def test_required_companions_and_report_template(self):
        for path in ("provenance.md", "compatibility.md", "assets/report.md"):
            with self.subTest(path=path):
                self.assertTrue((SKILL / path).is_file())
                self.assertIn(f"]({path})", (SKILL / "SKILL.md").read_text())
        report = (SKILL / "assets/report.md").read_text()
        for section in ("Decision", "Required gates and evidence", "Executed checks",
                        "Blockers and smallest next steps", "Boundaries and cleanup"):
            self.assertIn(f"## {section}", report)

    def test_frozen_task_has_public_pinned_input_and_rubric(self):
        task = (ROOT / "examples/repository-readiness/task.md").read_text()
        self.assertIn("3d023734ca0a2a22a873ca59d601f7616fed7716", task)
        self.assertIn("## Fixed acceptance rubric", task)
        self.assertIn("## Permissions and budget", task)
        self.assertIn("not proof", task)


if __name__ == "__main__":
    unittest.main()
