---
name: dexpot
description: Build synchronous typed HTTP APIs with Dexpot.
license: MIT
compatibility: Requires Python 3.12+ and Dexpot 0.8.0+ for documented lifecycle support; CLI commands require the cli extra. No host or runtime matrix is qualified by this package.
metadata:
  version: "0.2.0"
  upstream-repository: "tugrulguner/dexpot"
  upstream-revision: "409df5b68a2386bd04e1f2cf0f057773142e0759"
  status: "pinned-public-guidance"
---

# Dexpot applications

Use for building or changing a Dexpot application, typed path/body/response contracts,
and real HTTP verification. Do not use for ASGI/async handlers, a different framework,
or a claim of production or performance qualification.

This is a pinned distribution of existing ModePot project knowledge, not a second
canonical API guide. Read the [complete upstream guide](references/upstream.md) before
changing response contracts, request context, scheduling, parser or lifecycle behavior.
It describes the named source revision; do not assume an older package or a newer
checkout has identical features. Installation is not permission to start a server.

## Prerequisites and setup

Inspect the user's environment and installed package version before editing. Python
3.12+ is required. Dexpot's CLI needs the `cli` extra; all project packages retain their
own licenses. If the required source revision is absent, obtain permission to install
it in a fresh isolated environment, not over an existing user installation:

```sh
python -m pip install "dexpot[cli] @ git+https://github.com/tugrulguner/dexpot.git@409df5b68a2386bd04e1f2cf0f057773142e0759"
```

Use the environment's actual Python executable through your host's command tool.
Network, dependency installation, listeners and public deployment are separate access
boundaries; stop and report missing permission or tools instead of inventing a result.

## Procedure

1. Inspect the application and its Dexpot revision. Define the request, response,
   allowed data, expected status and supported runtime; preserve unrelated files.
2. Declare a synchronous `Dex` handler. Bind path captures by parameter name and JSON
   bodies explicitly with `body=YourStruct`; use msgspec Structs rather than inventing
   Pydantic or query-injection support. Register all routes before serving.
3. Declare `response=YourStruct` when output filtering/validation is needed.
   `response=None` is generic JSON encoding, not a privacy boundary. Do not return
   Request context or assume raw envelopes bypass checked response contracts.
4. Inspect the source guide's applicable restrictions and add actual application tests.
   Include success, invalid input, and registration-time rejection. Do not replace
   the owned socket server with an ASGI test adapter or second dispatcher.
   For Dexpot 0.8.0+ lifecycle resources, use synchronous `app.lifespan(factory)`
   managers with process-local ownership. Bounded shutdown does not forcibly cancel
   Python handlers: late work can defer cleanup to a finalizer thread. Do not assume
   enter/exit thread affinity or guaranteed cleanup after forced termination.
5. With listener permission, serve only on loopback for local verification. For an
   application in `main.py`, the documented command is:
   `dexpot serve main:app --host 127.0.0.1 --port 8000`.
   Choose an available authorized port rather than killing another process.
6. Send real HTTP requests and assert status and body. For scheduling/concurrency
   claims, record Python version and actual GIL state after application imports;
   include the configured pool/queue/workers and overload outcomes. A fast 503 is
   not successful throughput. Never infer benchmark results from this skill.
7. Stop only the process you started, retain actual test evidence, and report files
   changed, exercised revision, failures and untested behavior. Deployment, publication
   and repository merges require separate authorization.

## Limits and recovery

Do not invent OpenAPI, middleware, dependency injection, TLS, WebSockets or streaming
support. Source-specific scheduler and protocol details remain in the pinned guide.
If setup, registration or a request fails, preserve the actual error and diagnose it
before retrying; never label partial tests as a completed application. SIGINT/SIGTERM
and multiprocess behavior must be tested if the application relies on them. A bundled
guide or a successful skill installation proves neither runtime safety nor performance.

## Provenance

Canonical source is the Dexpot repository at the revision above, file
`src/dexpot/templates/skills/dexpot.md`. The reference is an unchanged snapshot; this
entry point adds portable task/setup/permission/reporting structure. Copyright and
permission notice: [upstream MIT license](references/LICENSE.md). Root provenance and
compatibility documents in the SkillPot source repository record packaging limits.
