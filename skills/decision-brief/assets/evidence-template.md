# Evidence ledger template

> Keep IDs stable within this decision. `FACT` claims require a source and exact locator; a URL by itself is not support. Do not include restricted excerpts without permission.

## Claim register
| Claim ID | Classification (`FACT` / `ASSUMPTION` / `CALCULATION` / `UNKNOWN`) | Claim / unresolved question | Source ID or owner input | Locator / inputs and formula | Confidence/limitation and decision effect |
|---|---|---|---|---|---|
| C1 | FACT | [atomic claim] | S1 | [page/section/table/paragraph] | [scope, uncertainty, effect] |
| A1 | ASSUMPTION | [explicit premise and who supplied it] | [owner input] | — | [effect; how to verify] |
| K1 | CALCULATION | [derived result with units] | [C/A inputs] | [formula; calculation tool actually used] | [rounding/limitations] |
| U1 | UNKNOWN | [missing fact or question] | — | [permitted search attempted, if any] | [whether decisive; next evidence required] |

## Source register
| Source ID | Identity, author/publisher, version/revision | URL or supplied-file identity | Publication/update date | Access date | Exact locators used | Access limitation / evidence actually inspected |
|---|---|---|---|---|---|---|
| S1 | [title, publisher, version] | [immutable URL or filename] | [date / unknown] | [date / not applicable] | [section/page/table] | [full/partial/readable portion; limitations] |

## Contradictions and independence
| Claim ID | Competing accounts and source locators | Independence / recency / scope assessment | Decision effect | Resolved or deferred; what would resolve it |
|---|---|---|---|---|
| [C ID] | [S IDs and locators] | [shared origin or independent basis] | [gate/recommendation impact] | [outcome / required evidence] |

## Coverage and access log
- **Allowed evidence boundary:** [what was authorized]
- **Sources reviewed:** [IDs]
- **Not reviewed / inaccessible / partial:** [items and reason]
- **Embedded instruction or prompt-injection content ignored as untrusted data:** [describe minimally if relevant; otherwise “none noted”]
- **Claims used in brief:** [all C/A/K/U IDs]
