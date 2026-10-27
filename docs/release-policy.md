# Collection releases and upstream maintenance

This policy prepares a versioned distribution of instructions, not a runtime package,
security certification or proof of model performance. The first planned tag is
`v0.1.0`. No tag or published release is created by this document.

## Version identity

- A collection release uses a `vMAJOR.MINOR.PATCH` Git tag pointing to one reviewed,
  approved commit on `main`. Never move or reuse a published tag.
- Patch increments cover corrections that preserve workflow inputs, outputs, required
  permissions, prerequisites and resource paths.
- Minor increments add backwards-compatible workflows or capabilities. Before 1.0,
  incompatible workflow/installation changes also require a minor increment with
  explicit migration notes. After 1.0, incompatible changes require a major increment.
- An upstream refresh is classified by its actual effects, not automatically treated
  as a patch. New permissions, services, dependencies or renamed skills are breaking
  contract changes, even when the prose edit is small.
- The collection tag, per-skill `metadata.version`, and upstream product version/pin
  are distinct identities. Change a skill's version when its instructions/resources
  change; do not churn unchanged skill metadata merely to match a collection tag.
- This is not a Python package. Do not introduce a runtime version module, dependency
  lockfile or package upload just to version Markdown. Use the Git tag and catalogue.

## What a release contains

The tagged source tree is the distribution: the catalogue, complete selected skill
folders, licenses/provenance, setup docs and public examples. GitHub's normal source
archives are sufficient; no new installer, account, registry or generated bundle is
required. Downloading source does not register every included skill with a harness.
Users install only their selected directories through the [quickstart](quickstart.md).

The seven public project skills and original repository-readiness skill retain their
individual scope. Refpot and repository-readiness remain experimental where their
package records say so; a collection tag does not promote their maturity. Examples
may need separately approved product dependencies. Nothing installs those implicitly.

## Release preparation — offline source gates

1. Review the exact proposed `main` commit and its changed files. Confirm maintainer
   authorization for the merge/publication; do not release an unmerged feature branch.
2. Check that catalogue entries, immutable upstream revisions, required references,
   full notices and per-package provenance agree. Inspect changed instructions for
   private context, personal paths, undeclared tools/services, rights and permissions.
3. Follow official host specifications for discovery/installation/invocation. Cite
   source docs for changed integrations; validate metadata and relative resources.
   No live client session, authentication probe, model call or runtime study is needed.
4. In a fresh checkout at that exact commit, run the repository's declared checks:

   ```sh
   uv run --no-project --with pyyaml==6.0.3 python scripts/check_docs.py
   uv run --no-project --with pyyaml==6.0.3 python scripts/check_project_skills.py
   uv run --no-project --with pyyaml==6.0.3 python -m unittest discover -s tests -v
   ```

   Inspect the committed release diff with `git diff --check PREVIOUS_TAG COMMIT`
   (use the reviewed base commit for the first release). Require successful CI for
   the exact candidate. Record its commit/tree identity and actual check results.
5. Prepare release notes with contents, exact commit, selective setup link, immutable
   product pins, notable instruction changes and limitations. Separate documented
   host integration from historical task results. Do not claim universal activation,
   safety, improved accuracy or speed without appropriate separate evidence.

Validation only covers its stated surface: local file destinations and source/hash/
license checks do not validate every external link, permission enforcement or product
runtime. Authorize executable-resource tests separately when those resources change;
this policy does not turn a format update into a live harness evaluation.

## Publication and readback

After the candidate is reviewed/merged and publication is authorized:

1. Confirm the candidate is on current `main`, its checks succeeded and the chosen tag
   and release do not already exist. Stop on a conflicting identity; never force it.
2. Create the version tag at that explicit candidate commit and publish GitHub release
   notes for it. Do not rely on an implicit latest-main target. Do not upload private
   logs, credentials, task environments or unrelated generated assets.
3. Read back the release's tag, published/draft/prerelease state and target. Resolve
   the tag to its actual commit (peel an annotated tag if needed) and compare with the
   approved candidate. A successful create call alone is not publication verification.
4. Verify the tagged catalogue, selected skill entry points and required resources
   against the candidate bytes through the public GitHub source endpoint. Read the
   release page and check its setup/source links; record the resulting release URL.
5. Inspect applicable post-publication CI at its actual commit, or explicitly state
   when the configured workflows do not trigger for a tag/release. Do not invent a
   release check or treat absent CI as green CI. Update source-facing release status
   only after the published release exists; never mark it released in advance.

Merge approval for a documentation change is not approval for an unrelated release or
future runtime changes. Existing installations stay untouched. A bad release gets a
new corrective version or a clearly disclosed withdrawal, not a silently moved tag.

## Upstream refresh rules

Upstream product repositories remain canonical. A release records what was reviewed
at its pins; it is not a promise to follow latest upstream automatically.

- Review freshness before each release and when an upstream API/command/license
  change, reported failure or host specification change affects a supported workflow.
  If keeping an older snapshot, retain its exact prerequisites and limitations;
  never relabel it as tested against current main.
- Fetch source and full license at the **same immutable revision**. Compare guide/API,
  prerequisites, permission boundaries and rights before accepting a refresh.
- Preserve unchanged upstream reference bytes. Disclose entry-point adaptations;
  update source/notice hashes and provenance together in the catalogue/package files.
- Keep product consumer and project contributor policies separate. An upstream review
  workflow must not acquire authority over another repository or permission to merge.
- Run the offline gates and review the complete diff. Update affected examples or
  compatibility notes when the documented contract changes; retain historical results
  at their original pins rather than rewriting them as fresh execution evidence.
- Publish the reviewed refresh in a new collection version. Never overwrite user edits,
  modify active skill stores or run clients/installers during source maintenance.

Optional runtime studies require their own explicit scope and budget. Preserve actual
results, failures and interventions; they support only their measured claims and are
not prerequisites for documented harness support or collection publication.
