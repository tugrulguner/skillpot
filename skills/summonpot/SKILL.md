---
name: summonpot
description: Use when building or changing a Summonpot API.
license: MIT
metadata:
  version: "0.1.0"
  maintainer: "tugrulguner"
  upstream-repository: "tugrulguner/summonpot"
  upstream-revision: "cdaf2f76ae5aa698aeed1d4654ecdb567eb6e2d5"
  status: "pinned-public-guidance"
---

# Build with Summonpot

Use this procedure when implementing an API endpoint in a repository that uses Summonpot. Do not use it as generic agent-framework guidance.

## Inputs and readiness

- Inspect the project’s installed Summonpot version, dependency lock, existing endpoint patterns, and relevant current public documentation/source. Do not assume archived details in [upstream guidance](references/upstream.md) still apply unchanged.
- Confirm the desired route/method, validated request shape, fixed endpoint goal, exact operations the application owns, response model, and which individual values genuinely require an agent choice. Ask for missing contract or authorization requirements before implementing.
- Identify tests and safe local checks. Never use fabricated provider output as evidence.

## Procedure

1. Define the typed request and response models and endpoint goal. In Summonpot, a decorated declaration body uses `...`; it is not a handler to implement or call directly. Route execution through the framework’s served HTTP endpoint.
2. Keep business effects in application-owned callables. Grant only exact capabilities required for this endpoint; enforce authorization inside each capability. Never expose ambient database/session, shell, filesystem, or arbitrary SQL authority.
3. Prefer typed `Operation` bindings when input provenance/order is part of the contract. Bind validated request/result values explicitly; mark only bounded semantic decisions as agent-owned. Unsupported explicit shapes must fail closed, not be silently broadened.
4. Determine the execution path from the exact installed version and contract. Eligible fully resolved `Exactly(1)` operations/sequential chains may run model-free under narrow predicates; producer-backed choices and legacy capabilities remain agent-mediated. Do not claim a path based only on this skill.
5. Bound model-backed execution with configured usage limits and a deadline; bind local development to loopback. Summonpot has no built-in authentication in the pinned snapshot. Before network exposure, establish authentication and operational controls with the service owner.
6. Test registration failures, request/response validation, capability arguments/effects, and both supported execution paths as applicable. Prefer the keyless test model only for safe wiring tests; it can invoke capabilities with generated placeholder inputs and is not a dry-run sandbox.
7. Review timeout/uncertain side effects and idempotency. A timeout does not prove an effect did not occur; applications own transactions and cross-request idempotency.

## Verify and stop

- Run focused tests and project-prescribed checks; report exact commands and actual exit/results. Use independent inspection of persisted state for effectful examples.
- Check generated OpenAPI/HTTP shape when routes change, and compare the diff against existing behavior. Distinguish tests run from tests merely recommended.
- Stop if current runtime behavior is unclear, credentials/permissions are unavailable, tests would invoke unsafe effects, or the request requires unsupported framework semantics. Do not invent live provider results or report a provider call that did not occur.
- Report changed files, verified behavior, execution path/version evidence, unresolved risks, and unrun checks.

## Boundaries

This procedure is guidance, not a sandbox or permission system. The host agent and application owner control tool use and authorization. The pinned source and complete [MIT notice](references/LICENSE.md) are bundled references; source-root provenance and compatibility documents record packaging limits, not host or runtime qualification.
