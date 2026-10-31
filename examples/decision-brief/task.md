# Task: choose storage for a local research log

This is an authored, shareable scenario, not a real customer's requirements or an agent-run record.

Decision owner: example maintainer. Reader: the contributor implementing a later change.
Choose between keeping the current two-file CSV append workflow and a single SQLite database.

## Given assumptions (not observations)

- A1: The target uses CPython 3.14 with `sqlite3` available. This is a scenario premise, not a runtime result.
- A2: The current workflow independently appends to `observations.csv` and `provenance.csv`; it has no coordinated commit/rollback mechanism.
- A3: A new entry must update both logical datasets together or leave neither update visible.
- A4: No separate database server or custom transaction journal is acceptable. Tabular CSV export must remain possible.
- A5: Single-user, local use only. No concurrency, benchmark, crash-durability or production qualification claim is requested.

## Permission and evidence boundary

Read this task and the supplied `sources.json` packet only; offline operation, no search or fetch required.
Create `brief.md` and `evidence.md` in a new owned output directory. Do not overwrite the checked-in expected artifacts.
No installation, database creation, migration, purchase, credentials, external messaging or implementation of the recommendation.

Compare the same constraints, distinguish the given assumptions from documented facts, and state when the conclusion would change.
If a decisive premise is removed, defer rather than invent it. The checked-in `brief.md` and `evidence.md` are parent-authored worked references, not outputs attributed to an autonomous agent.
