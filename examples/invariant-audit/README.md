# Invariant-audit authored example

**Synthetic, authored teaching fixture.** This is not a real incident, a real target, an observed defect, or an execution trace. The source snippets are inert text; do not execute them. This packet demonstrates how a report should reason about one identity-current guarantee. Expected dispositions are authored acceptance criteria, not outputs from a checker or test run.

## Guarantee and failure model

Guarantee: a report may say `CURRENT` only if the baseline, candidate, and checker identities were each successfully read and each equals its corresponding valid expected identity for the evidence being reported. Missing, unreadable, malformed, or differing identity must not be treated as equal to a valid identity. In particular, unknown is never equal to a known valid identity. Initial and final snapshots can reveal some changes but cannot prove identity continuity between snapshots.

Scope: this small fictional report-classification boundary only. It says nothing about other guarantees, real tools, continuous monitoring, or source behavior outside the shown snippets.

## Packet contents

- `source/baseline.txt`, `source/candidate.txt`, `source/checker.txt`: authored inert illustrative snippets.
- `inputs/cases.json`: cases and expected classification, including healthy control and negative cases.
- `expected/invariant-audit.md`: example report using the procedure's evidence labels.
- `inputs/cases.json` also records verifier-quality controls and a transfer case; no separate acceptance file is required.

No executable target source is supplied. `source/baseline.txt` is a deliberately flawed classifier sketch, `source/candidate.txt` an unexecuted alternative, and `source/checker.txt` a verifier-qualification sketch. The captured/actual identity labels are fictional nonblank strings, not cryptographic hashes.

Run the repository-owned fixture tests with `uv run --no-project --with-requirements requirements-ci.txt python -m unittest discover -s tests -p test_invariant_audit_proposal.py -v`. These recompute the authored input expectations and check the report ledger, including mutation controls. They do not execute the inert snippets, qualify an actual classifier, or grade arbitrary reports.

## How to read

Start from the guarantee above, not the sample report's labels. Each case says what a correct independent judgment should be. `source-only` means reasoning from the supplied inert text; `proposed` means a test is suggested but not run. There are no `executed` observations. A verifier that reports the wrong reason for rejecting a case has not demonstrated the guarantee. A control failure must not qualify a verifier merely because it also rejects a negative case.

The transfer case asks for an unrelated output-path refusal guarantee, requiring its own model, counterexample and handoff. This prevents the example from defining invariant-audit as an identity-only workflow.
