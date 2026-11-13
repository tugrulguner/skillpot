# Retrospective experiment design: Dexpot Linux screen

## Question and decision

**Plan version: retrospective-illustration-v3. Retrospective only; not a preregistration.** The illustration asks whether the recorded candidate merits further qualification against its recorded control for the stated scalar-response workloads—not whether it is generally faster or causally improved. The historical screen gate is retained only as an inherited illustrative decision rule. This design does not infer from summary flags alone that cells were valid or authorize a run. The future decision owner is not supplied; execution authority is absent. This v3 wording clarifies decision relevance and economical evidence gathering after the historical results were known; it is not a new prospective plan or trial authorization. No candidate-win conclusion is made here.

Closed-loop capacity and scheduled-arrival target-load results answer different questions. Capacity cannot satisfy the inherited 10,000 offered requests/s, 95–105% achieved-rate, 20,000 µs scheduled-p99, zero-error full-gate conditions. The retained record reports that full gate was not evaluated. The packet supports neither a full-qualification claim nor independent confirmation of a candidate win.

## Evidence and assumptions

Input: the full selected published JSON at Dexpot commit `798c449fd1337404c388abb2a177c0302ba35fc0`, copied byte-exactly from retained SkillPot capture commit `1b0ae953b56a439661861c8f8ec9bf5375e8e5a6`. See packet provenance for paths, blob IDs, byte counts and SHA-256. This is not fresh retrieval. Publication commit differs from the measured control (`e703edf18d1526ebc2a91398f18c9e808e5cf5aa`) and candidate (`92e8561aa96f7e799279b89c9c9453834f9e0cda`) identities named in the record.

The complete selected JSON includes the published records, including recorded invalid/failed cells and losses, but is not the original raw campaign. Original per-trial outputs, wheel bytes and independent execution receipts are unavailable. Hashes and status flags are source-reported; they do not authenticate their referents or independently establish runtime identity, comparison validity, or a full-gate result. This proposal does not infer causality.

Historical FT limits are attributed illustrative constraints on the DUT/server process: RSS 536,870,912 bytes, 80 threads, 512 file descriptors, 10.5 CPU cores. They do not bound total experiment or driver/host resources. The record describes sampled server descendants during timed client windows, excluding startup/drain. Original sampler implementation/coverage, actual driver/host CPU and memory, and total resource use are unknown. Recorded cadence/high-water values are not independently verified. Historical thresholds are inherited illustrative gates, not newly derived facts.

Four paired blocks per workload/stage, fixed order, four A/A pairs total, and 30-second future timed cells are authored design assumptions, not historical plan details or a power calculation. The existing closed-loop client does not prove a scheduled-arrival driver is available.

## Hypotheses and falsifiers

H1 and H2 are complementary formulations of qualification versus failure of the composite advance rule, not competing causal explanations; neither identifies a mechanism. A matched difference alone cannot distinguish an artifact effect from drift, carryover or measurement mismatch; the validity observations and explicit contrasts below address those alternatives within stated limits.

- **H1 — scoped capacity-screen acceptance:** In matched, identity-verified closed-loop cells, the candidate clears every applicable inherited capacity, correctness, tail and resource gate. A valid gate failure falsifies this scoped hypothesis; a missing or invalid cell is inconclusive, not a win.
- **H2 — failure of the composite screen rule:** The candidate does not clear the frozen capacity gate. The discriminator is eligible paired candidate/control goodput and tail outcomes. A valid result clearing every applicable gate falsifies H2 only for this scope, not universally. Here H2 means failure of the composite advance rule, not proof that a candidate with a tail/correctness failure has no capacity gain.
- **H3 — apparent effect is drift/order/artifact:** A/A calibration or fixed-order blocks reveal unacceptable drift, instrumentation mismatch or order-associated differences. A frozen validity breach blocks dependent qualification until addressed prospectively. Complete in-envelope A/A observations and independently checked artifact bindings count against the corresponding measured-drift/mismatch account; passing finite checks does not eliminate every possible order or environmental confound.
- **H4 — capacity and target-load conclusions differ:** A candidate may appear better under closed-loop saturation yet fail the separately measured scheduled-arrival gate. Only that distinct stage with a verified approved driver and frozen arrival schedule can discriminate H4. For this study, eligible capacity acceptance followed by all required target-load gates passing falsifies the specific capacity-pass/target-load-fail hypothesis; capacity failure or missing target-load evidence does not test that conditional claim.
- **Seeded-fault validator check:** A separately approved seeded correctness/transport fault should be detected by the frozen validator. Failure to detect it invalidates the detection pipeline. No safe fault injection or observed outcome is supplied.
- **Known-effects sensitivity control:** A known expected effect should be detected if the owner identifies a relevant, safe control. No such control or expected result is supplied; do not invent one.

## Design, controls and invariants

**Why this design:** The question is bounded to whether the named candidate clears scoped, inherited qualification gates. Pairing candidate and control within workload, stage, and block reduces exposure to between-block conditions; fixed AB/BA counterbalance makes each side occur first in two of four blocks, addressing simple order imbalance. A factorial design is not justified because no additional factor or interaction decision is specified; a sequential/adaptive design is not justified because there is no adaptation rule or prospective stopping rationale. Randomized order would be preferable if a reproducible random assignment, seed/record, and compatible reset protocol were specified; none is supplied, so this illustration keeps the deterministic schedule visible rather than mislabeling it random.

These comparisons address but do not eliminate alternatives. A/A pairs before comparisons can reveal baseline mismatch or early drift, not establish stability across later blocks. AB/BA balance can expose gross order association but does not remove temporal drift, carryover, environmental changes, or artifact/runtime mismatch. Independent artifact bindings and measured drift/reset observations would discriminate some of those accounts; missing wheels/receipts and absent prospective drift/reset protocol leave them unresolved. A valid candidate/control difference supports only the scoped screen, not causal attribution.

- **Drift/order/carryover:** compare paired outcomes descriptively by AB versus BA order and inspect run timestamps, state/reset records and ongoing baseline/resource observations. An order-associated difference or owner-defined stability breach blocks attribution; the initial A/A pair cannot certify later stability. The observation/reset protocol and drift bounds remain preflight gaps, not additional implied matrix cells.
- **Artifact or semantic mismatch:** compare independently bound loaded artifacts and response correctness under matched inputs. A mismatch blocks performance attribution even if the aggregate ratio is favorable; absent original wheels/receipts cannot be repaired by counterbalancing.
- **Measurement-boundary explanation:** keep the capacity and approved scheduled-arrival contrasts separate. Capacity passing with a valid target-load failure distinguishes scoped capacity acceptance from target-load qualification; missing driver/arrival evidence leaves that distinction untested.

The experimental unit is one artifact run (one cell), the unit to which the candidate or control condition applies. The paired analysis unit is the candidate/control comparison within one workload-stage block; a pair contains two runs. Blocks are intended independent repetitions only if a fresh run/reset and relevant state isolation are demonstrated. Requests within a timed run and samples within a run are repeated measurements, not independent experimental units or repetitions. Four blocks give two comparisons in each order for descriptive repeatability and order-stratified inspection, rather than one comparison per order. This is a bounded feasibility choice, not a variance-based sample-size calculation or evidence of independence or statistical adequacy. Thirty seconds defines an illustrative cell duration, not a guarantee of independence, stationarity, or precision. No noise estimate, precision target, or defensible power calculation is available; strong inferential claims are therefore unsupported. The report must retain uncertainty/precision limits and may support only a bounded descriptive qualification decision unless future noise and precision requirements are justified. Reset/washout, temporal drift monitoring and prospective sampling schedule remain preflight gaps; no matrix rows or durations are silently changed.

Controls are distinguished by function. **A/A measurement check:** the same control on both sides should satisfy owner-frozen stability bounds; failure invalidates dependent comparisons. It checks measured stability, not causal absence, and the initial check cannot establish later stability. **Known-effects sensitivity control:** an owner-specified relevant effect should be detected; no effect/value is supplied, and failure would leave sensitivity unestablished. **Seeded-fault validator check:** an approved seeded fault should trigger the validator; failure invalidates the detection pipeline. This is a software test, not a scientific no-effect control. Bounds, safe fault, expected effect, procedure, and budgets remain unspecified rather than invented.

For any separately authorized future study, compare owner-approved control and candidate identities on the same platform, runtime mode, validated input distribution, response semantics, client/validator and resource envelope; change only the candidate. Bind source, built artifact, loaded module and serving process independently. The original wheel bytes are missing, so the identity invariant is currently unmet.

Include four A/A measurement-check pairs overall: one pair in each of the four stage/profile strata (two stages × two profiles). These may expose mismatch or drift at their measurement time but do not establish later stability or detector sensitivity. A separately approved seeded-fault validator check tests software fault detection; an owner-defined known-effects sensitivity control tests expected-effect detection. Neither is specified sufficiently or observed here.

Per-cell invariants: exact correctness and semantic equivalence; matched workload/profile and input path; same platform/container limits, driver/client configuration and measurement boundary; source/artifact/runtime identities at startup and after drain; no unexpected source mutation; demonstrated sampling coverage/cadence; zero forbidden errors. Record DUT/server resources separately from driver/host resources. Correctness oracle, warmup/drain and sampling methods must pass preflight. A failed invariant invalidates that cell for dependent performance comparison. An independently attributable correctness/forbidden-error failure still fails its own correctness gate; invalid ratio evidence must not erase that known failure.

## Trial matrix and measurements

Two stages: `closed_loop_capacity` and `scheduled_arrival`. Two profiles: `item` and `large_nested`. In each of the four stage/profile strata, run four paired blocks, each with one control (A) and one candidate (B): order by block is AB, BA, BA, AB (two each). This is deterministic counterbalancing, **not randomized**. Regular cells: 2 stages × 2 profiles × 4 blocks × 2 sides = 32. Add one A/A pair per stage/profile stratum: 2 × 2 × 2 sides = 8 calibration cells. Total: **40 timed cells**.

Illustrative 30-second timed duration per cell yields 40 × 30 = 1,200 seconds (20 minutes); two separate one-second smoke cells add 2 seconds, for 1,202 seconds specified-matrix workload (20 minutes, 2 seconds). Setup, warmup, drain, cooldown, analysis and the separately unresolved known-effects sensitivity and seeded-fault validator controls are excluded; their cost is unknown, not zero. These durations are authored assumptions, not recorded historical timings or approved budgets. Unique key: `stage/profile/block/order/side/role/repetition`; calibration key: `stage/profile/AA/side`. Retain every planned, observed, invalid and missing cell with explicit denominators.

**Why each phase earns its place:** smoke cells screen basic correctness/identity readiness; A/A checks screen initial measurement stability; paired capacity cells address the inherited capacity decision; scheduled-arrival cells address the separate target-load claim that capacity cannot establish. Omitting a validity check cannot be justified by a favorable candidate outcome. This fixed 42-row illustration is not claimed globally minimal or a default recipe. Before an actual study, compare cheaper adequate evidence paths against the owner-selected decision and record why every retained phase can change a decision or its validity. A narrower capacity-only question could justify a separately revised plan, but cannot qualify target-load performance; it does not silently delete cells from this illustration.

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

Scheduled-arrival qualification is separate: every control and candidate scheduled-arrival trial must achieve 95–105% of 10,000 offered requests/s, have scheduled-arrival p99 <=20,000 µs and zero forbidden errors, plus all owner-approved correctness/resource gates. These values come from `/plan/original_full_gate_retained`; its minimum capacity ratio 0.95 must also hold on the separate closed-loop pairs, which the stricter item and explicit fallback rules already require. Require every applicable gate; do not average away failures. A/A drift limits and positive-control expectations are missing and must be frozen by the owner before execution. A/A measurement-check failure or seeded-fault validator failure invalidates dependent qualification; a failed known-effects sensitivity control leaves sensitivity for its chosen effect and scale unqualified. An identity or instrumentation mismatch invalidates attribution and blocks dependent decisions; it is not evidence of a candidate performance defect. An otherwise attributable candidate correctness/forbidden-error breach or resource-cap breach fails its corresponding acceptance gate; preserve the observation. A valid loss remains a loss, but a fallback loss within the explicit 0.95 tolerance does not by itself fail that gate. Missing scheduled-arrival observations or any required identity/measurement evidence means insufficient qualification; capacity-only win cannot qualify target-load performance.

### Scheduled-arrival rule bindings

| Rule | Operator | Value | Unit | Source JSON pointer |
|---|---|---|---|---|
| offered_rps | == | 10000 | requests/s | /plan/original_full_gate_retained/offered_rps |
| achieved_rate_fraction_ge | >= | 0.95 | fraction | /plan/original_full_gate_retained/achieved_rate_fraction/0 |
| achieved_rate_fraction_le | <= | 1.05 | fraction | /plan/original_full_gate_retained/achieved_rate_fraction/1 |
| each_trial_scheduled_p99_us_le | <= | 20000 | µs | /plan/original_full_gate_retained/scheduled_p99_us |
| forbidden_errors | == | 0 | count | /plan/original_full_gate_retained/errors |
| minimum_closed_loop_capacity_ratio | >= | 0.95 | ratio | /plan/original_full_gate_retained/minimum_capacity_ratio |

No optional stopping, adaptive outlier deletion, post-result threshold changes, or silent cell replacement. Stop at the first invalid cell, retain its receipt, and mark dependent decisions incomplete. A retry is a distinct authorized observation under unchanged frozen rules. These illustrative repetitions are not a power certificate and establish no causal mechanism.

## Freeze and execution handoff

This is a post-results retrospective illustration, version 3, clarifying decision relevance and economical evidence gathering after results were known; it is not a prospective freeze or execution protocol. The proposed design is not executable: owner/target, artifact bindings, driver capability and arrival schedule, safe control definitions, sampling coverage, total resource/time budgets, and permission remain unresolved. Preserve this version; any changes before future data must be separately versioned and frozen. Expected controls (A/A within owner-frozen drift limits, seeded-fault validator detection, owner-defined known-effects sensitivity) have not been observed.

### Prioritized decision handoff

- **Decidable now:** this supplied packet does not establish target-load qualification or independently authenticated execution. No new trial is needed to conclude that the present evidence is insufficient; do not run the 42 cells merely to rediscover that gap.
- **First dependency — owner and question:** ask the future decision owner (not supplied) whether the required decision is historical authentication, scoped future capacity qualification, or target-load qualification, and which available control/candidate artifacts are eligible. The answer changes the necessary evidence and comparison. A new run of different artifacts cannot authenticate the historical run; historical authentication needs an evidence-recovery/audit handoff, not a new performance experiment.
- **Smallest next evidence step — inspection, not a trial:** request separately approved, bounded artifact manifests and, for the target-load question, relevant driver/interface documentation from the responsible artifact/driver owners. Check whether the chosen future artifacts can be bound and the driver supports the selected measurement boundary. Permission and availability are not supplied here. If that capability or identity is absent, stop that execution path; ask whether to authorize recovery/development work or a prospectively revised narrower question, never substitute a capacity result for target-load evidence.
- **Only after that branch is resolved:** the decision and measurement owners must freeze safe controls, reset/drift/sampling rules and an approved total budget. Then justify the smallest sufficient comparison and version it before any future observations. The illustrative durations are not approved costs; no role, permission or outcome is invented by this ordering.

**Execution status: not run; not authorized; pending preflight.** No benchmark, model, server, client, wheel, or original trial record was executed or reconstructed for this illustration. A clean preflight is not a candidate observation or qualification result.
