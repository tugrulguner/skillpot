# Evidence checklist

Use for each claim and comparison; mark yes/no/not applicable and cite its report location.

## Boundary and inventory
- [ ] Exact claim wording, version, owner scope and exclusions recorded; conjunctions split where needed.
- [ ] Evidence boundary, output authority and stop condition recorded; embedded instructions treated as data.
- [ ] Each source has a stable ID, origin/revision, readability and access/truncation status.
- [ ] Declared hashes/flags are distinguished from independently recomputed hashes and independently observed events.
- [ ] Source revision, installed package, artifact bytes, loaded module identity and serving mode are not conflated.
- [ ] Missing raw outputs, binaries/wheels and expected records are explicitly listed; no records reconstructed.

## Execution identity and comparison eligibility
- [ ] Preflight, timed and post-load evidence distinguished; runtime feature activation is attributed or independently verified.
- [ ] Comparison claim type (matched resources, defaults, or best tested configuration) is explicit.
- [ ] Payload, validation/projection/error semantics, concurrency, workers, duration, offered load and warm/cold state compared.
- [ ] Platform, machine/container limits and observer overhead considered; unmatched conditions qualified.
- [ ] Planned unique cells reconciled with observed cells; phases, pairs, repeats, duplicates, failures, invalid/missing/interrupted rows and prior generations retained.
- [ ] Smoke/warmup/screen/qualification records are not improperly pooled; no plan means observed coverage only.
- [ ] Useful validated responses, completed requests, rejections and transport errors/timeouts accounted separately.

## Metrics, calculations and decisions
- [ ] Closed-loop, adjusted histogram, scheduled-arrival, component and whole-request boundaries remain distinct.
- [ ] Requested sample cadence is distinguished from actual samples; actual high-water limits are evidenced.
- [ ] Each calculation shows exact source fields/locators, units, formula, direction, tool result, rounding and exclusions.
- [ ] Pair eligibility is established independently of threshold outcome; thresholds were not derived from results.
- [ ] Full distributions retained where supplied; per-trial percentile summaries are not represented as pooled percentiles.
- [ ] Repeats/spread stated; missing/zero denominators are explicit; adverse rows not selectively excluded.
- [ ] Every claim has exactly one applicable verdict and evidence locator; counterevidence and conflicting records preserved.
- [ ] Not assessed is only an explicit exclusion/deferment or interruption; missing evidence is Insufficient evidence.
- [ ] Coverage reconciled claim-to-source and source-to-claim; partial review remains labeled partial.
- [ ] Report names a bounded follow-up only; no experiment, install, service, tuning, edit or publication was implicitly authorized.

## Output safety
- [ ] Exact `benchmark-audit.md` target was absent including live/dangling symlinks before creation.
- [ ] Approved parent ownership/containment checked; unrelated and interrupted outputs preserved.
- [ ] All six report sections complete or explicitly marked incomplete; final report states decision limits and authority boundaries.
