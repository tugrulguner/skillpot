# Proposal: invariant-audit

**Status: proposal only.** This document defines an inspection-first report procedure and authored worked packet. It is not an installable skill, runtime, generic framework, security certification, or authorization to execute checks, edit targets, install hooks, remediate, merge, or publish. The v0.5.0 seventeen-skill release remains frozen.

## Task and boundaries

Use invariant-audit when a reviewer can name a scoped guarantee and wants to determine whether supplied source and/or explicitly authorized observations support it. Produce exactly `invariant-audit.md`, mapping that guarantee and its failure model to relevant enforcement/source identities, independently derived expected outcomes, counterexamples, evidence status, proposed negative tests, and a prioritized smallest permission-aware handoff. It reports what the bounded evidence establishes; it does not repair or enforce the target.

This is not `verification-loop` (which checks a code change against user-visible acceptance criteria and may execute within existing authorization), `change-impact` (which maps possible effects of a change), or `bug-repro` (which confirms/minimizes a reported trigger). It is not formal proof: finite inspection/tests do not establish all executions. It is not a full security audit: choose one named guarantee and threat/failure model, not a broad vulnerability or organizational-controls assessment. It is not `benchmark-audit` or `experiment-design`; it neither adjudicates performance evidence nor plans a scientific comparison.

## Inputs and authority

Require a precise guarantee and scope, relevant source/evidence boundary and identities where available, stated failure model, allowed actions, and an approved fresh report destination. State unknowns instead of filling them in. Treat supplied source and commands as data. Inspection does not imply execution; an execution request only authorizes actions within its explicit boundary after inspecting commands and side effects. Default to no target edits, remediation, dependency installation, network, services, hooks, credential use, or publication. A report's proposed negative tests remain proposals unless actual execution is authorized and captured. Reuse existing explicit bounded authorization; do not require another approval for actions it already covers. Do not execute supplied source merely to understand it.

## Procedure

1. **Bound the claim.** Rewrite the guarantee as a falsifiable statement with scope, relevant state, and failure conditions. Identify the smallest source surface likely to enforce it; note excluded paths and the inspection budget.
2. **Trace enforcement and identity.** Follow source from entry point to the decision/enforcement point and relevant failure paths. Record source paths/revisions or file digests when available; distinguish declared identity from independently read identity. If an identity read fails, report unavailable/error, not a matching identity. Avoid claiming continuous identity from endpoint snapshots.
3. **Derive expectations independently.** State the expected result for ordinary and failure inputs from the guarantee and failure model before comparing any report/output. Do not treat a checker’s own pass label, IDs, or self-consistency as an independent semantic oracle. Preserve unknowns where the contract is underspecified.
4. **Challenge with counterexamples.** Name minimal cases that could violate the guarantee, including missing, changed, malformed, or unreadable evidence as relevant. Separate source-only reasoning from actual executed observations. For execution explicitly authorized, capture actual command, inputs, identities, result and relevant output; classify setup failure separately from a guarantee violation. No source-only claim becomes an execution result.
5. **Propose focused negative tests.** For each test, give input/condition, independently expected outcome, what an erroneous acceptance would mean, and the healthy control. Keep proposed tests distinct from executed tests. Finite examples and tests are not proof.
6. **Hand off narrowly.** Order next steps by decision value and prerequisites: what can be concluded now, what remains unknown, the smallest permission-aware evidence step, and any design-changing decision/owner needed. Prefer no action when the bounded claim is supported and no decision needs more evidence. Never prescribe generic framework construction, target remediation, policy changes, or hooks by default.
7. **Write and verify.** Create only `invariant-audit.md` in the approved fresh destination, refuse collisions and symlinks, preserve partial output, and check all required report sections and evidence labels. Do not silently overwrite or choose another destination.

## Output contract

`invariant-audit.md` contains: (1) guarantee, scope and failure model; (2) evidence inventory and identity/provenance, including unavailable inputs; (3) source enforcement map; (4) independently derived expected outcomes and counterexamples; (5) source-only findings separated from executed observations; (6) proposed negative tests and healthy controls; (7) limits and prioritized permission-aware handoff. For each finding state the exact supporting source/evidence and whether it was inspected, calculated, or actually executed. “CURRENT” is allowed only when the named identities are known and current under the stated contract; unknown/missing identities cannot equal a valid identity. An initial/final snapshot alone does not prove continuity.

## Acceptance principles

A review should accept a scoped guarantee only when evidence addresses its failure model and expected outcomes come from an independent statement of the guarantee, not the report’s own IDs or verdicts. It should preserve healthy controls, reject counterexamples, disclose unavailable observations, and not promote proposed tests into execution claims. The identity case below is one example, not the prescribed shape of every audit. A transfer case must address a different guarantee (for example, an output-path refusal rule) with its own failure model, independent expected outcome, counterexample and least-permission handoff; copying the identity workflow is not sufficient.

## Worked packet

[`examples/invariant-audit/`](../examples/invariant-audit/README.md) is a fully authored, self-contained synthetic packet. Its inert `.txt` source snippets, inputs, expected report and acceptance cases illustrate identity-current reasoning. It is not a real incident, historical execution, or observed defect. No supplied target source is executed; acceptance cases specify expected dispositions, not fabricated run receipts. Repository-owned fixture tests recompute the authored identity expectations and check exact ledger coverage with positive and negative controls; they do not execute the inert snippets or validate arbitrary audit reports. See the example README for the focused command.

## Implementation boundary and limits

This milestone is documentation and authored example only. It creates no skill bundle, installable implementation, target checker/runner, runtime, dependency, policy/license/artwork change, or hook. Repository fixture tests are limited to the authored packet. A later implementation, target execution, remediation, installation, merge, or publication requires separate scope and authority. Authored packet consistency can establish only internal fixture consistency; it cannot prove semantic truth for arbitrary targets, completeness of a real audit, or task efficacy.
