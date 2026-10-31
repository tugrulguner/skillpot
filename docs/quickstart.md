# Start with a task, not a harness

SkillPot is a collection of portable agent instructions. **Claude Code, Cursor, Codex,
Hermes and other Agent Skills hosts are ways to use it—not dependencies of the library.**
A skill is a directory containing `SKILL.md` and its supporting files. Your agent
provides file access, command execution and permission controls; the underlying product
may require its own Python environment, dependencies or credentials.

## 1. Choose one workflow

Start with the [task-first catalogue](../catalog/README.md):

- Intpot CLI or Python: define, inspect, export or convert a trusted application.
- Decision brief (unreleased source only): compare alternatives with a bounded evidence packet; use the [separate pinned first-use steps](#try-decision-brief-from-reviewed-source), not the v0.3.0 checkout.
- Dexpot: build and verify synchronous typed HTTP APIs.
- Summonpot: implement an endpoint with deterministic operations and bounded agent-owned decisions.
- Refpot: exercise the embedded database preview with temporary data.
- Summonpot contributor workflows: prepare or review a change in that project only.

Install only what you need. The separate repository-readiness workflow is an
experimental explicit-load audit, with its own [tested boundaries](../skills/repository-readiness/compatibility.md).

## 2. Inspect and pin the source

In a new source location you own:

```sh
git clone https://github.com/tugrulguner/skillpot.git skillpot-source
git -C skillpot-source checkout --detach b4dabf93e7e4a85a55d947a05eb2989f035a58c1
cd skillpot-source
```

That immutable public revision is the published `v0.3.0` collection and includes the
four refreshed project guides and existing consumer examples. Examples retain their
own historical product pins; they are not new runtime evidence for these guides.
You may choose a newer reviewed published revision, but record its exact commit; do
not silently refresh instructions. Read the chosen `SKILL.md`, provenance, compatibility
and complete license before granting access or running commands.

Copy the **whole chosen skill directory**, not just `SKILL.md`. References, scripts,
assets and permission notices must stay with it. Inspect provenance/compatibility in
the source checkout: their links to collection evaluations are source-review records,
not extra runtime resources to copy into every host. No installer account, registry,
custom runtime or MCP server is required merely to obtain these files.

## 3. Place it where your agent discovers project skills

Officially documented project locations are:

| Host | Project directory | Explicit use |
| --- | --- | --- |
| Claude Code | `.claude/skills/intpot-python/` | `/intpot-python` |
| Cursor | `.cursor/skills/intpot-python/` or `.agents/skills/intpot-python/` | Type `/` and select the skill in Agent chat |
| Codex CLI / IDE | `.agents/skills/intpot-python/` | Mention `$intpot-python` |
| Hermes | Use its existing [selective URL installer](project-skill-installation.md#hermes-direct-url-one-selected-skill) | `/intpot-python` or ask the agent to load it |

These are host-specific discovery locations, **not different versions of the skill**.
Use an approved project directory, and inspect existing files first. For example, in
a POSIX shell, choose one destination and run this from the cloned SkillPot source:

```sh
# Set this to an actual project you own, not the SkillPot source checkout.
PROJECT=/absolute/owned-parent/your-project
# Claude Code example. Cursor can use .cursor/skills; Codex uses .agents/skills.
SKILL_ROOT="$PROJECT/.claude/skills"
(
  set -eu
  mkdir -p "$SKILL_ROOT"
  mkdir "$SKILL_ROOT/intpot-python"
  cp -R skills/intpot-python/. "$SKILL_ROOT/intpot-python/"
)
```

The plain `mkdir` refuses an existing destination, including a same-name symlink;
do not remove it or merge over local edits just to make installation succeed. A failed
copy may leave a partial new directory: inspect it before opening an agent session.
Repeat deliberately for `intpot-cli` if the task needs both skills. No global user
skill store is changed by this project-local example. User/global paths exist in some
hosts, but are not necessary for this quickstart.

### Claude Code

The copied package is already a Claude Code skill; no adapter, plugin, MCP server or
Claude-specific rewrite is needed. The project layout is:

```text
.claude/skills/intpot-python/
├── SKILL.md
├── references/
│   ├── upstream.md
│   └── LICENSE.md
└── ...other files from the selected package
```

Open Claude Code in that project. Type `/intpot-python` to invoke the skill directly,
or describe a matching task and let Claude select it using the skill's `description`.
For example:

```text
/intpot-python Export this trusted invoice App as a standalone CLI using the pinned guide.
```

For availability across projects, Claude Code also documents
`~/.claude/skills/<skill-name>/`; choose that scope deliberately rather than installing
there by default. The same `SKILL.md` and supporting files work in either location.
Keep the portable `name` and `description` frontmatter; Claude-only extensions such as
`context: fork` and dynamic command injection are not required by SkillPot.

### Cursor and Codex

Use the same complete package under `.cursor/skills/<skill-name>/` for Cursor or
`.agents/skills/<skill-name>/` for Codex. Cursor also documents `.agents/skills/` and
compatibility discovery from `.claude/skills/`, so a project shared with Claude Code
need not duplicate the same package merely for Cursor. In Cursor, type `/` and select
the skill; in Codex, mention `$intpot-python` or select it through `/skills`.
Both hosts also document relevance-based selection from the skill description.

Cursor's **From GitHub Repository** plugin import is a different distribution path
that expects a plugin marketplace manifest; do not assume it imports an arbitrary
plain skill repository. Manual project-directory placement above does not require
SkillPot to provide a plugin or marketplace.

## 4. Ask for a real result

Open your harness in the target project and confirm the chosen skill is visible.
Invoke it explicitly first; automatic matching depends on the host and task and is
not guaranteed by the file format. If the host does not support discovery, ask it to
read the chosen `SKILL.md` and its linked resources explicitly—label that as explicit
file loading, not native skill activation.

For example, after selecting the Intpot skill in your agent:

> Use the installed Intpot skill on this trusted invoice tool. Match the documented
> product revision, export a standalone CLI, and run it against the original function
> for default, optional and invalid inputs. Preserve existing files. Ask before any
> missing dependency installation. Report the actual outputs, differences, failures,
> generated artifacts and cleanup; do not treat generation or compilation as execution.

You can also reproduce the [checked consumer examples](../examples/modepot-project-skills/README.md).
They use actual product environments and include CLI, HTTP or database assertions.
Installing instructions does not install Intpot, Dexpot, Summonpot or Refpot.

## 5. Updates and scope

These setup instructions follow each host's published skill contract. Supporting the
documented folder layout and portable format does not require a live model session,
a particular user's login, or a separate implementation for each harness. Local
account state is not a SkillPot installation or support gate.

For updates, inspect a newly pinned source and review the diff. Preserve local edits;
replacement behavior is host-specific. For removal, remove only the instruction bundle
you installed, using the host's documented method or your project's normal reviewed
file workflow. Do not remove product environments, applications or data with it.

Historical [installation](../evaluations/modepot-project-skills/native-install-001/README.md)
and [task observations](../evaluations/harness-portability/explicit-codex-001/README.md)
remain separate records, not prerequisites for using the documented integrations.

## Try decision-brief from reviewed source

`decision-brief` is reviewed but unreleased and is **not included in published v0.3.0**.
The stable instructions above intentionally select that older collection. For this
workflow, use the separate immutable source revision below. These POSIX shell steps
copy instructions and example inputs only; they do not launch an agent, install
product dependencies or execute the proposed storage change.

### Get the exact source

From a new source location you own:

```sh
git clone https://github.com/tugrulguner/skillpot.git skillpot-decision-source &&
git -C skillpot-decision-source checkout --detach 4ca53963cafc8a9a3965808c485dc8c6ad502a66 &&
cd skillpot-decision-source
```

This is the reviewed main snapshot after the status/task-record update, not a new
release. Do not replace the commit with moving `main` or rerun the v0.3.0 checkout
above before copying this skill. Inspect [the procedure](../skills/decision-brief/SKILL.md),
its linked templates, provenance, compatibility and both complete notices first.

### Copy only the selected bundle

Stay in that source checkout. Replace `PROJECT` with a real, existing project you own.
Choose one trusted project-local skill root using your [host's placement](#3-place-it-where-your-agent-discovers-project-skills).
This example selects Claude Code; Cursor can use `.cursor/skills`, and Codex can use
`.agents/skills`. Do not execute all three alternatives or change a global skill store.

```sh
PROJECT=/absolute/owned-parent/your-project
SKILL_ROOT="$PROJECT/.claude/skills"
(
  set -eu
  : "${SKILL_ROOT:?Choose an owned project-local skill root}"
  mkdir -p "$SKILL_ROOT"
  mkdir "$SKILL_ROOT/decision-brief"
  cp -R skills/decision-brief/. "$SKILL_ROOT/decision-brief/"
)
```

The plain `mkdir` refuses an existing selected directory, file or same-name symlink.
Preserve it and inspect local changes rather than deleting or merging over it. Parent
paths must be the trusted locations you selected; this recipe is not a sandbox.
A failed copy can leave a partial new directory, which must be inspected before use.
The complete bundle includes both templates, provenance, compatibility, `LICENSE`
and `LICENSES/github-spec-kit-MIT.txt`. No sibling skill is copied or modified.

Hermes and other hosts can instead explicitly read the selected `SKILL.md` and its
linked resources from this pinned checkout using their existing file tools. That is
explicit loading, not a claim of native installation or automatic discovery. Follow
[the existing host setup](#4-ask-for-a-real-result) for invocation; no client trial or
login is required merely to copy or inspect instructions.

### Prepare an offline input packet

From the same source checkout, with `PROJECT` still set, copy only the task, evidence
packet and their source notices into a fresh project directory. The output directory
must also be new:

```sh
(
  set -eu
  : "${PROJECT:?Choose an existing project you own}"
  test -d "$PROJECT"
  mkdir "$PROJECT/decision-brief-example"
  cp examples/decision-brief/task.md examples/decision-brief/sources.json examples/decision-brief/NOTICE.md examples/decision-brief/LICENSE-PYTHON.txt "$PROJECT/decision-brief-example/"
  mkdir "$PROJECT/decision-brief-output"
)
```

This omits the authored expected `brief.md` and `evidence.md`. Existing input/output
locations, including same-name symlinks, make `mkdir` fail. Earlier successful steps
may already have created a new input directory; preserve and inspect it rather than
rerunning or automatically cleaning up. The Python documentation notices remain with
the supplied excerpts. No database or dependency installation is involved.

### Give your agent the task

Open your host in `PROJECT`. Explicitly select `decision-brief` using its native skill
invocation, or ask it to read the complete selected entry point and linked resources.
Then paste this task; the paths are relative to that project:

```text
Use decision-brief. Read decision-brief-example/task.md and
decision-brief-example/sources.json as the only task evidence. The source notices
are in the same input directory. Keep the task offline and preserve all inputs.

Create only decision-brief-output/brief.md and
decision-brief-output/evidence.md in the fresh owned output directory.
Compare the stated alternatives against the same constraints, link factual claims
to the supplied excerpts, separate assumptions and unknowns, and recommend
conditionally or defer if decisive evidence is missing. State what would change
the recommendation and what remains untested. Reopen both outputs to check them.

Do not install dependencies, retrieve more sources, create a database, migrate
anything, publish the result or treat your recommendation as my acceptance.
If either output already exists or is a symlink, stop without overwriting it.
```

### Check the result

Expect a proposed recommendation or explicit deferral in `decision-brief-output/brief.md`
and a source/claim/assumption/unknown ledger in `decision-brief-output/evidence.md`.
Verify that every load-bearing claim is supported by a precise excerpt or explicitly
marked as an assumption, that missing decisive evidence is visible, and that the
recommendation states concrete reversal conditions. The owner still decides whether
to accept it. This workflow does not perform a storage migration.

Use [the worked example](../examples/decision-brief/README.md) for comparison after
the task, and the [three observed task attempts](../evaluations/decision-brief/offline-tasks-001/README.md)
for their actual outputs and limits. The example's Python checker validates its
checked-in artifacts, not a newly generated brief or semantic correctness. Copy
checks establish file placement only, not native activation or better decisions.

## Troubleshooting without changing your setup

- **The skill is not listed:** check that you opened the intended project and used
  that host's documented directory. The selected folder must contain `SKILL.md`
  directly, not an extra `skillpot-source/skills/` nesting. Check the host's official
  refresh/discovery instructions below; do not install a second copy globally as a fix.
- **A reference or notice is missing:** compare the installed folder with the complete
  selected source package. Copying only `SKILL.md` is incomplete. Do not patch around a
  missing pinned guide with unrelated current-main product documentation.
- **The copy says the destination exists:** stop. It may contain local edits or be a
  symlink. Compare it with the reviewed source before deciding on a separate update;
  deleting or overwriting it is not part of this quickstart.
- **The skill is visible but no task runs:** installation provides instructions, not
  tools, product dependencies or permission. Invoke it in agent chat, give a concrete
  task and inputs, and resolve missing prerequisites only with the required approval.
  `/intpot-python` and `$intpot-python` are host invocation syntax, not shell commands.
- **Product behavior differs from the guide:** inspect the package's provenance and
  compatibility record, then compare the actual product version with its pinned guide.
  Do not relabel a source check as runtime verification or silently switch snapshots.

When reporting a setup problem, include the selected skill, source commit, host name
and version, project-relative folder layout, expected behavior and redacted error.
Do not attach tokens, private instructions, full personal configuration or agent traces.

## Official host references

- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Cursor Agent Skills](https://cursor.com/docs/context/skills)
- [Codex / ChatGPT skill authoring and local discovery](https://learn.chatgpt.com/docs/build-skills)
- [Hermes skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)

Paths and invocation examples above were checked against these documents; they are
not a claim that every listed version, interface or cloud environment was executed.
