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

    def test_dependencies_and_site_build_outputs_are_not_authored_docs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for folder in ("website/node_modules/pkg", "website/dist", "website/.astro",
                           "website/.wrangler", "website/playwright-report", "website/test-results"):
                target = root / folder
                target.mkdir(parents=True, exist_ok=True)
                (target / "generated.md").write_text("[not-source](missing.md)")
            self.assertEqual(checker.check(root), [])

    def test_authored_website_and_skill_dist_docs_remain_checked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for folder in ("website/src", "skills/example/dist"):
                target = root / folder
                target.mkdir(parents=True, exist_ok=True)
                (target / "guide.md").write_text("[broken](missing.md)")
            self.assertEqual(len(checker.check(root)), 2)

    def test_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("[bad](../outside.md)")
            self.assertIn("escapes repository", checker.check(root)[0])

    def test_personal_home_without_trailing_slash(self):
        for prefix in ("Users", "home"):
            for suffix in ("", "\n", "`", "/project"):
                with self.subTest(prefix=prefix, suffix=suffix):
                    with tempfile.TemporaryDirectory() as directory:
                        root = Path(directory)
                        (root / "README.md").write_text(
                            "/" + prefix + "/alice" + suffix
                        )
                        self.assertTrue(checker.check(root))

    def test_personal_path(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("/" + "Users/example/private/file")
            self.assertIn("personal absolute path", checker.check(root)[0])


if __name__ == "__main__":
    unittest.main()
