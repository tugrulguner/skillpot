# Review checklist

- [ ] Exact fresh external case directory and artifact names agreed before any write.
- [ ] Destination and every selected path checked absent, including live/dangling symlinks; no overwrite or fallback.
- [ ] Partial/interrupted owner files preserved; no fake/empty runnable artifacts.
- [ ] Target source unchanged; exact bytes/import location, runtime, dependency versions, and input hashes reported as observed or unknown.
- [ ] Input privacy, secrets, destructive effects, and security reviewed before execution.
- [ ] Commands were explicitly authorized with budget and timeout; no implicit network, install, account, spend, hook, import, or repository execution.
- [ ] Evidence is captured from execution with argv, cwd, exit status, stdout/stderr, timeout, and source identities; no reconstructed receipts.
- [ ] Original report symptom matched before reduction; intended trigger preserved throughout.
- [ ] Counterexamples and negative controls included; incompatible environment not mislabeled as bug.
- [ ] Regression test fails for intended assertion on known-bug case and passes legitimate controls.
- [ ] Fixed baseline claimed only when supplied/authorized and actually run; otherwise `Not run`.
- [ ] Exact final published artifacts rerun after path cleanup, or explicitly `Not run`.
- [ ] Flaky counts represent actual observations; no universal claim.
- [ ] Status accurately `Reproduced`, `Not reproduced`, or `Blocked`; incomplete candidate distinguished.
- [ ] Observations, hypotheses, unknowns, and blockers separated; no root-cause certainty or fix/merge authority implied.
