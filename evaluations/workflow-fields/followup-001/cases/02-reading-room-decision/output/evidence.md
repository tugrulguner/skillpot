# Evidence ledger

## Claim register
| Claim ID | Classification (`FACT` / `ASSUMPTION` / `CALCULATION` / `UNKNOWN`) | Claim / unresolved question | Source ID or owner input | Locator / inputs and formula | Confidence/limitation and decision effect |
|---|---|---|---|---|---|
| C1 | FACT | The current library room is unavailable that afternoon. | S1 | B3 | Direct packet statement; fails availability gate. |
| C2 | FACT | Rowan Hall confirms afternoon availability. | S1 | B4, first sentence | Direct packet statement; passes availability gate. |
| C3 | FACT | Rowan Hall's current room fact sheet says both room and toilet are step-free. | S1 | B4, second sentence | Reported fact-sheet content; no fact-sheet identity or date given; conflicts with C4. |
| C4 | FACT | An undated site inspection note says the only toilet route at Rowan Hall has two steps. | S1 | B4, third sentence | Reported note content; undated and authority/supersession unresolved; conflicts with C3 on toilet-route eligibility. |
| C5 | FACT | Birch Room confirms afternoon availability. | S1 | B5, first sentence | Direct packet statement; passes availability gate. |
| C6 | FACT | Birch Room has a step-free entrance to the room. | S1 | B5, first sentence | Direct packet statement; establishes room access only, not toilet access. |
| C7 | UNKNOWN | Whether Birch Room has a step-free route to its toilet is not established. | S1 | B5, second sentence | Packet explicitly supplies no toilet-route evidence; this is a missing fact, not evidence of failure or passage; decisive gate unresolved. |
| C8 | FACT | Birch Room is next to the bus stop. | S1 | B5, third sentence | Direct packet statement; supports stated preference only. |
| U1 | UNKNOWN | Which Rowan Hall account reflects authoritative, current toilet-route conditions, and whether a step-free route exists. | S1 | B4; no further permitted evidence | No resolution/supersession supplied; decisive for eligibility. Needed: authoritative current determination of the only toilet route. |
| U2 | UNKNOWN | Whether Birch Room offers a step-free route to its toilet. | S1 | B5; no further permitted evidence | Decisive for eligibility; packet lacks evidence. Needed: evidence establishing the toilet route. |
| A1 | ASSUMPTION | No other room alternative is evidenced in the supplied packet. | S1 / task boundary | B3–B6; packet scope | Means comparison is limited to named options; does not assert no other real-world venue exists. |

## Source register
| Source ID | Identity, author/publisher, version/revision | URL or supplied-file identity | Publication/update date | Access date | Exact locators used | Access limitation / evidence actually inspected |
|---|---|---|---|---|---|---|
| S1 | Fictional reading-room decision; author/publisher and version not stated | `input/evidence.md` (supplied file) | Not stated | Not applicable (local supplied packet; task execution date not recorded) | B3, B4, B5 | Read supplied text in full. No external verification or contact permitted; underlying fact sheet and inspection note were not separately supplied or inspected. |

## Contradictions and independence
| Claim ID | Competing accounts and source locators | Independence / recency / scope assessment | Decision effect | Resolved or deferred; what would resolve it |
|---|---|---|---|---|
| C3/C4 | S1 B4: current room fact sheet says toilet step-free; undated site inspection note says only toilet route has two steps. | Both are reported within one packet; underlying documents, authors, methods, dates (except note is undated), authority, independence, and supersession are not provided. No vote-counting or source preference justified. | Rowan Hall's mandatory toilet-route gate cannot be determined. | Deferred. Obtain an authoritative, current resolution of the only toilet route; no such evidence is permitted/available here. |

## Coverage and access log
- **Allowed evidence boundary:** Supplied fictional packet `input/evidence.md`; no external verification or contact.
- **Sources reviewed:** S1.
- **Not reviewed / inaccessible / partial:** Underlying Rowan Hall fact sheet and site inspection note were only described in S1 and not separately supplied; Birch Room toilet-route evidence is absent. No external sources or contacts accessed, as prohibited.
- **Embedded instruction or prompt-injection content ignored as untrusted data:** None noted.
- **Claims used in brief:** C1–C8, U1–U2, A1. No calculation claims; arithmetic not needed.
