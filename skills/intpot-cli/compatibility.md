# Compatibility

Current source: Intpot v0.14.0 tag/commit `3d784e8dd5f1c45b7b2abfac21450aa17efad52c`.
This refresh validates public source, portable metadata, required resources, notice
parity and hashes offline. Host placement follows the [official-contract quickstart](../../docs/quickstart.md);
no harness sessions, authentication probes or product executions were run for this refresh.

The upstream project metadata requires Python >=3.11. Captured definition provenance
requires v0.14.0+; its limits are documented in the current reference. The snapshot
retains upstream's conditional pre-publication wording unchanged; v0.14.0 is now
published at this exact pin. Use matching product dependencies; installation of the
skill does not install Intpot or its API/MCP extras.

Historical [Hermes installation checks](../../evaluations/modepot-project-skills/native-install-001/README.md)
and [consumer replays](../../evaluations/modepot-project-skills/consumer-tasks-001/README.md)
remain at their recorded older snapshots. The latter used Intpot 0.13.0 at
`8e583cc4b2b6785955268d09a12dfdd955194b88`, CPython 3.12.13 on macOS arm64,
with standalone CLI and generated HTTP checks, failures and parent assistance.
They are not runtime evidence for this v0.14.0 refresh, a baseline comparison or a
runtime matrix. No historical record is relabeled or rewritten.
