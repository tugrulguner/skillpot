# Verification recommendations — authored, not executed

Target: authored AFTER snapshot; source vs installed artifact: source only, no package installed.
Authorization: inspect supplied source only. No fixture code, command or proposed check was run.
Every proposed check is **Not run**. These are recommendations, not a command journal.
Before any execution, obtain permission, inspect project commands and use an approved
external disposable checkout/environment. The following standard-library commands are
specific suggestions for these authored Python sources, not authority to run them.

### I1 — Required keyword-only contract
- Command: python -m unittest discover -s tests -v, after adding approved signature/compatibility assertions.
- Assertion: inspect.signature(api.fetch_items) has required keyword-only limit; explicit limit=25 succeeds, omitted and positional calls raise TypeError. Check both baseline accepted calls and changed-head refusal so negative tests cannot pass for unrelated errors.
- Prerequisite: approved BEFORE/AFTER source copies in separate external checkouts; inspect code first; Python and standard-library unittest; explicit execution permission. Existing test alone lacks these assertions.
- Expected result: the declared binding change is distinguished from function-body failures. Scope: isolated source fixture, not installed artifact or production.
- State: Not run

### I2 — Adapted caller
- Command: python -m unittest discover -s tests -v, with an approved caller.load assertion added.
- Assertion: caller.load supplies limit=25 and returns the expected list; retain a call/start observation to distinguish entering the intended function from a test-only substitute.
- Prerequisite: approved AFTER checkout and execution permission; new test must target the real caller module.
- Expected result: explicit caller contract works within this fixture; not proof of all consumer migration.
- State: Not run

### I3 — Legacy caller compatibility
- Command: python -m unittest discover -s tests -v, with an approved legacy_caller.load compatibility case added.
- Assertion: unchanged legacy_caller.load succeeds at BEFORE and raises the required-argument TypeError at AFTER; decide migration policy with the owner before changing its code.
- Prerequisite: permission and distinct source-pinned BEFORE/AFTER checkouts; no silent source edits by this review.
- Expected result: demonstrate or refute the predicted specific incompatibility rather than infer execution from an import.
- State: Not run

### I4 — Documentation consistency
- Command: manual source comparison of configuration.md:1 with api.py:1; no target code execution required.
- Assertion: remove or revise the obsolete default claim only in a separately authorized edit.
- Prerequisite: read access and confirmed canonical documentation; any write needs separate approval.
- Expected result: documented default is classified as stale without pretending a config loader was observed.
- State: Not run

### I5 — Coverage gaps
- Command: none yet; inventory actual consumer environments and dynamically resolved entry points with the owner before selecting commands.
- Assertion: add omitted/positional and known-consumer cases; do not count the explicit-limit smoke test as full compatibility.
- Prerequisite: additional approved source/consumer boundary and an execution plan; no open-ended search, private access or dependency installation.
- Expected result: scoped coverage plan or explicit remaining unknowns; absence of tests is not itself a product bug.
- State: Not run

Negative control E1 is checked by source module identity, not by launching a new analyzer.
No Passed/Failed result, stdout, runtime trace, activation or task-performance claim is supplied.
