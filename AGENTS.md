# Contributor and coding-agent guidance

SkillPot is a library of portable Agent Skills instructions, not an agent runtime or
custom installer. Read `README.md`, `CONTRIBUTING.md`, `docs/skill-contract.md` and the
relevant skill's provenance/compatibility before changing it. This file governs work
in this repository; it is not an installable end-user skill.

## Scope and ownership

- Keep changes scoped to the requested task. Preserve unrelated source, artwork,
  examples, historical evidence and user edits.
- Product repositories remain canonical for commands/APIs. Distribute reviewed public
  snapshots at immutable commits with complete licenses and computed hashes. Update
  catalogue pins, references, provenance and affected skill versions together.
- Never copy private skills, credentials, personal paths or unlicensed material into
  public source. Public visibility alone is not redistribution permission.
- Keep consumer guidance separate from project-specific contributor policy. Instructions
  do not authorize dependency installation, services, paid actions, publication or merges.
- Preserve canonical `assets/` bytes and README hero geometry. The product site lives
  under `website/`; do not move detailed manuals into the ModePot umbrella repository.

## Harness-neutral integration

Follow the host's official documented skill format, discovery directories and
invocation contract. Use ordinary complete-directory placement or established native
installers. Do not add a registry, custom runtime or mandatory plugin merely to copy
skills. Do not launch Claude, Cursor, Codex or Hermes, probe authentication or require
model trials merely to validate documented integration. Runtime studies need explicit
scope and remain separate from source/setup claims.

## Repository layout

- `skills/<name>/`: entry point, required resources and source-review records.
- `catalog/`: source inventory, immutable pins and hash/license mapping.
- `docs/`: canonical setup, authoring and maintenance guidance.
- `examples/`: runnable public examples with declared setup and limits.
- `evaluations/`: historical observations; never rewrite old results as fresh evidence.
- `website/`: independently built product-owned overview, generated documentation,
  static-site deployment configuration and browser checks.
- `scripts/`, `tests/`: offline source/integrity checks and regression tests.

## Verification

For source/documentation changes, from the repository root:

```sh
uv run --no-project --with pyyaml==6.0.3 python scripts/check_docs.py
uv run --no-project --with pyyaml==6.0.3 python scripts/check_project_skills.py
uv run --no-project --with pyyaml==6.0.3 python -m unittest discover -s tests -v
```

Check the committed base-to-head diff with `git diff --check BASE HEAD`, as well as
working/staged changes. Read current contribution guidance and CI before selecting
commands if declared versions change. These checks do not prove runtime behavior or
model improvement. Preserve real failures and distinguish syntax checks from execution.

For site changes, also follow `website/README.md` and its declared scripts: clean npm
installation, type/content checks, production build and browser tests. Validate the
production artifact's routes, Markdown downloads, sitemap, metadata, theme behavior,
keyboard access and desktop/mobile layouts. Never fabricate a runtime screenshot or
weaken existing checks to accept a redesign. Generated output and dependencies are
not authored Markdown; the source checker excludes only declared generated paths.

## Delivery and publication

Keep the exact tested source identity and report what ran, what did not and what is
still running. Publish focused changes for review; never merge without explicit
approval for that change. A source implementation is not a deployed website. Verify
custom HTTPS routing and served assets after an authorized deployment before claiming
the domain is live or adding its URL to public discovery. Do not expose secrets in CI.

Collection tags, upstream product versions and skill metadata versions are distinct.
Do not move published tags, refresh installed user copies or relabel historical
results. Follow `docs/release-policy.md`; releases and social posts require their own
explicit authorization.
