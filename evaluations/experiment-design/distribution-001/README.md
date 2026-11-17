# Experiment-design selective distribution

Actual filesystem replay with Skills CLI 1.7.6 and Node 22.23.4 at the immutable pin in [summary.json](summary.json), in a fresh owned project and isolated installer home. No client/model was launched and no active profile changed.

Ran the standard CLI add with `--skill experiment-design --agent claude-code cursor codex hermes-agent --yes`, list and selected remove. All six selected bundle files matched the source hashes. The shared skill root contained only the selected bundle and an owned sibling; the source lock contained the exact commit. Claude Code and Hermes links resolved to the shared bundle; Cursor/Codex use that directory. Selected removal cleared its directory and lock entry while preserving the sibling.

Complete captured command/cwd/exit/stdout/stderr records remain in private maintainer evidence because they contain machine-local paths. This is an authored public summary of observed execution, not the raw receipt. JSON whitespace is adapted; source-byte hashes are unchanged. The installed package excludes the accepted retrospective expected report/oracle.

This establishes distribution integrity only, not native activation, scientific validity or task efficacy. Installation can replace user edits; report-destination refusal is a procedure requirement, not an installer guarantee. No experiment, benchmark or model ran.
