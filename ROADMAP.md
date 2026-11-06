# SkillPot roadmap

SkillPot is a harness-neutral library of practical, selectively installable agent
skills. Start with the [catalogue](catalog/README.md) and [quickstart](docs/quickstart.md).
Its reach is not limited to ModePot projects.

Checked items describe implemented source, not an unpublished tag or a claim that
skills improve every model. Implementation, merge approval and release publication
remain separate steps.

## 1. Foundation and public collection — implemented

- [x] Publish project direction, contribution guidance and canonical family artwork.
- [x] Define the portable [Agent Skills contract](docs/skill-contract.md).
- [x] Audit public sources and redistribution rights in the bounded
      [seven-repository inventory](catalog/source-inventory.json).
- [x] Package seven public project skills: five consumer workflows and two
      Summonpot-specific contributor workflows, with immutable pins and full notices.
- [x] Keep upstream product guidance canonical; preserve source snapshots, hashes,
      adaptations and per-package compatibility/provenance records.
- [x] Provide the original experimental repository-readiness skill and report template.
- [x] Publish runnable [consumer examples](examples/modepot-project-skills/README.md)
      and retain bounded results, failures and assisted replays separately.
- [x] Validate catalogue identity, metadata, source/license hashes, local Markdown
      destinations and source regressions through offline checks and CI.

No skill was fabricated for Utilitypot, Lifepot or Strpot at their inspected revisions.
Private skill stores are not an input to this collection.

## 2. Harness integration — documented and implemented

- [x] Document complete-directory installation, explicit invocation and relevance-based
      selection according to official Claude Code, Cursor and Codex docs.
- [x] Document the existing selective Hermes URL installer as one host option.
- [x] Keep required references and license notices with each selected skill.
- [x] Explain project scope, refusal to overwrite an existing destination, updates,
      removal and the distinction between instructions and product dependencies.
- [x] Keep historical installation/task observations separate from setup instructions.

**Integration gate:** follow the host's published format/discovery contract and
validate package metadata/resources offline. A live model session, local account login,
activation benchmark or repeated harness trial is not required to document/support
that integration. Do not infer universal runtime behavior from format support either.

Do not build a custom installer, runtime, registry or mandatory plugin merely to copy
standard skill directories. Add other host instructions when their official contract
is known; proprietary client availability is not a collection-wide gate.

## 3. First versioned collection — published

The first collection release is [v0.1.0](https://github.com/tugrulguner/skillpot/releases/tag/v0.1.0),
at commit `86ce1b3c7afedc6144b53777ce462ec46f3df36f`. It is not a product-package
version or certification of agent performance. See the [release policy](docs/release-policy.md).

- [x] Define collection versioning and immutable source-pin/freshness rules.
- [x] Define offline preparation checks, release contents and publication readback.
- [x] Review and merge the release-policy change.
- [x] Pin the approved main commit and rerun source checks at that commit.
- [x] Publish `v0.1.0` at the approved commit with scoped contents and limitations.
- [x] Verify tag, release, source links and public archive against that commit;
      existing CI covers main pushes, not tag/release events.

These checkboxes do not authorize merging a future change or publishing from an
unreviewed branch. A collection release distributes instructions; it neither installs
all skills nor changes existing user copies.

Latest published collection: [v0.4.1](https://github.com/tugrulguner/skillpot/releases/tag/v0.4.1),
at commit `79284b3faa928dc556a9032aa9dbeb059b4ee915`. The
[publication record](docs/releases/v0.4.1.md) describes the two workflow corrections, retained
upstream pins and independently verified public source archives.

## 3a. Published v0.4.0 collection

The [v0.4.0 publication record](docs/releases/v0.4.0.md) records ten skills, adding
`decision-brief` and `document-actions` to the eight in v0.3.0. It preserves reviewed
upstream pins and existing maturity/evidence boundaries. The v0.4.0 tag is unchanged;
current setup now selects v0.4.1 as described below. Family discovery deploys independently.

## 3b. Published v0.4.1 patch

The [v0.4.1 publication record](docs/releases/v0.4.1.md) covers the two original workflows'
role, status, approval, timing and evidence-check corrections, with unchanged inputs,
outputs, permissions and the same ten-skill collection. Current stable setup selects
published v0.4.1. This source-facing alignment preserves the immutable published tag;
family discovery deploys independently and each alignment change needs merge approval.

## 4. Maintain and expand the library

- [x] Add `document-actions`, released in v0.4.0 and corrected in v0.4.1, for source-stated actions and focused questions,
      with assigned/required/proposed/historical classifications, verbatim deadlines,
      explicit conflicts, an authored offline example and pinned first-use instructions.
      Included in v0.4.0; source checks are not observed agent extraction results.

- [x] Implement [decision-brief](skills/decision-brief/SKILL.md) in current source,
      with a bounded evidence procedure, parent-authored worked example and offline
      artifact checks. [Three bounded task observations](evaluations/decision-brief/offline-tasks-001/README.md)
      record conditional recommendation, missing-evidence deferral and collision refusal.
      The skill was introduced in v0.4.0 and corrected in v0.4.1; these
      observations do not establish broad model performance or automatic discovery.

- [ ] Apply the source-refresh process when upstream commands, APIs, notices or host
      specifications change; review diffs rather than silently tracking moving main.
  - [x] Prepare the [Dexpot v0.8.1 guide correction](docs/published-upstream-refresh.md)
        in current source, with released-source parity, version/pin/notice consistency
        and explicit separation from published SkillPot v0.4.1. No new collection
        release or runtime qualification is implied.
- [ ] Review the [claim-check proposal](docs/claim-check-proposal.md) and its authored
      draft/source/review packet: factual-claim verdicts, exact evidence locators,
      minimal proposed edits and explicit permission/access limits. Proposal only;
      no installable skill, new collection release or observed accuracy claim yet.
- [ ] Add useful skills with concrete inputs, outputs, permissions, public source
      rights and a named maintenance owner.
- [ ] Improve task examples and failure guidance when users report actual gaps.
- [ ] Consider native plugin/marketplace packaging only for a requested distribution
      channel that requires it; preserve plain-directory use.
- [x] Implement product-owned website source with canonical generated guides,
      family presentation and build/browser checks.
- [x] Deploy the approved website, verify custom HTTPS routing/assets, and point
      the GitHub homepage at the verified site.
- [x] Merge and deploy the separate umbrella discovery correction; verify its
      public collection status and links independently of the product website
      ([ModePot #58](https://github.com/tugrulguner/modepot/pull/58),
      [live directory entry](https://modepot.io/#skillpot)).

Potential later tasks include sourced interactive explanations and further general
engineering workflows. They are opportunities,
not committed features or permission to copy private procedures.

## Optional research — not installation or release gates

Repeated paired trials, held-out tasks, non-trigger behavior, model/harness comparisons,
setup-cost measurements and incumbent comparisons can support specific improvement
claims. Run them only as an explicitly scoped evaluation, not as incidental work for
a format integration or documentation release. Preserve failures and interventions;
never invent results or attribute parent-assisted replays to an unassisted agent.

Existing readiness studies and historical demo proposals remain records, not the
mandatory next product milestone. No video, recording system or evaluation framework
is required to ship this collection.

## Non-goals and contribution boundary

- No new agent runtime, skill format, marketplace or custom package manager.
- No hidden dependency installation, paid service use, permission bypass or publication.
- No bulk private exports, unlicensed packs or catalogue-size targets.
- No guaranteed safety, task improvement or universal runtime claims.

Use [CONTRIBUTING.md](CONTRIBUTING.md) for proposed tasks and verification commands.
Keep implementation scoped; publishing, merging and modifying user installations
remain explicit maintainer/user decisions.
