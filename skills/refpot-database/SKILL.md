---
name: refpot-database
description: Use Refpot's embedded database preview safely.
license: MIT
compatibility: Refpot's pinned preview targets Linux x86_64 and macOS arm64, CPython 3.11-3.14; source builds require a C++17 toolchain. Windows and free-threaded Python are unsupported.
metadata:
  version: "0.1.0"
  upstream-repository: "tugrulguner/refpot"
  upstream-revision: "3294ce39f0e5630c660fad2e5a1e3977bf52a17f"
  status: "pinned-public-guidance"
---

# Refpot database preview

Use when writing an application against Refpot's Python database preview, testing
transactions/reopening, or checking an unsupported feature request. Do not use for
SQL/ORM work, important production data, multiwriter databases or a SQLite-compatibility
claim. Read the [complete pinned guide](references/upstream.md) before making changes.

## Prerequisites and setup

Inspect the actual checkout/package revision and the host before installing anything.
This guide is for the source revision above, not a promise that another release has
identical behavior. The preview targets CPython 3.11-3.14 on Linux x86_64 or macOS
arm64; source builds require C++17. Windows, other architectures and free-threaded
Python are unsupported by the pinned contract. Installing this skill does not install
Refpot or establish its platform support.

With permission, install the matching source into a fresh isolated environment:

```sh
python -m pip install "refpot @ git+https://github.com/tugrulguner/refpot.git@3294ce39f0e5630c660fad2e5a1e3977bf52a17f"
```

Use that environment's actual Python executable through the host's command tool.
Do not overwrite an existing checkout/environment or access real user databases as
an incidental example. Missing compiler/dependency/access permission is a reported
blocker, not a reason to fabricate successful setup.

## Procedure

1. Define the user's data, persistence needs and permissions. Confirm the preview's
   API fits before implementation; refuse to invent SQL, ORM, joins or public indexes.
2. Use a new temporary database file in an existing trusted parent directory for a
   demonstration. Keep one process as exclusive owner and use each handle only from
   its creating thread. Never reuse a handle inherited across `fork()`.
3. Open `Database(path)` as a context manager. Keys and integer values are signed
   64-bit integers; bool is not an accepted integer. Text is limited to 31 UTF-8 bytes,
   not 31 characters. Measure encoded bytes before insertion.
4. Exercise `insert`, `get`, `update` and `delete` against explicit expected `Row`
   values. Check duplicate insertion and missing-key behavior instead of swallowing
   arbitrary exceptions as success.
5. Use `with db.transaction():` for explicit transactions. An exception escaping the
   block rolls back; catching one inside the block does not request rollback. Nested
   transactions are unsupported. Run the pinned guide's repeatable example to check
   committed state, rollback and the UTF-8 boundary.
6. Checkpoint and close the handle, then reopen the database and assert persisted
   committed data. This verifies that example, not physical power-loss durability.
7. Report exact package/source identity, executed assertions, observed errors and
   remaining limits. Stop only owned resources and remove only temporary data you
   created; retain user data and failed-run evidence.

## Failure handling and limits

Duplicate inserts raise `ValueError`; missing keys raise `KeyError`. Wrong argument
types raise `TypeError`; out-of-range integers raise `OverflowError`. Treat capacity
refusal separately from uncertain I/O. An uncertain write poisons the handle: close,
reopen and inspect persisted state before retrying; the transaction may be present or
absent. Never blindly retry a write against important data.

The pinned preview has 64 MiB snapshot/WAL recovery limits and does not establish
physical power-loss safety or the overall SQLite performance target. A successful
example is not a durability guarantee, benchmark or production-readiness result.
Do not silently expand supported OS, process/thread or data-type boundaries.

## Provenance

Canonical upstream file: `skills/refpot-database/SKILL.md` at the revision above.
The complete reference is byte-identical upstream material; this entry point replaces
host-specific nested metadata with portable string metadata and adds pinned setup and
permission boundaries. Preserve the [upstream MIT notice](references/LICENSE.md).
Root provenance and compatibility documents in the SkillPot source describe this
package's verification; native skill installation alone does not prove the database.
