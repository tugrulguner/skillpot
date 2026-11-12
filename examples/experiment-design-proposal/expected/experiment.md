# Retrospective experiment design: Dexpot Linux screen

## Question and decision

**Plan version: retrospective-illustration-v1. Retrospective only; not a preregistration.** The illustration asks whether the recorded candidate merits further qualification against its recorded control for the stated scalar-response workloads—not whether it is generally faster or causally improved. The historical screen gate is retained only as an inherited illustrative decision rule. This design does not infer from summary flags alone that cells were valid or authorize a run. The future decision owner is not supplied; execution authority is absent. No candidate-win conclusion is made here.

Closed-loop capacity and scheduled-arrival target-load results answer different questions. Capacity cannot satisfy the inherited 10,000 offered requests/s, 95–105% achieved-rate, 20,000 µs scheduled-p99, zero-error full-gate conditions. The retained record reports that full gate was not evaluated. The packet supports neither a full-qualification claim nor independent confirmation of a candidate win.

## Evidence and assumptions

Input: the full selected published JSON at Dexpot commit `798c449fd1337404c388abb2a177c0302ba35fc0`, copied byte-exactly from retained SkillPot capture commit `1b0ae953b56a439661861c8f8ec9bf5375e8e5a6`. See packet provenance for paths, blob IDs, byte counts and SHA-256. This is not fresh retrieval. Publication commit differs from the measured control (`e703edf18d1526ebc2a91398f18c9e808e5cf5aa`) and candidate (`92e8561aa96f7e799279b89c9c9453834f9e0cda`) identities named in the record.

The complete selected JSON includes the published records, including recorded invalid/failed cells and losses, but is not the original raw campaign. Original per-trial outputs, wheel bytes and independent execution receipts are unavailable. Hashes and status flags are source-reported; they do not authenticate their referents or independently establish runtime identity, comparison validity, or a full-gate result. This proposal does not infer causality.

Historical FT limits are attributed illustrative constraints on the DUT/server process: RSS 536,870,912 bytes, 80 threads, 512 file descriptors, 10.5 CPU cores. They do not bound total experiment or driver/host resources. The record describes sampled server descendants during timed client windows, excluding startup/drain. Original sampler implementation/coverage, actual driver/host CPU and memory, and total resource use are unknown. Recorded cadence/high-water values are not independently verified. Historical thresholds are inherited illustrative gates, not newly derived facts.

Four paired blocks per workload/stage, fixed order, four A/A pairs total, and 30-second future timed cells are authored design assumptions, not historical plan details or a power calculation. The existing closed-loop client does not prove a scheduled-arrival driver is available.

## Hypotheses and falsifiers

- **H1 — scoped capacity-screen acceptance:** In matched, identity-verified closed-loop cells, the candidate clears every applicable inherited capacity, correctness, tail and resource gate. A valid gate failure falsifies this scoped hypothesis; a missing or invalid cell is inconclusive, not a win.
- **H2 — failure of the composite screen rule:** The candidate does not clear the frozen capacity gate. The discriminator is eligible paired candidate/control goodput and tail outcomes. A valid result clearing every applicable gate falsifies H2 only for this scope, not universally. Here H2 means failure of the composite advance rule, not proof that a candidate with a tail/correctness failure has no capacity gain.
- **H3 — apparent effect is drift/order/artifact:** A/A calibration or fixed-order blocks reveal unacceptable drift, instrumentation mismatch or order-associated differences. A frozen validity breach blocks dependent qualification until addressed prospectively. Complete in-envelope A/A observations and independently checked artifact bindings count against the corresponding measured-drift/mismatch account; passing finite checks does not eliminate every possible order or environmental confound.
- **H4 — capacity and target-load conclusions differ:** A candidate may appear better under closed-loop saturation yet fail the separately measured scheduled-arrival gate. Only that distinct stage with a verified approved driver and frozen arrival schedule can discriminate H4. For this study, eligible capacity acceptance followed by all required target-load gates passing falsifies the specific capacity-pass/target-load-fail hypothesis; capacity failure or missing target-load evidence does not test that conditional claim.
- **Negative-control detection:** A separately approved seeded correctness/transport fault should be detected by the frozen validator. Failure to detect it invalidates the detection pipeline. No safe fault injection or observed outcome is supplied.
- **Positive calibration:** A known expected effect should be detected if the owner identifies a relevant, safe control. No such control or expected result is supplied; do not invent one.

## Design, controls and invariants

For any separately authorized future study, compare owner-approved control and candidate identities on the same platform, runtime mode, validated input distribution, response semantics, client/validator and resource envelope; change only the candidate. Bind source, built artifact, loaded module and serving process independently. The original wheel bytes are missing, so the identity invariant is currently unmet.

Include four A/A calibration pairs overall: one pair in each of the four stage/profile strata (two stages × two profiles). These expose drift but do not establish detector sensitivity. A separate approved negative control tests detection; an owner-defined positive calibration tests expected-effect detection. Neither is observed here.

Per-cell invariants: exact correctness and semantic equivalence; matched workload/profile and input path; same platform/container limits, driver/client configuration and measurement boundary; source/artifact/runtime identities at startup and after drain; no unexpected source mutation; demonstrated sampling coverage/cadence; zero forbidden errors. Record DUT/server resources separately from driver/host resources. Correctness oracle, warmup/drain and sampling methods must pass preflight. A failed invariant invalidates that cell for dependent performance comparison. An independently attributable correctness/forbidden-error failure still fails its own correctness gate; invalid ratio evidence must not erase that known failure.

## Trial matrix and measurements

Two stages: `closed_loop_capacity` and `scheduled_arrival`. Two profiles: `item` and `large_nested`. In each of the four stage/profile strata, run four paired blocks, each with one control (A) and one candidate (B): order by block is AB, BA, BA, AB (two each). This is deterministic counterbalancing, **not randomized**. Regular cells: 2 stages × 2 profiles × 4 blocks × 2 sides = 32. Add one A/A pair per stage/profile stratum: 2 × 2 × 2 sides = 8 calibration cells. Total: **40 timed cells**.

Illustrative 30-second timed duration per cell yields 40 × 30 = 1,200 seconds (20 minutes); two separate one-second smoke cells add 2 seconds, for 1,202 seconds specified-matrix workload (20 minutes, 2 seconds). Setup, warmup, drain, cooldown, analysis and the separately unresolved positive/negative validator controls are excluded; their cost is unknown, not zero. These durations are authored assumptions, not recorded historical timings or approved budgets. Unique key: `stage/profile/block/order/side/role/repetition`; calibration key: `stage/profile/AA/side`. Retain every planned, observed, invalid and missing cell with explicit denominators.

Frozen illustrative schedule: the two smoke cells run first; then strata follow the stage/profile order below. In each stratum the A/A pair precedes its four A/B blocks and must clear its owner-frozen calibration rule before dependent cells. For calibration, slots A and B both use the same control artifact; for comparisons A is control and B is candidate. This schedule is authored, not a historical receipt.

| ID | Stage | Profile | Phase | Block | Slot | Artifact role | Seconds |
|---|---|---|---|---|---|---|---|
| P001 | closed_loop_capacity | item | smoke | 0 | A | control | 1 |
| P002 | closed_loop_capacity | item | smoke | 0 | B | candidate | 1 |
| P003 | closed_loop_capacity | item | calibration | 0 | A | control | 30 |
| P004 | closed_loop_capacity | item | calibration | 0 | B | control | 30 |
| P005 | closed_loop_capacity | item | comparison | 1 | A | control | 30 |
| P006 | closed_loop_capacity | item | comparison | 1 | B | candidate | 30 |
| P007 | closed_loop_capacity | item | comparison | 2 | B | candidate | 30 |
| P008 | closed_loop_capacity | item | comparison | 2 | A | control | 30 |
| P009 | closed_loop_capacity | item | comparison | 3 | B | candidate | 30 |
| P010 | closed_loop_capacity | item | comparison | 3 | A | control | 30 |
| P011 | closed_loop_capacity | item | comparison | 4 | A | control | 30 |
| P012 | closed_loop_capacity | item | comparison | 4 | B | candidate | 30 |
| P013 | closed_loop_capacity | large_nested | calibration | 0 | A | control | 30 |
| P014 | closed_loop_capacity | large_nested | calibration | 0 | B | control | 30 |
| P015 | closed_loop_capacity | large_nested | comparison | 1 | A | control | 30 |
| P016 | closed_loop_capacity | large_nested | comparison | 1 | B | candidate | 30 |
| P017 | closed_loop_capacity | large_nested | comparison | 2 | B | candidate | 30 |
| P018 | closed_loop_capacity | large_nested | comparison | 2 | A | control | 30 |
| P019 | closed_loop_capacity | large_nested | comparison | 3 | B | candidate | 30 |
| P020 | closed_loop_capacity | large_nested | comparison | 3 | A | control | 30 |
| P021 | closed_loop_capacity | large_nested | comparison | 4 | A | control | 30 |
| P022 | closed_loop_capacity | large_nested | comparison | 4 | B | candidate | 30 |
| P023 | scheduled_arrival | item | calibration | 0 | A | control | 30 |
| P024 | scheduled_arrival | item | calibration | 0 | B | control | 30 |
| P025 | scheduled_arrival | item | comparison | 1 | A | control | 30 |
| P026 | scheduled_arrival | item | comparison | 1 | B | candidate | 30 |
| P027 | scheduled_arrival | item | comparison | 2 | B | candidate | 30 |
| P028 | scheduled_arrival | item | comparison | 2 | A | control | 30 |
| P029 | scheduled_arrival | item | comparison | 3 | B | candidate | 30 |
| P030 | scheduled_arrival | item | comparison | 3 | A | control | 30 |
| P031 | scheduled_arrival | item | comparison | 4 | A | control | 30 |
| P032 | scheduled_arrival | item | comparison | 4 | B | candidate | 30 |
| P033 | scheduled_arrival | large_nested | calibration | 0 | A | control | 30 |
| P034 | scheduled_arrival | large_nested | calibration | 0 | B | control | 30 |
| P035 | scheduled_arrival | large_nested | comparison | 1 | A | control | 30 |
| P036 | scheduled_arrival | large_nested | comparison | 1 | B | candidate | 30 |
| P037 | scheduled_arrival | large_nested | comparison | 2 | B | candidate | 30 |
| P038 | scheduled_arrival | large_nested | comparison | 2 | A | control | 30 |
| P039 | scheduled_arrival | large_nested | comparison | 3 | B | candidate | 30 |
| P040 | scheduled_arrival | large_nested | comparison | 3 | A | control | 30 |
| P041 | scheduled_arrival | large_nested | comparison | 4 | A | control | 30 |
| P042 | scheduled_arrival | large_nested | comparison | 4 | B | candidate | 30 |

Capacity metrics: validated good replies / actual timed seconds (replies/s), errors/counts, and per-trial closed-loop latency distribution including p99 in microseconds; retain raw histograms and elapsed time. Scheduled-arrival metrics: scheduled and achieved requests/s, scheduled-arrival p99 in microseconds, errors, and target-rate shortfall. Never compare scheduled-arrival latency with closed-loop p99. Report DUT and driver resource maxima separately with actual sample coverage/cadence. Preflight must establish high-water capture and correctness; do not assume them from a requested sampling interval. No runnable driver command is specified because availability is unproven.

## Budgets and permissions

The illustrative measured-workload budget is 1,200 seconds for timed cells plus 2 seconds for smoke cells. This excludes overhead and is not an authorized wall-clock allocation. The recorded FT limits apply to DUT/server process scope only; no total-resource guarantee follows. Driver/host budgets must be separately specified and measured. Before execution, obtain owner approval for total wall-clock cap, overhead, resources/storage, platform, driver, sampling and stop authority. No new driver, dependency, service, benchmark, or execution is authorized here.

Preflight gaps: decision owner and exact target; recover/verify control and candidate artifact bytes/bindings; correctness oracle and safe controls; approved scheduled-arrival driver/schedule; sampling implementation/coverage; total DUT-plus-driver resource and wall-clock budgets; execution permission and destination. Missing original artifacts remain historical evidence gaps, not invitations to reconstruct them.

## Analysis and decision rules

For eligible matched cells, compute goodput as validated good replies divided by actual timed seconds; form candidate/control ratios within the same stage, profile and block. Higher goodput is better. In the closed-loop stage, all four `item` pair goodput ratios must exceed 1.0 and their median must be at least 1.05; every `large_nested` pair goodput ratio must be at least 0.95. The median of the four item adjusted closed-loop p99 pair ratios must be at most 1.10; each large-nested p99 pair ratio must be at most 1.10. Median pair ratios do not mean pooled-trial percentiles. These numeric limits are inherited from `/plan/screen_gate/flat_pairs`, `/plan/screen_gate/fallback_pair` and `/plan/screen_gate/tail`; applying them to four new pairs per profile is an **authored extension**, not the original two-flat-pair protocol. No per-pair tail gate is invented for item beyond the declared median rule. Keep all individual adverse values visible and never substitute values from a different measurement mode.

Scheduled-arrival qualification is separate: every control and candidate scheduled-arrival trial must achieve 95–105% of 10,000 offered requests/s, have scheduled-arrival p99 <=20,000 µs and zero forbidden errors, plus all owner-approved correctness/resource gates. These values come from `/plan/original_full_gate_retained`; its minimum capacity ratio 0.95 must also hold on the separate closed-loop pairs, which the stricter item and explicit fallback rules already require. Require every applicable gate; do not average away failures. A/A drift limits and positive-control expectations are missing and must be frozen by the owner before execution. A/A or negative-control failure invalidates dependent qualification. An identity or instrumentation mismatch invalidates attribution and blocks dependent decisions; it is not evidence of a candidate performance defect. An otherwise attributable candidate correctness/forbidden-error breach or resource-cap breach fails its corresponding acceptance gate; preserve the observation. A valid loss remains a loss, but a fallback loss within the explicit 0.95 tolerance does not by itself fail that gate. Missing scheduled-arrival observations or any required identity/measurement evidence means insufficient qualification; capacity-only win cannot qualify target-load performance.

No optional stopping, adaptive outlier deletion, post-result threshold changes, or silent cell replacement. Stop at the first invalid cell, retain its receipt, and mark dependent decisions incomplete. A retry is a distinct authorized observation under unchanged frozen rules. These illustrative repetitions are not a power certificate and establish no causal mechanism.

## Freeze and execution handoff

This is a post-results retrospective illustration, not a prospective freeze. The proposed design is not executable: owner/target, artifact bindings, driver capability and arrival schedule, safe control definitions, sampling coverage, total resource/time budgets, and permission remain unresolved. Preserve this version; any changes before future data must be separately versioned and frozen. Expected controls (A/A within owner-frozen drift limits, seeded negative detection, owner-defined positive calibration) have not been observed.

**Execution status: not run; not authorized; pending preflight.** No benchmark, model, server, client, wheel, or original trial record was executed or reconstructed for this illustration. A clean preflight is not a candidate observation or qualification result.
