import base64
import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys

HERE = Path(__file__).resolve().parent
TIMEOUT_SECONDS = 3
GENERATOR_SEED = 20261117
GENERATED_CASE_COUNT = 24
MAX_JSON_DEPTH = 64


class OutputLimitError(ValueError):
    """The teaching fixture cannot safely inspect this output depth."""


def normalized(stdout):
    value = json.loads(stdout)
    pending = [(value, 1)]
    while pending:
        item, depth = pending.pop()
        if isinstance(item, (dict, list)):
            if depth > MAX_JSON_DEPTH:
                raise OutputLimitError(f"JSON nesting exceeds the fixture limit of {MAX_JSON_DEPTH}")
            children = item.values() if isinstance(item, dict) else item
            pending.extend((child, depth + 1) for child in children)
    return value


def json_equal(left, right):
    """Compare decoded JSON recursively without bool/number coercion."""
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(json_equal(left[key], right[key]) for key in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(json_equal(a, b) for a, b in zip(left, right))
    return left == right


def identity_status(recorded_hashes, current_hashes):
    return "CURRENT" if recorded_hashes == current_hashes else "STALE"


def source_identities(sources):
    """Unavailable source bytes have no digest, never an invented identity."""
    hashes, errors = {}, {}
    for name, path in sources.items():
        try:
            hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError as exc:
            hashes[name] = None
            errors[name] = {"path": str(path), "error": type(exc).__name__, "detail": str(exc)}
    return hashes, errors


def safe_text(value):
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def captured_output(stdout, stderr):
    """Keep exact bytes separately from explicitly lossy display previews."""
    stdout, stderr = stdout or b"", stderr or b""
    return {"raw_stdout": safe_text(stdout), "raw_stderr": safe_text(stderr),
            "stdout_base64": base64.b64encode(stdout).decode("ascii"),
            "stderr_base64": base64.b64encode(stderr).decode("ascii"),
            "text_preview_policy": "raw_stdout/raw_stderr are UTF-8 replacement previews; base64 fields and receipt files retain exact bytes"}


def baseline_trustworthy(run):
    return run.get("classification") == "OK" and run.get("semantic_assertion") == "PASS"


def generated_records(seed=GENERATOR_SEED, count=GENERATED_CASE_COUNT):
    """Produce bounded, repeatable JSON objects spanning values and schemas."""
    if not isinstance(count, int) or not 1 <= count <= 128:
        raise ValueError("generated case count must be between 1 and 128")
    rng = random.Random(seed)
    values = ["", "雪☃", 0, False, None, [], {}, {"inside": [None, False, 0, "λ"]}, [0, False, None, "é"]]
    keys = ["extra", "metadata", "nested", "zero", "unicode_雪", "flag", "nullable", "items"]
    records = []
    for index in range(count):
        record = {"id": f"generated-{index:02d}",
                  "name": rng.choice(["", "generated", "Δ-record", f"case-{index}"]),
                  "enabled": rng.choice([True, False])}
        for key in rng.sample(keys, rng.randint(1, len(keys))):
            record[key] = rng.choice(values)
        if index % 4 == 0:
            record["nested"] = {"children": [None, {"value": rng.choice(values)}, False]}
        if index % 5 == 0:
            record["zero"] = 0
        if index % 6 == 0:
            record["flag"] = False
        if index % 7 == 0:
            record["nullable"] = None
        if index % 8 == 0:
            record["unicode_雪"] = "雪☃ café"
        records.append(record)
    return records


def invoke(source, value, cwd=None):
    cwd = cwd or HERE
    argv = [sys.executable, str(source)]
    started = __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat()
    try:
        completed = subprocess.run(argv, input=json.dumps(value).encode("utf-8"), capture_output=True,
                                   timeout=TIMEOUT_SECONDS, check=False, cwd=cwd)
    except subprocess.TimeoutExpired as exc:
        return {"classification": "TIMEOUT", **captured_output(exc.stdout, exc.stderr), "argv": argv, "cwd": str(cwd),
                "started_at": started, "timeout_seconds": TIMEOUT_SECONDS}
    except OSError as exc:
        return {"classification": "LAUNCH_ERROR", "launch_error": str(exc), "argv": argv,
                "cwd": str(cwd), "started_at": started, "timeout_seconds": TIMEOUT_SECONDS}
    run = {"exit_code": completed.returncode, **captured_output(completed.stdout, completed.stderr),
           "argv": argv, "cwd": str(cwd),
           "started_at": started, "timeout_seconds": TIMEOUT_SECONDS}
    if completed.returncode:
        run["classification"] = "SETUP_OR_EXECUTION_ERROR"
    else:
        try:
            run["normalized"] = normalized(completed.stdout.decode("utf-8"))
            run["classification"] = "OK"
        except (OutputLimitError, RecursionError) as exc:
            run["classification"] = "OUTPUT_LIMIT"
            run["parse_error"] = str(exc)
            run["max_json_depth"] = MAX_JSON_DEPTH
        except UnicodeDecodeError as exc:
            run["classification"] = "INVALID_OUTPUT"
            run["decode_error"] = str(exc)
        except (ValueError, TypeError) as exc:
            run["classification"] = "INVALID_OUTPUT"
            run["parse_error"] = str(exc)
    return run


def main():
    if len(sys.argv) != 3 or sys.argv[1] != "--output":
        raise SystemExit("usage: replay.py --output FRESH_OUTPUT_DIRECTORY")
    destination = Path(sys.argv[2]).absolute()
    if (not destination.parent.is_dir() or destination.exists()
            or any(component.is_symlink() for component in (destination, *destination.parents))
            or destination.resolve().is_relative_to(HERE.parents[1])):
        raise SystemExit(f"refusing unsafe, missing-parent, existing, internal or symlink destination: {destination}")
    try:
        destination.mkdir()
    except OSError as exc:
        raise SystemExit(f"refusing destination: {exc}")

    sources = {name: HERE / f"{name}.py" for name in ("baseline", "candidate")}
    identity_inputs = {**sources, "checker": Path(__file__).resolve()}
    hashes, initial_errors = source_identities(identity_inputs)
    controls = [
        {"id": "known-extension", "name": "primary", "enabled": True,
         "extension": {"vendor": "example", "flags": ["x", 4]}},
        {"id": "minimal", "name": "secondary", "enabled": False},
    ]
    records = [("named-control", value) for value in controls]
    records.extend(("generated-invariant", value) for value in generated_records())
    results = []
    for idx, (kind, value) in enumerate(records):
        result = {"case_index": idx, "case_kind": kind, "input": value,
                  "input_sha256": hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest(),
                  "runs": {}}
        for name, source in sources.items():
            run = invoke(source, value, HERE)
            # Persist completed streams before later checks or identity reads.
            for channel in ("stdout", "stderr"):
                (destination / f"case-{idx}-{name}.{channel}").write_bytes(
                    base64.b64decode(run.get(channel + "_base64", "")))
            if run["classification"] == "OK":
                run["semantic_assertion"] = "PASS" if json_equal(run["normalized"], value) else "FAIL"
            result["runs"][name] = run
        old, new = result["runs"]["baseline"], result["runs"]["candidate"]
        result["differential_equal"] = (old.get("classification") == new.get("classification") == "OK"
                                         and json_equal(old.get("normalized"), new.get("normalized")))
        if not baseline_trustworthy(old):
            result["verdict"] = "BASELINE_NOT_TRUSTWORTHY"
        elif new["classification"] != "OK":
            result["verdict"] = new["classification"]
        elif new.get("semantic_assertion") != "PASS":
            result["verdict"] = "FAIL"
        else:
            result["verdict"] = "PASS" if result["differential_equal"] else "FAIL"
        results.append(result)

    current, final_errors = source_identities(identity_inputs)
    status = "STALE" if initial_errors or final_errors else identity_status(hashes, current)
    generated = [r for r in results if r["case_kind"] == "generated-invariant"]
    counterexample = next((r["case_index"] for r in generated if r["verdict"] == "FAIL"), None)
    summary = {"cases": len(results), "generated_cases": len(generated),
               "baseline_trustworthy": all(baseline_trustworthy(r["runs"]["baseline"]) for r in results),
               "candidate_detected_regression": any(r["verdict"] == "FAIL" for r in results),
               "named_controls_match_expected": [r["verdict"] for r in results if r["case_kind"] == "named-control"] == ["FAIL", "PASS"],
               "generated_counterexample_case_index": counterexample,
               "generated_pass_count": sum(r["verdict"] == "PASS" for r in generated),
               "generated_fail_count": sum(r["verdict"] == "FAIL" for r in generated)}
    answer = {"example": "serialization-export-roundtrip",
              "contract": "For every JSON object input, parsed subprocess output equals the entire input value (including every field/value); key order and insignificant whitespace alone are ignored.",
              "generator": {"seed": GENERATOR_SEED, "generated_case_count": len(generated),
                            "finite_testing_limit": "This bounded deterministic sample is evidence for these cases, not proof of the invariant for all JSON inputs."},
              "source_sha256": hashes, "post_execution_sha256": current, "identity_status": status,
              "initial_identity_errors": initial_errors, "post_execution_identity_errors": final_errors,
              "timeout_seconds": TIMEOUT_SECONDS, "results": results, "summary": summary}
    if status != "CURRENT":
        for result in results:
            result["verdict"] = "NO_CURRENT_VERDICT_STALE_SOURCE"
    (destination / "result.json").write_text(json.dumps(answer, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")
    lines = ["# Verification results", "", f"Seed: `{GENERATOR_SEED}`; generated cases: **{len(generated)}**.",
             "Each subprocess receipt (stdout and stderr) is retained per case under its exact case index.", ""]
    lines.extend(f"- Case {i} (`{r['input']['id']}`, {r['case_kind']}): **{r['verdict']}**; full-input contract baseline={r['runs']['baseline'].get('semantic_assertion', 'N/A')}, candidate={r['runs']['candidate'].get('semantic_assertion', 'N/A')}; differential_equal={r['differential_equal']}; receipts: `case-{i}-baseline.stdout`, `case-{i}-candidate.stdout`." for i, r in enumerate(results))
    lines += ["", f"Generated counterexample case index: **{counterexample}**. This finite sample is not proof of the universal invariant.",
              f"Source identity: **{status}**. Baseline trustworthy: **{summary['baseline_trustworthy']}**. Candidate regression detected: **{summary['candidate_detected_regression']}**.",
              "Missing/unreadable identity diagnostics: `initial_identity_errors` and `post_execution_identity_errors` in result.json; unavailable digests are null, not invented hashes.",
              "Detailed per-case JSON and subprocess receipts: [`result.json`](result.json)."]
    (destination / "verification.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(answer, indent=2, sort_keys=True, ensure_ascii=True))
    if (status != "CURRENT" or not summary["baseline_trustworthy"]
            or not summary["named_controls_match_expected"]
            or not summary["candidate_detected_regression"] or counterexample is None):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
