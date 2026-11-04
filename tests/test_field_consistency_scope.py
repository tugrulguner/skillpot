"""Source corrections must not silently change published installation defaults."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RELEASE = "3624eaaf2aa6c870e1dad6190ac3466e4e378f35"


class FieldConsistencyScopeTests(unittest.TestCase):
    def test_current_corrections_are_separate_from_the_published_snapshot(self):
        note = ROOT / "docs/field-consistency.md"
        self.assertTrue(note.is_file(), "current-source patch boundary note is missing")
        text = note.read_text()
        for required in ["0.1.1", "0.1.2", "v0.4.0", RELEASE,
                         "unreleased", "not a controlled comparison"]:
            self.assertIn(required, text)
        self.assertIn("docs/field-consistency.md", (ROOT / "README.md").read_text())
        self.assertIn("../docs/field-consistency.md", (ROOT / "catalog/README.md").read_text())

    def test_stable_installation_still_selects_the_published_snapshot(self):
        self.assertIn("git clone --branch v0.4.0 --depth 1",
                      (ROOT / "README.md").read_text())
        setup = (ROOT / "docs/quickstart.md").read_text()
        for directory in ["skillpot-source", "skillpot-actions-source", "skillpot-decision-source"]:
            self.assertIn(f"git -C {directory} checkout --detach {RELEASE}", setup)


if __name__ == "__main__":
    unittest.main()
