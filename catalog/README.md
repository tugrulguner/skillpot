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

The [machine-readable source catalogue](modepot-sources.json) identifies every imported package,
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

## Claim-check — current source, unreleased

The original **[claim-check](../skills/claim-check/SKILL.md)** bundle is in current
source and remains unreleased; it is one of twelve current-source bundles, not part of
published v0.4.1's ten-skill set. Use the standard Skills CLI to install only this
skill from the exact reviewed source revision:

```sh
npx skills@1.7.6 add https://github.com/tugrulguner/skillpot/tree/4139aff1dd8127fc4c9bb3916a4bc5e3fd5cd23c --skill claim-check
```

See the [claim-check first-use guide](../docs/claim-check-first-use.md), with a
[GitHub main fallback](https://github.com/tugrulguner/skillpot/blob/main/docs/claim-check-first-use.md).
This discovery describes source availability and installation, not task efficacy.

## Change-impact — current source, unreleased

The original [change-impact](../skills/change-impact/SKILL.md) bundle maps a specified
diff to callers, contracts, configuration, docs and focused verification needs. It
produces exactly `impact.md` and `verification.md`, linking static evidence and
explicit unknowns without claiming runtime reachability or automatically running tests.
It is one of twelve current-source bundles, not part of the ten published in v0.4.1.
Use the [one-command first-use guide](../docs/change-impact-first-use.md), also
[available on GitHub](https://github.com/tugrulguner/skillpot/blob/main/docs/change-impact-first-use.md).
This is instruction distribution, not a custom dependency analyzer or task-efficacy claim.

## General decision workflow — version 0.1.1 in v0.4.1

Published v0.4.1 contains ten skills. They are also present in current source: the seven imported public guidance files,
experimental repository-readiness, **[decision-brief](../skills/decision-brief/SKILL.md)**
and **[document-actions](../skills/document-actions/SKILL.md)**.
The stable quickstart selects that published release. Current-source
[field-consistency patches](../docs/field-consistency.md) for both original workflows
are included in that release; current-source publication labels do not rewrite its
prepublication metadata. Use the
[decision-brief first-use guide](../docs/quickstart.md#try-decision-brief-from-reviewed-source)
for its exact release commit, safe copy steps and task prompt.

Use decision-brief to compare real alternatives for one decision using supplied
evidence, constraints, claim/source links, trade-offs and explicit uncertainty.
It creates a proposed brief and evidence ledger; it neither accepts nor implements
the decision. The [worked example and failure cases](../examples/decision-brief/README.md)
are authored references, not observed agent runs or evidence of better decisions.
A separate [task record](../evaluations/decision-brief/offline-tasks-001/README.md)
archives three actual, bounded attempts without claiming broad reliability or gains.
Its [provenance](../skills/decision-brief/provenance.md) records narrow public-source
use and exclusions; the seven-package upstream catalogue remains unchanged.

## Document actions — version 0.1.2 in v0.4.1

Use [document-actions](../skills/document-actions/SKILL.md) to extract source-stated
assignments and requirements, separate proposals and historical items, preserve exact
deadline wording, and expose conflicting or missing fields without inventing commitments.
It produces `actions.md` and `questions.md`; it creates no tickets or messages.
This workflow is included in v0.4.1. Follow the
[document-actions first-use guide](../docs/quickstart.md#try-document-actions-from-pinned-source)
for a pinned source checkout, complete selected bundle, bounded input packet and prompt.
The [worked example](../examples/document-actions/README.md) and executable offline checks
validate authored fixtures and setup, not semantic extraction quality or native activation.

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

The [current published-guide correction](../docs/published-upstream-refresh.md) selects
Dexpot v0.8.1 for current-source instruction 0.3.0 only. Published SkillPot v0.4.1
keeps the earlier Dexpot package; its stable install command is unchanged. The other
six imported packages and three original bundles are not refreshed.

The historical [public-guide refresh audit](../docs/public-guide-refresh.md) records four
changed consumer guides and three unchanged imported guides. The refreshed source
packages are included in published SkillPot v0.3.0; v0.2.0 retains its older
snapshots. Published v0.4.0 added the two original workflows; v0.4.1 retains those
guide snapshots and distributes bounded corrections to the two originals.
The stable quickstart selects v0.4.1. Each package distinguishes published upstream
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
