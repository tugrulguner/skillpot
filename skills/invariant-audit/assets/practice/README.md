# Input-only practice packet

**Authored synthetic practice inputs, not an incident, target, defect report, or execution record.** The source illustrations intentionally show commented defects; their notes are part of the supplied inputs. Read them as text only. This packet includes no expected report, oracle, cases, expected verdicts, or acceptance answers.

## Practice prompt

“Review whether the supplied identity-current guarantee is supported by the named source snippets. Treat unavailable identities as unknown, distinguish endpoint snapshots from continuity, and do not execute or modify supplied material. Produce the seven-section report in a fresh approved destination.” The reviewer must independently supply scope, failure model, permissions and destination; this packet does not supply answers.

## Inputs

Named guarantee: a snapshot may be labeled `CURRENT` only when the captured and later identities for each required role (baseline, candidate and checker) are nonblank strings, each role matches its own captured identity, and no identity-read error is recorded. These are toy labels, not authenticated Git revisions or hashes. Equal endpoint snapshots alone do not establish continuous identity between observations. The snippets illustrate classification logic; no actual captured or later run records are supplied.

- `source/baseline.txt`
- `source/candidate.txt`
- `source/checker.txt`

All three files are byte-for-byte copies of the corresponding authored source illustrations in `examples/invariant-audit/source/`. No expected outputs are included.
