"""Authored fixture integrity, not impact inference or target code execution."""
import ast
import copy
import difflib
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1] / "examples/change-impact"


def snapshot(side):
    return {p.relative_to(ROOT / side).as_posix(): p.read_text()
            for p in (ROOT / side).rglob("*") if p.is_file()}


def validate(manifest, impact, verification):
    old, new = snapshot("before"), snapshot("after")
    for side, files in [("before", old), ("after", new)]:
        assert manifest[side] == {p: hashlib.sha256(v.encode()).hexdigest() for p, v in files.items()}
    changed = {p for p in old.keys() | new.keys() if old.get(p) != new.get(p)}
    assert set(manifest["changed_files"]) == changed
    records = manifest["impacts"]
    assigned = [i for ids in manifest["changed_files"].values() for i in ids]
    assert len(assigned) == len(set(assigned)) and set(assigned) == set(records)
    blocks = re.findall(r"(?ms)^### (I\d+) — .*?(?=^### |^## |\Z)", impact)
    assert len(blocks) == len(set(blocks)) and set(blocks) == set(records)
    checks = re.findall(r"(?ms)^### (I\d+) — .*?(?=^### |\Z)", verification)
    assert len(checks) == len(set(checks)) and set(checks) == set(records)
    assert manifest["check_states"] == {i: "Not run" for i in records}
    for item, record in records.items():
        assert item in manifest["changed_files"][record["changed_file"]]
        block = re.search(r"(?ms)^### " + item + r" — .*?(?=^### |^## |\Z)", impact).group()
        check = re.search(r"(?ms)^### " + item + r" — .*?(?=^### |\Z)", verification).group()
        assert "- Changed file: " + record["changed_file"] + "\n" in block
        assert record["basis"] in {"Direct change", "Source-linked", "Potential", "Unknown"}
        assert "- Change: " + record["basis"] + "\n" in block
        assert "- Check: Not run\n" in block and "- State: Not run\n" in check
        for required in ["- Command:", "- Assertion:", "- Prerequisite:", "- Expected result:"]:
            assert required in check
        assert record["evidence"]
        for citation in record["evidence"]:
            side, path, line = citation["snapshot"], citation["path"], citation["line"]
            assert side in {"before", "after"} and path in manifest[side]
            lines = snapshot(side)[path].splitlines()
            assert 1 <= line <= len(lines) and lines[line - 1] == citation["text"]
            assert f"{side}/{path}:{line}" in block
    assert not re.search(r"(?m)^- (?:Check|State): (?:Passed|Failed|Blocked)$", impact + verification)


class ChangeImpactExampleTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((ROOT / "manifest.json").read_text())
        self.impact = (ROOT / "impact.md").read_text()
        self.verification = (ROOT / "verification.md").read_text()

    def test_fixture_and_exact_diff_are_complete(self):
        old, new = snapshot("before"), snapshot("after")
        changed = {p for p in old.keys() | new.keys() if old.get(p) != new.get(p)}
        self.assertEqual(changed, {"api.py", "caller.py"})
        expected = "".join("".join(difflib.unified_diff(
            old.get(p, "").splitlines(True), new.get(p, "").splitlines(True), n=0,
            fromfile="before/" + p if p in old else "/dev/null",
            tofile="after/" + p if p in new else "/dev/null")) for p in sorted(old.keys() | new.keys()))
        self.assertEqual((ROOT / "change.diff").read_text(), expected)
        for p in ["legacy_caller.py", "configuration.md", "unrelated.py", "tests/test_api.py"]:
            self.assertEqual(old[p], new[p])
        for side, files in [("before", old), ("after", new)]:
            self.assertEqual({p: hashlib.sha256(v.encode()).hexdigest() for p, v in files.items()},
                             self.manifest[side])

    def test_source_contract_and_negative_control_without_execution(self):
        old, new = snapshot("before"), snapshot("after")
        before = ast.parse(old["api.py"]).body[0]
        after = ast.parse(new["api.py"]).body[0]
        assert isinstance(before, ast.FunctionDef) and isinstance(after, ast.FunctionDef)
        assert isinstance(before.args.defaults[0], ast.Constant)
        self.assertEqual(before.args.args[0].arg, "limit")
        self.assertEqual(before.args.defaults[0].value, 100)
        self.assertEqual(after.args.args, [])
        self.assertEqual(after.args.kwonlyargs[0].arg, "limit")
        self.assertEqual(after.args.kw_defaults, [None])
        legacy = ast.parse(new["legacy_caller.py"])
        assert isinstance(legacy.body[0], ast.ImportFrom)
        assert isinstance(legacy.body[1], ast.FunctionDef)
        self.assertEqual(legacy.body[0].module, "api")
        returned = legacy.body[1].body[0]
        assert isinstance(returned, ast.Return) and isinstance(returned.value, ast.Call)
        call = returned.value
        assert isinstance(call.func, ast.Name)
        self.assertEqual(call.func.id, "fetch_items")
        self.assertEqual(call.args + call.keywords, [])
        unrelated = ast.parse(new["unrelated.py"])
        self.assertFalse(any(isinstance(n, (ast.Import, ast.ImportFrom)) for n in ast.walk(unrelated)))
        self.assertIn("E1", self.impact)
        self.assertIn("unavailable", self.impact.lower())
        self.assertIn("not runtime reachability", self.impact)

    def test_optional_installed_input_matches_all_authored_sources_without_oracle(self):
        packet = (ROOT.parents[1] / "skills/change-impact/assets/example-input.md").read_text()
        blocks = re.findall(r"## ((?:before|after)/[^\n]+)\nSHA-256: `([0-9a-f]{64})`\n\n```(?:python|text)\n(.*?)```", packet, re.S)
        expected = {f"{side}/{path}": body for side in ["before", "after"] for path, body in snapshot(side).items()}
        self.assertEqual(len(blocks), len(expected))
        self.assertEqual({path: body for path, _, body in blocks}, expected)
        for _, digest, body in blocks:
            self.assertEqual(hashlib.sha256(body.encode()).hexdigest(), digest)
        self.assertIn((ROOT / "change.diff").read_text(), packet)
        self.assertNotIn("### I1", packet)

    def test_authored_reports_pass_consistency_baseline(self):
        validate(self.manifest, self.impact, self.verification)

    def test_mutations_reject_omissions_orphans_locators_and_false_execution(self):
        mutations = []
        bad = copy.deepcopy(self.manifest); bad["changed_files"].pop("caller.py"); mutations.append((bad, self.impact, self.verification))
        bad = copy.deepcopy(self.manifest); bad["changed_files"]["caller.py"] = ["I99"]; mutations.append((bad, self.impact, self.verification))
        bad = copy.deepcopy(self.manifest); bad["changed_files"]["caller.py"].append("I2"); mutations.append((bad, self.impact, self.verification))
        bad = copy.deepcopy(self.manifest); bad["impacts"]["I2"]["changed_file"] = "api.py"; mutations.append((bad, self.impact, self.verification))
        bad = copy.deepcopy(self.manifest); bad["impacts"]["I3"]["evidence"][1]["line"] = 4; mutations.append((bad, self.impact, self.verification))
        bad = copy.deepcopy(self.manifest); bad["after"].pop("configuration.md"); mutations.append((bad, self.impact, self.verification))
        mutations.append((self.manifest, self.impact.replace("- Check: Not run", "- Check: Passed", 1), self.verification))
        mutations.append((self.manifest, self.impact.replace("after/legacy_caller.py:5", "after/legacy_caller.py:4"), self.verification))
        mutations.append((self.manifest, self.impact, self.verification.replace("- State: Not run", "- State: Passed", 1)))
        mutations.append((self.manifest, self.impact, self.verification.replace("### I5", "### I99")))
        for index, (manifest, impact, verification) in enumerate(mutations):
            with self.subTest(mutation=index), self.assertRaises(AssertionError):
                validate(manifest, impact, verification)


if __name__ == "__main__":
    unittest.main()
