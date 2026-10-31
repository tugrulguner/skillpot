"""Check this worked example's local integrity; no semantic or agent evaluation."""
import argparse
import hashlib
import json
from pathlib import Path
import re


def check(root):
    errors = []
    data = json.loads((root / "sources.json").read_text())
    source_ids = set()
    for source in data["sources"]:
        source_ids.add(source["id"])
        if not re.fullmatch(r"[a-f0-9]{40}", source["revision"]):
            errors.append("invalid source revision")
        if f'/blob/{source["revision"]}/' not in source["url"]:
            errors.append("source URL does not identify its revision")
        if not re.fullmatch(r"[a-f0-9]{64}", source["original_sha256"]):
            errors.append("invalid original-file hash")
        if not 0 < source["first_line"] <= source["last_line"]:
            errors.append("invalid source line range")
        digest = hashlib.sha256(source["excerpt"].encode()).hexdigest()
        if digest != source["excerpt_sha256"]:
            errors.append(f'{source["id"]}: excerpt hash mismatch')
    if source_ids != {"S1", "S2", "S3", "S4"} or len(data["sources"]) != 4:
        errors.append("expected four unique source excerpts")
    evidence = (root / "evidence.md").read_text()
    brief = (root / "brief.md").read_text()
    claims = set(re.findall(r"^## (C\d+)\s*$", evidence, re.MULTILINE))
    if claims != {"C1", "C2", "C3", "C4"}:
        errors.append("expected four explicit claim entries")
    for claim in re.findall(r"\[(C\d+)\]", brief):
        if claim not in claims:
            errors.append(f"unknown claim: {claim}")
    if not claims.issubset(set(re.findall(r"\[(C\d+)\]", brief))):
        errors.append("brief must refer to each worked claim")
    for source in re.findall(r"Supported by (S\d+)", evidence):
        if source not in source_ids:
            errors.append(f"unknown source: {source}")
    cases = (root / "cases.md").read_text()
    case_ids = set(re.findall(r"^## ([a-z-]+)\s*$", cases, re.MULTILINE))
    if case_ids != {"conflicting-evidence", "missing-decisive-fact", "source-instruction-injection", "existing-output-conflict"}:
        errors.append("expected four authored failure cases")
    for name in ["README.md", "task.md", "NOTICE.md", "LICENSE-PYTHON.txt"]:
        if not (root / name).read_text().strip():
            errors.append(f"empty companion: {name}")
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    try:
        errors = check(args.root)
    except (OSError, ValueError, KeyError, TypeError) as error:
        errors = [f"unreadable example: {error}"]
    print(json.dumps({"kind": "offline-example-integrity", "network_used": False,
                      "failure_cases": 4, "errors": errors}, indent=2))
    raise SystemExit(bool(errors))
