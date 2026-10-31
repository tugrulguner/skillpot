# Evidence: local research log

This ledger separates copied documentation excerpts, authored assumptions and decision inferences.
All sources were inspected at CPython v3.14.0 commit `ebf955df7a89ed0c7968f79faec1de49f61ed7cb`.
The exact excerpts, source line ranges, original-file hashes, immutable URLs and capture date are in [sources.json](sources.json).

## C1

Supported by S1: by default a CSV reader returns string fields; the documented `QUOTE_NONNUMERIC` exception converts unquoted fields to floats.
This does not establish that CSV can never preserve types, support an application-level journal or be used in a correct transactional design.

## C2

Supported by S2: SQLite is described as a local disk-based database not requiring a separate server process.
This supports the no-server criterion only, not a performance or durability promise.

## C3

Supported by S3: Python 3.14 recommends transaction control through `Connection.autocommit`, suggesting `False`, with explicit commit and rollback.
This describes one configured API contract. It is not a test of a target interpreter, a multi-process system, a migration or physical crash recovery.

## C4

Supported by S4: `csv.writer` provides a writer interface over an object with a write method.
Using that interface for an export is a proposed implementation choice, not evidence that any existing application already exports correctly.
The same excerpt warns that `None` becomes an empty string irreversibly and other non-string values are stringified; it does not promise a lossless typed or NULL round trip.

## Assumptions and derived conclusions

A1–A5 are authored scenario inputs in [task.md](task.md), not measured facts.
Excluding the existing append workflow follows from A2–A4, not from an absence of transaction language in the CSV documentation.
The recommendation connects A3 to the documented mechanism C3 and is conditional on A1. No weighted calculation or benchmark is used.

## Contradictions, access and missing evidence

No contradiction between the selected source excerpts was identified; the reader-conversion exception in S1 is retained rather than hidden.
These excerpts are deliberately partial, not full-text copies or an exhaustive literature search. No inaccessible document is cited as if read.
No target availability, actual schema, rollback implementation, migration behavior, performance or crash durability was tested.
See [cases.md](cases.md) for separate authored failure scenarios, including contradictory evidence and a missing decisive premise.

## Rights

Documentation excerpts retain the PSF License Version 2 terms and copyright notice; see [NOTICE.md](NOTICE.md) and the unchanged [CPython license](LICENSE-PYTHON.txt).
The surrounding scenario, ledger and decision narrative are newly authored; the excerpts are not relicensed MIT.
