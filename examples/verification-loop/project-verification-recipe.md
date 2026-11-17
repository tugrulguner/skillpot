# Authored JSON export verification recipe

Scope: this small offline CLI fixture only. It is an example of repeatable project verification, not a general application harness or an observed agent task.

## Prerequisites and repeat command

Use Python 3.10+ standard library, from the SkillPot repository root. Inspect `baseline.py`, `candidate.py` and `replay.py` first. Provide a fresh external output directory with an existing owned parent; resolve system aliases in that parent and do not use symlinks or an in-repository destination.

```sh
python3 examples/verification-loop/replay.py --output /absolute/owned/new-evidence
```

The replay refuses collisions and redirecting ancestor links. It starts only short-lived local subprocesses, with three-second command timeouts; no service, network, dependency installation, account or cleanup daemon is involved. Run within a separately approved total budget. Do not overwrite an earlier run; each repeat needs a new approved evidence path.

## Acceptance and controls

The independent contract is complete JSON round-trip preservation, not agreement with an implementation by itself. Parsed output must preserve every supplied field/value. Differential comparison ignores JSON key order and insignificant whitespace only.

- Healthy control: the authored baseline should satisfy that contract for the two named cases and all generated inputs.
- Isolated seeded-fault control: the authored candidate intentionally drops extra fields. The named extension case and generated counterexample must fail the intended preservation assertion; a setup failure is not qualification.
- Legitimate control: the minimal supported record should pass for both implementations.
- Generated checks: use the recorded generator seed and bounded case count. Keep exact inputs, case indexes and the first failing generated case. Finite checking does not prove the invariant universally.

## Evidence and qualification

Inspect `verification.md`, `result.json`, and per-case stdout/stderr. Require current pre/post source identity, actual command/cwd/timestamp/timeout receipts, independent baseline assertions, the intended candidate failure and a passing legitimate control. An overall replay exit zero means the teaching controls behaved as expected; the candidate still failed acceptance. Do not mistake it for candidate approval.

Record actual run identity and observed timing from receipts when available; do not invent a duration. Repeatability claims are bounded by the actual executed repeats. The recipe supplies no permission to inject faults into another project, edit protected policy, install hooks, repair production code or merge a change.
