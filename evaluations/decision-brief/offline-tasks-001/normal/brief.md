# Decision brief

## Decision frame
- **Question:** Keep the two-file CSV append workflow or use one SQLite database for a local research log?
- **Decision owner / reader:** Example maintainer / contributor implementing a later change.
- **Status:** Conditional recommendation for owner review; not accepted or implemented.
- **Evidence cutoff and scope:** Supplied task assumptions and `sources.json` only; offline. No network retrieval or implementation.
- **Stop condition:** Defer if the requirement for coordinated all-or-nothing updates is not actually mandatory, or if a one-database solution cannot be accepted.

## Constraints and criteria
- **Hard constraints (gates):** A new entry must update both logical datasets together or leave neither visible (A2–A3); no separate server or custom transaction journal (A4); CSV export must remain possible (A4). Under the scenario premises, SQLite is eligible; the current independent two-file appends do not meet the atomic-update gate (A2–A3). CSV export is a required property, not proven by this packet to be an automatic SQLite feature (A4, U1).
- **Preferences (trade-offs):** Preserve a familiar tabular workflow where possible; avoid unsupported complexity. No weights supplied.

## Alternatives
| Option | Gate result | Evidence-backed fit and trade-offs | Assumptions / unknowns |
|---|---|---|---|
| Keep independent appends to `observations.csv` and `provenance.csv` | Fails coordinated-update gate under A2–A3 | Simple existing workflow, but the supplied premise says it has no coordinated commit/rollback mechanism. | Depends on A2 being accurate and A3 being mandatory. |
| Single SQLite database | Passes server constraint under A1/A4; transaction mechanism is documented in S2–S3; CSV export feasibility not demonstrated | SQLite is documented as disk-based and requiring no separate server (C1). Python `sqlite3` documents explicit commit/rollback transaction control (C2). A single database is the best fit to the required single coordinated transaction; export remains an implementation requirement. | CPython 3.14 with sqlite3 and transaction behavior are scenario premises, not tested here (A1). Export method and preservation of required CSV semantics remain unverified (U1). |

## Recommendation or deferral
Conditionally recommend one SQLite database, with both logical datasets written within the same explicit transaction, provided the owner confirms A3 is mandatory and accepts a tested CSV export path. The current two-file append approach is the runner-up but fails the stated atomic-update gate (A2–A3). S2–S3 support SQLite's serverless nature and transaction controls; they do not prove a particular schema or implementation meets the task. Do not implement or migrate on the basis of this brief alone.

## Risks, uncertainty, and reversal conditions
- **Residual uncertainty:** CSV export behavior and data/format compatibility are not established by the packet (U1); no application code, failure handling, migration, durability, or runtime was tested.
- **Reversal condition:** If the owner withdraws the all-or-nothing requirement, or requires continued direct multi-file CSV writes without an added coordination mechanism, re-evaluate keeping CSV. If a practical SQLite-to-CSV export cannot preserve required data, defer until the format requirement is clarified.

## Owner action
Confirm whether A3 is mandatory and define the required CSV export/round-trip behavior before authorizing implementation. Acceptance is not recorded.

## Limitations
Offline, supplied-packet-only decision. Task statements are scenario assumptions, not observations. The source excerpts are supplied in `sources.json`; their hashes and revision metadata were not independently verified against upstream. No code, database, migration, benchmark, concurrency, crash-durability, or production qualification was performed.
