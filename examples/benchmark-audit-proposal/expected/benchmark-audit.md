# Benchmark audit — authored expected report

## Scope and decision

Audit the exact C1–C6 text in [claims.md](../claims.md) against source S1 below.
C7 is explicitly deferred by the owner. This is a **parent-authored specification
example**, not an observed agent output or a new performance campaign.

**Decision:** do not use this packet to promote the candidate or claim clean performance
qualification. The published record retains timeout-invalid trials and a valid flat
pair with lower recorded goodput and higher adjusted p99. Independently authenticating
original execution is outside what these supplied bytes permit. This is not a claim
that the current Dexpot release has these historical characteristics.

## Evidence inventory

- **S1:** [sources/linux-screen.json](../sources/linux-screen.json), the complete published
  Dexpot Linux ARM64 container-loopback FT scalar-screen record at publication snapshot
  `798c449fd1337404c388abb2a177c0302ba35fc0`; file SHA-256
  `6537c1aeb85abe9afd5bdcdcf69dd1013ee12f3100efe6523094838599b06f9c`.
- [provenance.json](../provenance.json) separately records publication revision, Git
  blob identity, copied-file hashes and notice. S1 `/plan/control_commit` and
  `/plan/candidate_commit` identify measured source roles, not the publication snapshot.
- Its per-trial raw-record digests, wheel-source fields and lifecycle events
  describe retained upstream observations. Original per-trial raw files, wheel bytes,
  client/application binaries and independently captured commands are **not supplied**.
  This audit checks the published file's bytes/accounting, not those original events.

JSON locators below are RFC 6901 pointers into S1, with zero-based array indexes.
The asterisk above is descriptive, not an exact pointer used as evidence.

## Claims

### C1 — Supported within scope

> The published JSON contains one trial record for each of the eight planned cells,
> including two smoke cells and six screen cells.

Reconciled `/plan/cells` with `/trials`: every planned `cell.id` occurs once, with
matching cell metadata. Two have `phase: smoke` and six have `phase: screen`.
`/evaluation/expected_trials` and `/evaluation/collected_trials` both say 8, but the
independent inventory check—not merely those summary totals—supports this statement.
This establishes completeness of the published cell inventory, not completeness of
original raw evidence or successful qualification.

### C2 — Contradicted

> All eight trial records report zero timeout errors.

`/trials/3/cell/id` is `item-1-candidate`; `/trials/3/metrics/timeout_errors` is 6.
`/trials/6/cell/id` is `fallback-control`; `/trials/6/metrics/timeout_errors` is 2.
Both `/trials/3/comparison_valid` and `/trials/6/comparison_valid` are false.
Zero recorded bad bodies does not erase these transport failures. Supported wording:
**“The record preserves two timeout-invalid trials, reporting eight timeouts in total.”**
The counters' historical accuracy remains source-reported, not independently rerun.

### C3 — Contradicted

> Both 30-second flat pairs demonstrate candidate/control goodput above 1.0 and
> adjusted closed-loop p99 ratios at most 1.10.

The valid recorded `item-2` pair (`/trials/4`, candidate; `/trials/5`, control) is a
counterexample: recomputed goodput ratio 0.968621 and p99 ratio 1.296943. Also retain
`item-1` (`/trials/2`, `/trials/3`) as comparison-ineligible because its candidate
reports timeouts; do not omit it or derive a clean two-pair median.
The plan's flat gates are at `/plan/screen_gate/flat_pairs` and `/plan/screen_gate/tail`.
This contradicts the exact recorded-pair claim; it does not prove universal inferiority.

### C4 — Supported within scope

> For the archived `item-2` pair, the candidate's recorded goodput is lower and its
> recorded adjusted closed-loop p99 is higher than the control's.

Recompute from `/trials/4/metrics` and `/trials/5/metrics`, rather than adopting the
ratios in `/evaluation/pairs/1`. The source marks both rows comparison-valid and both
resource observations passing. The values describe about **3.14% lower recorded goodput
and 29.69% higher recorded adjusted p99** for this single pair. They establish arithmetic
within the archived record, not independently verified, repeatable product behavior.

### C5 — Insufficient evidence

> The wheel bytes actually loaded in every recorded trial match that side's
> declared wheel digest.

The wheel digests at `/plan/control_wheel_sha256` and `/plan/candidate_wheel_sha256`
are declared identities. For example, `/trials/0/source` and `/trials/0/lifecycle/events` add recorded
startup/after-workload evidence, but no original wheel/raw bytes or independently
captured execution chain are supplied. Correct hash format and internally consistent
flags do not establish this underlying execution claim. Missing wheel bytes and source-bound execution receipts leave it
unresolved; they do not prove that different bytes actually ran. The separate claim
that the packet supplies original wheel bytes would be contradicted by its inventory.

### C6 — Insufficient evidence

> At 10,000 offered requests per second, the candidate's scheduled-arrival
> p99 latency is at most 20 ms.

`/plan/original_full_gate_retained/offered_rps` is 10000 and
`/plan/original_full_gate_retained/scheduled_p99_us` is 20000, but
`/plan/original_full_gate_retained/status` says
“Not evaluated by this closed-loop screen; original #116 failures retained”. The
screen's adjusted closed-loop p99 cannot establish that scheduled-arrival budget.
The source's `/evaluation/full_qualification_pass` is false; this is not itself a new
measurement disproving the underlying scheduled-latency proposition. Preserve the
prior-failure statement as attributed history, not a separately inspected #116 corpus.

### C7 — Not assessed

> The candidate is faster on macOS as well.

The owner explicitly deferred C7 and other platforms in claims.md. No macOS evidence
was selected, inspected or compared here. This exclusion must remain visible; neither
this omission nor the Linux observations establish macOS speed or regressions.

## Comparison and accounting

- Eight planned/observed unique cells; two smoke and six screen records. No missing
  or duplicate IDs. Six rows are marked comparison-valid, including the two smoke rows;
  **that is not six valid screen trials**. Four screen rows are marked comparison-valid.
- Three screen pairs: `item-1`, `item-2`, `fallback`. All are present; only `item-2`
  has both rows marked valid. There is no eligible two-repeat flat aggregate.
- S1 records 10,451,995 good replies across all eight rows, zero bad replies and eight
  timeout errors. Good completed replies and failure-free transport are different axes.
  Do not promote that all-row sum to an error-free qualification population.
- Preserve both invalid rows and the adverse valid pair. Smoke records are not
  30-second screen replacements. The fallback payload is not the flat item workload.
- The record's environment is Linux ARM64 Docker-loopback FT; runtime/activation
  observations are source-reported. It does not qualify bare metal, another platform,
  an independently authenticated loaded artifact, or a whole-application speedup.
- All source-reported resource checks pass; sampled resource observations neither
  erase transport/performance losses nor establish exact continuous peak usage.

## Calculations

Tool-recomputed from S1, no benchmark or framework executed:

- Candidate goodput: `2607747 * 1000000 / 30100399` replies/s.
- Control goodput: `2683339 * 1000000 / 30001020` replies/s.
- Goodput ratio: `(2607747 / 30100399) / (2683339 / 30001020)` =
  `0.9686205521773416`, displayed as `0.968621`.
- Adjusted closed-loop p99 ratio: `891 / 687` = `1.296943231441048`, displayed
  as `1.296943`; the source's p99 values are microseconds.
- Relative goodput change: `(ratio - 1) * 100` = `-3.1379447822658446%`.
- Relative adjusted p99 change: `(ratio - 1) * 100` = `29.694323144104807%`.

These are per-pair ratios, not a median, pooled percentile, offered-load result or
causal decomposition. The invalid pairs do not contribute clean qualifying ratios.

## Evidence limits and next checks

The published packet is fully readable, but original raw records, wheels and source
artifacts named only by hashes are not supplied. This audit does not validate the
collector, independently establish workload-contract parity, authenticate serving
telemetry, verify that thresholds were frozen before execution, or reproduce timings.
No source chronology, scheduled-load result, causal diagnosis or current-version
performance claim is invented. No benchmark, application, container or agent-model
trial was run to produce this authored example.

Before any independent execution/performance qualification, recover the original
records/artifacts and verify their source/runtime bindings and the relevant comparison
contract. Design new tests only under separately authorized scope. Owner approval,
implementation, merge, deployment and publication remain separate decisions.
