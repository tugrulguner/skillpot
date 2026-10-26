import importlib.util
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location(
    "check_docs", Path(__file__).resolve().parents[1] / "scripts/check_docs.py"
)
assert SPEC is not None and SPEC.loader is not None
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


class CheckDocsTests(unittest.TestCase):
    def test_valid_destinations_and_external_links(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a file.md").write_text("# Target\n")
            (root / "README.md").write_text(
                "[local](a%20file.md#target) [web](https://example.com/missing)\n"
            )
            self.assertEqual(checker.check(root), [])

    def test_missing_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("[bad](missing.md)")
            self.assertIn("missing destination", checker.check(root)[0])

    def test_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("[bad](../outside.md)")
            self.assertIn("escapes repository", checker.check(root)[0])

    def test_personal_path(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("/" + "Users/example/private/file")
            self.assertIn("personal absolute path", checker.check(root)[0])


if __name__ == "__main__":
    unittest.main()
