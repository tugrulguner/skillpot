# Repository automation and protection

SkillPot follows LifePot's repository pattern at public commit
`51f30665f9fbb4d9c2e36b76458657a69f2e9583`: checks, browser verification, a fail-closed
`verify` aggregate, separate production deployment, weekly dependency updates and
bounded issue/pull-request templates. The implementation is adapted to a collection
of instructions, not LifePot's simulation engine or Next.js runtime.

## Verification contract

- `.github/workflows/ci.yml` runs on every pull request and main push, without path
  filtering away a required gate.
- `checks` tests the offline repository tooling on Python 3.11–3.14. Ruff enforces
  Python error rules `E9,F63,F7,F82` on `scripts/` and `tests/`; this is not a
  claim of repository-wide formatting enforcement. Pyright checks `scripts/`.
- `browser` calls the existing website workflow once. That workflow uses the declared
  Node 22.23.4 runtime, clean locked installation, type/content checks, static build,
  output tests and browser tests. It retains screenshots/failure traces for seven days.
- `verify` runs with `always()` and passes only when **both** `checks` and `browser`
  succeed. Failed, cancelled or skipped dependencies must fail the aggregate. Offline
  tests execute all dependency-result combinations through the actual shell command.
- The existing `source` check remains intact. The protection contract is `source`
  plus `verify`, bound to the GitHub Actions integration, with an up-to-date branch.

Repository development checks can run without installing a product or agent host:

```sh
uv run --no-project --with-requirements requirements-ci.txt ruff check --select E9,F63,F7,F82 scripts tests
uv run --no-project --with-requirements requirements-ci.txt pyright scripts
uv run --no-project --with-requirements requirements-ci.txt python -m unittest discover -s tests -v
```

The pinned CI tools are development-only. Skill installation does not install them.

## Live controls versus source configuration

GitHub settings do not live in workflow YAML. Inspect them independently:

```sh
gh api repos/tugrulguner/skillpot/rulesets
gh api repos/tugrulguner/skillpot/environments/production/deployment-branch-policies
gh api repos/tugrulguner/skillpot/actions/permissions/workflow
```

Main protection requires a pull request, successful required checks, resolved review
threads and an up-to-date branch. Force pushes and deletion are blocked; no bypass
actors are configured. Zero formal approving reviews permits the single maintainer's
workflow, but never grants an agent permission to merge without explicit approval.
Production permits the `main` branch only, in addition to the workflow's main-ref
condition. Deployment credentials are exposed only to the upload step, not builds/tests.

LifePot's audited default branch had no ruleset or classic branch protection. SkillPot
keeps its stronger existing protections rather than weakening them for literal parity.
Actions' default token is read-only and cannot approve pull requests.

Dependabot follows LifePot's weekly schedule and five-open-request limit. SkillPot
adds the actual root pip manifests alongside GitHub Actions and `website/` npm files.
TypeScript major upgrades are deliberately manual: update the Astro checker and
TypeScript together only when their declared peer ranges overlap, then run clean
`npm ci`, the complete build/type checks and browser suite. For example,
`@astrojs/check@0.9.4` requires TypeScript 5; `0.9.12` supports 5/6, not 7. Do not
use `--force` or `--legacy-peer-deps` to turn an incompatible proposal green.
Minor/patch TypeScript updates and updates to other dependencies remain enabled.
Issue and pull-request forms request source revision, permission/provenance impact and
redacted evidence, not simulation seeds, model login or private instruction exports.

No changelog, release, labeler or stale-closing stack is added by this alignment. The
existing collection release policy and immutable published tags are unchanged. Source
changes still require separate review and merge approval; live settings, merged
workflows and actual successful executions are distinct verification surfaces.
