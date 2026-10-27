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
git -C skillpot-source checkout --detach 8b6f1b32c9c3cda5438402a992659b016fe97bb3
cd skillpot-source
```

That immutable public revision contains the project collection and consumer examples.
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

## 5. Keep the evidence boundaries

A successful copy, a discovered skill, an explicit skill invocation, and a completed
application task are four different observations. None alone proves better results
than an ordinary workflow or universal compatibility.

Existing [installation evidence](../evaluations/modepot-project-skills/native-install-001/README.md)
and [consumer replays](../evaluations/modepot-project-skills/consumer-tasks-001/README.md)
state what actually ran. In particular, the earlier native Hermes gateway-isolation
failure is **not a prerequisite or blocker for users of other harnesses**. It remains
a limit on that specific host experiment. A host may also need a working account and
model entitlement; SkillPot does not supply those or authorize changing credentials.

For updates, inspect a newly pinned source and review the diff. Preserve local edits;
replacement behavior is host-specific. For removal, remove only the instruction bundle
you installed, using the host's documented method or your project's normal reviewed
file workflow. Do not remove product environments, applications or data with it.

## What has actually been checked

- **Codex CLI 0.157.0:** a real native session explicitly used the two project Intpot
  skills and completed a CLI export task with 52 passing assertions. The source and
  dependencies were provided; this is not automatic selection or setup qualification.
- **Claude Code:** full-directory project placement was byte-checked. Native task
  execution was blocked by expired OAuth, not presented as a pass.
- **Cursor:** project-directory placement was byte-checked against the documented
  layout. No native model task ran; the installed CLI was not logged in.
- **Hermes:** selective instruction installation/removal was exercised separately.
  Its earlier model-loading limitation remains scoped to that host experiment.

See [actual host observations and retained failures](../evaluations/harness-portability/explicit-codex-001/README.md).
An unavailable account or model does not change the portable files or make another
harness depend on Hermes. Do not infer support for every host/version from this list.

## Official host references

- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Cursor Agent Skills](https://cursor.com/docs/context/skills)
- [Codex / ChatGPT skill authoring and local discovery](https://learn.chatgpt.com/docs/build-skills)
- [Hermes skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)

Paths and invocation examples above were checked against these documents; they are
not a claim that every listed version, interface or cloud environment was executed.
