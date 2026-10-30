# Compatibility

Current source: audited Intpot main commit `470584e21ee518e983087175f217c65664bd0ec5`.
Latest observed release: [v0.16.0](https://github.com/tugrulguner/intpot/releases/tag/v0.16.0),
commit `f6ec26afc60011d41209cd705636f60e881d492f`. Its guide differs from this snapshot.
This refresh validates public source, portable metadata, required resources, notice
parity and hashes offline. Host placement follows the [official-contract quickstart](../../docs/quickstart.md);
no harness sessions, authentication probes or product executions were run for this refresh.

The upstream project metadata requires Python >=3.11. Definition provenance requires
v0.14.0+, binding-chain explanations v0.15.0+, and exact reference ranges/source digests
v0.16.0+. Those releases exist, although archived conditional publication caveats
remain unchanged in the reference. Numeric-range conversion and its guarantees are
explicitly unreleased in this source snapshot and are not provided by v0.16.0. Use
matching product dependencies; installing the skill installs no product or extras.

Historical [Hermes installation checks](../../evaluations/modepot-project-skills/native-install-001/README.md)
and [consumer replays](../../evaluations/modepot-project-skills/consumer-tasks-001/README.md)
remain at their recorded older snapshots. The latter used Intpot 0.13.0 at
`8e583cc4b2b6785955268d09a12dfdd955194b88`, CPython 3.12.13 on macOS arm64,
with standalone CLI and generated HTTP checks, failures and parent assistance.
They are not runtime evidence for this source refresh, a baseline comparison or a
runtime matrix. No historical record is relabeled or rewritten.
