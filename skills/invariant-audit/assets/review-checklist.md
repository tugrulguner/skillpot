# Review checklist

- [ ] One falsifiable guarantee, bounded scope and explicit failure model.
- [ ] Source/evidence inventory records declared and independently read identities; unavailable stays unknown.
- [ ] Enforcement path and relevant failure branches traced to exact source.
- [ ] Expected outcomes derived from the guarantee independently of checker labels/IDs.
- [ ] Minimal failure cases and unchanged healthy controls are both considered; rejection for an unrelated reason or a failed healthy control does not qualify the intended check.
- [ ] Findings distinguish inspected/calculated source-only reasoning from actual execution; no invented run receipts.
- [ ] Any execution was explicitly authorized, bounded, inspected for side effects, and records command, inputs, identities and result.
- [ ] `CURRENT` is used only with known valid current identities; snapshots do not imply continuity.
- [ ] Proposed tests are not represented as executed; setup failure is not a guarantee violation.
- [ ] Report has all seven required sections and a prioritized least-permission handoff.
- [ ] Only the approved fresh `invariant-audit.md` was created; collisions/symlinks refused, partial output preserved.
- [ ] No target edits, installation, hooks, network, credentials or publication occurred without explicit authority.
