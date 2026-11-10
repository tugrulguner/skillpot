"""Check grading coverage and quotations, not whether judgments are semantically true."""
import copy
import hashlib
import json
from pathlib import Path
import unittest

CORPUS = Path(__file__).resolve().parents[1] / "evaluations/skill-quality"


def grade_errors(root, grade, cases, citation_addendum=None):
    errors = []
    if not isinstance(grade, dict) or not isinstance(grade.get("case"), str) or grade["case"] not in cases:
        return ["unknown grade case"]
    case = cases[grade["case"]]
    expected = {item["id"] for item in case["assertions"]}
    attempts = grade.get("attempts")
    if not isinstance(attempts, list) or not attempts:
        return ["missing attempt grades"]
    seen = set()
    for attempt in attempts:
        if not isinstance(attempt, dict) or attempt.get("id") not in ("attempt-1", "attempt-2"):
            errors.append("invalid graded attempt")
            continue
        if attempt["id"] in seen:
            errors.append("duplicate graded attempt")
        seen.add(attempt["id"])
        assertions = attempt.get("assertions")
        if not isinstance(assertions, list) or not all(isinstance(item, dict) for item in assertions):
            errors.append("invalid assertion grades")
            continue
        ids = [item.get("id") for item in assertions]
        if len(ids) != len(expected) or any(not isinstance(identity, str) for identity in ids) or set(ids) != expected:
            errors.append("incomplete or duplicate assertion grades")
        for assertion in assertions:
            if assertion.get("verdict") not in ("pass", "fail", "unverified"):
                errors.append("invalid grade verdict")
            if not isinstance(assertion.get("reason"), str) or not assertion["reason"].strip():
                errors.append("missing grade reason")
            evidence = assertion.get("output_evidence")
            if not isinstance(evidence, list) or (assertion.get("verdict") == "pass" and not evidence):
                errors.append("missing passing evidence")
                continue
            for item in evidence:
                if (not isinstance(item, dict) or item.get("file") not in case["required_outputs"]
                        or not isinstance(item.get("quote"), str) or not item["quote"].strip()):
                    errors.append("invalid output citation")
                    continue
                path = root / "initial" / f'{case["id"]}-{attempt["id"]}' / item["file"]
                if path.is_symlink() or not path.is_file():
                    errors.append("missing cited artifact")
                    continue
                quote = item["quote"]
                if (citation_addendum and citation_addendum["case"] == case["id"]
                        and citation_addendum["attempt"] == attempt["id"]
                        and citation_addendum["file"] == item["file"]):
                    for change in citation_addendum["changes"]:
                        if change["assertion"] == assertion.get("id") and change["original_quote"] == quote:
                            if hashlib.sha256(path.read_bytes()).hexdigest() != citation_addendum["artifact_sha256"]:
                                errors.append("citation correction artifact changed")
                            quote = change["corrected_quote"]
                if quote not in path.read_text(encoding="utf-8"):
                    errors.append("nonliteral grade quotation")
    return errors


class SkillQualityGradesTests(unittest.TestCase):
    def setUp(self):
        self.cases = {case["id"]: case for case in json.loads((CORPUS / "cases.json").read_text())["cases"]}
        self.grades = [json.loads(path.read_text()) for path in sorted((CORPUS / "grading/raw").glob("grade-*.json"))]
        self.addendum = json.loads((CORPUS / "grading/decision-brief-citation-addendum.json").read_text())

    def test_every_original_attempt_has_every_frozen_assertion_with_bound_evidence(self):
        pairs = []
        for grade in self.grades:
            self.assertEqual(grade_errors(CORPUS, grade, self.cases, self.addendum), [])
            pairs += [(grade["case"], attempt["id"]) for attempt in grade["attempts"]]
        expected = {(identity, f"attempt-{number}") for identity in self.cases for number in (1, 2)}
        self.assertEqual(set(pairs), expected)
        self.assertEqual(len(pairs), len(expected))

    def test_original_nonliteral_quotes_remain_detectable_not_silently_rewritten(self):
        errors = [error for grade in self.grades for error in grade_errors(CORPUS, grade, self.cases)]
        self.assertEqual(errors, ["nonliteral grade quotation", "nonliteral grade quotation"])
        wrong = copy.deepcopy(self.addendum)
        wrong["artifact_sha256"] = "0" * 64
        grade = next(g for g in self.grades if g["case"] == "decision-brief-region-gates-001")
        self.assertIn("citation correction artifact changed", grade_errors(CORPUS, grade, self.cases, wrong))

    def test_missing_duplicate_invalid_verdict_and_fake_evidence_are_rejected(self):
        original = next(g for g in self.grades if g["case"] == "doc-actions-handoff-001")
        mutations = [
            lambda g: g.update(case="unknown"),
            lambda g: g["attempts"].append(copy.deepcopy(g["attempts"][0])),
            lambda g: g["attempts"][0]["assertions"].pop(),
            lambda g: g["attempts"][0]["assertions"].append(copy.deepcopy(g["attempts"][0]["assertions"][0])),
            lambda g: g["attempts"][0]["assertions"][0].update(verdict=True),
            lambda g: g["attempts"][0]["assertions"][0].update(reason=" "),
            lambda g: g["attempts"][0]["assertions"][0].update(output_evidence=[]),
            lambda g: g["attempts"][0]["assertions"][0]["output_evidence"][0].update(quote="Invented evidence."),
            lambda g: g["attempts"][0]["assertions"][0]["output_evidence"][0].update(file="../../outside.md"),
        ]
        for number, mutate in enumerate(mutations):
            with self.subTest(mutation=number):
                grade = copy.deepcopy(original)
                mutate(grade)
                self.assertTrue(grade_errors(CORPUS, grade, self.cases))
        self.assertEqual(grade_errors(CORPUS, original, self.cases), [])
