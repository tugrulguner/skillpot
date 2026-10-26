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
or broad compatibility claim. Other product tasks require their own execution evidence.
