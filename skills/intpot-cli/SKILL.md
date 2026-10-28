---
name: intpot-cli
description: Use intpot CLI to scaffold, inspect, or convert Python apps.
license: MIT
metadata:
  version: "0.2.0"
  maintainer: "intpot contributors"
  upstream-repository: "tugrulguner/intpot"
  upstream-revision: "3d784e8dd5f1c45b7b2abfac21450aa17efad52c"
  status: "pinned-public-guidance"
---
# intpot CLI

Use the `intpot` command for project scaffolding, serving `intpot.App`, inspecting trusted framework apps, and conversion/ejection. This procedure covers consumer workflows; detailed product behavior and version-specific API are in [the pinned upstream guide](references/upstream.md).

## When to use
- User requests CLI-based setup, serving, inspection, or conversion among Typer, FastAPI, and FastMCP.
- Use `intpot-python` for Python API operations inside a script or codebase.
- Do not convert code the user does not trust; discovery imports and executes source modules.

## Setup and version check
1. Use the project's existing environment and dependency policy. Install `intpot` there, or install `intpot[api]`, `intpot[mcp]`, or `intpot[all]` when the source/target framework must be loaded or run.
2. Check `intpot --version` and `intpot --help`; consult the pinned guide for required feature versions. If the package is older than a feature's stated minimum, do not assume it exists. When published release diverges from this pinned snapshot, use a matching upstream source checkout at the pinned revision or a compatible published version; never silently mix docs and runtime.
3. Confirm source and intended output paths. Preserve existing files; use `--dry-run` for conversion previews.

## Procedure
1. For a new project, run `intpot init <name> --type cli|api|mcp` with one type; inspect generated files.
2. For an existing `intpot.App`, run `intpot serve <file.py> --cli|--api|--mcp`. CLI tool arguments follow mode flags; use `--` if app flags collide with intpot options. API defaults to loopback; network exposure requires an explicit host choice.
3. For framework conversion, run `intpot inspect <source> --json` (or the table form), review extracted tools and diagnostics, then run `intpot to cli|api|mcp <source> [--output ...]`. Preview with `--dry-run`. For standalone export from an `intpot.App`, use `intpot eject <source> --to cli|api|mcp`.
   `inspect` discovers existing framework instances, not native `intpot.App` declarations. A native App's inspect refusal does not establish that its documented serve/eject path is blocked; inspect a trusted Typer/FastAPI/FastMCP source when testing framework conversion.
4. Treat refusals as meaningful. Missing bodies/bindings, CLI callbacks, FastAPI dependency injection, and other unsupported cases can prevent conversion before writes. `--allow-scaffold` only opts into explicitly failing `NotImplementedError` stubs for eligible missing-body recovery; it does not bypass callback, dependency, or binding refusals. Never present a scaffold as working output.
5. Verify every generated file: compile it, import it in the target runtime environment, and execute a representative CLI invocation, API request, or MCP tool call. Help text, generation success, and compilation alone do not prove behavior.

## Failure boundaries and safety
- Inspection/conversion imports trusted source. `--dry-run` prevents generated output writes, not source execution; it is not a sandbox.
- Before retrying a refusal, check output is absent/unchanged. Avoid overwriting user output without consent.
- Direct file loading may not put the source directory on `sys.path`; sibling imports can require installing the project or setting `PYTHONPATH`. Intpot does not provision services/configuration.
- Recovery scope is version-dependent and bounded. The pinned snapshot documents v0.11 helper recovery for required undecorated functions and immutable literal constants, including supported transitive helpers. It excludes mutable/dynamic state, closures, classes and other unsupported dependencies. Do not repeat older blanket claims that all same-module helpers are unsupported, nor infer universal helper copying. Consult the versioned reference and actual diagnostics.
- Framework semantic gaps remain, including nested Typer sub-apps, repeatable CLI options, certain FastAPI parameter forms, factory apps, multi-method routes, callbacks, and dependencies.

## Verification report
For v0.14.0+ inspection diagnostics, `source_location` and helper locations are
optional snapshots of owning-file definition bounds: absolute path and inclusive,
1-based `line`/`end_line`, starting at `def` rather than decorators. They are not
exact missing-name positions or proof the whole source is unchanged. A top-level
diagnostic identifies the affected tool, not a refused callback/dependency. Synthetic
wrappers and unverifiable definitions have no captured location; never infer one
from `source_path` or generated-code offsets. Inspect the actual JSON and the pinned
guide's bounded-provenance section; do not promise location capture in Intpot 0.13.0.

Record installed version, source/target, command/output path, diagnostics/refusals, and real behavior exercised. State unverified frameworks and limitations; distinguish generated, compiled, imported, and behaviorally tested.

## Reference
- [Pinned complete upstream public guide](references/upstream.md)
- [Complete upstream MIT notice](references/LICENSE.md)
