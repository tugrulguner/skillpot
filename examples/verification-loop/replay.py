import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
TIMEOUT_SECONDS = 3


def normalized(stdout):
    return json.loads(stdout)


def identity_status(recorded_hashes, current_hashes):
    return "CURRENT" if recorded_hashes == current_hashes else "STALE"


def safe_text(value):
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def baseline_trustworthy(run):
    return run.get("classification") == "OK" and run.get("semantic_assertion") == "PASS"


def invoke(source, value, cwd=None):
    cwd = cwd or HERE
    argv = [sys.executable, str(source)]
    started = __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat()
    try:
        completed = subprocess.run(argv, input=json.dumps(value), text=True, capture_output=True,
                                   timeout=TIMEOUT_SECONDS, check=False, cwd=cwd)
    except subprocess.TimeoutExpired as exc:
        return {"classification": "TIMEOUT", "raw_stdout": safe_text(exc.stdout),
                "raw_stderr": safe_text(exc.stderr), "argv": argv, "cwd": str(cwd),
                "started_at": started, "timeout_seconds": TIMEOUT_SECONDS}
    except OSError as exc:
        return {"classification": "LAUNCH_ERROR", "launch_error": str(exc), "argv": argv,
                "cwd": str(cwd), "started_at": started, "timeout_seconds": TIMEOUT_SECONDS}
    run = {"exit_code": completed.returncode, "raw_stdout": safe_text(completed.stdout),
           "raw_stderr": safe_text(completed.stderr), "argv": argv, "cwd": str(cwd),
           "started_at": started, "timeout_seconds": TIMEOUT_SECONDS}
    if completed.returncode:
        run["classification"] = "SETUP_OR_EXECUTION_ERROR"
    else:
        try:
            run["normalized"] = normalized(completed.stdout)
            run["classification"] = "OK"
        except (ValueError, TypeError) as exc:
            run["classification"] = "INVALID_OUTPUT"
            run["parse_error"] = str(exc)
    return run


def main():
    if len(sys.argv) != 3 or sys.argv[1] != "--output":
        raise SystemExit("usage: replay.py --output FRESH_OUTPUT_DIRECTORY")
    destination = Path(sys.argv[2]).absolute()
    parent = destination.parent
    if parent.is_symlink() or not parent.is_dir() or destination.is_symlink() or destination.exists():
        raise SystemExit(f"refusing unsafe, missing-parent, existing or symlink destination: {destination}")
    try:
        destination.mkdir()
    except OSError as exc:
        raise SystemExit(f"refusing destination: {exc}")
    sources = {name: HERE / f"{name}.py" for name in ("baseline", "candidate")}
    hashes = {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in sources.items()}
    records = [
        {"id": "known-extension", "name": "primary", "enabled": True, "extension": {"vendor": "example", "flags": ["x", 4]}},
        {"id": "minimal", "name": "secondary", "enabled": False},
        {"id": "generated-invariant", "name": "generated", "enabled": True, "extra": {"nested": [None, False, 19], "tag": "control"}},
    ]
    results = []
    for idx, value in enumerate(records):
        result = {"input": value, "input_sha256": hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest(), "runs": {}}
        for name, source in sources.items():
            run = invoke(source, value, HERE)
            if run["classification"] == "OK":
                run["semantic_assertion"] = "PASS" if run["normalized"] == value else "FAIL"
            result["runs"][name] = run
        old, new = result["runs"]["baseline"], result["runs"]["candidate"]
        if not baseline_trustworthy(old):
            result["verdict"] = "BASELINE_NOT_TRUSTWORTHY"
        elif new["classification"] != "OK":
            result["verdict"] = new["classification"]
        else:
            result["verdict"] = "PASS" if old["normalized"] == new["normalized"] else "FAIL"
        results.append(result)
    current = {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in sources.items()}
    status = identity_status(hashes, current)
    answer = {"example": "serialization-export-roundtrip", "normalization": "Parse JSON and compare complete values; ignore only JSON key order and whitespace.",
              "source_sha256": hashes, "post_execution_sha256": current, "identity_status": status,
              "timeout_seconds": TIMEOUT_SECONDS, "results": results,
              "summary": {"cases": len(results), "baseline_trustworthy": all(baseline_trustworthy(r["runs"]["baseline"]) for r in results),
                          "candidate_detected_regression": any(r["verdict"] == "FAIL" for r in results),
                          "invariant_generated_control_failed": results[-1]["verdict"] == "FAIL"}}
    if status != "CURRENT":
        for result in results:
            result["verdict"] = "NO_CURRENT_VERDICT_STALE_SOURCE"
    (destination / "result.json").write_text(json.dumps(answer, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    for index, result in enumerate(results):
        for name, run in result["runs"].items():
            (destination / f"case-{index}-{name}.stdout").write_text(run.get("raw_stdout", ""), encoding="utf-8")
            (destination / f"case-{index}-{name}.stderr").write_text(run.get("raw_stderr", ""), encoding="utf-8")
    verification = "# Verification results\n\n" + "\n".join(f"- Case {i} (`{r['input']['id']}`): **{r['verdict']}**; baseline semantic assertion {r['runs']['baseline'].get('semantic_assertion', 'N/A')}. Receipts: `case-{i}-baseline.stdout`, `case-{i}-candidate.stdout`." for i, r in enumerate(results)) + f"\n\nSource identity: **{status}**. Baseline trustworthy: **{answer['summary']['baseline_trustworthy']}**. Candidate regression detected: **{answer['summary']['candidate_detected_regression']}**. Detailed evidence: [`result.json`](result.json).\n"
    (destination / "verification.md").write_text(verification, encoding="utf-8")
    print(json.dumps(answer, indent=2, sort_keys=True))
    if status != "CURRENT" or not answer["summary"]["baseline_trustworthy"] or not answer["summary"]["candidate_detected_regression"]:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
