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

## 3. First versioned collection — next publication

The source is available now. No versioned GitHub release has been published yet.
The first planned collection tag is `v0.1.0`, not a product-package version or a
certification of agent performance. See the [release policy](docs/release-policy.md).

- [x] Define collection versioning and immutable source-pin/freshness rules.
- [x] Define offline preparation checks, release contents and publication readback.
- [ ] Review and merge the release-policy change.
- [ ] Pin the approved main commit and rerun source checks at that commit.
- [ ] Publish `v0.1.0` at the approved commit with scoped contents and limitations.
- [ ] Verify tag, release, source links and post-publication checks against that commit.

These checkboxes do not authorize merging a future change or publishing from an
unreviewed branch. A collection release distributes instructions; it neither installs
all skills nor changes existing user copies.

## 4. Maintain and expand the library

- [ ] Apply the source-refresh process when upstream commands, APIs, notices or host
      specifications change; review diffs rather than silently tracking moving main.
- [ ] Add useful skills with concrete inputs, outputs, permissions, public source
      rights and a named maintenance owner.
- [ ] Improve task examples and failure guidance when users report actual gaps.
- [ ] Consider native plugin/marketplace packaging only for a requested distribution
      channel that requires it; preserve plain-directory use.
- [ ] Consider a project website when it adds value beyond the catalogue/quickstart.

Potential later tasks include sourced interactive explanations, reproducible
analysis-to-decision briefs and general engineering workflows. They are opportunities,
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
