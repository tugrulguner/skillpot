---
name: intpot-python
description: Use intpot Python APIs to define, inspect, or convert apps.
license: MIT
metadata:
  version: "0.1.0"
  maintainer: "intpot contributors"
  upstream-repository: "tugrulguner/intpot"
  upstream-revision: "8e583cc4b2b6785955268d09a12dfdd955194b88"
  status: "pinned-public-guidance"
---
# intpot Python API

Use intpot from Python to register tools with `App`, or load an existing trusted framework app and project/generate a target. This entry point gives the workflow; detailed API surface and versioned behavior are in [the pinned upstream guide](references/upstream.md).

## When to use
- User needs `App`, `intpot.load()`, schema inspection, projection, generation, or writing from Python code.
- Use `intpot-cli` for command-line-oriented workflows.
- Do not load unfamiliar app modules: file loading executes their module code.

## Setup and version check
1. Use the active project environment. Install `intpot` for core/CLI use; add `intpot[api]` or `intpot[mcp]` if inspecting/loading that source framework or importing/running that target. `intpot[all]` installs both.
2. Check `python -m pip show intpot` (or the environment's package manager) and confirm the installed version supports each API/diagnostic intended. This snapshot is revision `8e583cc4b2b6785955268d09a12dfdd955194b88`; if package release differs, pin a compatible published version or use that matching source checkout rather than assume docs match runtime.
3. Confirm project dependency policy and trusted input. File loading imports and executes the source; live-instance loading requires its framework runtime available.

## Procedure
1. For new tools, define explicit named parameters using `@app.tool()` on an `intpot.App`. Avoid `*args`/`**kwargs`, which do not map consistently across CLI/API/MCP.
   Native `App` exports use `app.eject("api")` (or target `"cli"`/`"mcp"`), which returns source text. The conversion methods below belong to the `IntpotApp` returned by `intpot.load()`, not the native `App` class.
2. For conversion, call `intpot.load(path)` on a trusted source or pass a live supported app instance. Inspect `app.source_type`, `app.schema.to_dict()`, and `app.project(target)` before generating. Prefer immutable `.schema` for canonical data; `.tools` is a compatibility view.
3. Generate with `.to_cli()`, `.to_api()`, `.to_mcp()`, or write via `.write(path, target)`. Inspect `app.assess()` and exceptions/diagnostics where available. Do not catch a refusal and continue as if conversion succeeded.
4. If deliberately requesting a body scaffold, pass `allow_scaffold=True` only where supported; output raises `NotImplementedError` for unrecovered behavior, and this option does not bypass callback, dependency, or binding guards.
5. Verify generated code independently: compile it, import with runtime dependencies installed, then invoke a real representative target operation.
   Inspect the generated HTTP schema rather than assuming identical wire formats: at this pin native App API export returns the function value, while framework conversion can wrap a scalar in `{"result": ...}` and preserve a CLI option alias such as `discount-cents` in its request body. Test optional inputs using the emitted contract.

## Failure boundaries
- Loading untrusted source is arbitrary code execution; this workflow is not a sandbox.
- Generation success or an empty bounded assessment does not establish full Python equivalence, import availability, runtime state, framework resolution, configuration, or service provisioning.
- Supported recovery is bounded and versioned. The revision guide describes v0.11 recovery for certain undecorated helper functions and immutable literals; closures, mutable/dynamic globals, classes, and other unsupported dependencies remain limitations. Earlier broad statements that no helpers are copied are stale for that bounded subset; neither claim implies universal copy/refusal. Respect concrete diagnostics and installed version.
- Callback/dependency guards and missing body/binding/definition/annotation diagnostics can refuse before output. Preserve existing output and inspect exception details; do not use scaffold opt-in to evade refusal.

## Verification report
Record Python/intpot versions, source form (file or live instance), target, diagnostics, whether output was written, and compile/import/behavior checks separately. State any runtime/framework not exercised.

## Reference
- [Pinned complete upstream public guide](references/upstream.md)
- [Complete upstream MIT notice](references/LICENSE.md)
