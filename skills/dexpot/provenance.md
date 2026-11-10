# Provenance

Canonical source: [Dexpot consumer guide](https://github.com/tugrulguner/dexpot/blob/a670e626cf73e1c4b21e0529294a87f1aa83e74f/src/dexpot/templates/skills/dexpot.md).
Repository: `tugrulguner/dexpot`. Revision: `a670e626cf73e1c4b21e0529294a87f1aa83e74f` (published Dexpot v0.8.1).

- Original path: `src/dexpot/templates/skills/dexpot.md`.
- Unmodified snapshot: `references/upstream.md`.
- Snapshot SHA-256: `064792cb9897483af66fa1199cbcf4be97cc3e26417533dbb87a36e471a3fa0d`.
- Upstream MIT LICENSE SHA-256: `44c84c4f83c7c902b4d7d96ae40b395b4a9c943c1a145e7db92928ba2f21c958`.
- Complete notice is retained in both `LICENSE` and `references/LICENSE.md` so direct
  URL installation preserves redistribution rights with the installed reference.

Adaptation: original portable entry point summarizes the task, source-matched setup,
permissions, source/API checks, real HTTP verification and bounded reporting. The API
reference itself is unchanged; no private skill or unpublished procedure is included.
No raw source-speed, production, concurrency or compatibility result is inferred from
this packaging. Upstream Dexpot owns API truth; SkillPot distributes a pinned snapshot,
not an independently evolving fork. Maintainer of this distribution: `tugrulguner`.

The selected release adds the supported-path annotation allowlist and registration-time
`TypeError` correction in Dexpot 0.8.1. The portable entry point spells out that boundary,
the migration alternative and the distinction from body/response schemas. Instruction
version `0.3.0` raises the required product version to 0.8.1+. Existing 0.8.0 lifecycle
guidance remains; lifecycle/thread cleanup limits are documentation, not runtime qualification.
Main-only typed query/header/cookie inputs are not imported.

This source refresh is not in published SkillPot v0.4.1, whose Dexpot package remains
at instruction 0.2.0 and the earlier v0.8.0 pin. Earlier installed/task records keep their
original identities. See the [current refresh record](https://github.com/tugrulguner/skillpot/blob/203e942848b33ca5b1250b99d17536a19c145a5c/docs/published-upstream-refresh.md).

- Audited upstream license SHA-256: `44c84c4f83c7c902b4d7d96ae40b395b4a9c943c1a145e7db92928ba2f21c958`; complete MIT notices remain byte-identical.

Refresh only by inspecting the new immutable public source and license together,
reviewing changed guidance against its implementation, updating both catalog hashes
and references, and rerunning checks. Never refresh a moving branch silently.
