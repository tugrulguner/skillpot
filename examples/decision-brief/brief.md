# Brief: storage for a local research log

## Decision and status

Owner: example maintainer. Status: proposed; not accepted or implemented.
Scope: the authored scenario in [task.md](task.md), not all CSV or SQLite applications.

## Criteria and alternatives

Hard constraints are a coordinated update of two logical datasets, no separate server, no custom transaction journal, and retained CSV export (A3–A4).
No numerical scores or invented performance weights are used.

- **Current two-file CSV append workflow:** remains easy to exchange, but fails the required coordinated-update contract *as described by A2*. This is a scenario inference, not proof that every CSV-based design lacks transactions. The default CSV reader's type handling also requires attention; its documented conversion exception remains explicit. [C1]
- **Single SQLite database with explicit transaction control:** is a documented local, serverless option with explicit commit/rollback behavior under the selected configuration. [C2] [C3] Export through the standard CSV writer remains a documented building block, not a shipped migration. [C4]

## Conditional recommendation

Recommend SQLite for the proposed design, conditional on A1 and correctly implemented transaction control, because that documented mechanism addresses A3 without adding the server or custom journal excluded by A4. [C2] [C3]
This is reasoning from the evidence and the authored assumptions, not an executed storage comparison.
Keep the current files untouched until the human owner accepts a separately verified implementation.

## Trade-offs, gaps and reversal conditions

A migration and explicit schema would introduce implementation/maintenance work; this example has not measured that work or any speed, cost, corruption recovery or crash behavior.
CSV export needs an explicit type/NULL representation policy if reversible exchange matters; the documented writer defaults alone do not provide that guarantee. [C4]
The module's presence in the actual target and its runtime configuration have not been tested here; A1 is provided input, not evidence.
If A1 is unknown, defer adoption until target availability is established. If coordinated updates cease to be required, reconsider retaining the simpler current workflow.
If future requirements include simultaneous writers or crash-durability guarantees, obtain new evidence and tests before reusing this recommendation.

See [evidence.md](evidence.md) for precise excerpts, inference boundaries and source identities.
