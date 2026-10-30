# Start with a task, not a harness

SkillPot is a collection of portable agent instructions. **Claude Code, Cursor, Codex,
Hermes and other Agent Skills hosts are ways to use it—not dependencies of the library.**
A skill is a directory containing `SKILL.md` and its supporting files. Your agent
provides file access, command execution and permission controls; the underlying product
may require its own Python environment, dependencies or credentials.

## 1. Choose one workflow

Start with the [task-first catalogue](../catalog/README.md):

- Intpot CLI or Python: define, inspect, export or convert a trusted application.
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
