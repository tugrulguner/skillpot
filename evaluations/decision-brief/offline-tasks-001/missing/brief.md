# Decision brief

## Decision frame
- **Question:** Keep two-file CSV appends or use one SQLite database for the local research log?
- **Decision owner / reader:** Example maintainer / contributor implementing a later change.
- **Status:** Deferred pending confirmation of target interpreter `sqlite3` availability.
- **Evidence cutoff and scope:** Supplied task and `sources.json` only; offline; source excerpts pinned to CPython commit `ebf955df7a89ed0c7968f79faec1de49f61ed7cb`, retrieved date recorded in packet as 2026-10-31.
- **Stop condition:** Do not choose SQLite as implementable until availability in the target interpreter is established; do not retain CSV if the required atomicity guarantee cannot be met by the stated design.

## Constraints and criteria
- **Hard constraints (gates):** Each entry updates both logical datasets or neither (A3); no separate server or custom journal; CSV export remains possible (A4). SQLite must be available in the target interpreter, currently unknown (A1/U1).
- **Preferences (trade-offs):** No additional preference weights were supplied. Avoid claiming benchmarks, concurrency, or crash-durability properties.

## Alternatives
| Option | Gate result | Evidence-backed fit and trade-offs | Assumptions / unknowns |
|---|---|---|---|
| Keep current two-file CSV append workflow | **Fail** atomic-update gate under the supplied current-design premise (A2, A3). | CSV stores rows read as strings absent an explicit conversion option (C1); CSV writer supports file-like output and stringifies non-string values, but `None` becomes empty string and is not reversible (C4). | Current independent appends and lack of coordinated rollback are supplied assumptions, not inspected implementation (A2). |
| One SQLite database | **Conditional fit**, but implementation eligibility is unknown until runtime availability is checked (U1). | SQLite is documented as disk-based and requiring no separate server process (C2). The documented transaction guidance includes explicit commit and rollback (C3), which is aligned with the requested all-or-neither update; CSV output remains possible in principle through the documented writer behavior (C4). | Target interpreter/module availability is unknown (A1/U1). No task-specific implementation or export test was run. |

## Recommendation or deferral
Defer the final storage selection until the contributor confirms that the target interpreter provides `sqlite3` (U1). If confirmed, select SQLite as the best-supported candidate: the current two-independent-file workflow fails the explicit atomic-update requirement (A2/A3), while the supplied Python documentation describes SQLite transactions with explicit commit/rollback (C2/C3) and CSV writing remains available (C4). This is a conditional design recommendation, not proof of task-specific atomic behavior or an implementation authorization. If `sqlite3` is unavailable and the hard requirement remains, neither listed option is established as eligible; revisit the alternatives only with owner authorization, without assuming a custom journal or server is acceptable.

## Risks, uncertainty, and reversal conditions
- **Residual uncertainty:** `sqlite3` availability in the target interpreter is unverified and decisive (U1). The packet does not demonstrate the exact schema/update sequence or a tested export path. CSV conversion may lose the distinction between SQL NULL and empty text when written (C4).
- **Reversal condition:** If the target interpreter lacks `sqlite3`, or the owner removes the atomic-update requirement, reassess the choice. If availability is confirmed and the two logical updates can be placed in one explicit transaction, the conditional recommendation becomes actionable for a later implementation decision; no such test is claimed here.

## Owner action
The example maintainer should first confirm target-interpreter `sqlite3` availability, then accept or reject the conditional recommendation. Acceptance and implementation are not recorded.

## Limitations
Only the supplied assumptions and excerpted, pinned CPython documentation in `sources.json` were used. No network retrieval, code inspection, runtime probe, database creation, migration, or implementation was performed. The excerpts establish documented API concepts, not behavior of a proposed application design.
