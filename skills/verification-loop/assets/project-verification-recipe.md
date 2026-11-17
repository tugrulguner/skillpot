# Project verification recipe

Status: PROPOSED / QUALIFIED / BLOCKED. This is a reusable project recipe, not proof that a particular change passed. Owner: __. Version: __.

## Task, authority and discovery
- User-visible behavior covered and explicit exclusions:
- Existing recipe/tooling inspected; reuse choice and demonstrated gap:
- Target/base/healthy-control identity and trusted contract/criterion IDs:
- Approved local execution, output, service and exact recipe/test write paths:
- Actions not allowed (dependencies, network/accounts, repairs, policy/hooks, publication):
- Diff triggers that make these checks relevant; non-trigger exclusions:

## Prerequisites and readiness
- Runtime, dependency versions and source/artifact identity checks:
- Working directory and inspected cheap check commands:
- Actual application start command, owned service identity and readiness signal:
- Startup timeout/failure and cleanup handling:

## Repeatable checks
For each check state criterion, expected observation and independent oracle, actual command or user-flow steps, per-check timeout, evidence files and failure classification. Use actual application entry points for user-facing behavior. Separate cheap per-change checks from heavier pre-commit checks. Do not substitute unit success for an unexercised flow.

- End-to-end flow, steps, response/persisted-state assertions:
- Property invariant, input generator/domain/seed/case budget and counterexample capture, if relevant:
- Trusted differential baseline, shared inputs, frozen normalization and approved differences, if relevant:
- Total command/time/resource budget, stop boundaries and owned-process cleanup:
- Exact repeat invocation with fresh external evidence destination:

## Qualification and maintenance
- Healthy control expected/observed assertions and actual receipt:
- Approved isolated seeded fault, intended assertion and actual receipt (or NOT RUN with reason):
- Before/after source, recipe, fixture/input and check hashes; stale-result handling:
- Observed duration and explicitly authorized repeat count/outcomes; flaky limits:
- Output collision/ancestor-link containment check and cleanup observed:
- Owner-approved status, unresolved gaps, next review/retirement condition:

Never qualify from an unrelated nonzero exit, a typed example log, or merely creating this recipe. No new runner, hook or policy edit is authorized by this template.
