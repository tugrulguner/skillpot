# Refpot consumer task — actual source-matched execution

The agent explicitly read the new `refpot-database` entry point and its pinned public
reference. It cloned the public source and checked out
`3294ce39f0e5630c660fad2e5a1e3977bf52a17f`, built/installed that source into a fresh
isolated CPython **3.11.12** environment, and imported Refpot **0.1.2** from that
venv's `site-packages`, not an accidental source import.

Host: macOS 26.5.2 arm64. The worker controller's Python 3.14.9 in provenance is not
the consumer interpreter; the isolated interpreter probe records 3.11.12 explicitly.
Skill, reference and setup-manifest hashes were recomputed by the parent and matched
[worker provenance](worker-provenance.json); source Git HEAD matched the public pin.

## What ran

[Worker command records](worker-commands.json) retain eleven actual subprocess
invocations, including the initial setup failure:

- `uv pip install --python .venv/bin/python .` from the source subdirectory failed:
  that venv existed in its parent, not inside `source/`.
- The corrected `--python ../.venv/bin/python` command built/installed the exact source.
  The failure remains in the log; it was not replaced by the retry.
- `examples/crud.py` passed, returning `Row(key=1, value=43, text='answer')`.
- `examples/transactions.py` passed, returning `Row(key=1, value=10, text='')`.
- The upstream repeatable example passed CRUD, explicit transaction commit/rollback,
  UTF-8 size rejection, checkpoint, close and reopen assertions.

The original worker example supplied a local temporary-directory override, so its
private bytes are not represented as a portable public file. The public
[portable fixture](../../../examples/modepot-project-skills/refpot_preview.py) removes
that machine-specific override and retains the original assertions. The parent
[separately executed it](parent-replay.json) with the same isolated installed package;
exit 0, same expected final row. Fixture hash and the distinction between the worker
attempt and parent replay are retained.

Public JSON replaces only the local workspace prefix. Original hashes, private
retention and redaction details are in [evidence provenance](evidence-provenance.json).
No stdout, error, failed attempt or source identity was rewritten into a pass.

## Boundaries

This is one bounded source-matched database task after explicit skill loading, not
a comparison against a baseline, native model activation, broad host/runtime matrix,
performance result, power-loss test or production/durability qualification. Other
products' consumer workflows were not exercised by this task. Native instruction
installation for all seven packages is [separate evidence](../native-install-001/README.md).

Only owned temporary/example data and a fresh scratch source/venv were used. Context
managers closed database handles and removed the temporary databases. Source checkout,
venv and evidence remain as owned test artifacts; no existing project, registered
Hermes profile, real database, release or merge was targeted. No process remains running.
