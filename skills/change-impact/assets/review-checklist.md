# Change-impact review checklist

- [ ] Confirm literal repository, base, head or supplied-diff identity; state exact comparison mode.
- [ ] Inspect old/new blobs at pinned revisions; use no mutable worktree substitution.
- [ ] Inventory all changed paths, including rename/delete/binary/generated limitations.
- [ ] For every changed path, record an impact ID or reasoned exclusion/unchecked boundary.
- [ ] Reconcile IDs bidirectionally; no orphan, duplicate, or wrong-file mapping.
- [ ] Cite old/new source and relevant callers, contracts, configuration, docs and tests with path and line ranges.
- [ ] Separate Direct change, Source-linked (static only), Potential, and Unknown.
- [ ] Distinguish demonstrated effects, suspected dependencies, and unknowns; imported names do not prove execution.
- [ ] Treat dynamic dispatch/string matching as Potential/Unknown; enumerate external-consumer limits.
- [ ] Record compatibility risks and relevant tests without asserting missing tests are bugs.
- [ ] For each check, report exact command, prerequisites, permissions, expected observation, target identity and execution state.
- [ ] Keep unrun checks Not run; smoke checks do not establish full behavior.
- [ ] Before either output write, refuse existing files/dirs and live/dangling same-name symlinks; ensure fresh approved output is external to target.
- [ ] Produce exactly impact.md and verification.md; no source changes or fabricated results.
- [ ] Do not claim runtime reachability, security completeness, activation, performance, or exhaustive consumer coverage.
