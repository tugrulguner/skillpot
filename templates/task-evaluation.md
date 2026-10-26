# Task evaluation record

Template only. Replace placeholders with measured results; unknown is not zero.
Never copy an example success into an actual run record.

## Identity and frozen inputs

- Run ID / date:
- Skill revision and source provenance:
- Task ID / primary or held-out / frozen brief revision:
- Input fixtures and permissions:
- Expected artifact and acceptance rubric (fixed before trial):
- Environment: OS, hardware, agent, model identifier, harness version/configuration:
- Tool and dependency versions / installation commands:
- Allowed tools, permissions, network access, and budget:
- Baseline and strongest applicable incumbent / selection rationale:
- Conditions held constant / unavoidable differences:
- Trial count and execution order / changes since protocol freeze:

## Per-attempt record

Repeat for every attempt in every condition; retain failures and retries.

- Condition: no skill / SkillPot / incumbent
- Attempt ID and random seed if supported:
- Activation expected / actually observed / evidence:
- Commands, source revision, exact inputs, and retained raw trace:
- Output paths and hashes:
- Deterministic checks: command, exit code, observed result:
- Human rubric: reviewer, score per criterion, explanation, blinded status:
- Success / failure / blocked and reason:
- Interventions and retries, including setup repair:
- Elapsed time with defined start/end boundaries:
- Tokens and service cost, currency and price source; unknown if unavailable:
- Sensitive evidence redactions and retained reproducibility:
- Cleanup performed / processes and files left behind:

## Aggregate and limitations

- Counts by condition: attempts, successes, failures, blocked, interventions:
- Per-task results, including held-out and non-trigger cases:
- Time/cost distributions with failures accounted for:
- Differences and uncertainty; do not infer causation from unmatched runs:
- Negative findings and unsupported environments:
- Public evidence locations and publication permission:
- Maintainer decision: revise / retire / experimental / ready for release review:

A successful command, a small trial sample, or a model judging its own output is not
proof of broad usefulness. Separate deterministic evidence, human judgment, and
model-assisted judgment explicitly.
