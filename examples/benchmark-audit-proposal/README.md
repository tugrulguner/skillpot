# Worked packet: benchmark-audit proposal

**Proposal fixture, not an installed skill, new benchmark or model evaluation.**
Read the [proposal](../../docs/benchmark-audit-proposal.md) before using this example.

## Task and inputs

Audit C1–C6 in [claims.md](claims.md) using only the supplied evidence. C7 is explicitly
deferred by the owner and must remain Not assessed. Create one `benchmark-audit.md`
in a fresh, approved owned directory; preserve sources and refuse an existing target.
Do not run benchmark commands, fetch binaries, install Dexpot or start a server.

The claims are newly authored, intentionally misleading review inputs. They are
**not statements made by upstream**. The Dexpot source itself preserves the failed
screen. Do not present this fixture as exposing a concealed upstream success claim.

## Historical source and provenance

- [Full published Linux-screen record](sources/linux-screen.json): eight published
  records, including two smoke cells, six screen cells and both timeout-invalid rows.
- [Source identity manifest](provenance.json): immutable upstream revision, Git blob
  identities, file SHA-256, lengths and byte-exact-copy status.
- [Complete incorporated notice](sources/DEXPOT-LICENSE).

The source is Dexpot's `benchmarks/scalar_response/linux-screen.json` at commit
`798c449fd1337404c388abb2a177c0302ba35fc0`. That is the **publication snapshot**,
not the candidate measured-source revision. The record separately names control
`e703edf18d1526ebc2a91398f18c9e808e5cf5aa` and candidate
`92e8561aa96f7e799279b89c9c9453834f9e0cda`. Keep those roles distinct.

This packet contains the complete selected **published summary/structured records**,
not the original per-trial raw files or wheel bytes. Their declared hashes do not
recover or independently authenticate them. Runtime/feature/validity fields are
source-reported observations, not newly executed or independently authenticated
serving telemetry. Original timing, collector correctness, plan-freeze chronology,
workload equivalence and causal mechanisms are not independently qualified here.
No private skills, private records or personal paths were copied.

## Authored expected artifact and acceptance cases

[expected/benchmark-audit.md](expected/benchmark-audit.md) is a parent-authored example
of the proposed output, not an agent attempt. [acceptance.json](acceptance.json)
records seven claim expectations, literal source pointers, arithmetic and separately
labeled adversarial input variants. Never provide expected answers to a future
independent task attempt; only the claims, allowed scope and source packet are inputs.

The valid recorded `item-2` comparison is a **loss**, not a positive optimization
result. Validity, performance acceptance and completeness are separate judgments.
An authored positive wording variant attributes that loss accurately; invalid/missing
records and unfair comparison variants must not be promoted to clean speed evidence.

## Offline proposal checks

From the repository root, using the declared development environment:

```sh
uv run --no-project --with-requirements requirements-ci.txt python -m unittest discover -s tests -p test_benchmark_audit_proposal.py -v
```

These checks perform local packet parsing, hashes, pointer/claim coverage and numeric
recalculation. The authored mutation controls check bounded integrity/comparison
predicates, not arbitrary report semantics. No benchmark scripts are executed and no
network is required by the test. Passing them establishes fixture consistency, not
historical measurement truth, native skill activation, held-out task quality or
performance improvement. Source meaning and proposed verdicts require review.

The packet remains a proposal example; no `skills/benchmark-audit/` bundle exists.
