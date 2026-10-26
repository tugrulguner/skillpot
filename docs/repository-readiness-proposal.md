# Current workflow: repository readiness

Status: experimental skill source with an accepted
[bounded repaired-version audit task](../evaluations/repository-readiness/repaired-smoke/README.md).
The original failed attempts and baseline remain
[recorded](../evaluations/repository-readiness/initial-smoke/README.md), not relabeled.
No qualified release, supported-host badge or usefulness advantage is established.
The earlier project-to-demo direction is superseded; video work is out of scope.

## User and outcome

A maintainer or contributor needs to know whether a repository is ready for a named
consumer task before approving a handoff, installation or release. The agent should
answer that concrete question with source citations, executed command evidence,
blockers and the smallest next actions—not just say the code looks good.

Implementation: [repository-readiness](../skills/repository-readiness/SKILL.md) and its
[report template](../skills/repository-readiness/assets/report.md). This is an original
procedure with no copied private skills, product-specific API guide or custom agent runtime.
Git and the target's documented tools do the work; the skill guides evidence collection
and a bounded decision. A bundled standard-library helper records command results
directly and refuses evidence destinations inside the target; it is not a sandbox.
No custom agent execution, media, packaging or installation engine.

## Real first task and verification

The [frozen task](../examples/repository-readiness/task.md) asks whether a new user can
install and use a skill from a specified historical public SkillPot revision. That is
an actual repository and delivery question, not a mock application. Its limitations
are explicit: it is a small, in-project source-readiness task with a largely inspectable
answer, not an independent held-out repository or a difficult release qualification.

One fresh agent explicitly reads the candidate entry point and template, then carries
out the task. A separate fresh agent receives the same task and input without the
candidate skill. Both have the same read-only target, permitted checks, time budget
and acceptance rubric. Retain their reports, command outputs, failures, deviations,
skill/task hashes and source revision. One attempt per condition is a smoke, not an
improvement study. Shared host and model variability limit interpretation; ordering
and cache effects are not controlled. Existing system skills may affect both agents.

Check every report against the frozen rubric, source citations and actual command
results; keep deterministic source/command checks separate from model-assisted quality
judgment. If both agents succeed, report that rather than manufacturing a benefit.
Explicit reading is not automatic discovery or native host activation.

## Remaining gates

- Final source/evidence validation at the published head; the repair's source review
  is complete, and the parent checked the added task artifacts separately.
- Another real repository and held-out delivery question.
- Failure/interruption and permission-boundary trials.
- Repeated paired trials and an applicable established repository-audit incumbent.
- Native host installation, discovery, non-trigger behavior and selective removal.
- Human acceptance and an explicit decision on any qualified release.

None of these may be marked complete by frontmatter tests or by a fluent report.
Merging, releasing and external publication remain separate authorization decisions.
