# Codex-created Intpot CLI verification

This is the byte-identical verifier created and executed by a real Codex CLI session
using the project's public Intpot skills. It is an application example, not a SkillPot
runtime or a Codex-specific implementation of those skills. The same Python verifier
can be executed by another harness or by a person with the required environment.

It exports the supplied native invoice App through both the Intpot CLI and Python
`App.eject("cli")`, compiles/imports the results, and invokes both CLIs. It checks four
valid and three invalid cases for each export and retains command output and assertion
records. It does not exercise HTTP, MCP, foreign-framework conversion, another OS,
or a minimal target environment with Intpot removed.

## Run in a new owned project

Copy `invoice.py` and `verify_invoice.py` together into a fresh project outside your
SkillPot source checkout. The verifier deliberately writes a new `scratch/` subdirectory
beside these files; preserve that evidence privately, not as incidental library source.
Use the host's normal permissions and an approved environment. Never bypass approvals
to make this example pass.

With permission to obtain public source/dependencies:

```sh
ENV=/absolute/owned-parent/new-intpot-environment
uv venv --python 3.12 "$ENV"
uv pip install --python "$ENV/bin/python" "intpot[api] @ git+https://github.com/tugrulguner/intpot.git@8e583cc4b2b6785955268d09a12dfdd955194b88"
# From the new project containing the two copied files:
"$ENV/bin/python" -B verify_invoice.py
```

Choose an environment path that does not already exist. No dependency installation
or network access is performed by the verifier itself. A failed `pip show` is retained
and handled by an installed-distribution metadata probe; it is not a request to install
pip automatically. Raw records may include local paths, so review/redact them before
publication while retaining the original hashes and failures.

To try the workflow in an agent, first install the complete selected skills using the
[harness-neutral quickstart](../../../docs/quickstart.md). In Codex, mention
`$intpot-cli` and `$intpot-python` explicitly. In Claude Code, invoke the corresponding
`/intpot-cli` or `/intpot-python` project skill; in Cursor, select the skill through `/`.
Those host-specific entry points do not change the package contents.

[Actual native execution and parent replay](../../../evaluations/harness-portability/explicit-codex-001/README.md)
are deliberately separate from placement checks and unsuccessful host launches.
Copyright/permissions for SkillPot examples are covered by the root [MIT notice](../../../LICENSE);
Intpot retains its [complete upstream notice](../../../skills/intpot-python/LICENSE).
