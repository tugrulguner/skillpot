# Investigation: item-2 candidate/control slowdown signal

## 1. Symptom, scope and decision

**Question.** What might explain the observed lower successful goodput and higher closed-loop tail latency for the candidate in `item-2`, and what is the smallest useful next discriminator before optimization?

**Observed symptom.** The supplied summary records a 30-second, 16-connection, Linux ARM64 Docker-loopback, free-threaded (`ft`) capacity-screen pair on the `item` profile. Candidate goodput is below control and its recorded p99 is higher. This is one pair, not evidence of a repeatable regression. The values below are retained summary values, not recomputed from missing raw streams.

| Cell | Order in retained plan | Good requests | Duration (µs) | Recorded goodput (req/s) | p50 (µs) | p95 (µs) | p99 (µs) | Timeout errors | Validity |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| item-2-candidate | first | 2,607,747 | 30,100,399 | 86,634.965 | 151 | 382 | 891 | 0 | recorded valid |
| item-2-control | second | 2,683,339 | 30,001,020 | 89,441.592 | 149 | 341 | 687 | 0 | recorded valid |

**Recomputed comparison.** Goodput is `good_requests / (duration_us / 1,000,000)`. From the displayed raw summary counts and durations: candidate = 2,607,747 / 30.100399 ≈ 86,634.965 req/s; control = 2,683,339 / 30.001020 ≈ 89,441.592 req/s. Candidate/control = 86,634.965 / 89,441.592 ≈ **0.968621**. The retained p99 ratio is 891 / 687 ≈ **1.296943**. These are descriptive ratios for this one pair; neither establishes repeatability or cause. Do not subtract percentiles to infer time spent in a component.

**Decision boundary.** Explain what is and is not supported and select a low-cost next discriminator. Exclude broad capacity or scheduled-arrival claims, universal causality, tuning, repair, deployment, and merge. Budget for this retrospective: inspect the supplied packet once; no diagnostic execution. A future run needs separate bounded authority.

## 2. Evidence and execution identity

The packet's `provenance.json` identifies three exact public snapshots: `sources/linux-screen.json` from upstream `benchmarks/scalar_response/linux-screen.json` at source commit `798c449fd1337404c388abb2a177c0302ba35fc0`; `sources/candidate-scalar-response.py.txt` from `src/dexpot/_scalar_response.py` at candidate source commit `92e8561aa96f7e799279b89c9c9453834f9e0cda`; and `sources/DEXPOT-LICENSE` from the upstream repository. Provenance reports these files as unchanged public snapshots and records MIT license parity. The source-text file is inert text and was not executed.

The summary declares control source commit `e703edf18d1526ebc2a91398f18c9e808e5cf5aa` and candidate source commit `92e8561aa96f7e799279b89c9c9453834f9e0cda`. It separately records control wheel SHA-256 `8b9ed82c9f70d92594190ccde530fa20f7c1a817feb8e01814af92714f3ad12d` and candidate wheel SHA-256 `fb39bd08e614e9f65adb30c6f0b6d758d658c15b9a5de0d8e86d5cb57bf9ad17`. Each item-2 trial repeats its side's wheel and Python-source hash, and lifecycle events record compiled-scalar activation. These are distinct identity/activation claims: a commit, wheel digest, Python-source digest, and runtime flag are not interchangeable. They are recorded declarations; this packet does not include wheel bytes or independently reproduce these checks.

The summary records a Linux 6.10.14 LinuxKit aarch64 container, Python 3.14.7 free-threading build, `gil_enabled: false` at startup and after workload for both item-2 processes, `bounded-ft` execution, pool size 22, max queue 44, connection limit 1024, and the same `msgspec`/`dexpot` versions. It records compiled-scalar false for control and true for candidate at both endpoints. These lifecycle flags are observations at recorded endpoints, not continuous tracing.

**Absent evidence.** Per-trial client streams, latency histograms, wheel bytes, and other original raw artifacts are not supplied. The packet provenance characterizes recorded validity and identity as attributed, not independently reproduced. The eight summary rows and their raw-record SHA-256 receipts are present, but a receipt is not the underlying stream. No private paths or repository history are required or used.

## 3. Comparison validity and observations

### Retained cells

The plan and evaluation record eight expected and eight collected trials; no planned cell is missing. Preserve all cells and their outcomes:

| Cell | Phase/profile | Side | Goodput (req/s) | p99 (µs) | Transport/validity note |
|---|---|---|---:|---:|---|
| smoke-control | 1 s smoke / item | control | 62,073.798 | 13,825 | valid; zero timeout errors |
| smoke-candidate | 1 s smoke / item | candidate | 72,488.450 | 1,772 | valid; zero timeout errors |
| item-1-control | 30 s screen / item | control | 74,029.028 | 3,033 | recorded valid |
| item-1-candidate | 30 s screen / item | candidate | 79,730.016 | 1,168 | **invalid**; six timeout errors |
| item-2-candidate | 30 s screen / item | candidate | 86,634.965 | 891 | recorded valid; zero timeout errors |
| item-2-control | 30 s screen / item | control | 89,441.592 | 687 | recorded valid; zero timeout errors |
| fallback-control | 30 s screen / large_nested | control | 6,681.706 | 7,450 | **invalid**; two timeout errors |
| fallback-candidate | 30 s screen / large_nested | candidate | 6,742.776 | 5,923 | recorded valid; zero timeout errors |

The evaluation marks item-2 complete, comparison-valid, both resource-pass, with candidate/control goodput ratio 0.9686205521773416 and p99 ratio 1.296943231441048. The six-timeout item-1 candidate and two-timeout fallback control are retained, not repaired or pooled. Item-1 and fallback pair-level comparison values are null/invalid. All resource checks are marked pass, but that does not cure transport-invalid records. The summary says the overall screen failed; its gate requires both flat pairs to exceed 1.0 goodput ratio, flat median at least 1.05, and the applicable tail limits. No full qualification passed.

### Measurement boundary and scope

The screen is closed-loop capacity at 16 connections, not scheduled arrivals. Its p99 values are not scheduled-load latency and cannot establish behavior at the original 10,000 offered requests/s gate. Goodput is successful requests per observed timed duration; it is not offered rate, latent capacity, or a universal workload result. The reported histogram percentiles cannot be differenced to infer time in projection, dispatch, queueing, or any other subpath.

For item-2, recorded server CPU time is 168.28 s candidate and 175.9 s control, sampled over the stable descendant tree within the timed client window and excluding startup/drain. Recorded sampled peak RSS is 53,899,264 and 48,705,536 bytes respectively; both resource checks pass their recorded budgets. CPU time is not a direct per-request attribution and these limited samples do not identify or exclude a bottleneck. Sampling is recorded at approximately 0.2-second intervals; no continuous trace or per-request spans are provided.

### Source-only path map

The inert candidate source text (`candidate-scalar-response.py.txt`, lines 12–108) depicts eligibility guards, primitive field selection, generated field access and response-dictionary creation, followed by a thread-local function binding. This is a source inspection only: it does not establish which operations dominated this workload, how much time they cost, or that the displayed source was the exact code executed. The summary records endpoint activation and source/wheel digests, but the underlying artifacts are absent. No control implementation source is in this packet, so comparison of source paths is incomplete.

## 4. Competing explanations

| ID | Mechanism and support | Counterevidence / limits | Predicted discriminator | Actual outcome | Disposition |
|---|---|---|---|---|---|
| H1 | Candidate projection-path cost: inspected source lines 12–108 show guards, generated field access and thread-local binding; summary `/trials/4` records activation and worse item-2 metrics. | No profile or independent executed-artifact binding. Candidate direction differs in smoke and transport-invalid item-1; these cannot supply clean repeat evidence. | If an artifact effect persists across controlled order/repeats, a verified path-specific contrast or matched mechanism ablation should distinguish projection work from other artifact differences. Preserve semantics and healthy controls. | Source inspected; no path-specific timing, ablation or new comparison performed. | UNRESOLVED |
| H2 | Run/order/environment variation: `/plan/cells/4` and `/plan/cells/5` list candidate then control; only one valid screen pair survives. | `/trials/4` and `/trials/5` record common setup and passing resource/identity flags, but lack detailed temporal contention or thermal records. Plan order is recorded order, not independently observed timing. | Interleaved/randomized matched repeats with environment records: an effect following run position rather than artifact supports this explanation; a persistent artifact effect argues against it as the sole cause. | No order-balanced repeated discriminator performed. | UNRESOLVED |
| H3 | Observer/extraction/summary effects: original streams and histograms are absent; `/trials/4/server_resources` and `/trials/5/server_resources` describe periodic sampling. | Both rows record zero errors, accuracy pass and common planned workload; these are attributed checks, not replayed pipeline validation. | Recompute recovered original streams using one parser and denominator. If the contrast survives, an observer-off matched control can test observer overhead; no change would narrow that explanation within its tested scope. | Only summary arithmetic performed; original-stream reanalysis and observer-off contrast unavailable/unrun. | UNRESOLVED |
| H4 | Specific hypothesis that candidate's recorded endpoints had GIL enabled. A runtime-mode difference could affect performance. | `/trials/4/lifecycle/events/0/gil_enabled` and `/trials/4/lifecycle/events/1/gil_enabled` are false, as are control `/trials/5` endpoint values. | A true value would support endpoint enablement. Continuous in-window evidence would address the separate unobserved interval only if that concern became material. | Recorded startup and after_workload endpoints contradict this endpoint hypothesis; continuous state remains unverified. | CONTRADICTED_AT_RECORDED_ENDPOINTS |

The “valid” flags and activation fields remain attributed summary assertions, not an independent replay. H1–H3 can coexist; observed candidate/control difference alone does not select among them.

## 5. Checks performed and proposed

### Performed

- Read the exact supplied public JSON summary, inert candidate source text, license, provenance manifest, and proposal contract. No embedded code was executed.
- Recomputed item-2 goodput from successful-request counts divided by each recorded duration in seconds; ratio 0.968621. Recomputed the descriptive p99 ratio from the two supplied p99 summary values; ratio 1.296943.
- Retained and reviewed all eight planned/collected cells; preserved invalid timeout rows. No new benchmark, profiler, server/client, dependency, or network call was run.

### Proposed, not performed

1. **First, retrieve original retained item-2 records if an owner can provide them under explicit bounded scope.** Recompute both trials from the same original client streams/histograms and verify parser, timeout treatment, units, and artifact mapping. This is the cheapest discriminator for H3 and may determine whether the symptom itself is robust. The current packet does not contain those artifacts; retrieval is a prerequisite, not an assumed capability.
2. **If the contrast survives and the owner authorizes a new diagnostic, repeat matched candidate/control item trials in randomized/interleaved order with a healthy control.** Predeclare pair-level outcomes, required artifact/runtime/workload identity and resource/error stop bounds; keep timing and observer configuration comparable and record environment state. This is the smallest useful contrast for H1 versus H2. A small number of repeats is diagnostic, not a qualification sample or proof of universal behavior.
3. **Only if repeated difference persists, add targeted low-overhead instrumentation or observer-off comparison.** Instrument the mapped projection/response path with a healthy control, retaining measurement-overhead comparison; decide this after confirming the effect and granting profiling authority. Do not infer path cost from the source listing or sampled CPU totals.

All proposed work requires an owner to grant explicit time/resource limits and evidence/output scope. No check in this section was executed; no favorable outcome is assumed.

## 6. Diagnosis and limits

**Diagnosis: the cause is unresolved.** The retained item-2 summary records a candidate/control goodput ratio of about 0.9686 and p99 ratio about 1.2969 in this one closed-loop pair. That is a narrow observed difference, not a demonstrated repeatable regression or causal explanation. H1 (candidate path cost), H2 (run-order/environment variation), and H3 (measurement/observer effects) remain unresolved. H4's specific endpoint-enabled-GIL claim is contradicted by recorded startup and after-workload values, but continuous in-window runtime state is not established.

The overall screen failed, and invalid timeout trials remain part of that result. The evidence does not establish scheduled-load latency, original full-gate performance, full-system capacity, an isolated hot function, or general candidate performance. Missing original client records/histograms and wheel bytes prevent independent recomputation and artifact verification. No confidence interval, causal estimate, or repeatability claim is warranted. A repeated healthy-control contrast, raw-record reanalysis, or verified identity mismatch could change this conclusion.

## 7. Prioritized handoff

1. **Decidable now:** one valid recorded item-2 pair has a descriptive disadvantage for candidate; the screen as a whole failed; this record does not say why. The timeout-invalid item-1 candidate and fallback control must remain visible. Optimization, merge, deployment, qualification, and a broad speed claim are outside scope and not authorized.
2. **True prerequisite:** ask the evidence owner whether the original item-2 streams/histograms can be supplied within a defined input-only boundary. If yes, make that read-only recomputation the first cheap step; if no, record the gap and stop rather than reconstructing records.
3. **Smallest fresh discriminator, only after authorization:** if source records support the contrast, run a bounded, healthy-control, randomized/interleaved matched item pair set with verified source/artifact/runtime identities and predeclared stop conditions. Compare whether the effect follows artifact or run order. This still diagnoses a local screen and is not full qualification.
4. **Optimization remains unapproved:** only after a repeatable contrast and more specific path evidence should the owner decide whether a separately authorized profiler or targeted intervention is worth considering. No patch or optimization is proposed by this report.

**Required authority still missing:** permission to retrieve any absent retained artifact, and (only if needed afterward) permission for bounded new runs/instrumentation specifying host/environment, time/resource limits, healthy controls, allowed inputs, and destination for a fresh report. No further action is needed without those decisions.
