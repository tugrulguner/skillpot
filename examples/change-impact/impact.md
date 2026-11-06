# Impact inventory — authored assessment, not observed agent output

Scope: supplied authored BEFORE/AFTER snapshots, not Git commits or runtime observations.
Exact comparison: change.diff; all six files on each side are hashed in manifest.json.
Only api.py and caller.py changed. Other supplied files are inspected context, not changes.

### I1 — API contract
- Change: Direct change
- Changed file: api.py
- Evidence: before/api.py:1; after/api.py:1
- Finding: The default is removed and limit becomes required and keyword-only. Calls omitting it or passing it positionally no longer match the signature. This is a source-supported contract consequence, not an observed runtime error.
- Check: Not run

### I2 — Adapted caller
- Change: Direct change
- Changed file: caller.py
- Evidence: before/caller.py:5; after/caller.py:5
- Finding: load changes its explicit positional 25 to limit=25, matching the new signature. Its import is after/caller.py:1. No claim is made that this path was executed or that every caller migrated.
- Check: Not run

### I3 — Unchanged incompatible caller
- Change: Source-linked
- Changed file: api.py
- Evidence: after/api.py:1; after/legacy_caller.py:1; after/legacy_caller.py:5
- Finding: The unchanged load imports api.fetch_items and omits limit. The new signature requires it. The static caller link demonstrates a source-level compatibility risk, not runtime reachability. No fixture source was imported or executed.
- Check: Not run

### I4 — Stale documented default
- Change: Source-linked
- Changed file: api.py
- Evidence: after/api.py:1; after/configuration.md:1
- Finding: The unchanged documentation still says default 100; it conflicts with the new required keyword-only signature. This file is explanatory documentation, not evidence that a configuration loader supplies a value.
- Check: Not run

### I5 — Unavailable consumer coverage
- Change: Unknown
- Changed file: api.py
- Evidence: after/api.py:1; after/tests/test_api.py:7
- Finding: The one supplied test exercises an explicit keyword argument only. It does not cover omitted or positional callers, the legacy load function, dynamic dispatch or external clients. Unprovided consumers remain unenumerated; the test was Not run and cannot establish full compatibility.
- Check: Not run

## Changed-file coverage
- api.py: I1, I3, I4, I5.
- caller.py: I2.
Every impact maps back to one changed file. Supporting unchanged paths are not misclassified as changes.

## Exclusions and limits
E1: after/unrelated.py:1 defines another fetch_items with no import/reference link to api.fetch_items. A matching name alone is not evidence of a caller. Treat a textual match as Potential until identity is resolved; exclude this known separate definition rather than promoting it to a proven dependency.
The source helper query_items is visible in both snapshots, but no behavioral test was run.
Reflection, alias mutation, external consumers, generated code, deployment and runtime reachability are not established. This is a bounded static assessment, not merge/release approval or an efficacy measurement.
