# Initial source audit

Status: bounded inventory and source review, not runtime qualification or extraction.
No source instructions have been copied into a published SkillPot skill.

This is a historical snapshot. Its project-to-demo recommendation was superseded by
the [repository-readiness proposal](repository-readiness-proposal.md); its video-tooling
discussion is not a prerequisite for current SkillPot work. The new skill is original,
not an extraction of the inventoried product guides.

## Method and scope

Read GitHub repository metadata, complete recursive default-branch trees (all reported
`truncated: false`), source skill Markdown, and root licenses. Search included both
`SKILL.md` and Markdown templates under paths containing `skills`; searching only for
`SKILL.md` misses the product-shipped templates. Immutable revisions below identify the
inventory snapshot. Seven repositories were inspected; seven candidate Markdown files
were found across four repositories. Counts exclude this repository and private skills.

The public repositories' root licenses are MIT: Intpot credits intpot contributors;
the other inspected projects credit Tugrul Guner. No separate license file was found
under the inventoried skill directories. This is initial license evidence, not a legal
certification or permission to copy third-party material referenced by those documents.
Preserve applicable copyright and permission notices on any future extraction.

## Inventory and recommendations

### Intpot — retain upstream; refresh before any redistribution

Revision: `8ef249f1b044afc086ec3488d3b1588f9f932525`.

- [CLI skill template](https://github.com/tugrulguner/intpot/blob/8ef249f1b044afc086ec3488d3b1588f9f932525/src/intpot/templates/skills/intpot-cli.md)
- [Python skill template](https://github.com/tugrulguner/intpot/blob/8ef249f1b044afc086ec3488d3b1588f9f932525/src/intpot/templates/skills/intpot-python.md)
- [License](https://github.com/tugrulguner/intpot/blob/8ef249f1b044afc086ec3488d3b1588f9f932525/LICENSE)

Both are product API guidance, not a complete cross-product demo workflow. Keep Intpot
as their canonical owner. The CLI template contains an older categorical statement
that same-module helpers/constants are not copied, followed by a newer bounded helper
recovery section explaining when they are. Reconcile those descriptions before reuse;
do not simplify the current behavior to either universal recovery or universal refusal.
Published-versus-source availability labels also require rechecking at extraction time.
No Intpot conversions or generated consumers were executed in this audit.

### Summonpot — retain upstream; keep contributor and consumer guidance separate

Revision: `1c2c7a3da4ce55088613b5a78e29bfb0aa85503b`.

- [PR mechanics](https://github.com/tugrulguner/summonpot/blob/1c2c7a3da4ce55088613b5a78e29bfb0aa85503b/.claude/skills/pr-review/SKILL.md)
- [Code review](https://github.com/tugrulguner/summonpot/blob/1c2c7a3da4ce55088613b5a78e29bfb0aa85503b/.claude/skills/review-code/SKILL.md)
- [Consumer skill template](https://github.com/tugrulguner/summonpot/blob/1c2c7a3da4ce55088613b5a78e29bfb0aa85503b/src/summonpot/templates/skills/summonpot.md)
- [License](https://github.com/tugrulguner/summonpot/blob/1c2c7a3da4ce55088613b5a78e29bfb0aa85503b/LICENSE)

Source cross-check: the CI workflow targets `main` for pull requests; `Makefile` defines
`make check`; `pyproject.toml` defines Towncrier and the documented Python range and
server/CLI/provider extras. Those align with selected contributor/setup instructions.
The PR skill's advice to prefer merge commits is project-specific and must not become
a SkillPot merge policy. Its timestamp heuristic cannot establish that an old review
comment was actually addressed. The consumer template is detailed, changing API guidance;
keep its version-sensitive capability and runtime boundaries canonical upstream. No
provider call, server, registration contract, or full quality suite was executed here.

### Dexpot — retain upstream

Revision: `ca4979a6339e533f11ad135bc760aa081f3f60ab`.

- [Consumer skill template](https://github.com/tugrulguner/dexpot/blob/ca4979a6339e533f11ad135bc760aa081f3f60ab/src/dexpot/templates/skills/dexpot.md)
- [License](https://github.com/tugrulguner/dexpot/blob/ca4979a6339e533f11ad135bc760aa081f3f60ab/LICENSE)

The CLI source confirms the `serve` entry and explicit host/port flags with loopback
host default. The template includes runtime, parser, scheduling, and benchmark rules
that would drift if duplicated. It is not a browser-demo workflow. Detailed runtime
claims and application behavior still need the project's real socket tests; no such
execution is claimed by this inventory.

### Refpot — retain upstream; adapt metadata only if separately packaged

Revision: `3294ce39f0e5630c660fad2e5a1e3977bf52a17f`.

- [Database skill](https://github.com/tugrulguner/refpot/blob/3294ce39f0e5630c660fad2e5a1e3977bf52a17f/skills/refpot-database/SKILL.md)
- [License](https://github.com/tugrulguner/refpot/blob/3294ce39f0e5630c660fad2e5a1e3977bf52a17f/LICENSE)

The package contract agrees with the documented signed-integer/UTF-8 bounds, explicit
transactions, thread/process ownership, experimental status, and unsupported SQL/ORM.
Its nested Hermes metadata and extra host-oriented frontmatter should not be copied
as portable Agent Skills metadata. Installation/examples and durability behavior were
not executed; platform and package-publication statements need renewed verification
before any distribution change. Keep database-specific instructions with Refpot.

### Repositories with no candidate skill Markdown in this snapshot

- Utilitypot: `dc3fd03aa1a1593bb26001ebb72cd720424eb1dd`.
- Lifepot: `9445b1f212a9d764333d6413077952d5635e86a5`.
- Strpot: `510c04156a8d72ac1c76ead1657e6c470814f371`.

All three have root MIT licenses. No candidate `SKILL.md` or skill-path Markdown was
found in their complete trees. This does not mean they contain no guidance, examples,
or reusable knowledge; none was extracted or proposed for distribution here.

## First-workflow sources not ready to redistribute

The maintainer's local project-video procedure is the closest conceptual candidate
for generalization: source/revision reconciliation, causal capture, truthful claims,
separate capture/render, encoded-frame review, and approval boundaries. It also contains
personal storage conventions, product-specific requirements, and dependencies on a
local unpublished video kit. Treat it as an audit lead, not licensed public input.
No private collection or kit code is copied into this change.

The kit README was successfully recovered from a cloud placeholder and read. It names
Node.js, Python 3.11+, Playwright, Pillow, FFmpeg/ffprobe and existing test commands.
The kit implementation, package provenance, dependency installation, tests, and actual
capture/render remain unaudited here. It is therefore not yet a clean-install public
dependency. Do not replace it with a new renderer just to conceal that prerequisite.

## Decision and remaining gates

Recommend generalizing only the project-to-demo procedure for the first experimental
SkillPot workflow. Retain all seven inventoried product/contributor files upstream;
this audit recommends no bulk import and retires no upstream skill. Product-specific
accuracy concerns belong upstream, not in drifting SkillPot copies.

The inventory and recommendations are complete for this snapshot. Full command/API
freshness, failure-path testing, rights clearance for local material, and canonical
ownership of any extracted tooling remain open. Follow the
[first-workflow proposal](first-workflow-proposal.md) before implementation. The roadmap
must not mark these execution or redistribution gates complete from this document alone.
