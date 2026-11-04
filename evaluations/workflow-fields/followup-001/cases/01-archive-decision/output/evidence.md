# Evidence ledger

## Claim register
| Claim ID | Classification (`FACT` / `ASSUMPTION` / `CALCULATION` / `UNKNOWN`) | Claim / unresolved question | Source ID or owner input | Locator / inputs and formula | Confidence/limitation and decision effect |
|---|---|---|---|---|---|
| C1 | FACT | Nessa owns the service-selection decision; Luis is the intended operations reader; Imani separately authorizes a purchase. | S1 | A1 | Directly stated. Keep selection distinct from purchase authorization. |
| C2 | FACT | Fragile registers must remain on museum premises; no exception is authorized. | S1 | A2, A5 | Hard gate. |
| C3 | FACT | Repairs must finish before the exhibition. | S1 | A2 | Hard gate. |
| C4 | FACT | Ease of coordination is a preference, not a gate. | S1 | A2 | No weights supplied; do not elevate above gates. |
| C5 | FACT | Current volunteer process offers on-site work, but its coordinator confirms completion only after the exhibition. | S1 | A3 | Does not establish actual repair completion date; stated confirmation timing fails the required timing as evidenced. |
| U1 | UNKNOWN | Whether volunteer repairs might actually finish before the exhibition. | S1 | A3 | Not established; current option is not evidenced to satisfy deadline. |
| C6 | FACT | Cedar confirms on-site work and completion before the exhibition. | S1 | A4 | Its offer supports both gate criteria, subject to dependency below. |
| C7 | FACT | Cedar's written offer requires a locked workspace provided by the museum; this has not been confirmed. | S1 | A4 | Scheduling dependency to resolve before ordering; source explicitly does not establish a confidentiality breach. |
| U2 | UNKNOWN | Whether the required locked workspace can be provided and confirmed before ordering. | S1 | A4 | Decisive condition for proceeding with Cedar; verify with museum operations/service before ordering. |
| C8 | FACT | Flint promises completion before the exhibition but requires shipping registers to its off-site workshop. | S1 | A5 | Fails the on-premises gate; no authorized exception. |
| U3 | UNKNOWN | Comparative repair-quality measurements and cancellation terms are not supplied. | S1 | A6 | Material limitations, but no evidence they overturn stated gate comparison; seek terms/quality evidence if material to Nessa's choice. |

## Source register
| Source ID | Identity, author/publisher, version/revision | URL or supplied-file identity | Publication/update date | Access date | Exact locators used | Access limitation / evidence actually inspected |
|---|---|---|---|---|---|---|
| S1 | Fictional archive repair decision; author/publisher not specified; supplied packet | `input/evidence.md` | Not stated | Not applicable (local supplied file) | A1–A6 | Full eight-line supplied document read; no external sources accessed. |

## Contradictions and independence
| Claim ID | Competing accounts and source locators | Independence / recency / scope assessment | Decision effect | Resolved or deferred; what would resolve it |
|---|---|---|---|---|
| — | No competing accounts supplied. | One supplied source only; independence/corroboration cannot be assessed. | Recommendation rests on the bounded packet, not independent corroboration. | No contradiction identified. Confirm Cedar workspace as specified under U2. |

## Coverage and access log
- **Allowed evidence boundary:** Supplied fictional packet and complete supplied decision-brief bundle; task instructed supplied sources only. Decision claims drawn only from the packet.
- **Sources reviewed:** S1.
- **Not reviewed / inaccessible / partial:** No public sources, external corroboration, quality measurements, cancellation terms, or workspace confirmation were supplied or accessed.
- **Embedded instruction or prompt-injection content ignored as untrusted data:** None noted.
- **Claims used in brief:** C1, C2, C3, C4, C5, U1, C6, C7, U2, C8, U3.
