# ModePot project consumer examples

The packaged skills live in `skills/`; installing instructions does not install their
underlying Python projects. Use approved isolated environments, never an existing user
application or important data as incidental fixture input.

## Refpot preview

[refpot_preview.py](refpot_preview.py) is a portable adaptation of the repeatable
example in the [pinned public guide](../../skills/refpot-database/references/upstream.md).
It checks CRUD, transaction rollback, UTF-8 text limits, checkpoint and reopen behavior.
Copyright/permission notice: [Refpot MIT license](../../skills/refpot-database/LICENSE).

With permission to fetch/build public source, choose a **new** external environment
path and use its actual Python executable. For a POSIX shell, from the SkillPot root:

```sh
ENV=/absolute/owned-parent/new-refpot-example-env
uv venv --python 3.11 "$ENV"
uv pip install --python "$ENV/bin/python" "refpot @ git+https://github.com/tugrulguner/refpot.git@3294ce39f0e5630c660fad2e5a1e3977bf52a17f"
"$ENV/bin/python" examples/modepot-project-skills/refpot_preview.py
```

A source build needs the public project's declared C++17 build toolchain. Respect its
supported OS/architecture/interpreter range and approved dependency policy. If you
choose a source subdirectory for installation, keep the interpreter path absolute
(or correctly relative to that working directory); do not accidentally target a venv
that lives somewhere else. Do not overwrite an existing environment.

The final row should be `Row(key=1, value=43, text='answer')`, but inspect the actual
exit code and assertions rather than copying that expected result into a report.
Temporary storage makes reruns independent; Python's normal temporary-directory policy
applies, so set `TMPDIR` to an approved scratch location when required.

[Retained actual execution](../../evaluations/modepot-project-skills/refpot-consumer-001/README.md)
includes the worker's failed setup/retry, the upstream shipped examples and a separate
parent replay of this exact portable fixture. It is not a speed, durability, usefulness
or broad compatibility claim.

## Intpot CLI export and Python conversion

Use a new external Python 3.12 environment and a new evidence destination:

```sh
ENV=/absolute/owned-parent/new-intpot-example-env
uv venv --python 3.12 "$ENV"
uv pip install --python "$ENV/bin/python" "intpot[api] @ git+https://github.com/tugrulguner/intpot.git@8e583cc4b2b6785955268d09a12dfdd955194b88"
"$ENV/bin/python" examples/modepot-project-skills/intpot/verify.py --evidence /absolute/owned-parent/new-intpot-evidence
```

The [native App](intpot/invoice.py) is exported with the CLI; the
[trusted Typer source](intpot/foreign_cli.py) is inspected and converted through Python.
The [verifier](intpot/verify.py) checks three quotation cases through standalone CLI
and two real loopback HTTP applications, plus invalid CLI/input rejection and cleanup.
Native API export returns the scalar directly; framework conversion wraps it as
`{"result": ...}` and preserves the public `discount-cents` option alias. These are
not identical wire formats. No scaffold opt-in or fake service output is used.

## Dexpot typed HTTP contracts

```sh
ENV=/absolute/owned-parent/new-dexpot-example-env
uv venv --python 3.12 "$ENV"
uv pip install --python "$ENV/bin/python" "dexpot[cli] @ git+https://github.com/tugrulguner/dexpot.git@ca4979a6339e533f11ad135bc760aa081f3f60ab"
"$ENV/bin/python" examples/modepot-project-skills/dexpot/verify.py
```

The [application](dexpot/app.py) and [verifier](dexpot/verify.py) test real HTTP success,
invalid bodies, typed paths and response filtering. The owned subprocess is stopped
in `finally`, and the listener is checked closed. The temporary port reservation is
released before startup; a bind race is a failed run, not authority to kill another
listener. This is not a scheduling, overload, native-parser or throughput benchmark.

## Summonpot deterministic operation

```sh
ENV=/absolute/owned-parent/new-summonpot-example-env
uv venv --python 3.12 "$ENV"
uv pip install --python "$ENV/bin/python" "summonpot[serve] @ git+https://github.com/tugrulguner/summonpot.git@cdaf2f76ae5aa698aeed1d4654ecdb567eb6e2d5"
"$ENV/bin/python" examples/modepot-project-skills/summonpot/verify.py
```

The [application](summonpot/invoice_app.py) declares a bounded `Operation` with explicit
request bindings and `Exactly(1)`. The [verifier](summonpot/verify.py) checks live HTTP,
request rejection, capability arguments/count, invalid registration and cleanup. A
pinned-runtime test guard rejects entry into the model-backed branch; it does not
fabricate a provider response. This tests only the eligible deterministic path, not
provider-backed choices, authentication or broad compatibility.

## Evidence and scope

[Consumer run records](../../evaluations/modepot-project-skills/consumer-tasks-001/README.md)
separate initial worker failures, interrupted verification, parent-assisted replays
and the failed native host-loading attempts. These scripts are executable fixtures,
not a new runner, installer or evaluation platform. Current source CI validates the
collection; it does not install all three product environments or execute these HTTP
tasks on every platform. Permission to build dependencies and bind loopback is required.
Use a separately approved scratch policy (`TMPDIR` on POSIX) when needed.
