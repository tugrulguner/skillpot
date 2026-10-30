# ModePot project skills

SkillPot distributes pinned, selectively installable copies of existing **public**
ModePot project guidance. Upstream projects remain canonical; this is not a second
independently maintained API manual and does not import the private local skill store.

## Choose the task

- **intpot-cli** — turn typed Python declarations into a CLI; preserve supported
  signature/default/helper-recovery boundaries.
- **intpot-python** — use Intpot through its Python API rather than assuming CLI-only
  behavior or inventing parser recovery.
- **summonpot** — build agent-owned APIs with deterministic operations and bounded
  agentic decisions; preserve contracts and authorization.
- **dexpot** — build synchronous typed HTTP APIs and verify behavior through real sockets.
- **refpot-database** — use the embedded database preview with explicit data, transaction,
  process/thread and durability limits.

Related **project-scoped contributor workflows**:

- **summonpot-pr-review** — inspect a Summonpot change at an exact head, check review
  resolution against source/tests, and keep merge/publication permission separate.
- **summonpot-code-review** — review Summonpot changes against its own development rules.

These are not interchangeable consumer/contributor personas. Installing one does not
install the other workflows or the underlying product. Summonpot contributor policies
must not override another project's policy or a user's explicit approval boundary.

## What is and is not included

The [machine-readable source catalogue](modepot-sources.json) identifies every package,
immutable upstream revision/path, original source hash and license hash. Complete MIT
notices are included in each package. An unchanged upstream reference sits behind an
adapted portable entry point: specific task, setup, permissions, checks and limitations.
Changed entry-point behavior is disclosed in each provenance file.

The [complete-tree inventory](source-inventory.json) covers Intpot, Summonpot, Dexpot,
Refpot, Utilitypot, Lifepot and Strpot. No existing public skill Markdown was found for
the last three at their inspected revisions. They are **not represented by fabricated
skills**. This is a bounded set of seven project repositories, not a claim to have
audited every ModePot-family repository or every private workflow.

`repository-readiness` is an original related engineering workflow in this source
branch, separate from the seven imported public guidance files. Video tooling is
not included. Private authoring, release, marketing and operational workflows require
individual source/rights/privacy review before any later extraction.

## Selective installation

Start with the [harness-neutral quickstart](../docs/quickstart.md). Use documented
project skill directories or the host's established installer, not a new SkillPot
package manager. For Hermes,
see [installation and verification](../docs/project-skill-installation.md). The seven
packages expose their necessary reference and license files through explicit relative
links under `references/`, so a direct SKILL.md URL can fetch the complete runtime
instruction bundle. Root provenance/compatibility files remain source-review records.

No all-skills auto-install or hidden product dependency installation is performed.
Other Agent Skills consumers can use the directories, but format compatibility is
not a tested-host claim. Actual host and task results must be recorded separately.
The [native Hermes verification](../evaluations/modepot-project-skills/native-install-001/README.md)
records successful individual install/list/removal and complete reference/license
byte parity for every listed package, without bypassing scans. Model activation and
product execution are separate from those checks.
One [Refpot consumer task](../evaluations/modepot-project-skills/refpot-consumer-001/README.md)
also executed against its exact pinned source with a separately replayed
[portable example](../examples/modepot-project-skills/README.md). No other project's
runtime or the whole collection's usefulness is established by that result.
Later [Intpot/Dexpot/Summonpot consumer replays](../evaluations/modepot-project-skills/consumer-tasks-001/README.md)
add bounded installed-artifact checks and runnable examples while preserving original
worker failures and parent interventions. Native model loading remains unverified;
these are not baseline comparisons or broad compatibility results.

## Maintenance

The [public-guide refresh audit](../docs/public-guide-refresh.md) records four
changed consumer guides and three unchanged imported guides. The refreshed source
packages are not part of published SkillPot v0.2.0; the stable quickstart continues
to install that release. Each affected package distinguishes published upstream
features from newer-main-only instructions. Historical examples remain at their
original pins rather than becoming fresh execution evidence.

Review `modepot-sources.json` before updating a package. Fetch both the source and
license at the **same immutable upstream revision**. Compare API/command changes and
rights before replacing the pinned reference. Update the entry point only where the
new behavior requires it, record adaptations, update hashes and rerun catalogue,
Markdown and source checks. Native client trials are not required for source refreshes
or documented harness support; scope them separately if explicitly requested.
Follow the [release policy](../docs/release-policy.md). Never silently rewrite a user's
installed copy or imply that a pinned snapshot follows current main automatically.
