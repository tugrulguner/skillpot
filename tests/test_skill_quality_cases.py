"""Offline integrity of authored evaluation packets, not semantic or agent scoring."""
import copy
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "evaluations/skill-quality"
OUTPUTS = {
    "document-actions": ["actions.md", "questions.md"],
    "decision-brief": ["brief.md", "evidence.md"],
    "claim-check": ["review.md", "claims.md"],
}


def packet_errors(root, manifest):
    """Check declared structure, containment and literal evidence; not source meaning."""
    errors = []
    if (not isinstance(manifest, dict) or type(manifest.get("schema_version")) is not int
            or manifest.get("schema_version") != 1
            or not isinstance(manifest.get("cases"), list) or not manifest["cases"]):
        return ["invalid manifest shape"]
    if root.is_symlink() or (root / "cases").is_symlink():
        return ["source root symlink"]
    seen = set()
    declared = set()
    for case in manifest["cases"]:
        if not isinstance(case, dict):
            errors.append("invalid case")
            continue
        name = case.get("id")
        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            errors.append("invalid case id")
            continue
        if name in seen:
            errors.append("duplicate case id")
        seen.add(name)
        skill = case.get("skill")
        if not isinstance(skill, str) or skill not in OUTPUTS:
            errors.append("unknown pilot skill")
        elif case.get("required_outputs") != OUTPUTS[skill]:
            errors.append("wrong output contract")
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            errors.append("missing task prompt")
        inputs = case.get("input_files")
        if not isinstance(inputs, list) or not inputs:
            errors.append("missing input inventory")
            continue
        texts = {}
        for relative in inputs:
            if (not isinstance(relative, str) or not relative.startswith("cases/")
                    or any(not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", part)
                           or part in {".", ".."} for part in relative.split("/"))):
                errors.append("unsafe input path")
                continue
            if relative in declared:
                errors.append("duplicate input identity")
            declared.add(relative)
            path = root
            linked = False
            for part in relative.split("/"):
                path = path / part
                if path.is_symlink():
                    linked = True
                    break
            if linked:
                errors.append("source symlink")
                continue
            try:
                texts[relative] = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                errors.append("cannot read input")
        if sum(map(len, texts.values())) > 10000:
            errors.append("input budget exceeded")
        assertions = case.get("assertions")
        if not isinstance(assertions, list) or not assertions:
            errors.append("missing assertions")
            continue
        assertion_ids = set()
        for assertion in assertions:
            if not isinstance(assertion, dict):
                errors.append("invalid assertion")
                continue
            identity = assertion.get("id")
            if not isinstance(identity, str) or not identity.strip():
                errors.append("missing assertion id")
            elif identity in assertion_ids:
                errors.append("duplicate assertion id")
            else:
                assertion_ids.add(identity)
            if (not isinstance(assertion.get("criterion"), str) or not assertion["criterion"].strip()
                    or type(assertion.get("critical")) is not bool):
                errors.append("invalid rubric fields")
            evidence = assertion.get("source_evidence")
            if not isinstance(evidence, list) or not evidence:
                errors.append("missing source evidence")
                continue
            for item in evidence:
                if not isinstance(item, dict):
                    errors.append("invalid evidence")
                    continue
                file, quote = item.get("file"), item.get("quote")
                if (not isinstance(file, str) or file not in texts or not isinstance(quote, str)
                        or not quote.strip() or quote not in texts[file]):
                    errors.append("unsupported evidence quote")
    actual = set()
    for path in (root / "cases").rglob("*"):
        if path.is_symlink():
            errors.append("source inventory symlink")
        elif path.is_file():
            actual.add(path.relative_to(root).as_posix())
    if actual != declared:
        errors.append("input inventory differs from declared files")
    return errors


class SkillQualityCasesTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((CORPUS / "cases.json").read_text())

    def test_actual_pilot_and_literal_citations_are_consistent(self):
        self.assertEqual(packet_errors(CORPUS, self.manifest), [])
        self.assertEqual({case["skill"] for case in self.manifest["cases"]}, set(OUTPUTS))
        self.assertEqual(len(self.manifest["cases"]), 3)

    def test_shape_identity_contract_and_citation_mutations_are_rejected(self):
        mutations = [
            lambda m: m.update(schema_version=True),
            lambda m: m.update(cases=[]),
            lambda m: m["cases"].append(copy.deepcopy(m["cases"][0])),
            lambda m: m["cases"][0].update(required_outputs=["review.md"]),
            lambda m: m["cases"][0].update(input_files=["../outside.md"]),
            lambda m: m["cases"][0].update(input_files=["cases//packet.md"]),
            lambda m: m["cases"][0].update(skill=["document-actions"]),
            lambda m: m["cases"][0].update(prompt=" "),
            lambda m: m["cases"][0]["assertions"].append(copy.deepcopy(m["cases"][0]["assertions"][0])),
            lambda m: m["cases"][0]["assertions"][0].update(critical=1),
            lambda m: m["cases"][0]["assertions"][0].update(source_evidence=[]),
            lambda m: m["cases"][0]["assertions"][0]["source_evidence"][0].update(quote="Not in the source."),
            lambda m: m["cases"][0]["assertions"][0]["source_evidence"][0].update(file="cases/not-declared.md"),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(mutation=index):
                manifest = copy.deepcopy(self.manifest)
                mutate(manifest)
                self.assertTrue(packet_errors(CORPUS, manifest))
        self.assertEqual(packet_errors(CORPUS, self.manifest), [])

    def test_symlink_input_is_rejected_before_target_read(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "packet"
            shutil.copytree(CORPUS / "cases", root / "cases")
            outside = Path(directory) / "outside.md"
            relative = self.manifest["cases"][0]["input_files"][0]
            path = root / relative
            path.rename(outside)
            path.symlink_to(outside)
            reads = []
            original = Path.read_text

            def observe(file, *args, **kwargs):
                if file == path:
                    reads.append(file)
                return original(file, *args, **kwargs)

            with patch.object(Path, "read_text", observe):
                errors = packet_errors(root, self.manifest)
            self.assertEqual(reads, [])
            self.assertTrue(any("symlink" in error for error in errors))

    def test_missing_changed_unreadable_and_extra_inputs_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(CORPUS / "cases", root / "cases")
            self.assertEqual(packet_errors(root, self.manifest), [])
            path = root / self.manifest["cases"][0]["input_files"][0]
            original = path.read_bytes()
            for content in (b"changed source", b"\xff", b"x" * 10001):
                path.write_bytes(content)
                self.assertTrue(packet_errors(root, self.manifest))
            path.unlink()
            self.assertTrue(packet_errors(root, self.manifest))
            path.write_bytes(original)
            extra = root / "cases/unlisted-answer.md"
            extra.write_text("This file is not in the input inventory.\n")
            self.assertTrue(packet_errors(root, self.manifest))
            extra.unlink()
            self.assertEqual(packet_errors(root, self.manifest), [])
