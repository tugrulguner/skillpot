# Contributing to SkillPot

Start with the [README](README.md) and [roadmap](ROADMAP.md). SkillPot is in development;
there are no released skills, install commands, or established compatibility results yet.

## Propose a real task

Use [GitHub Issues](https://github.com/tugrulguner/skillpot/issues) for scoped work.
For exploratory discussion, join the [ModePot Discord](https://discord.gg/u3AANZr6RG).
Before substantial implementation, describe:

- Who has the task and how they handle it today.
- Representative inputs you have permission to share.
- The expected artifact and explicit acceptance checks.
- The strongest applicable existing skill or workflow.
- Prerequisites, external services, costs, permissions, and failure modes.
- How you will compare results and maintain the skill as its tools change.

Do not attach credentials, private code, personal records, or proprietary instructions.
Focused documentation and artwork fixes may be proposed directly as pull requests.

## Skill quality bar

Skills must encode a reusable procedure, not a persona or an answer to one fixture.
Keep the entry point concise and load references when needed. Include practical
resources where they help, explicit review boundaries, realistic examples, and recovery
steps. Record unsupported situations rather than silently improvising success.

Check both activation and results. Evaluate with and without the skill under matched
conditions, include repeated runs and held-out inputs, and compare a relevant incumbent.
Separate deterministic checks from human or model judgment. A structural lint pass
is not evidence of improved task performance. Never invent transcripts or measurements.

## Provenance and safety

Submit your own work or material you are allowed to redistribute. State sources and
license obligations. Do not copy a skill merely because its repository is public;
individual directories may have different terms.

Audit any proposed extraction from existing projects against current behavior. Remove
personal paths and private context. Preserve a canonical upstream source where possible.
Disclose executable scripts, network access, dependencies, credentials, paid services,
and side effects. The agent host controls execution; a skill is not a sandbox.

## Working on this repository

```sh
git clone https://github.com/tugrulguner/skillpot.git
cd skillpot
```

The current repository contains Markdown and artwork; it has no runtime package,
package installation step, or committed task-evaluation runner. For a documentation change:

1. Check local links, heading anchors, and current-versus-planned wording.
2. Preview the README and confirm artwork loads at the intended display size.
3. Keep SVG sources and PNG renderings in sync; follow [the artwork guide](assets/README.md).
4. Run `git diff --check`.
5. Describe the exact scope and verification in the pull request.

Do not add product code or skills as incidental scaffolding to a documentation change.
When executable skills arrive, their setup and canonical verification commands must be
introduced alongside their actual implementation.

## Reviews and publishing

Keep changes small enough to review. Explain the outcome, changed files, source
permissions, verification performed, and remaining limitations. Do not mark roadmap
items complete merely because a design exists. Public posting, paid actions, releases,
and repository merges remain separate maintainer decisions.

Contributions to this repository are provided under its [MIT License](LICENSE), except
where an explicitly identified third-party license applies. Disclose such material before
submission; do not change the project's license as part of an unrelated contribution.
