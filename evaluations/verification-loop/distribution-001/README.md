# Verification-loop selective distribution

Actual filesystem replay using Skills CLI 1.7.6 and Node 22.23.4 against the immutable pin in [summary.json](summary.json). A fresh owned project and isolated installer home were used; no active agent profile was modified and no client/model was launched.

Executed standard CLI add with `--skill verification-loop --agent claude-code cursor codex hermes-agent --yes`, list, and selected remove. All six installed files matched the source bytes. Only the selected bundle and a pre-existing owned sibling appeared in the shared skill root. The source lock contained the exact requested commit. Claude Code and Hermes had links resolving to the shared bundle; Cursor/Codex use the shared directory. Removal removed the selected directory/lock entry and preserved the sibling.

The parent retained complete directly captured command/cwd/exit/stdout/stderr receipts privately because they contain machine-local paths. This public summary contains source-relative hashes and qualified outcomes only; it is an authored summary of observed execution, not the raw log. JSON formatting differs from the private summary; source hashes are unchanged. The initial classification-only draft was replaced before this distribution run; no claim is made that that draft verified an application.

Distribution establishes placement, complete-byte parity and selected removal. It does not establish native loading, automatic skill selection, safety enforcement or task efficacy. Installer updates may overwrite user edits; report-destination refusal belongs to the procedure, not the installer.
