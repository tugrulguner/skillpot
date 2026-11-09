# Reduction log

Record each change only after the original reported symptom has matched. Keep the report's triggering condition; a different failure is not a successful reduction. Preserve input privacy and record hashes rather than sensitive contents where appropriate.

- Original report symptom and observed baseline:
- Pinned target/runtime/dependencies:
- Trigger condition that must remain true:

| Step | Single change | Trigger preserved? | Original symptom/assertion observed? | Counterexample or control result | Evidence record |
|---|---|---|---|---|---|
| 0 (baseline) | None | | | | |

A reduction is accepted only when the reported symptom remains observed, not merely a nonzero exit. Record incompatible environments and flaky repetitions as observed; do not generalize beyond the evidence.
