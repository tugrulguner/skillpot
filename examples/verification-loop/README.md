# Verification loop worked example

A stdlib-only, offline before/after verification case for a JSON serialization/export CLI. The baseline preserves all fields; the candidate intentionally keeps only three documented core fields. The replay runs both subprocesses on two named regression/minimal controls plus 24 deterministic generated JSON objects (seed `20261117`). Generated cases vary schema/field presence and values, deliberately covering empty strings, Unicode, zero, false, null, nested objects/lists and additional fields.

For every case, the independently stated contract is full JSON round-trip equality: parsed output must equal the complete input value, preserving decoded types recursively (in particular, booleans are not numbers). Only object key order and insignificant whitespace are ignored. Replay success also requires the named extension control to FAIL for the intended loss and the minimal legitimate control to PASS; a candidate that fails every input cannot qualify the teaching fixture. Differential equality is recorded separately and cannot make two equally incorrect results trustworthy. Each case retains actual baseline and candidate stdout/stderr receipts, exact input, input digest, semantic assertions and differential result in `result.json`; `verification.md` lists the seed, count, exact generated counterexample index and receipt paths. The fixture is finite deterministic testing, not proof of the invariant for all JSON inputs. Nonzero exits, invalid output, timeout and launch error remain distinct outcomes.

Subprocess streams are captured as bytes. The `.stdout`/`.stderr` receipt files and `stdout_base64`/`stderr_base64` JSON fields retain exact bytes, including invalid UTF-8 and CRLF. For compatibility, `raw_stdout`/`raw_stderr` are explicitly labeled UTF-8 replacement **previews**, not byte-exact evidence. JSON stdout is decoded strictly as UTF-8; decoding failures become `INVALID_OUTPUT` with `decode_error`, without losing the report or other receipts. Non-UTF-8 diagnostic stderr does not invalidate otherwise valid JSON stdout. Timeout/nonzero output retains the same exact-byte evidence. Structured report strings are JSON-escaped so even an escaped lone surrogate returned by a candidate cannot break report encoding.

From the repository root, provide a **new** output directory outside this example bundle:

```sh
python3 examples/verification-loop/replay.py --output /absolute/path/to/new-evidence
```

The replay exclusively creates the destination; existing paths and symlinks are refused and never overwritten. Completed stdout/stderr receipts are persisted after each invocation, before later checks and final identity reads. Source-byte SHA-256 is computed before execution and rehashed afterward; stale source identity does not yield a current verdict. Missing, unreadable or directory-valued source paths produce explicit initial/post-execution identity diagnostics and null digests rather than an exception or invented hash. Any unavailable identity makes the report STALE and the replay unsuccessful, even when both unavailable digests are null. Reports and completed receipts are retained. The tests hold the independent expected contract and verify generated cases, named controls, actual intentional field-loss counterexamples and protected output/error paths.

```sh
python3 -m unittest tests.test_verification_loop_example -v
```

This is one local authored acceptance workflow, not a general runtime/evaluation framework or a claim about any external task.
