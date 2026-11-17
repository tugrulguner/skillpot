# Verification loop worked example

A stdlib-only, offline before/after verification case for a JSON serialization/export CLI. The baseline preserves all fields; the candidate intentionally keeps only three documented core fields. The replay runs both subprocesses on two named regression/minimal controls plus 24 deterministic generated JSON objects (seed `20261117`). Generated cases vary schema/field presence and values, deliberately covering empty strings, Unicode, zero, false, null, nested objects/lists and additional fields.

For every case, the independently stated contract is full JSON round-trip equality: parsed output must equal the complete input value. Differential equality is recorded separately and cannot make two equally incorrect results trustworthy. Each case retains actual baseline and candidate stdout/stderr receipts, exact input, input digest, semantic assertions and differential result in `result.json`; `verification.md` lists the seed, count, exact generated counterexample index and receipt paths. The fixture is finite deterministic testing, not proof of the invariant for all JSON inputs. Nonzero exits, invalid output, timeout and launch error remain distinct outcomes.

From the repository root, provide a **new** output directory outside this example bundle:

```sh
python3 examples/verification-loop/replay.py --output /absolute/path/to/new-evidence
```

The replay exclusively creates the destination; existing paths and symlinks are refused and never overwritten. Source-byte SHA-256 is computed before execution and rehashed afterward; stale source identity does not yield a current verdict. The tests hold the independent expected contract and verify generated cases, named controls, actual intentional field-loss counterexamples and protected output/error paths.

```sh
python3 -m unittest tests.test_verification_loop_example -v
```

This is one local authored acceptance workflow, not a general runtime/evaluation framework or a claim about any external task.
