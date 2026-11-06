# Runnable fictional zero-limit reproduction

This is an authored Python example, not a bug in a real product or an observed agent
trial. Python 3.9+ and its standard library suffice. Review the source and authorize
execution before running it; no dependencies, network or accounts are needed. The
source target is never edited. The scripts work from an arbitrary working directory
and explicitly select their target with --target (default: the neighboring buggy.py).

From the collection root, resolve an absolute example location:

```sh
EXAMPLE="$PWD/examples/bug-repro"
python3 -I -B "$EXAMPLE/reproduce.py" --items 3
# Expected exit 1: original reported zero-limit symptom observed.
python3 -I -B "$EXAMPLE/reproduce.py" --items 1
# Expected exit 1: one item retains the SAME symptom.
python3 -I -B "$EXAMPLE/reproduce.py" --items 0
# Expected exit 0: empty input removes the trigger.
python3 -I -B "$EXAMPLE/regression.py"
# Expected exit 1: exactly test_zero_limit fails with AssertionError; other controls pass.
python3 -I -B "$EXAMPLE/regression.py" --target "$EXAMPLE/known-good-control.py"
# Expected exit 0: all four tests pass on the authored contrast, not a released fix.
```

The reproduce script emits structured JSON. Exit 0 means Not reproduced for these
inputs; 1 means the specific zero-limit-returns-all symptom was observed; 2 means
Blocked by setup/execution error; 3 means a DIFFERENT mismatch, not this reported bug.
Its --items option is bounded to 0..32 and --limit accepts an integer or none.
The regression script supports --case zero/positive/none/empty/all, returns 2 on setup
failure and 1 on failed tests; inspect the assertion/error type instead of treating
any nonzero status as reproduction. Neither script is a sandbox for arbitrary targets.

## Executed example, not model evidence

[repro.md](repro.md) summarizes a parent replay of these exact public scripts. All ten
command receipts are under receipts/cases and bound by receipts/manifest.json. Source
hashes bind the four executed Python files; stdout/stderr are captured from subprocesses,
not reconstructed. Original three-item, reduced one-item and empty non-trigger runs
are separate records. The contrast is supplied authored code, not a discovered product fix.

Public receipts replace only literal paths with `<REPO_ROOT>`, `<CASE_CWD>` and
`<CONSUMER_PYTHON>`, including occurrences in argv and captured output. The manifest
retains both raw-original and redacted-public SHA-256 values; unmodified originals
are retained privately. These location adaptations are not executable command lines.
Interpreter/version observations remain tied to that replay, not all supported hosts.
Earlier worker artifacts are preserved privately and are not relabeled as this replay.

Repository checks also execute the exact public scripts with finite timeouts in fresh
owned temporary directories, exercising intended failure, valid controls, setup errors
and different-failure classification. They do not run real projects or any agent/model.
