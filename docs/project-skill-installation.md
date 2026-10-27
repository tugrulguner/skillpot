# Selectively install a ModePot skill

These are agent instructions, not the underlying Python products. Install only the
task you need; product dependencies, listeners, credentials, data changes, code pushes
and public review publication remain separate authorization decisions.

The public project collection is available on `main`. Start from an inspected checkout
of `main`, then pin that published commit so updating your agent does not silently
change project guidance. A merge is not a versioned or generally qualified release.

## Hermes: direct URL, one selected skill

Hermes' established installer fetches a SKILL.md and its explicitly referenced support
files. See the [official skills documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills#8-direct-url-url).
No custom SkillPot installer or registry account is needed.

From an inspected SkillPot checkout of `main`:

```sh
REV=$(git rev-parse HEAD)
hermes skills inspect "https://raw.githubusercontent.com/tugrulguner/skillpot/$REV/skills/intpot-cli/SKILL.md"
hermes skills install "https://raw.githubusercontent.com/tugrulguner/skillpot/$REV/skills/intpot-cli/SKILL.md"
hermes skills list --source hub
```

Choose `intpot-python`, `summonpot`, `dexpot`, `refpot-database`,
`summonpot-pr-review` or `summonpot-code-review` instead of `intpot-cli` for another
individual workflow. Read the scan result; do not add `--force` just to make a check
pass. A block is not a completed install.

The installer writes to the **active Hermes profile**. Do not point it at another
existing profile without permission. For verification, an owned temporary empty
`HERMES_HOME` can isolate install/list/uninstall checks from the real profile. That is
a temporary test home, not authorization to change another registered profile.

Each package links its complete source guide and MIT notice under `references/`.
Those files must accompany the entry point. Root `provenance.md` and `compatibility.md`
in the source repository document the distribution and its measured limits; direct
URL consumers do not depend on those root files being fetched.

## Use, updates and removal

After installation, ask the agent to load the selected skill, or invoke its supported
slash command (for example `/intpot-cli`) in a host/session that exposes it. Confirm
that the host loads the installed entry point before claiming activation. A successful
install alone does not establish successful product execution.

Inspect your actual product revision against the upstream revision in the skill
metadata. The copied reference is pinned, not a promise about every published product
version. Stop on a mismatch requiring APIs that your package does not provide.

For an unchanged installed source, the host's normal update flow can check that same
URL; an immutable URL deliberately does not move to newer guidance. To adopt a newly
reviewed SkillPot revision, inspect its new URL and the host's documented replacement
behavior first. Preserve local edits; do not force overwrite. Remove only a selected
hub skill using the host's existing command:

```sh
hermes skills uninstall intpot-cli
```

Uninstalling the instruction bundle must not remove product environments, code or data.
Other Agent Skills hosts may support these directories, but their installation,
activation, update and removal paths are not established by Hermes-only evidence.

## Verification boundaries

Collection integrity tests parse YAML, validate source pins and compare source/license
hashes. Native install/load/selectivity/removal evidence and actual product-consumer
examples are separate gates, recorded only when executed. No broad compatibility,
security certification or usefulness advantage follows from distributing source files.

The [recorded native check](../evaluations/modepot-project-skills/native-install-001/README.md)
exercised all seven packages at the named immutable revision in a temporary Hermes
home, with normal scanning and no force override. Each installed entry point, source
reference and license matched source bytes; selected removal preserved siblings.
This evidence does not establish automatic task activation or another agent host.
