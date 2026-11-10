# Prospective physical-placement cohort

This is a new cohort, not a rewritten rubric or regrade of the original six task
attempts. `cases.json` and all four fictional source inputs were parent-reviewed
and fingerprinted before the new task attempts were dispatched. `protocol.json`
records that immutable identity and the unchanged public skill snapshot. The
initial mechanical checker was implemented and calibrated during task execution,
before parent report inspection. Later missing-record diagnostics and ATX syntax
guards were repaired after grading; checker code was not part of the pre-execution
freeze. The source-derived criteria, not a post-hoc
checker implementation, define the prospective judgments.

## Predeclared acceptance

Each case has five source-grounded canonical records and eight critical criteria.
The placement criterion explicitly requires every record's actual containing
section, complete/unique record coverage, and the existing template headings.
Category labels inside a record do not establish where that record appears.

Assigned work with only an owner or deadline conflict remains assigned. A separate
status conflict requires a single canonical unresolved record. The source packets
also require an unassigned mandatory requirement, an unaccepted proposal and a
completed historical item with its source-known actor.

Two independent attempts per packet were executed; their eight unmodified reports
are retained in `initial/` and `reports-exact.zip`, with hashes and actual runtime
metadata in `observations.json`. Writers received only the complete public skill
and source inputs, never the expected-record inventory or rubric.
The explicit template-heading prompt and valid command working directory are
recorded differences from the first cohort; these are not matched conditions for
an improvement or causal comparison.

## Independent semantic mapping and bounded structural checking

After execution, a separate grader reads the complete sources and actual reports.
For each source key in `expected_records`, the grader supplies its literal output
H3 heading, with source/output evidence. The grader must establish proposition
identity; selecting a physically convenient but semantically different record is
an invalid mapping. Output IDs are not prescribed by the corpus.

`tests/placement_contract.py` checks the resulting data against the saved report:

- Every source record maps exactly once to one actual H3, with no missing,
  duplicated, additional or aliased records.
- Every required category H2 appears once; the record's containing section must
  match the independently reviewed source category.
- A nonempty section cannot claim that none were identified.
- Quoted heading lines and fenced backtick/tilde code are data. Up to three spaces
  of ATX heading indentation, tab delimiters and physical LF/CRLF/CR are supported;
  a new H1 (including an empty heading) resets the H2 context.

This is a test-only checker for the explicit ATX template profile, not a general
Markdown parser or semantic classifier. It does not infer facts from Category
labels, certify the correctness of grader mappings, or establish host permissions.
Synthetic positive and mutation controls are labeled separately from real task
outputs. The original narrow A3 regression remains unchanged.

## Evidence rules

Preserve all actual attempts, including missing/incorrect reports or tool failures.
Retain full raw report bytes and their SHA-256 identities; any readable formatting
adaptation needs a separate hash and explanation. Assess the frozen placement
criterion before any correction or post-hoc change. Never overwrite failed attempts
or revise their criteria to make them pass.

Host standing guidance remains active; supplementary skills and preview-truncated
runtime logs are limitations. No clean no-skill baseline, automatic-selection,
native-client activation or causal skill-improvement claim is made. The CI checks
are offline and do not launch agents or models.

## Recorded results and repairs

Independent grading retained 29 pass and 3 fail judgments across 32 criteria. Three
reports passed the frozen placement criterion. Harbor-archive attempt 2 omitted the
sleeve-chart proposal and placed the status-conflicted inspection under Outstanding,
despite labeling it unresolved. Its placement, proposal-retention and single
unresolved-record criteria failed. None of those failures is overwritten.

`grading/raw/` retains the original judges. The harbor judge also incorrectly mapped
the present A1 packing-list requirement to null. `grading/mapping-addendum.json`
binds a separately reviewed correction to the raw grade and original report hashes;
`grading/map-reconciliation-raw.json` retains that review, including its explicit
lack of independent guide/template inspection. Some raw reconciliation source
excerpts are paraphrases or combined statements, not literal spans. The addendum
supplies separate literal source evidence without rewriting the review.

`grading/parent-audit.json` retains the raw-map failure and reconciled structural
results. The corrected map exposes two separate original artifact defects: a missing
proposal record and an inspection in the wrong containing section. Semantic mapping
remains a reviewed input, not a fact inferred by the checker.

`controls.json` records three untouched actual-report baselines and 99 authored
negative variants: 45 whole-record relocations, 15 omissions, 15 duplications and
24 missing/duplicate section headings. CI reconstructs every variant and compares
its digest and actual checker result. Synthetic controls are not agent trials.

`assisted/harbor-archive-attempt-2/` restores proposal P1 and relocates unchanged A3;
existing IDs and questions are preserved and original/corrected hashes are explicit.
Independent source/artifact review accepted that bounded correction, and structural
checking passes. It is an assisted derivative, not an unassisted success or a claim
that the unchanged skill now performs better.

A parent audit also notes a blank-line citation in harbor attempt 1 (line 26 rather
than Dev's statement on line 27). Passing frozen judgments are not complete report
correctness or source-locator certification. One visible terminal ERROR event is
retained for orchard attempt 2 even though its completion summary did not mention
an issue; truncated logger previews do not establish the error's exact cause.
