# Explicit-loading task observations on authored fiction

Read [the quality protocol and limitations](../../docs/skill-quality.md) first.
This directory contains an executed bounded study, not a skill accuracy certificate.

- `cases.json`: frozen eighteen-criterion rubric for three fictional offline tasks.
- `cases/`: only the four source input files, never expected reports.
- `initial-artifacts.json`: six actual initial attempts, two per task; input, bundle
  and report fingerprints, runtime-reported metadata and explicit limitations.
- `reports-exact.zip`: all twelve byte-exact original reports plus the two separately
  labeled assisted reports. Archive members have their own SHA-256 fingerprints.
- `initial/`: readable reports. Two have disclosed whitespace-only adaptations to
  satisfy the unchanged committed-whitespace gate; originals remain exact in ZIP.
  Two-space Markdown hard breaks become backslash hard breaks, and extra EOF blank
  lines are removed. No source assertions, IDs, verdicts or findings are changed.
- `grading/raw/`: four original independent grading artifacts covering six attempts.
- `grading/decision-brief-citation-addendum.json`: two corrected literal citations;
  original grader quotations remain in the raw artifact. Verdicts are unchanged.
- `grading/addenda/document-actions-reviewer-addendum.json`: independent withdrawal
  of the mistaken A2 allegation and retention of the actual A3 placement finding.
  Some source-contract excerpts are formatting-normalized or ellipsized; do not
  treat every `quote` field in this addendum as a literal span.
- `grading/document-actions-reconciliation.json`: controller-verified literal A3
  evidence and correction scope, distinct from the original reviewer text.
- `assisted/doc-actions-attempt-2/`: separately labeled parent placement correction;
  unchanged record content, unchanged questions, original/corrected SHA-256 receipt.

All thirty-six frozen criterion judgments were pass; the physical placement defect
still exists in one original. A passing rubric can miss a source-contract defect,
and graders can misquote or conflate records. Neither the original scores nor the
corrected derivative should be advertised as complete task correctness.

All attempts loaded supplementary host guidance. The study has no clean no-skill
control, native-client or automatic-selection trial, immutable model fingerprint,
token counters, or complete raw process journal. Retained private runtime logs are
preview-truncated. Tool errors were preserved separately from artifact findings.
A reported ignored footer is output-level evidence, not general injection resistance.

The archived reports and grading records are historical observations at the recorded
source snapshot. Future tasks or criteria need a new cohort; do not edit this frozen
corpus, erase unsuccessful behavior, or overwrite original reports to fit new checks.
The offline test suite verifies containment, inventories, fingerprints, literal
citations and bounded placement controls; semantic judgments still require review.
