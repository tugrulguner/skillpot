# Compatibility and limits

Pinned source guidance, not a newly qualified Refpot release. Upstream's preview
contract states CPython 3.11-3.14 on Linux x86_64 and macOS arm64, with a C++17
compiler for source builds. Windows, other architectures and free-threaded Python
are unsupported. Installing this skill does not install the Refpot database package.

Package/metadata/reference/license checks are separate from native host installation
and actual database execution. [Native Hermes install/list/selective-removal](../../evaluations/modepot-project-skills/native-install-001/README.md)
was exercised with exact installed instruction/reference/license byte parity.
The [bounded source-matched consumer task](../../evaluations/modepot-project-skills/refpot-consumer-001/README.md)
built this exact Refpot source as 0.1.2 in an isolated CPython 3.11.12 environment
on macOS 26.5.2 arm64. The two shipped examples and repeatable CRUD/rollback/UTF-8/
checkpoint/reopen assertions passed, including a separate parent replay of the
public portable fixture. Its initial failed interpreter-path setup is retained.
No performance target, physical power-loss safety, general host compatibility,
important-data suitability or full runtime matrix is established here.

Use only approved temporary/example data for initial verification. Preserve process/
thread ownership, signed-64-bit bounds, 31-byte UTF-8 text and explicit transaction
semantics. The skill is guidance, not a sandbox or permission to mutate real data.
