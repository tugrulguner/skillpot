# SkillPot roadmap

SkillPot is a library of practical, installable agent skills for building, researching,
and presenting real work. Its reach is not limited to the ModePot ecosystem.

This is an outcome-gated roadmap, not a release schedule. Unchecked items are planned;
headings and proposed names do not indicate shipped functionality. Implementation is
limited to the milestone explicitly taken on for a change.

## Milestone 0 — Establish the project

- [x] Define the audience, intended outputs, and project boundaries.
- [x] Select repository readiness as the current experimental implementation target.
- [x] Publish the README, roadmap, and contribution guidance.
- [x] Create editable ModePot-family artwork and its README renderings.
- [x] Publish a scoped implementation proposal with representative task inputs:
      [repository → readiness report](docs/repository-readiness-proposal.md).

**Exit gate:** The repository explains what SkillPot is, what exists, what is planned,
and how a contributor can help without implying that skills are already released.

## Milestone 1 — Audit reusable knowledge and define the contract

Start with existing project skills and real workflows. Do not import a private skill
collection wholesale or assume that old instructions still match a current project.

- [x] Inventory candidate skills, canonical sources, owners, and licenses in a
      [bounded seven-repository audit](docs/source-audit.md).
- [x] Classify each inventoried candidate; retain the product-specific sources upstream.
      The current skill is original; no private procedure or tooling is extracted.
- [ ] Check commands, APIs, prerequisites, and failure paths against current behavior.
- [ ] Remove personal paths, secrets, private context, and machine-specific assumptions.
- [ ] Establish a single canonical source for each maintained skill; avoid drifting copies.
- [x] Define the skill layout using the open Agent Skills format in the
      [initial authoring contract](docs/skill-contract.md).
- [x] Define metadata for tested environments, dependencies, permissions, provenance,
      known limits, and maintenance ownership in that contract.
- [x] Define a [task-evaluation record](templates/task-evaluation.md): input, acceptance
      checks, baseline, model/harness versions, tool versions, trials, time, costs,
      results, and failure notes. Initial execution smokes are not qualification studies.

**Exit gate:** Every retained candidate has traceable provenance and a concrete task.
One public skill can be authored without depending on undisclosed local knowledge.

## Milestone 2 — Build the first complete workflow

### Repository → readiness report

The experimental skill guides an agent through a concrete delivery question: pin the
source, trace the consumer path, inspect and run authorized checks, and produce a
cited report with actual command results, blockers and minimal next steps.

- [x] Author the original portable skill and reusable report template.
- [x] Freeze a real public-repository task and acceptance rubric before its trial.
- [ ] Observe an agent explicitly load the skill and complete that task; retain results.
- [ ] Verify source citations, actual command outputs and target preservation.
- [ ] Exercise missing prerequisites, unavailable checks and interrupted execution.
- [ ] Test another representative repository and a held-out goal.
- [ ] Verify host installation, discovery, selective removal and non-trigger behavior.
- [ ] Establish usefulness through repeated matched trials and an applicable incumbent.

**Exit gate:** An agent can use the skill to answer a real delivery question with
reproducible evidence. Packaging checks or a single successful trial do not establish
general usefulness, host compatibility or readiness for a qualified release.

**Not in this milestone:** video work, a new execution framework, automatic fixes,
publication, releases or merges. The earlier demo proposal is retained as history.

## Milestone 3 — Establish usefulness and compatibility

A successful example is not enough to claim that the skill improves agent performance.

- [ ] Define representative tasks before tuning the skill against them; reserve held-out cases.
- [ ] Run repeated paired trials with and without the skill using the same model,
      harness, tools, inputs, permissions, and budget.
- [ ] Compare the strongest applicable existing repository-audit or delivery workflow.
- [ ] Check skill activation as well as output quality; include tasks where it should not trigger.
- [ ] Use deterministic artifact checks where possible and an explicit review rubric
      for qualities requiring human judgment.
- [ ] Record setup burden, task success, intervention, elapsed time, and token/service costs.
- [ ] Test permission boundaries, sensitive-data handling, and recovery from failures.
- [ ] Publish results, relevant traces/artifacts with consent, and negative findings.
- [ ] Ask people outside ModePot to complete tasks and return for a second use.
- [ ] Add another agent host only after installation, activation, and execution are tested.

**Exit gate:** The skill demonstrates a worthwhile improvement on the defined tasks,
with reproducible evidence and an explicit compatibility matrix. If it does not,
revise or retire it rather than publishing a quality claim.

## Milestone 4 — Publish a selectively installable library

- [ ] Publish only skills that meet the task, provenance, and maintenance gates.
- [ ] Verify clean installation and removal through established distribution mechanisms.
- [ ] Document exactly where files are written and how updates affect user edits.
- [ ] Confirm that installing one skill does not silently install an unrelated bundle.
- [ ] Publish exact commands and link to task-first usage examples.
- [ ] Automate packaging, relative-link, script, fixture, and regression checks.
- [ ] Establish versioning and a compatibility/freshness review process.
- [ ] Distribute through relevant existing directories and agent/plugin surfaces.
- [ ] Consider a project website only once there is a usable collection to explain.

**Exit gate:** A new user can discover, inspect, install, run, update, and remove a
specific skill using documented, verified paths. No custom account or runtime is
required merely to obtain the instructions.

## Later candidates — Earn the next collection

These are opportunities to investigate, not committed features or release promises.

| Candidate | Intended artifact | Question to answer first |
| --- | --- | --- |
| Research → interactive explanation | Sourced explanation and runnable visual | Can evidence and scientific accuracy survive the full pipeline? |
| Messy data → decision brief | Reproducible analysis, charts, and assumptions | Which repeated task is materially better than existing data/document skills? |
| Engineering delivery | Verified changes and review evidence | What does the workflow improve beyond established engineering collections? |
| ModePot integrations | Current, task-specific product guidance | Where should the canonical skill live to avoid duplicated maintenance? |

Expand only when a candidate has a real audience, a named alternative, measurable
acceptance criteria, redistribution rights, and someone responsible for maintenance.
Broad usefulness does not mean installing every collection by default.

## Non-goals

- A new agent runtime, model, or skill format.
- A marketplace, registry, package manager, or custom installer as the initial product.
- Replacing MCP, CLI tools, existing renderers, or the host agent's permission system.
- Bulk-generated expertise, copied third-party skill packs, or catalogue-size targets.
- Compatibility inferred from format support alone.
- Guaranteed safety, universal task improvement, or benchmark claims without evidence.

## Proposing work

Open a [GitHub issue](https://github.com/tugrulguner/skillpot/issues) with the task,
representative input, expected artifact, current alternative, acceptance checks, and
required tools or permissions. Discuss substantial scope before implementation.
See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution boundary.
