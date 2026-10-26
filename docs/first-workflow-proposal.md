# First workflow proposal: working project → accurate demo

Status: superseded experiment, retained as history. Video tooling is not the active
SkillPot implementation target. See the current
[repository-readiness proposal](repository-readiness-proposal.md). The text below
records the earlier design, not current instructions or a released skill.

## User and task

A builder has a functioning browser application and wants a short demo that shows
one reproducible user journey. Today they combine an agent, browser capture,
FFmpeg or an existing compositor, and manual factual/visual review. The workflow
should make that combination repeatable, not replace its tools.

The first implementation should target **one browser application, one local agent
host, one capture adapter, and one landscape MP4**. Terminal capture, native desktop
capture, vertical recuts, narration, website delivery, and social posting are out
of scope. Proposed host: Hermes; compatibility remains untested until the complete
clean-install and task path is exercised. Do not infer compatibility with other hosts.

## Representative task inputs

Use repository-owned, public fixtures, never a private working project as the only
reproduction case. The following are specifications to implement, not fixtures
that already exist:

1. **Primary case — small record transformer.** A local browser application accepts
   two rows with the same identifier, groups them, and shows one record containing
   two items. Begin empty, enter both rows, run the transformation, and hold the
   actual result. The brief must distinguish fixture behavior from a SkillPot feature.
2. **Held-out case — unit conversion.** A separately implemented local browser
   application accepts a value and unit selection and produces a checked result.
   Freeze its task brief before tuning against the primary case.
3. **Failure cases.** Unreachable application, missing capture dependency, capture
   interruption, stale source revision, sensitive input, and output path already
   containing an earlier take. No success package may be emitted for a failed run.
4. **Non-trigger case.** A request to summarize documentation without producing media
   must not launch capture or rendering.

Each input brief includes project revision, setup and readiness commands, public UI
journey, audience, permitted claims and data, output path, target duration, dimensions,
audio policy, approved tools, and budget. Missing authority to publish never blocks
local production; missing authority to access inputs does.

## Toolchain boundary and current prerequisite

Reuse a reviewed existing browser recorder and compositor. The maintainer's existing
video kit is an audit candidate, not a public dependency: its current source is not
available in this repository, and redistribution and clean-environment setup are not
yet established. Do not put a personal path into the public skill or implement a
parallel video engine to work around that gap.

Before implementation, choose a public, license-reviewed capture/render path and pin
its version. The local kit README was recovered from a cloud placeholder during this
audit; it documents Node.js, Python 3.11+, Playwright, Pillow, FFmpeg/ffprobe and separate
capture/render commands. Its capture/render source and tests have not been audited in
this change, and there is no public redistribution path established here. If extracting
the existing kit, read and review its actual source,
verify ownership/license, remove private recipes and paths, add clean setup instructions,
and run its tests plus real capture/render. Otherwise make an explicit toolchain
selection with the maintainer. Compare a relevant existing HyperFrames or Remotion
workflow if applicable; neither is currently selected or tested.

## Deliverable contract

One newly created run directory contains:

- `brief.md`: inputs, source revision, audience, scope, permissions, and tool versions.
- `capture-plan.md`: ordered UI actions, expected visible states, and allowed claims.
- `raw/`: original recording, capture manifest, and real input/output evidence.
- `demo.mp4`: proposed initial target H.264, yuv420p, 1280×720, 30 fps, 30–40 seconds;
  silent unless the brief explicitly selects audio. Confirm this profile in the first
  implementation rather than presenting it as a compatibility result.
- `captions.vtt` and `transcript.md`: timed explanation of actual actions and outcomes.
- `evidence.json`: claims mapped to source revision, executed checks, capture markers,
  and final encoded time ranges. Label editorial overlays and fixture data explicitly.
- `verification.json`: actual probe/decode commands, results, visual-review decisions,
  file hashes, and known limitations. Never manufacture a passing report.
- `reproduce.md`: exact setup, capture, render, verification, and cleanup commands.

Preserve prior runs. Never overwrite originals or silently reuse footage from another
revision. A blocked run may retain diagnostic files, but must state its failure and
must not label an incomplete video as a finished delivery.

## Acceptance checks

- [ ] A clean environment can install only this skill, inspect all resources, and remove
      it without deleting user-authored work. Record exact files written and host version.
- [ ] A real agent activates on the demo request and does not activate on the non-trigger.
- [ ] Both representative applications run through setup, readiness, real UI capture,
      render, review, and delivery without undisclosed private dependencies.
- [ ] The video begins on a ready, empty application; shows actual input, action, and
      output in causal order; and holds the result long enough to read.
- [ ] Probe verifies codec, pixel format, duration, dimensions, frame rate, and audio
      policy; a full decode completes without errors.
- [ ] Review frame zero, each action/result transition, and final frame from the encoded
      video at intended playback size. Fix clipped text, missing clicks, timing errors,
      unreadable output, and misleading overlays before delivery.
- [ ] Every claim has evidence; edited playback speed is never presented as measured
      latency. Captions and transcript match the final edit, not an earlier capture.
- [ ] Failure fixtures produce an explicit blocked result and preserve originals;
      interruption cleanup stops only processes created by the workflow.
- [ ] No source, screenshot, caption, metadata, or log contains credentials, private
      records, local personal paths, or unrelated browser/desktop content.
- [ ] No upload, publication, paid-service call, merge, or deployment occurs without
      separate explicit authorization. Local production uses no paid service by default.

## Evaluation before publication

Use the [evaluation record](../templates/task-evaluation.md). Freeze task inputs and
rubric before tuning. Run at least three matched trials per representative task with
and without the skill, using the same model/harness, tools, permissions, and budget.
Report every attempt, including setup failures and interventions. Keep the held-out
case separate and include the strongest applicable incumbent workflow under equivalent
conditions. This trial minimum is an initial protocol, not statistical proof.

Deterministic checks cover media integrity, required files, reproducibility, source
identity, and forbidden actions. Human review covers clarity, readability, causal flow,
and factual accuracy using the same rubric across conditions. Report time and cost
without implying improvement from one successful example. Publish an experimental
skill only with honest status; do not call it a released, useful workflow until the
roadmap's evaluation and distribution gates are met.

## Implementation sequence

1. Resolve capture/render source availability, license, canonical home, and public setup.
2. Add one experimental skill following the [skill contract](skill-contract.md), with
   the primary fixture and deterministic checks. Keep public release wording unchanged.
3. Exercise real capture/render and failure recovery, then run the frozen held-out case.
4. Run matched evaluations and clean install/update/removal; publish actual evidence.
5. Only then propose release and additional project types or hosts.
