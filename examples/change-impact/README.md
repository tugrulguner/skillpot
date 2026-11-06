# Change-impact: authored snapshot example

This is an authored specification fixture, not real repository history or observed agent output.
BEFORE and AFTER are labels, not Git commits. manifest.json hashes every file in both
snapshots; change.diff is reproduced from all paths, including unchanged-context checks.
Only api.py and caller.py change: the API requires keyword-only limit and one caller
adapts. The unchanged legacy caller, stale documentation, separate same-name function
and explicit-argument-only test expose different impact and coverage boundaries.

impact.md and verification.md are authored expected reports, not an answer oracle shipped
inside the installed skill. All proposed checks are Not run. No fixture source is imported
or executed by the integrity tests; parseable Python and source linkage do not prove runtime
behavior or full semantic coverage.

From the collection root, run the source-integrity and authored-contract checks:

```sh
uv run --no-project --with-requirements requirements-ci.txt python -m unittest discover -s tests -p test_change_impact_example.py -v
```

The checks compare snapshot bytes/hashes, exact diff, rendered locators, coverage and check
states, and reject missing/wrong/orphan mappings and false Passed claims. Their baseline
expectations are authored and still require an independent semantic review.
