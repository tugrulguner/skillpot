# Verification loop worked example

A stdlib-only, offline before/after verification case for a JSON serialization/export CLI. The baseline preserves extension fields; the candidate intentionally drops them. The replay invokes both as subprocesses on the same authored records, including a deterministic invariant-generated record requiring all fields to survive. JSON is parsed and complete values compared: only key order and insignificant whitespace are normalized. A trustworthy baseline plus a differential mismatch is reported as a defect; nonzero exits, invalid output and timeout are distinct setup/execution outcomes.

From the repository root, provide a **new** output directory outside this example bundle:

```sh
python3 examples/verification-loop/replay.py --output /absolute/path/to/new-evidence
```

The replay exclusively creates the destination; existing paths and symlinks are refused and never overwritten. The report keeps source-byte SHA-256 identity (`identity_status`) separate from per-run semantic assertions against the authored input. Expected answers remain in this separate test, not the runnable fixture bundle. Run tests with:

```sh
python3 -m unittest tests.test_verification_loop_example -v
```

This demonstrates one local acceptance workflow; it is not a general runtime/evaluation framework or a claim about any external task.
