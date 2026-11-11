# Benchmark-audit: bounded historical practice

The `benchmark-audit` skill reviews supplied performance claims into one
`benchmark-audit.md`. Follow the [one-command setup and bounded task](../../docs/benchmark-audit-first-use.md).
Current-source instructions are separate from the stable v0.4.1 collection.

## Inputs and source boundaries

The installed input-only packet is under `skills/benchmark-audit/assets/practice/`:
claims, historical JSON, source provenance and full incorporated notice. Read the
installed entry point, report template and evidence checklist with it. Expected
answers are deliberately outside that installable directory.

The original [approved proposal packet](../benchmark-audit-proposal/README.md) preserves
its [authored claims](../benchmark-audit-proposal/claims.md), the full published record,
[acceptance cases](../benchmark-audit-proposal/acceptance.json) and
[parent-authored expected report](../benchmark-audit-proposal/expected/benchmark-audit.md).
These are worked specifications, **not observed agent outputs or new measurements**.
Practice input copies retain their provenance; complete published records are not
complete original execution evidence. Original raw trials and wheel bytes remain
unavailable in this supplied packet. Do not certify what actually ran from hashes alone.

## Repeatable offline checks

From the repository root, with the declared development environment:

```sh
uv run --no-project --with-requirements requirements-ci.txt python -m unittest discover -s tests -p test_benchmark_audit.py -v
uv run --no-project --with-requirements requirements-ci.txt python -m unittest discover -s tests -p test_benchmark_audit_proposal.py -v
```

These execute source/resource/metadata and packet-provenance checks, claim coverage,
literal locators, arithmetic and bounded authored mutation controls. They do not
execute Dexpot, import a benchmark target, launch a server/model/harness, authenticate
original execution or establish semantic accuracy on arbitrary new audit reports.
The fixture retains eight source records, including two timeout-invalid rows and a
valid losing pair; source-record validity and optimization acceptance are separate.

A practical walkthrough requires only the selected installed resources, the user's
explicit output permission, host file tools and ordinary calculation tools. Use the
first-use task's C1-C6 boundary, keep C7 visibly Not assessed, refuse output collisions
and write outside the evidence/project/installed package. Do not copy the expected
report or turn recorded commands into permission to execute them.

## What is verified separately

The [distribution record](../../docs/benchmark-audit-distribution.json) records actual
isolated public add/list/remove, complete selected-file byte parity, source lock,
agent links and sibling preservation. This is filesystem distribution, not native
client loading, automatic discovery or an observed model task. No benchmark run or
claim of model improvement accompanies this implementation. Merge and publication
remain separate owner decisions.
