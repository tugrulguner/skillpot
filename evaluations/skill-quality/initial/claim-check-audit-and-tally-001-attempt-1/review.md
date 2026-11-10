# Claim-check review

**Draft version:** “Fictional draft for review,” version 1.2; prepared 3 June (year unspecified).\
**Cutoff:** Not specified; jurisdiction not specified. Product/context: fictional AcmeFlow / Northstar.\
**Evidence boundary:** Supplied `sources.md` appendix only; no external retrieval.\
**Audience:** Not specified.\
**Access / coverage:** Complete review of readable draft and appendix within this boundary. No audit report, statement of work, benchmark underlying data, or incident records were supplied.\
**Source inventory:** See `claims.md` S1–S3. Vendor sheet S1 is vendor-published; S2 is a commissioning letter limited to planned engagement; S3 is an internal tally. None independently corroborates the others.

## Paragraph coverage map

| Draft paragraph/location | Claim IDs | Reasoned exclusions | Explicitly unchecked content |
|---|---|---|---|
| P1, `draft.md` line 7 | C1–C3 | none | none |
| P2, line 11 | C4–C8 | none | none |
| P3, line 15 | C9–C12 | none | none |
| P4, line 19 | C13–C17 | none | none |

## Material findings and proposed local edits

- **C1–C2 / P1 — Benchmark scope and Northstar causation.** **Overstated** as “across all customers last year”: S1 reports a vendor benchmark of 25 customers, median processing time, and a comparison with each customer's prior measurement window; it does not identify Northstar or report a control group (S1, `sources.md` lines 3–5). The Northstar-specific causal claim is **Unresolved** for lack of team data and causal evidence. Proposed local edit: “AcmeFlow’s revision 3 sheet reports that, among 25 customers in its 2025 benchmark, median processing time was 40% lower with AcmeFlow enabled than in each customer’s prior measurement window.” Remove the conclusion that AcmeFlow therefore caused a 40% improvement for Northstar's team unless separately supported. Attribution alone (C3) is supported; it does not validate the result.
- **C4–C8 / P2 — Commissioning is not an independent completed audit or a security proof.** Northstar's commissioning and planned 18 March start are **Supported** (C4; S2, `sources.md` lines 7–9). Independence (C5), completion (C6), and the reported “no critical issues” finding (C7) are **Unresolved**: the letter says independence arrangements would be documented separately and does not report fieldwork, completion, or findings. The claim that this “proves the product is secure” is **Overstated** (C8); the letter expressly gives no security opinion. Proposed edit: “Northstar commissioned Cedar Audit Group to review the AcmeFlow deployment, with work planned to begin 18 March.” Remove the independence, completion, finding, and security-proof assertions unless the missing evidence is obtained; even a report would not automatically prove product security.
- **C9–C12 / P3 — Ticket-to-account ratio is not a rate, increase, or user-impact estimate.** The worksheet's 18 ticket and 60 account counts are supported as recorded values (C9; S3, `sources.md` lines 11–13). The calculation 18 ÷ 60 × 100 = 30.0 was executed with local Python; it is only a raw ratio of 30 logged tickets per 100 included accounts, not an established incident rate or percentage of affected accounts (C10). Rollout-caused 30% increase (C11) and 30% of all users affected (C12) are **Unresolved**: the worksheet has no baseline/comparison tally, causal analysis, user count, or impact estimate. Proposed edit: “The internal worksheet logs 18 incident tickets across 60 included accounts.” Do not report an increase or user share without corresponding denominators and comparison/causal evidence.

## Supported statements and exclusions

- **C3 / P1:** It is supported that the performance statement is attributed to a sheet published by AcmeFlow. The vendor's report must remain attributed and qualified; this does not independently establish its truth.
- **C4 / P2:** S2 supports that Northstar commissioned Cedar Audit Group to review the deployment and that the work was planned to begin 18 March. It does not support that work actually began.
- **C9, C13–C17 / P3–P4:** S3 supports the reported tally of 18 incident tickets, 60 accounts, and a 20-day pilot. It also supports the stated absences: no comparison tally, user count, or causal analysis. The packet does not establish ticket deduplication or distinct affected incidents/users.
- No reasoned exclusions: every paragraph's factual assertions and key attributions/limitations are itemized in `claims.md`.

## Unresolved evidence needs and limitations

- Northstar/team-level before/after measurements and an adequate causal comparison are absent; the vendor benchmark does not identify Northstar as a participant.
- The security statement of work and final review report are absent. Accordingly, independence, performance/completion, and findings remain unknown; the supplied letter expressly has no product-security opinion.
- The pilot worksheet's underlying tickets, incident definition, unique affected accounts/users, user denominator, comparison tally, and causal analysis are absent. The computed raw ratio does not repair those gaps.
- The packet is fictional, provides no years for the letter and worksheet dates, and supplies no additional context or independent corroboration. No external validation was authorized or performed.

## Completion boundary

Reviewed within stated scope; not factual certification, specialist security advice, an accepted rewrite, or publication approval. The owner retains approval and publication authority.
