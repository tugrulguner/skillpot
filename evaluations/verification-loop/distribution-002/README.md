# Verification-loop 0.2.0 selective distribution

Fresh filesystem replay with Skills CLI 1.7.6 and Node 22.23.4 at the pin in [summary.json](summary.json). A new owned project and isolated installer home were used. Add/list/remove ran with selected `verification-loop` and explicit Claude Code, Cursor, Codex and Hermes targets; no clients/models launched or active profiles changed.

All eight selected files matched source bytes, the source lock contained the exact commit, and no unselected bundle appeared. Claude Code/Hermes links resolved to the shared bundle; Cursor/Codex use that directory. Selected removal cleared its directory/lock entry and preserved an owned sibling. Raw captured command/cwd/exit/stdout/stderr receipts remain private because of machine-local paths. This public summary adapts JSON whitespace only, not source hashes; it is a bounded summary, not raw evidence.

The earlier [distribution-001](../distribution-001/README.md) record is preserved unchanged at its original 0.1.0 pin. It does not qualify the new recipe/rule assets. This fresh replay covers the revised complete bundle and its selected removal, not native activation, permission enforcement or task efficacy. Installer replacement risk remains separate from report collision refusal.
