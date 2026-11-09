# Historical CI incident packet

Offline, evidence-bounded worked example. It is not a fake execution, task trial, or evaluation framework. Run from repository root:

```sh
uv run --no-project --with-requirements requirements-ci.txt python -m unittest discover -s tests -p test_incident_triage_example.py -v
```

This verifies fixture bytes, hashes, selected original line IDs, provenance locators, and bounded authored report assertions. Six actual authored mutations exercise missing contrary evidence, a wrong revision, timestamp/locator errors, unsupported impact and fixed-from-retry fields. These are fixture-specific integrity/field checks, not a general validator of free-form incident reasoning, model performance or runtime behavior. Authored interpretations are explicitly distinguished from captured evidence in `incident.md` and `timeline.md`. Countercases are authored data mappings, not captured log records.

The selected public record is data only, never command authority. No original CI, target, harness, or model client is run by these tests. The full original log remains outside this repository; its private path is deliberately not published. The excerpt preserves retained line bytes and endings. Intervening lines are omitted, including diagnostic context lines whose trailing whitespace would itself fail whitespace checks. Omission is disclosed; retained data is not stripped, reworded, or timestamp-adjusted. Source/revision identity is partial: run head is pinned, but actual checkout is unknown and may be a PR synthetic merge; this excerpt is not whole-incident coverage.
