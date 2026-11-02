#!/usr/bin/env python3
"""Check this authored fixture and oracle; this is not a semantic model evaluation."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

INPUT_SHA256 = {'README.md': '470b4a2c77626190f24b8531835e590c4509b0e57099dae59e43d915ed47c841', 'notes.md': 'ee5ce1e3962b0992e8657f30d9be9ff05bedcd99edd86a5f9258e5a277359d6c', 'task.md': 'b80edb5cbd9397ac63af60e9b06669167a44c02995bfc23cc0d8c020a0556b31'}

EXPECTED = {
    "A01": ("assigned", ["N02:L4", "N13:L15"], "Mira", "unknown", None),
    "A02": ("unassigned_requirement", ["N03:L5"], None, "unknown", "before release"),
    "A03": ("proposal", ["N04:L6"], None, "not accepted", None),
    "A04": ("unassigned_requirement", ["N05:L7"], None, "unknown", "tomorrow"),
    "A05": ("assigned", ["N06:L8", "N07:L9"], None, "unknown", None),
    "A06": ("assigned", ["N08:L10"], "Mira", "unknown", "Thursday"),
    "A08": ("assigned", ["N12:L14"], "Jon", "unknown", "before release"),
}
EXCLUDED = {
    "A07": ("completed_historical", ["N09:L11"], "Jon", "unknown", None),
    "A09": ("cancelled_historical", ["N10:L12"], "Mira", "unknown", None),
}


def fail(message):
    print(f"verification failed: {message}", file=sys.stderr)
    return 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    root = parser.parse_args().root
    try:
        for name, digest in INPUT_SHA256.items():
            if hashlib.sha256((root / "inputs" / name).read_bytes()).hexdigest() != digest:
                return fail(f"authored input fingerprint changed: {name}")
        oracle = json.loads((root / "expected.json").read_text(encoding="utf-8"))
        notes = (root / "inputs" / "notes.md").read_text(encoding="utf-8")
        task = (root / "inputs" / "task.md").read_text(encoding="utf-8")
        actions = (root / "actions.md").read_text(encoding="utf-8")
        questions = (root / "questions.md").read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError) as exc:
        return fail(f"cannot read required example artifact: {exc}")

    if "Read all files in this input directory" not in task or "document-actions-output/" not in task:
        return fail("input task lacks bounded input/output instructions")
    for forbidden in ("expected.json", "actions.md", "questions.md", "verify.py"):
        if (root / "inputs" / forbidden).exists():
            return fail(f"oracle/output/checker leaked into inputs: {forbidden}")

    labels = {}
    for lineno, line in enumerate(notes.splitlines(), 1):
        match = re.match(r"\[(N\d+)\]", line)
        if match:
            label = match.group(1)
            if label in labels:
                return fail(f"duplicate source label {label}")
            labels[label] = lineno
    if set(labels) != {f"N{i:02d}" for i in range(1, 14)}:
        return fail("fictional packet source labels are incomplete or unexpected")

    seen_ids = set()
    for group, expected in (("items", EXPECTED), ("exclusions", EXCLUDED)):
        rows = oracle.get(group)
        if not isinstance(rows, list):
            return fail(f"oracle {group} must be a list")
        keyed = {row.get("id"): row for row in rows}
        if len(keyed) != len(rows) or set(keyed) != set(expected):
            return fail(f"oracle {group} IDs do not match authored classifications")
        for item_id, signature in expected.items():
            row = keyed[item_id]
            category, locators, owner, acceptance, due = signature
            actual = (row.get("category"), row.get("source_locators"), row.get("owner"),
                      row.get("acceptance"), row.get("due"))
            if actual != signature:
                return fail(f"{item_id} classification/fields differ from authored oracle")
            if row.get("history") != (group == "exclusions"):
                return fail(f"{item_id} history flag is inconsistent")
            for locator in locators:
                match = re.fullmatch(r"(N\d+):L(\d+)", locator)
                if not match or labels.get(match.group(1)) != int(match.group(2)):
                    return fail(f"{item_id} unresolved locator {locator}")
            seen_ids.add(item_id)
    if seen_ids != set(EXPECTED) | set(EXCLUDED):
        return fail("oracle item coverage is incomplete")

    # Check each Markdown record, not merely the structured oracle beside it.
    headings = list(re.finditer(r"(?m)^### (A\d+) — (.+)$", actions))
    if len(headings) != len(seen_ids) or {m[1] for m in headings} != seen_ids:
        return fail("Markdown records missing, duplicated or unexpected")
    display = {"assigned": "Assigned action", "unassigned_requirement": "Unassigned requirement",
               "proposal": "Proposal", "completed_historical": "Completed historical",
               "cancelled_historical": "Cancelled historical"}
    records = {row["id"]: row for row in oracle["items"] + oracle["exclusions"]}
    for index, heading in enumerate(headings):
        block = actions[heading.end():headings[index + 1].start() if index + 1 < len(headings) else len(actions)]
        row = records[heading[1]]
        conflicts = row.get("conflicts", {})
        fields = {"Category": display[row["category"]],
                  "Owner": "Conflicting" if "owner" in conflicts else row["owner"] or "Unknown",
                  "Acceptance": row["acceptance"].capitalize(),
                  "Due": "Conflicting" if "due" in conflicts else row["due"] or "Unknown"}
        for name, value in fields.items():
            found = re.search(r"(?m)^- \*\*" + re.escape(name) + r":\*\* (.+)$", block)
            if not found or found[1] != value:
                return fail(f"{heading[1]} Markdown {name} differs from authored expectation")
        evidence = re.search(r"(?m)^- \*\*Evidence:\*\* (.+)$", block)
        if not evidence or any(locator not in evidence[1] for locator in row["source_locators"]):
            return fail(f"{heading[1]} Markdown evidence omits an item locator")
    for text in (actions, questions):
        for label, number in re.findall(r"(N\d+):L(\d+)", text):
            if labels.get(label) != int(number):
                return fail(f"Markdown locator {label}:L{number} does not resolve")

    conflicts = oracle["items"]
    conflict = next(row for row in conflicts if row["id"] == "A05")
    if conflict.get("conflicts") != {"owner": ["Mira", "Jon"], "due": ["Friday", "Monday"]}:
        return fail("A05 conflict must preserve both owners and deadlines")
    if "tomorrow" not in actions or "not normalized" not in actions:
        return fail("relative deadline was normalized or omitted")
    if "**Owner (conflicting):** Mira (`N06:L8`); Jon (`N07:L9`)" not in actions:
        return fail("outstanding output silently resolves or mis-cites the owner conflict")
    if "**Due (conflicting):** Friday (`N06:L8`); Monday (`N07:L9`)" not in actions:
        return fail("outstanding output silently resolves or mis-cites the due conflict")
    if "## Proposed (not assigned)" not in actions or "A03" not in actions:
        return fail("proposal is not visibly separated from assigned actions")
    if any(line.startswith(("### A07 ", "### A09 ")) for line in actions.split("## Completed or cancelled historical items", 1)[0].splitlines()):
        return fail("historical item appears among outstanding/proposed items")
    if "N11:L13" not in actions or "not an assignment" not in actions:
        return fail("embedded hostile directive is not explicitly treated as source data")
    if "N05:L7" not in questions or "N06:L8" not in questions or "N07:L9" not in questions:
        return fail("actionable unknowns/conflict questions are missing")
    print(json.dumps({"kind": "authored-document-actions-example", "network_used": False,
                      "item_count": len(EXPECTED), "historical_exclusions": len(EXCLUDED),
                      "locators_checked": sum(len(v[1]) for v in (*EXPECTED.values(), *EXCLUDED.values()))},
                     sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
