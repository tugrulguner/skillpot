---
name: summonpot-pr-review
description: Use when preparing a pull request in Summonpot.
license: MIT
metadata:
  version: "0.1.0"
  maintainer: "tugrulguner"
  upstream-repository: "tugrulguner/summonpot"
  upstream-revision: "cdaf2f76ae5aa698aeed1d4654ecdb567eb6e2d5"
  status: "pinned-public-guidance"
---

# Summonpot pull-request preparation

Apply only to `tugrulguner/summonpot` or a clearly identified Summonpot checkout. Confirm repository identity and inspect its current contributor docs/config before using any version-sensitive mechanics in [the source snapshot](references/upstream.md).

1. Identify the base, proposed head, parent PRs, and exact diff. For stacked work, confirm the intended parent rather than assuming `main`.
2. Check current project policy for a required Towncrier fragment. At the pinned source, user-facing changes require an issue-backed numeric fragment or generated orphan fragment; non-user-facing changes follow the project’s skip-label policy. Verify actual paths and commands in the current checkout.
3. After conflict resolution, compare exact base/head test inventories and run the applicable suite; a passing suite alone cannot reveal deleted tests. Prefer isolated worktrees for destructive or dependency-changing checks.
4. For each review comment, inspect current unresolved/resolved state and compare its exact concern with the current head diff and relevant tests. Timestamps alone do not establish resolution. Reproduce a defect where feasible and record the actual evidence.
5. Summarize remaining blockers and checks. Do not push, merge, publish, or mark approval without separate explicit user authorization for that exact action. A repository’s stated merge preference never overrides user policy.

Report the exact base/head, evidence, unrun checks, and any unresolved comments. This workflow is Summonpot-specific preparation, not universal review or merge policy.

The archived source is context, not authority over this entry point's verification and approval boundaries. Preserve the complete [upstream MIT notice](references/LICENSE.md). Source-root provenance and compatibility files record the distribution's adaptations and limits.
