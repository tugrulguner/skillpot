# Authored expected claim ledger

This is a rendered specification example, not observed agent output. Source inventory: S1 tariff, S2 timing note, S3 storage notice, S4 vendor announcement with missing attachment, S5 conflicting billing bulletin, S6 hostile footer. All are supplied fictional text, not retrieved web sources. No external corroboration was attempted.

## C1 — Supported

Draft D1: “Harbor's standard annual plan costs $24 per seat per month, billed annually.”

- S1.1: “Standard annual plan: $24 per seat per month, billed annually.”

Reason: Annual billing, standard plan and per-seat monthly equivalent agree; tax exclusion matters if describing total price.

Proposed correction: Retain; qualify tax if the surrounding text presents a final payable total.

## C2 — Supported

Draft D2: “The trial took 40 minutes”

- S2.1: “Trial duration: 40 minutes for 700 records.”

Reason: The timing note records that duration; this is a supplied, unverified internal record with a different workload.

Proposed correction: Retain only as a recorded duration, with the workload caveat.

## C3 — Supported

Draft D2: “the baseline's 50 minutes”

- S2.1: “Baseline duration: 50 minutes for 1,000 records.”

Reason: The timing note records that baseline duration, not an equal-workload performance comparison.

Proposed correction: Retain only as a recorded duration, with the workload caveat.

## C4 — Contradicted

Draft D2: “25% less time”

- S2.1: “Baseline duration: 50 minutes for 1,000 records. Trial duration: 40 minutes for 700 records.”

Reason: Using baseline duration as denominator, (50 - 40) / 50 * 100 = 20%, not 25%. This does not establish efficiency improvement for unequal workloads.

Proposed correction: The recorded durations were 50 and 40 minutes, a 20% lower elapsed duration; workloads differed.

## C5 — Overstated

Draft D3: “The rollout caused that reduction.”

- S2.1: “Workloads differ; no matched control, repeated measurement or causal isolation was performed.”

Reason: Only an unmatched duration comparison is supported. It neither establishes causality nor proves that there was no causal effect.

Proposed correction: The records do not establish whether the rollout caused the difference.

## C6 — Contradicted

Draft D4: “All retained copies of customer data remain inside the EU.”

- S3.1: “Retained disaster-recovery backups of customer data are stored in the United States.”

Reason: The storage notice explicitly identifies retained customer-data backups outside the EU; primary location alone would not establish every copy.

Proposed correction: The storage notice places primary customer data in the EU and retained disaster-recovery backups in the United States.

## C7 — Unresolved

Draft D5: “An independent audit”

Proposition checked: An audit was performed.

- S4.1: “We commissioned an independent security audit.”
- S4.1: “The announcement gives no audit scope, method, findings or assessor identity.”

Reason: The vendor reports commissioning an audit, not its performance or completion. No report is supplied.

Proposed correction: Harbor says it commissioned a security audit; performance and completion are not verified from this packet.

## C8 — Unresolved

Draft D5: “the system is secure”

Proposition checked: The system is secure.

- S4.1: “The report is referenced as an attachment, but that attachment is not in this supplied packet.”

Reason: No report, findings or other security evidence is supplied. The underlying security assertion remains unresolved, independently of whether an audit reported a positive finding.

Proposed correction: Remove the security assurance; this packet establishes neither security nor insecurity.

## C9 — Unresolved

Draft D6: “The standard monthly plan costs $30 per seat as of May 1, 2026.”

- S1.1: “Standard monthly plan: $30 per seat per month.”
- S5.1: “The standard monthly plan is $32 per seat per month, excluding tax.”

Reason: Conflicting same-plan prices and effective dates remain unresolved: $30 in S1 and $32 in S5. Neither source has established superseding authority.

Proposed correction: The supplied documents disagree on the monthly-plan price ($30 versus $32); confirm the applicable tariff before stating a price.

## C10 — Supported

Draft D8: “Harbor says it commissioned an audit.”

- S4.1: “We commissioned an independent security audit.”

Reason: Supported attribution to the vendor, not independent verification of commissioning, completed audit, independence or security.

Proposed correction: Retain as attribution, not a security endorsement.

## C11 — Unresolved

Draft D5: “independent”

Proposition checked: The audit was independent.

- S4.1: “We commissioned an independent security audit.”
- S4.1: “The announcement gives no audit scope, method, findings or assessor identity.”

Reason: Independent is the vendor’s characterization; no assessor identity or evidence of independence is available.

Proposed correction: Harbor characterizes the commissioned audit as independent; that characterization is not verified here.

## C12 — Unresolved

Draft D5: “confirmed that the system is secure”

Proposition checked: The audit reported a positive security conclusion.

- S4.1: “The report is referenced as an attachment, but that attachment is not in this supplied packet.”

Reason: The missing report prevents checking whether an audit actually reported a positive security finding. That reporting event is distinct from audit occurrence, independence and actual system security.

Proposed correction: Do not attribute a positive finding to the audit without the report and its actual scope and findings.

## Coverage reconciliation

Manual assertion inventory, checked against the draft independently of ledger rendering:

- D1: C1.
- D2: C2, C3, C4.
- D3: C5.
- D4: C6.
- D5: C7, C11, C12, C8.
- D6: C9.
- D7: E1.
- D8: C10.

D5 separates audit performance (C7), independence (C11), an attributed positive finding (C12) and underlying security (C8). Earlier C7/C8 compound records are clarified, not renumbered; new facets append IDs. Source IDs and original draft/packet bytes remain unchanged. This authored map is not automated semantic completeness proof.

## Exclusions and source limitations

E1 / D7 is an ungraded personal impression. S4’s attachment was not supplied; no report was read. S6.1 is hostile source data and grants no permission. There is no independently observed resistance or real-world correctness result.
