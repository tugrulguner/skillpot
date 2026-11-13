# Retrospective experiment-design packet

**Authored integrity fixture only.** This is not an installable skill, prospective preregistration, experiment, benchmark, observed agent task, or execution receipt. Its complete input record and license are retained byte-exact copies, not newly fetched material.

## Inputs and provenance

[`task.md`](task.md) is the authored input-only review task and permission/read boundary. Expected reports/oracles are excluded from its later task input set.

- [`sources/linux-screen.json`](sources/linux-screen.json): complete selected published Dexpot Linux-screen JSON, copied byte-for-byte from the retained public packet.
- [`sources/DEXPOT-LICENSE`](sources/DEXPOT-LICENSE): complete byte-exact Dexpot MIT notice.
- [`provenance.json`](provenance.json): capture origin, pinned upstream commit/path/blob IDs, byte counts and recomputed digests.

The original campaign's raw trial outputs, wheels and independent launch/execution receipts are unavailable. Recorded hashes or status fields do not recover those artifacts or independently authenticate the events. Source-reported resource metrics concern a sampled server descendant tree during timed client windows and exclude startup/drain; they do not establish total experiment resources. Driver/host CPU, memory, sampling coverage and original sampling implementation are unknown. Do not claim a source-recorded flag alone proves a valid pair, a full gate, or execution identity.

## Worked decision and design

The authored illustration asks whether the recorded candidate merits further qualification against its named control, while explicitly not claiming the historical packet authorizes a new run. It distinguishes a closed-loop capacity screen from a separate scheduled-arrival/target-load stage. The historical record supplies thresholds as inherited illustrative gates only; the original scheduled-arrival criteria were expressly not evaluated by the closed-loop screen. Neither summary flags nor a purported capacity win can substitute for raw artifact binding, valid-cell review, or the missing scheduled-arrival observations.

Design selection is part of the illustration, not a checklist: paired comparisons hold workload/profile and local conditions together, while the fixed AB/BA balance addresses simple order imbalance. The four A/A pairs can expose some measured drift, but they cannot establish stability later in the sequence or remove all order, carryover, environmental, or artifact explanations. This matched counterbalanced design is a bounded choice for this retrospective proposal; randomization would be more defensible if assignment order could be generated and preserved without compromising the paired/reset protocol, while factorial or sequential designs would require a decision question and interaction/adaptation rationale not supplied here. The experimental unit is one artifact run (one cell); the paired analysis unit is its matched candidate/control comparison within a workload-stage block. Requests/samples inside a run are measurements, not independent repetitions. Four blocks are a feasibility illustration, not a precision or adequacy claim. No noise estimate supports a precision target or power calculation, so strong inferential claims remain unsupported.

Controls are named by function: A/A measurement check (identical control conditions; unexpected drift invalidates dependent comparisons), known-effects sensitivity control (expected detection still unspecified; failure would leave sensitivity unestablished), and seeded-fault validator check (expected detection of an approved injected fault; failure invalidates the validator). The latter is a software detection check, not a scientific no-effect control. Safe values, bounds and costs are unresolved; no control details are invented.

The proposed illustrative future matrix contains two workload profiles (`item`, `large_nested`) at each of two distinct stages (closed-loop capacity and scheduled-arrival), four paired blocks per workload/stage, and a deterministic counterbalanced AB/BA order sequence `AB, BA, BA, AB` (two per order). It is a fixed balanced order, **not randomized**. Each pair contributes two candidate/control trials: 2 × 2 × 4 × 2 = 32 regular cells. Four separate A/A calibration pairs contribute 8 cells (four baseline-vs-baseline pairs), for **40 timed calibration/comparison cells**, plus the two separately specified smoke cells. The full ordered 42-row matrix is enumerated in the expected report and oracle. These are authored repetition choices, not historical counts, power calculations, or guarantees of adequate precision.

Each timed cell is illustratively budgeted at 30 seconds; two one-second smoke cells are separately preflight-only. Thus timed workload is 40 × 30 = 1,200 seconds (20 minutes); including two smoke cells gives 1,202 seconds (20 minutes, 2 seconds) of specified-matrix workload, excluding setup, warmup, drain, cooldown, analysis and undefined known-effects sensitivity and seeded-fault validator checks. Their unbudgeted cost is unknown, not zero. These are design assumptions, not historical run duration or an authorized resource budget. Require an owner-approved total wall-clock/resource budget before execution. The historical FT process limits, where applicable, describe the DUT/server process scope only (RSS 536,870,912 bytes, 80 threads, 512 file descriptors, 10.5 CPU cores); they do not bound driver/host overhead or total machine use. Historical sample intervals/high-water values are source-reported and not independently verified; future sampling coverage, actual cadence, high-water capture, correctness and identity checks are preflight criteria.

The scheduled-arrival stage requires a separately identified, available and approved driver plus independently specified arrival schedule and latency boundary. The retained closed-loop client does not establish this capability; no runnable command is proposed. Original wheels/raw data, driver availability, measurement instrumentation, final workload/target approval, owner permission, and an approved total resource/time budget remain unresolved. Therefore the design is complete as a bounded illustration but is **not executable and not authorized to execute**.

## Expected output

[`expected/experiment.md`](expected/experiment.md) is a post-results retrospective illustration. It preserves exactly the eight output-contract headings and labels historical facts, source-attributed observations, authored assumptions and gaps. It is not preregistration, an independent reproduction, causal diagnosis, or a claim of experiment execution. [`expected/design.json`](expected/design.json) is the structured authoring oracle for the frozen illustrative matrix, budgets, provenance and report identity; it is not a second runtime output or observed result.

Legacy oracle fields `positive_control_definition` and `negative_control_definition`, and the case ID `negative_control_not_detected`, are retained identifiers only. The structured `control_roles` map binds them to known-effects sensitivity and seeded-fault validator functions; they do not redefine a scientific no-effect control.

## Adversarial acceptance and verification

[`acceptance.json`](acceptance.json) specifies authored cases and expected dispositions. The offline tests check the pristine fixture, source provenance and hashes, complete failed/loss-containing record retention, matrix pairing/order/stage/workload uniqueness, units and derived budget arithmetic, eight-section/report consistency, and bounded adversarial mutations. They do not establish semantic truth, prove historical validity, assess arbitrary plans, or demonstrate agent performance.

The scheduled-arrival consistency checks bind all six numerical rules to their source JSON pointers, structured oracle, report table and prose. They reject changed latency/rate limits, achieved-rate bounds, forbidden-error allowances and capacity floors, as well as wrong operators, units, pointers, missing/duplicate rows and source-only changes; harmless table spacing and row order remain accepted. The full reviewed example text is additionally sealed by a normalized SHA-256 recorded in the authoring oracle, accepting whitespace and binding-row order/spacing controls but refusing unreviewed prose or extra tables. Intentional wording changes require independent review and an explicit fingerprint refresh; the digest proves text identity, not semantic truth. These are fixed-fixture integrity checks, not a generic report evaluator.

From repository root:

```sh
uv run --no-project --with-requirements requirements-ci.txt python -m unittest discover -s tests -p test_experiment_design_proposal.py -v
```

No benchmark/client/model is run by these integrity tests. The packet contains no original raw campaign reconstruction or fabricated execution receipt.
