# Verification loop: first use

This workflow was not included in published SkillPot v0.4.1. It is included in v0.5.0. Earlier distribution records keep their original pins; the selected release contains byte-identical bundles. Bundle metadata and compatibility/provenance notices retain their construction-time publication labels; collection publication status here and in the Release is authoritative.

`verification-loop` is an original portable workflow for running a bounded verification loop against user-visible criteria. It can also prepare an inspection-only plan or, when requested, qualify a reusable project recipe. It is **included in published v0.5.0**. Conceptually inspired by Addy Osmani's [verification article](https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/), independently authored and not an official Anthropic skill.

## Install only this bundle

With Node.js 22.20+ and Git, run in your owned project:

```sh
npx skills@1.7.6 add https://github.com/tugrulguner/skillpot/tree/044213fd00343e94b4d389c3ca2c0f2909feb79f --skill verification-loop
```

Choose a host, optionally adding `--agent claude-code`, `--agent cursor`, `--agent codex` or `--agent hermes-agent`. Installation is project-local unless deliberately global. Inspect existing destinations before confirmation: installer updates may overwrite edits. This differs from the procedure's fresh-report collision guard. The complete bundle has linked report, checklist, input-only practice, project recipe and rule-candidate assets; it installs no target, answer oracle or runner. Source/placement checks do not prove native loading or better task outcomes.

## Bounded authorized verification

Provide the named local project and base/candidate change, criteria, allowed paths and a fresh external evidence directory with an existing owned parent. Then use this prompt, adjusting the explicit limits to your task:

> Use verification-loop to verify this change against the acceptance criteria I supply. I authorize inspecting the named project's source/diff and documented verification instructions, and executing its already-installed local checks/application within this project scope. Discover and inspect the appropriate commands; I do not need to supply each one. Reuse an existing project verification recipe where available. Read at most 100,000 characters, use at most 20 commands, 30 seconds per command and 10 minutes total. Create verification.md and direct receipts only in the fresh external directory I name; refuse existing paths and symlinks, including redirecting ancestors. Local application execution may use loopback only; no external network, dependencies, credentials, paid services or agent clients. Do not repair code, edit policy, install hooks, commit, publish or merge. Execute the cheapest suitable checks first, then the actual user flow. Where relevant, generate bounded invariant inputs and compare against a trusted baseline with declared normalization. Preserve first failures, seeds/counterexamples and actual source/input/check hashes. Stop and ask only for authority outside this scope or a decision that changes the checks, not to repeat existing authorization. Report verified failures separately from setup/timeout/flakiness, and never mark required unrun/stale checks as passing. Clean up only owned services and state whether anything remains running.

This grants execution of inspected commands within the named boundary, not blind execution of repository instructions. A command that installs dependencies or contacts an external service remains out of scope even if documented. A task requiring more time must request a revised budget. Repairs remain opt-in, at most three rounds or the smaller approved limit, without weakening checks.

## Bounded inspection-first task

When execution is not authorized, use the narrower mode:

> Use verification-loop to inspect only the named change and supplied criteria, within 100,000 characters. Do not import or execute target code or checks, install dependencies, start services or repair files. Use my approved fresh external report directory, refusing collisions/symlinks and preserving partial work. Create verification.md mapping criteria to independent expected observations, existing documented commands and protected versus candidate-authored oracles. Mark all unexecuted checks NOT RUN and unresolved criteria unknown. This is a plan, not completed verification. No credentials, publication, merge or fallback output.

The [input-only practice task](../skills/verification-loop/assets/example-input.md) supplies a fictional scenario, not a target or execution authority.

## Optional project recipe setup

Request this mode when the project lacks adequate repeatable verification. Existing recipes should be reused rather than duplicated:

> Use verification-loop in project recipe setup mode for the named local project and user flow. Inspect existing verification instructions first, then propose the smallest recipe covering actual startup/readiness, assertions, evidence, bounded command/repeat invocation and cleanup. I authorize writing a new project-verification-recipe.md only inside the fresh external report directory I supply, alongside verification.md and evidence/. I authorize offline execution of already-installed local tooling and an isolated authored healthy/seeded-fault control in that same fresh owned directory: at most 20 commands, 30 seconds each and 10 minutes total, no network, dependencies or services beyond explicitly approved loopback. Retain genuine control receipts, recipe/input/source hashes, observed duration and failure reason. Do not inject faults into the original target or write project files, policy or hooks. Mark unavailable controls NOT RUN rather than claiming the recipe qualified. Propose any target destination and request its exact write permission separately. Preserve existing and partial files; no commits, publication or merge.

A qualified recipe has an independently accepted healthy pass and the intended seeded assertion failure, not just two exit codes. The [recipe template](../skills/verification-loop/assets/project-verification-recipe.md) is harness-neutral; it is not a new runner.

## Turn recurring misses into focused checks

Use the [rule-candidate template](../skills/verification-loop/assets/reliability-rule-candidate.md) to record supporting incidents, an observable diff trigger, scoped check, healthy/non-trigger controls, owner approval and retirement condition. Carry prior-round findings forward; do not add every historical check to every task. Proposed rules remain observation-only until separately approved. Do not adopt automatic gate bypass or delete failing tests merely to obtain green.

## Worked example and limits

The separate [authored worked example](../examples/verification-loop/README.md) runs an offline CLI comparison and bounded seeded generated-input invariant checks, preserving real receipts and counterexamples. Targets and expected controls stay outside the installed bundle. This is teaching-fixture execution, not an observed agent task or model-efficacy study. Inspect sources and the documented permission boundary before executing its exact command with a fresh external output path.

## Inspect, update and remove

Use `npx skills@1.7.6 list` and `npx skills@1.7.6 remove verification-loop`, checking agent and scope. Preserve local edits before updates. Removing instructions does not remove reports or siblings. See the [common setup](quickstart.md).
