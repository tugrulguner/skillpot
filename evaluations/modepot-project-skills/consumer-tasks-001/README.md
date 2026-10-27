# Additional consumer tasks: original attempts and assisted replays

## What this establishes

This increment adds executable examples for Intpot CLI/Python, Dexpot HTTP and the
eligible deterministic Summonpot path. It does **not** establish native model discovery,
comparative usefulness, an unassisted success rate, or a full product/runtime matrix.
Accepted consumer replays ran on macOS arm64, CPython 3.12.13, using exact public source pins.
Existing Refpot execution is [separate evidence](../refpot-consumer-001/README.md).

Initial instruction packages came from public SkillPot revision
`f65395e3fa6eb1ebb27a953e1b144d6b15101c92`, individually installed in an owned temporary
Hermes home. [Setup commands](setup-commands.json) retain normal scanning. Each required
entry point, reference and complete license matched source bytes. Fresh delegated
agents explicitly read these installed files; that is not a native `skill_view` call.

## Original attempts — not a fully accepted trial

- **Intpot:** [records](intpot-task/commands.json) show an `intpot.App` inspect refusal,
  followed by successful ejection. The worker stopped before execution/equivalence
  checks. It also omitted some setup commands from its JSON. This is partial, not a
  passing task, and not evidence that the documented native App ejection is broken.
- **Dexpot:** [records](dexpot-task/commands.json) contain real HTTP observations, but
  the original smoke had no semantic assertions and used an editable source install.
  The parent did not accept that as complete installed-artifact qualification.
- **Summonpot:** [records](summonpot-task/commands.json) include actual successful HTTP
  assertions and expected registration rejection, but use an editable source install.
  Some earlier failed setup/probe commands were absent from that JSON. Those missing
  records were not reconstructed or inserted into the original log.
- Two narrow replay workers were interrupted by the conversation persistence failure.
  They produced no accepted terminal result. The parent reconciled their partial files
  and took over rather than claiming they were still running or had passed.

Original files and complete first-worker traces are retained privately. Public copies
replace machine-local prefixes only; [original hashes and transformation descriptions](provenance.json)
are separate from [later replay provenance](replay-provenance.json). The incomplete
worker JSON is preserved as such, not retrospectively certified as complete history.

## Accepted assisted replays

### Intpot 0.13.0

The [parent journal](intpot-parent-replay/commands.json) records the installed module,
version and VCS receipt at `8e583cc4b2b6785955268d09a12dfdd955194b88`. The module resolves
to the isolated environment's `site-packages`, not a source checkout. The
[portable verifier](../../../examples/modepot-project-skills/intpot/verify.py) exercised:

- CLI inspection and dry-run conversion of a trusted Typer source;
- actual CLI ejection of the native App, compile and standalone invocation;
- three quotation cases, including the optional discount and zero unit price;
- Python assessment/projection/conversion of the Typer source and native `App.eject`;
- actual HTTP responses from both generated FastAPI apps and 422 integer rejection;
- invalid CLI amount rejection, server termination and closed listeners.

The parent initially called a conversion method on the native App class, then used
an incorrect shared HTTP oracle. Those failed commands remain recorded. Source
inspection confirmed two API types and two wire contracts: native export returns the
scalar directly; framework conversion wraps it in `result` and preserves the Typer
option alias `discount-cents`. Correcting the verifier is an explicit intervention,
not an unassisted pass or a claim that those wire formats are identical.

[Final nested command records](intpot-parent-replay/public-fixture-004/commands.json)
and [HTTP assertions](intpot-parent-replay/public-fixture-004/http-results.json) accompany
the successful final replay. Earlier failing and successful parent attempts remain.
The two Intpot entry points were clarified; their updated immutable packages were
[reinstalled and byte-checked](intpot-refresh-commands.json) at
`5355263097c9727facea02356fb7f39aab065cab`, without force and with siblings preserved.
The original agents had read the earlier instructions; they were not silently rerun
or relabeled as fresh trials of these clarifications.

### Dexpot 0.7.1

[Parent build/probe/command records](verified-replays/commands.json) verify exact source
`ca4979a6339e533f11ad135bc760aa081f3f60ab`, a fresh non-editable installation and an
actual `site-packages` import. The [public verifier](../../../examples/modepot-project-skills/dexpot/verify.py)
asserted 200 success, exact response filtering, 422 invalid body, typed path success
and 422 invalid path. The actual Dex socket server stopped with exit 0 after SIGINT;
no forced kill was needed and its listener was checked closed. This is not an ASGI
substitute, performance test, lifecycle matrix or parser-backend qualification.

### Summonpot 0.12.0

The same [parent records](verified-replays/commands.json) verify source
`cdaf2f76ae5aa698aeed1d4654ecdb567eb6e2d5`, a fresh non-editable install and an actual
`site-packages` import. The [public verifier](../../../examples/modepot-project-skills/summonpot/verify.py)
asserted HTTP success, two 422 failures, exact capability arguments/count and exact
registration-time TypeError for an invalid binding. The final guard rejects entry into
`Runtime._agent_for`, the model-backed branch after deterministic dispatch selection.
No provider output was fabricated or model/provider call made by the application.

An earlier parent probe incorrectly guarded the common `_call_with_deadline` entry,
which also handles deterministic execution. It failed with 500 and remains recorded.
The source-guided guard correction is a harness repair, not a product fix. The final
probe shut down its Uvicorn thread/socket and checked that the listener was closed.
The provider-backed path, authentication and the full upstream suite were not run.

## Native host-loading blocker — still unexecuted

Two CLI attempts failed before creating a session or invoking model/tools:

1. [Initial attempt](native-agent.json): this installed gateway-client CLI rejected
   `--run-budget`, despite the flag appearing in its help.
2. [Supported-option retry](native-agent-retry.json): the temporary-home gateway could
   not start because the existing default host gateway already owns the host.

[Status](native-loading-status.json) records the boundary. The active gateway was not
restarted, no registered profile was changed, and credentials were not copied. These
failures do not invalidate instruction-file installation, but do leave native model
loading/selection unverified. Explicit delegated file loading and assisted application
replays are not substituted for that missing result.

## Reproduction and cleanup

Use the [example instructions](../../../examples/modepot-project-skills/README.md) with
approved new external environments and owned loopback listeners. Exact portable file
hashes are in [replay provenance](replay-provenance.json). No changes to upstream
product code, real data, releases or benchmarks are included. All task servers ended;
owned source checkouts, environments and evidence remain. No general security,
durability, compatibility or usefulness certification follows from these examples.
