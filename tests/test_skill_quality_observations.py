"""Integrity of retained real artifacts; these checks do not grade task correctness."""
import copy
import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest
import zipfile

CORPUS = Path(__file__).resolve().parents[1] / "evaluations/skill-quality"


def artifact_errors(root, index, manifest):
    errors = []
    if (not isinstance(index, dict) or type(index.get("schema_version")) is not int
            or index.get("schema_version") != 1 or not isinstance(index.get("attempts"), list)):
        return ["invalid artifact index"]
    if not re.fullmatch(r"[0-9a-f]{40}", str(index.get("source_snapshot", ""))):
        errors.append("invalid source commit")
    if index.get("manifest_sha256") != hashlib.sha256((root / "cases.json").read_bytes()).hexdigest():
        errors.append("changed frozen rubric manifest")
    expected_inputs = {path for case in manifest["cases"] for path in case["input_files"]}
    fingerprints = index.get("input_sha256")
    if not isinstance(fingerprints, dict) or set(fingerprints) != expected_inputs:
        errors.append("wrong input fingerprints")
    else:
        for relative in expected_inputs:
            path = root / relative
            if path.is_symlink() or not path.is_file():
                errors.append("invalid input source")
            elif fingerprints[relative] != hashlib.sha256(path.read_bytes()).hexdigest():
                errors.append("changed frozen input")
    cases = {case["id"]: case for case in manifest["cases"]}
    expected_pairs = {(identity, number) for identity in cases for number in (1, 2)}
    seen = set()
    declared_files = set()
    for row in index["attempts"]:
        if not isinstance(row, dict):
            errors.append("invalid attempt")
            continue
        identity, number = row.get("case"), row.get("attempt")
        if (not isinstance(identity, str) or identity not in cases
                or type(number) is not int or number not in (1, 2)):
            errors.append("unknown attempt identity")
            continue
        pair = (identity, number)
        if pair in seen:
            errors.append("duplicate attempt")
        seen.add(pair)
        expected_id = f"{identity}-attempt-{number}"
        if row.get("id") != expected_id:
            errors.append("wrong attempt id")
        outputs = row.get("outputs")
        expected_paths = {f"initial/{expected_id}/{name}" for name in cases[identity]["required_outputs"]}
        if not isinstance(outputs, dict) or set(outputs) != expected_paths:
            errors.append("wrong output inventory")
            continue
        for relative in expected_paths:
            declared_files.add(relative)
            path = root / relative
            if path.parent.is_symlink() or path.is_symlink() or not path.is_file():
                errors.append("invalid output file")
            elif outputs[relative] != hashlib.sha256(path.read_bytes()).hexdigest():
                errors.append("changed original output bytes")
        for key in ("runtime_reported_api_calls", "visible_tool_error_count", "tokens"):
            value = row.get(key)
            if value is not None and (type(value) is not int or value < 0):
                errors.append("invalid metric type")
    if seen != expected_pairs:
        errors.append("incomplete attempt pairs")
    actual = {path.relative_to(root).as_posix() for path in (root / "initial").rglob("*") if path.is_file()}
    if actual != declared_files:
        errors.append("undeclared or missing original artifacts")
    return errors


class SkillQualityObservationsTests(unittest.TestCase):
    def setUp(self):
        self.index = json.loads((CORPUS / "initial-artifacts.json").read_text())
        self.manifest = json.loads((CORPUS / "cases.json").read_text())

    def test_all_six_attempts_bind_actual_inputs_rubric_and_exact_output_bytes(self):
        self.assertEqual(artifact_errors(CORPUS, self.index, self.manifest), [])
        self.assertEqual(len(self.index["attempts"]), 6)
        self.assertTrue(all(row["tokens"] is None for row in self.index["attempts"]))

    def test_archive_preserves_every_original_and_only_disclosed_preview_adaptations(self):
        record = self.index["raw_archive"]
        path = CORPUS / record["file"]
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), record["sha256"])
        originals = {name: digest for row in self.index["attempts"]
                     for name, digest in row["raw_output_sha256"].items()}
        expected = set(originals) | {"assisted/doc-actions-attempt-2/actions.md",
                                    "assisted/doc-actions-attempt-2/questions.md"}
        self.assertEqual(set(record["members"]), expected)
        changed = set()
        with zipfile.ZipFile(path) as archive:
            self.assertEqual(set(archive.namelist()), expected)
            self.assertEqual(len(archive.namelist()), len(expected))
            for name, digest in record["members"].items():
                raw = archive.read(name)
                self.assertEqual(hashlib.sha256(raw).hexdigest(), digest)
                self.assertIsNone(re.search(rb"/(?:Users|home)/[A-Za-z0-9_.-]+", raw))
                if name in originals:
                    self.assertEqual(digest, originals[name])
                preview = (CORPUS / name).read_bytes()
                if preview != raw:
                    changed.add(name)
                    adaptation = self.index["preview_adaptations"][name]
                    self.assertEqual(digest, adaptation["raw_sha256"])
                    self.assertEqual(hashlib.sha256(preview).hexdigest(), adaptation["preview_sha256"])
                    normalized = b"".join(line[:-3] + bytes([92, 10]) if line.endswith(b"  \n")
                                          else line for line in raw.splitlines(keepends=True))
                    while normalized.endswith(b"\n\n"):
                        normalized = normalized[:-1]
                    self.assertEqual(preview, normalized)
        self.assertEqual(changed, set(self.index["preview_adaptations"]))

    def test_missing_duplicate_misidentified_and_wrong_hash_records_are_rejected(self):
        mutations = [
            lambda m: m.update(schema_version=True),
            lambda m: m.update(source_snapshot="not-a-commit"),
            lambda m: m.update(manifest_sha256="0" * 64),
            lambda m: m.update(input_sha256={}),
            lambda m: m["attempts"].pop(),
            lambda m: m["attempts"].append(copy.deepcopy(m["attempts"][0])),
            lambda m: m["attempts"][0].update(id="other"),
            lambda m: m["attempts"][0].update(attempt=True),
            lambda m: m["attempts"][0].update(outputs={"../../outside.md": "0" * 64}),
            lambda m: m["attempts"][0].update(tokens=False),
        ]
        for number, mutate in enumerate(mutations):
            with self.subTest(mutation=number):
                index = copy.deepcopy(self.index)
                mutate(index)
                self.assertTrue(artifact_errors(CORPUS, index, self.manifest))
        self.assertEqual(artifact_errors(CORPUS, self.index, self.manifest), [])

    def test_newline_changed_input_and_extra_artifact_do_not_pass_integrity(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "copy"
            shutil.copytree(CORPUS, root)
            self.assertEqual(artifact_errors(root, self.index, self.manifest), [])
            relative = next(iter(self.index["attempts"][0]["outputs"]))
            path = root / relative
            original = path.read_bytes()
            path.write_bytes(original + b"\n")
            self.assertIn("changed original output bytes", artifact_errors(root, self.index, self.manifest))
            path.write_bytes(original)
            source = root / next(iter(self.index["input_sha256"]))
            before = source.read_bytes()
            source.write_bytes(before + b"\n")
            self.assertIn("changed frozen input", artifact_errors(root, self.index, self.manifest))
            source.write_bytes(before)
            extra = path.parent / "undeclared.md"
            extra.write_text("Not an original authorized output.\n")
            self.assertTrue(artifact_errors(root, self.index, self.manifest))
            extra.unlink()
            self.assertEqual(artifact_errors(root, self.index, self.manifest), [])
