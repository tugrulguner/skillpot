# Skill authoring contract

Status: initial authoring contract. No skill, host compatibility, or installer is
implemented by this document. Follow the [Agent Skills specification](https://agentskills.io/specification)
for the portable entry point; host extensions must not become required portable metadata.

## Canonical layout

```text
skills/<name>/
  SKILL.md
  references/       # optional, directly linked from SKILL.md
  scripts/          # optional, dependencies and side effects documented
  assets/           # optional templates/static resources
  provenance.md
  compatibility.md
examples/<name>/    # runnable public tasks, setup, fixtures, expected checks
evaluations/        # see below; no generated results required merely to author
```

Evaluation records live at repository-root `evaluations/<name>/<run-id>/`, not inside
an unrelated installed skill. The layout is proposed for future implementation;
these directories are not yet a catalogue. Install only the selected skill directory.
Keep runnable task examples in the repository and link exact public revisions from
skill documentation; installed operation must not depend on invisible local files.

## Entry point

Start with YAML frontmatter containing `name` and `description`. The name matches
its directory, is at most 64 characters, uses lowercase ASCII letters, digits and
single hyphens, and has no leading/trailing hyphen. Description states the task and
trigger; SkillPot targets a concise first sentence readable in a truncated catalogue.
Use `license: MIT` only when provenance permits it. Optional `compatibility` describes
actual requirements, not untested host support. Custom `metadata` values are strings,
for example `version: "0.1.0"` and `maintainer: "tugrulguner"`.

Do not copy nested host-specific metadata from private skills into portable frontmatter.
Do not treat `allowed-tools` or skill instructions as an enforced security boundary.

The body includes:

1. Positive triggers and counter-triggers.
2. Required inputs, tools/versions, setup, readiness checks, costs, and permissions.
3. A causal procedure with checkable outcomes; use the host's available file/browser/
   command tools without depending on one host's private tool names.
4. Failure handling, interruption cleanup, retry/overwrite rules, and stop conditions.
5. Artifact verification and a precise completion report, including limitations.
6. Direct relative links to supporting resources; keep large references out of the entry point.

## Provenance and maintenance

`provenance.md` identifies each incorporated source by public URL and immutable revision
where available, its license and notices, what was adapted, and the maintenance owner.
Record canonical ownership: retain product commands upstream rather than duplicating
entire product guides. Private material or unclear rights means hold, not an assumed
license. An audit inventory is not permission to redistribute its sources.

`compatibility.md` distinguishes proposed, structurally validated, manually exercised,
and complete-task-tested environments. Record actual OS, agent/model/harness version,
tool versions, setup path, revision, limitations, and evidence location. A Markdown
parser, format validator, or successful media probe cannot establish agent activation
or task usefulness. No supported-host badge without complete-task evidence.

## Verification gates

- Validate frontmatter and relative resources against the open specification.
- Test scripts, failure modes, examples, clean setup, and exact output artifacts.
- Check portable source for secrets, private paths, and undeclared external dependencies.
- Evaluate activation, non-trigger tasks, output quality, and repeated matched trials
  with the [task record](../templates/task-evaluation.md).
- Exercise selective installation, update with user edits, and removal using the
  chosen host's documented mechanism; do not invent a custom installer as scaffolding.
- State experimental/released status explicitly. Documentation-only work cannot check
  off an execution or evaluation gate.

The initial docs-only verification command is `python3 scripts/check_docs.py`; it
checks local Markdown destinations and source hygiene, not skills, media, or agent behavior.
