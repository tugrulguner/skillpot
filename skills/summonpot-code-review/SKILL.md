---
name: summonpot-code-review
description: Use when reviewing a Summonpot code change.
license: MIT
metadata:
  version: "0.1.0"
  maintainer: "tugrulguner"
  upstream-repository: "tugrulguner/summonpot"
  upstream-revision: "cdaf2f76ae5aa698aeed1d4654ecdb567eb6e2d5"
  status: "pinned-public-guidance"
---

# Review a Summonpot change

This checklist is scoped to Summonpot. Confirm repository and version first; inspect the exact base/head diff, current implementation, tests, README, roadmap, and current public API. Archived [upstream guidance](references/upstream.md) is context, not authority over contradictory current code.

1. **Documentation vs shipped behavior:** verify each API/runtime claim against source and executable tests. Version-specific claims must identify the relevant release.
2. **Validation guards:** test both rejection of invalid declarations and acceptance of valid edge cases; avoid false positives.
3. **Failure timing:** verify invalid contracts fail at registration when promised, not after traffic/effects begin.
4. **Regression quality:** establish that new tests fail without the fix where practical; check exact assertions and test inventory against the base. Use isolated worktrees for test-only/red checks and clean up safely.
5. **Information exposure:** inspect response bodies and logs for exception/provider text, prompts, inputs, outputs, or capability data contrary to the current redaction contract.
6. **Typed bindings:** verify source provenance, declared output types, choice bounds, response validation, and whether the exact contract is in the supported execution slice. Do not infer behavior from type declarations alone.
7. **Effect and timeout safety:** ensure capabilities are application-owned and authorized; uncertain timeout outcomes are not treated as rollback or exactly-once guarantees.
8. Run the project-prescribed checks appropriate to the diff (the pinned guidance names `make check`); record commands and actual outputs. Parse workflow YAML if changed.

Deliver prioritized findings with file/line locations, reproduction/evidence, severity, and checks not run. If no finding is evidenced, state the scope and limits of review. Never push, merge, publish, or approve without separate explicit user authorization.

Preserve the complete [upstream MIT notice](references/LICENSE.md). Source-root provenance and compatibility documents record this distribution's adaptations and limits; packaging alone does not prove host activation or runtime behavior.
