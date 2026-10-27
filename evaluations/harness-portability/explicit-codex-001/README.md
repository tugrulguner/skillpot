# Explicit skill use in a non-Hermes harness

## Result and scope

A real **Codex CLI 0.157.0** session used the public `intpot-cli` and `intpot-python`
packages placed under a fresh project's `.agents/skills/`. The prompt explicitly
mentioned both skills; the captured native commands read both entry points, their
pinned guides and complete licenses before executing the task. This is explicit skill
use in Codex, **not automatic-selection or universal compatibility evidence**.

Source SkillPot revision: `8b6f1b32c9c3cda5438402a992659b016fe97bb3`. Whole installed
skill directories and the supplied invoice source were byte-compared with that source.
The existing Intpot 0.13.0 environment was provided to the agent, matching upstream
`8e583cc4b2b6785955268d09a12dfdd955194b88`; consumer Python was 3.12.13 on macOS arm64.
This run did not qualify dependency installation or an independently minimal Typer-only
target environment. The authenticated CLI used its default model after an unsupported
explicit-model attempt; the default model ID was not reported by the captured stream.

## Real task

The agent authored and ran a [portable verifier](../../../examples/harness-portability/codex-intpot/verify_invoice.py)
against the supplied invoice App. It performed actual `intpot eject` and native Python
`App.eject("cli")` exports, compared their source, compiled/imported them, checked that
the emitted code does not import Intpot, and executed each CLI for four valid and
three invalid cases. Optional discount, zero amounts and original exception messages
were checked. API/MCP and foreign-framework conversion were not exercised here.

The [native assertion journal](verification.jsonl) records **52 passing assertions,
zero failed assertions**, and final `PASS`. Seven nonzero subprocess results remain:
six intentional invalid-input cases and one failed local `pip show` probe. Pip was
absent; installed-distribution metadata supplied the actual version. No missing
command result was replaced by invented output.

[Native observations](native-observations.json) retain selected completed host command
events, including actual exit codes and explicitly labeled output tails. Full raw
traces are private and hashed; reasoning events and unrelated startup context are
not published. The public verifier copies are byte-identical to the agent-created
files, and a [separate parent replay](parent-replay.json) passed the same 52 assertions.
That replay confirms the file can run; it does not replace native host execution.

## Installation and host distinctions

The [placement checks](placement-checks.json) execute the quickstart's ordinary `mkdir`
and copy recipe for `.claude/skills`, `.cursor/skills` and `.agents/skills`. Complete
package files matched their hashes. A repeated installation refused the existing
destination and preserved all original bytes. This verifies placement/copy behavior,
not three native model runs.

- **Codex CLI:** explicit project-skill use and the bounded CLI task passed. Standard
  `workspace-write` sandboxing stayed enabled, user config was not loaded, and session
  persistence was disabled. Existing account authentication was used; no credential
  copying, login flow or permission bypass was requested.
- **Claude Code 2.1.263:** project-directory placement was checked. The first launch
  used an invalid empty MCP configuration, which was corrected. The next launch failed
  before tools ran: OAuth was expired and could not refresh. Its terminal event says
  `subtype: success` but also `is_error: true`, and the process exited 1; it is **not a
  pass**. No reauthentication or credential replacement was attempted.
- **Cursor:** current documented project layouts were checked. Installed CLI version
  was `2025.09.18-7ae6800`; its auth-status check reported not logged in. A model task
  was not attempted, and no compatibility with that old CLI is asserted.
- **Hermes:** earlier normal instruction installation and selective removal are
  [separate evidence](../../modepot-project-skills/native-install-001/README.md).
  Its isolated model-loading failure does not block this Codex result or the collection.

The failed Claude launches and unsupported `gpt-6.1-sol` Codex model attempt are
preserved in [failed launches](failed-launches.json). The successful Codex retry omitted
the model override rather than silently relabeling or normalizing the failed identifier.

## Limitations and cleanup

This is one assisted, explicitly invoked task with preprovided source and dependencies,
not a clean-room comparison, implicit-trigger study, freshness matrix, provider-backed
application result or performance benchmark. Existing host/account context may affect
behavior; no claim of independence from all user/admin instructions is made.

All invoked CLI processes exited. No servers were started by this task. Generated
files and evidence remain in owned scratch projects; no existing user project, global
skill store, active Hermes gateway or another registered profile was selected for
installation. Source-copy examples remain project-local; no host configuration edits,
new registry, custom installer, plugin manifest or release is included.

[Provenance](provenance.json) records private-original and portable-file hashes and
public transformations. Workspace/environment prefixes become labeled placeholders;
actual statuses, errors, assertion results and source identities are retained. For
reproduction, follow the [harness-neutral quickstart](../../../docs/quickstart.md) and
[fixture instructions](../../../examples/harness-portability/codex-intpot/README.md).
