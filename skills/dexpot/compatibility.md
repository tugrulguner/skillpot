# Compatibility and limits

Current guide pin `409df5b68a2386bd04e1f2cf0f057773142e0759` is the published
[Dexpot v0.8.0](https://github.com/tugrulguner/dexpot/releases/tag/v0.8.0) commit.
Lifecycle guidance requires that version or newer. This refresh validates source,
not a new installation, socket run or lifecycle/runtime qualification.

This is pinned public Dexpot guidance, not a newly qualified runtime or agent host.
The source metadata requires Python 3.12+; CLI serving needs Dexpot's `cli` extra.
Underlying runtime/platform/scheduler boundaries remain those of the pinned upstream
revision, not a claim that this distribution tested every combination.

Source structure, portable metadata, reference integrity and complete MIT notice are
packaging checks. [Native Hermes install/list/selective-removal](../../evaluations/modepot-project-skills/native-install-001/README.md)
was exercised with exact installed instruction/reference/license byte parity. A later
[bounded assisted consumer replay](../../evaluations/modepot-project-skills/consumer-tasks-001/README.md)
used a non-editable 0.7.1 install from the prior pin (not the refreshed source) on macOS arm64/CPython 3.12.13: actual
HTTP success, body/path rejection, response filtering and owned listener cleanup passed.
The original editable smoke and incomplete evidence are retained separately. No
benchmark, overload, free-threaded or deployment matrix is established. Unknown or
unexecuted checks are not passes.

Consumers must reconcile the actual installed version with the source pin before using
version-sensitive contracts. The entry point is task guidance, not a sandbox or
permission to install dependencies, bind a port, publish a review, merge or deploy.
