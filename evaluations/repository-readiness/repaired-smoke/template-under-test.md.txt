# Readiness report

## Decision

- Goal and intended consumer:
- Ready / not ready / blocked by missing evidence, specifically for that goal:
- Inspected repository, revision and local changes:
- Environment and scope:

## Required gates and evidence

For each required consumer step:

- Gate:
- Claim being checked:
- Evidence: repository-relative path and line range, or retained command record:
- State: source-only / executed / failed / blocked / unexecuted:
- What the evidence does and does not establish:

## Executed checks

For each attempt, retain the exact command, working directory relative to the target,
tool versions, timeout, exit code, actual output or evidence-file reference, and any
retry. Do not replace raw failures with a successful summary. Unknown is not zero.
Use the bundled recorder's JSON files as the command references, including initial
and final Git status. Do not retype their stdout/stderr or omit an unsuccessful check.

## Blockers and smallest next steps

For each blocker: affected user step, observed gap, evidence, minimal remedy and
verification needed. Keep optional improvements separate. Do not silently implement
or publish the proposed remedy.

## Boundaries and cleanup

- Unexecuted checks, skips and unavailable prerequisites:
- Unsupported or untested environments and limitations:
- Target worktree status before/after:
- Report/evidence files written and owned process cleanup:
- Anything still running:
- Separate authorization needed for changes, merge, installation, release or upload:
