"""Contract regression for the explicitly selected fictional target."""
import argparse
import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, default=ROOT / "buggy.py")
    parser.add_argument("--case", choices=["all", "zero", "positive", "none", "empty"], default="all")
    args = parser.parse_args()
    target = args.target.resolve()
    try:
        if not target.is_file():
            raise FileNotFoundError(target)
        spec = importlib.util.spec_from_file_location("bug_repro_selected_target", target)
        if spec is None or spec.loader is None:
            raise ImportError("target has no Python source loader")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if not callable(getattr(module, "page", None)):
            raise TypeError("target has no callable page")
    except Exception as error:
        print(f"SETUP ERROR: {type(error).__name__}: {error}", file=sys.stderr)
        return 2

    class PageRegressionTests(unittest.TestCase):
        def test_zero_limit(self):
            self.assertEqual(module.page(["only"], 0), [])

        def test_positive(self):
            self.assertEqual(module.page(["a", "b"], 1), ["a"])

        def test_none(self):
            self.assertEqual(module.page(["a"], None), ["a"])

        def test_empty(self):
            self.assertEqual(module.page([], 0), [])

    methods = {"zero": "test_zero_limit", "positive": "test_positive", "none": "test_none", "empty": "test_empty"}
    suite = (unittest.defaultTestLoader.loadTestsFromTestCase(PageRegressionTests) if args.case == "all"
             else unittest.TestSuite([PageRegressionTests(methods[args.case])]))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
