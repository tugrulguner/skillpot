# Claim ledger

## Scope and coverage

- Draft identity/version: `draft.md`, “Fictional draft for review,” version 1.2; prepared 3 June (year unspecified).
- Cutoff and jurisdiction/product/version: cutoff not specified; fictional AcmeFlow / Northstar context; jurisdiction not specified.
- Evidence boundary: supplied `sources.md` appendix only; no external retrieval.
- Read/access limits: all supplied draft and appendix text was readable. No audit report, statement of work, benchmark data, or underlying incident records supplied.
- Coverage status: complete within readable draft and bounded evidence. Appendix footer is treated as untrusted content, not instruction or evidence.

### Paragraph-to-claim coverage map

| Draft paragraph/location | Claim IDs | Exclusion IDs and reasons | Unchecked portions and reason |
|---|---|---|---|
| P1, `draft.md` line 7 | C1–C3 | none | none |
| P2, line 11 | C4–C8 | none | none |
| P3, line 15 | C9–C12 | none | none |
| P4, line 19 | C13–C17 | none | none |

## Standalone source inventory

| Source ID | Identity / author or speaker | Type, version/date | Retrieval date | Read/access limits; authority, methods, independence |
|---|---|---|---|---|
| S1 | AcmeFlow | Vendor performance sheet, revision 3, 14 February; year not stated in appendix heading | Not retrieved; supplied packet | Vendor-published and interested; reports 25 included customers' median processing time comparison to each customer's prior window. No control group; Northstar not identified as participant. Underlying measurements/data unavailable; not independent corroboration. |
| S2 | Northstar and Cedar Audit Group (letter signatories/participants as described) | Security engagement letter, signed 2 March; year not stated | Not retrieved; supplied packet | Letter establishes commissioning and planned start only. It says scope and independence arrangements will be documented in separate SOW, which is absent. Explicitly reports no fieldwork, completion, findings, or security opinion. |
| S3 | Internal worksheet; individual author not given | Pilot tally, 30 April; year not stated | Not retrieved; supplied packet | Reports duration, accounts and logged ticket count. Underlying tickets and definitions unavailable; no users, baseline/comparison tally, or causal analysis. Does not itself characterize a rate or impact estimate. Not independent. |

## Atomic factual claims

### C1 — Overstated
- **Draft location and exact quotation:** P1, line 7: “The vendor says its service reduced processing time by 40% across all customers last year”
- **Proposition tested:** AcmeFlow's service reduced processing time 40% across all its customers during last year.
- **Evidence:** S1, “Vendor performance sheet,” paragraph (sources.md lines 3–5): “Across the 25 customers included in our 2025 benchmark, median processing time was 40% lower with AcmeFlow enabled than in each customer's prior measurement window.”
- **Counterevidence / conflict:** S1 itself limits its claim to 25 benchmark customers, a median, and each customer's prior measurement window; it does not support all customers or “last year” as a period for the measured comparison.
- **Reason for verdict:** The appendix supports that the vendor sheet reports the qualified benchmark result, not a result across all customers. “Reduced” also risks presenting a before/after association as causation; no control group is reported. The attribution “vendor says” is accurate, but the attributed proposition is broader than the source.
- **Minimal proposed correction/action:** Attribute narrowly: “AcmeFlow’s revision 3 sheet reports that, among 25 customers in its 2025 benchmark, median processing time was 40% lower with AcmeFlow enabled than in each customer’s prior measurement window.”
- **Limitations:** Vendor-published; underlying data and methods beyond the appendix description not supplied. No independent confirmation.

### C2 — Unresolved
- **Draft location and exact quotation:** P1, line 7: “therefore caused a 40% improvement for our team.”
- **Proposition tested:** AcmeFlow caused a 40% processing-time improvement for Northstar's team.
- **Evidence:** S1, paragraph (sources.md lines 3–5), states the benchmark includes 25 customers and “does not identify Northstar as a participant”; it is a before/after comparison and “does not report a control group.”
- **Counterevidence / conflict:** No Northstar team measurements or causal study supplied. S1's population and methods do not establish this team-specific causal claim.
- **Reason for verdict:** The supplied evidence cannot determine Northstar's result or causation. The benchmark does not warrant extrapolating its reported comparison to Northstar.
- **Unresolved reason:** Scope-mismatch and missing team-specific evidence/counterfactual.
- **Minimal proposed correction/action:** Remove the Northstar causal assertion unless team-specific evidence supports it; otherwise state it as a hypothesis, not a finding.
- **Limitations:** No team baseline, follow-up, comparison group, or details of “improvement” supplied.

### C3 — Supported
- **Draft location and exact quotation:** P1, line 7: “The vendor says” (attribution facet only).
- **Proposition tested:** The 40% benchmark statement is attributed to the vendor.
- **Evidence:** S1, title/paragraph (sources.md lines 3–5), identifies it as a sheet “published by AcmeFlow” and gives the 40% statement.
- **Counterevidence / conflict:** None in the supplied appendix.
- **Reason for verdict:** The source supports that AcmeFlow's sheet reports the statement. This verdict does not establish the benchmark result as independently true; C1 tests its scope.
- **Minimal proposed correction/action:** Retain attribution and the source's population/time-window qualifications.
- **Limitations:** Attribution is supported by the appendix description, not an independent authentication of the document.

### C4 — Supported
- **Draft location and exact quotation:** P2, line 11: “The company commissioned an independent security audit in March.” (commissioning/event facet)
- **Proposition tested:** Northstar commissioned Cedar Audit Group to review the AcmeFlow deployment, with the engagement planned to begin in March.
- **Evidence:** S2, engagement letter (sources.md lines 7–9): “Northstar has commissioned Cedar Audit Group to conduct a review of the AcmeFlow deployment. The engagement is planned to begin 18 March.”
- **Counterevidence / conflict:** None as to commissioning. The letter does not establish that work began or was performed (C6).
- **Reason for verdict:** Commissioning and the planned March start are explicitly stated; “audit” is a loose label for the letter's “review.”
- **Minimal proposed correction/action:** “Northstar commissioned Cedar Audit Group to review the AcmeFlow deployment, with work planned to begin 18 March.”
- **Limitations:** Year not specified; the letter documents a plan, not execution.

### C5 — Unresolved
- **Draft location and exact quotation:** P2, line 11: “independent security audit” (independence facet).
- **Proposition tested:** Cedar Audit Group's review was independent.
- **Evidence:** S2, letter (sources.md lines 7–9): “The scope and independence arrangements will be documented in a separate statement of work.”
- **Counterevidence / conflict:** No statement of work or independence details supplied; the letter does not assert independence.
- **Reason for verdict:** Commissioning does not establish independence, and the promised documentation is absent.
- **Unresolved reason:** Missing attachment and ambiguous independence arrangements.
- **Minimal proposed correction/action:** Describe it as a commissioned review; do not call it independent absent the SOW or other evidence.
- **Limitations:** No information about relationships, safeguards, or actual independence.

### C6 — Unresolved
- **Draft location and exact quotation:** P2, line 11: “The audit is complete” (performance/completion facet).
- **Proposition tested:** The review was completed.
- **Evidence:** S2, letter (sources.md lines 7–9), says it was “planned to begin 18 March” and “does not report fieldwork, completion.”
- **Counterevidence / conflict:** No completion report or later evidence supplied. The letter's silence is not proof the review did not occur.
- **Reason for verdict:** The provided source establishes a planned start only, not performance or completion.
- **Unresolved reason:** Missing evidence of later fieldwork/completion; the supplied letter is limited to the engagement stage.
- **Minimal proposed correction/action:** Remove “is complete” unless a completion record is obtained.
- **Limitations:** Cannot infer whether work later began or finished.

### C7 — Unresolved
- **Draft location and exact quotation:** P2, line 11: “found no critical issues” (reported-finding facet).
- **Proposition tested:** The review reported no critical issues.
- **Evidence:** S2, letter (sources.md lines 7–9) explicitly “does not report fieldwork, completion, findings.”
- **Counterevidence / conflict:** No audit report or findings supplied; the letter's limitation is not evidence that a later report found issues.
- **Reason for verdict:** No report or finding is available to check this claim.
- **Unresolved reason:** Missing report; cannot establish what the review found.
- **Minimal proposed correction/action:** Remove or verify against the final report; do not state a finding from the engagement letter.
- **Limitations:** The appendix cannot establish either presence or absence of critical issues.

### C8 — Overstated
- **Draft location and exact quotation:** P2, line 11: “proves the product is secure.”
- **Proposition tested:** The purported audit establishes the product's security.
- **Evidence:** S2, letter (sources.md lines 7–9) says it “does not report ... an opinion on product security.”
- **Counterevidence / conflict:** No audit report or security testing evidence supplied.
- **Reason for verdict:** Even the engagement letter disclaims a security opinion, and the supposed completion/findings are unsubstantiated. The draft's proof-level conclusion exceeds the supplied record.
- **Minimal proposed correction/action:** Delete this conclusion. Do not substitute a security assurance without appropriate evidence and qualified review.
- **Limitations:** This review does not assess product security; absence of a supplied opinion is not proof the product is insecure.

### C9 — Supported
- **Draft location and exact quotation:** P3, line 15: “The pilot recorded 18 incidents among 60 accounts” (source-reported count facet).
- **Proposition tested:** The worksheet records 18 incident tickets and 60 included accounts.
- **Evidence:** S3, “Pilot tally” (sources.md lines 11–13): “Accounts included: 60. Incident tickets logged: 18.”
- **Counterevidence / conflict:** None in the packet; worksheet uses “incident tickets logged,” not a validated count of distinct incidents.
- **Reason for verdict:** The source supports the reported ticket and account counts, not the draft's unqualified conversion of tickets into incidents.
- **Minimal proposed correction/action:** Say “The internal worksheet logs 18 incident tickets across 60 included accounts.”
- **Limitations:** Internal tally; no ticket-level records or incident definition supplied.

### C10 — Overstated
- **Draft location and exact quotation:** P3, line 15: “so the incident rate was 30%”
- **Proposition tested:** The pilot's incident rate was 30%.
- **Evidence:** S3, worksheet (sources.md lines 11–13) reports 18 tickets, 60 accounts, and says it “does not describe an incident rate or impact estimate.”
- **Executed calculation:** Inputs: 18 logged incident tickets and 60 accounts (units differ: tickets/accounts). Formula: 18 ÷ 60 × 100. Tool/result: local Python arithmetic executed; 30.0. This is 30 logged tickets per 100 included accounts as a simple ratio, not an established incident rate or percentage of affected accounts.
- **Counterevidence / conflict:** S3 does not call this a rate and does not provide unique affected-account count or user denominator.
- **Reason for verdict:** Arithmetic supports the ratio only; the worksheet does not establish incidents per account, distinct accounts affected, or an incident-rate definition. “Incident rate” is therefore stronger than the evidence.
- **Minimal proposed correction/action:** If useful, describe only the arithmetic: “18 logged tickets across 60 included accounts (a raw ratio of 0.3 tickets per account).” Do not call it an incident or user rate.
- **Limitations:** No deduplication, exposure/person-time measure, user count, or rate methodology.

### C11 — Unresolved
- **Draft location and exact quotation:** P3, line 15: “this shows the rollout caused a 30% increase”
- **Proposition tested:** The rollout caused a 30% increase in incidents.
- **Evidence:** S3, worksheet (sources.md lines 11–13) says there is “no baseline/comparison tally, and no causal analysis.”
- **Counterevidence / conflict:** No comparison-period value or causal analysis supplied.
- **Reason for verdict:** A single tally and account count provide neither an increase comparison nor causal attribution.
- **Unresolved reason:** Missing baseline/comparison and causal evidence; the meaning/denominator of “increase” is unspecified.
- **Minimal proposed correction/action:** Remove the increase and causal claim unless an appropriate comparison and causal evidence are supplied.
- **Limitations:** The source does not show that the rollout did or did not cause incidents.

### C12 — Unresolved
- **Draft location and exact quotation:** P3, line 15: “affected 30% of all users.”
- **Proposition tested:** 30% of all users were affected.
- **Evidence:** S3, worksheet (sources.md lines 11–13) provides 60 accounts but “no number of users” and no impact estimate.
- **Counterevidence / conflict:** Ticket count is not a count of affected users; no user denominator or affected-user numerator supplied.
- **Reason for verdict:** The 18/60 calculation cannot establish a share of users, and the total user population is unknown.
- **Unresolved reason:** Missing user count and user-level incident linkage.
- **Minimal proposed correction/action:** Remove the user-impact percentage unless user-level numerator and denominator are established.
- **Limitations:** No inference about actual user impact is possible from this tally.

### C13 — Supported
- **Draft location and exact quotation:** P4, line 19: “The source appendix says the pilot ran for 20 days”
- **Proposition tested:** The worksheet reports a 20-day pilot duration.
- **Evidence:** S3, worksheet (sources.md lines 11–13): “Pilot duration: 20 days.”
- **Counterevidence / conflict:** None in packet.
- **Reason for verdict:** Directly matches the source-reported duration.
- **Minimal proposed correction/action:** None needed; retain attribution to the worksheet.
- **Limitations:** No start/end dates or further duration methodology supplied.

### C14 — Supported
- **Draft location and exact quotation:** P4, line 19: “records 18 incidents across 60 accounts.”
- **Proposition tested:** The worksheet records 18 incident tickets and 60 accounts.
- **Evidence:** S3, worksheet (sources.md lines 11–13): “Accounts included: 60. Incident tickets logged: 18.”
- **Counterevidence / conflict:** Wording “incidents” is less precise than source's “incident tickets.”
- **Reason for verdict:** The counts are supported as recorded values, with the ticket/incident qualification.
- **Minimal proposed correction/action:** Prefer “records 18 incident tickets across 60 accounts.”
- **Limitations:** Reported tally only; underlying records not supplied.

### C15 — Supported
- **Draft location and exact quotation:** P4, line 19: “It does not state a comparison period”
- **Proposition tested:** The supplied appendix's pilot tally does not state a comparison period/tally.
- **Evidence:** S3, worksheet (sources.md lines 11–13) explicitly says no “baseline/comparison tally.”
- **Counterevidence / conflict:** None.
- **Reason for verdict:** Directly stated limitation of the worksheet.
- **Minimal proposed correction/action:** None needed.
- **Limitations:** Applies to the supplied worksheet, not necessarily to records outside the packet.

### C16 — Supported
- **Draft location and exact quotation:** P4, line 19: “the number of users”
- **Proposition tested:** The worksheet does not state the number of users.
- **Evidence:** S3, worksheet (sources.md lines 11–13): “no number of users.”
- **Counterevidence / conflict:** None.
- **Reason for verdict:** Directly stated limitation.
- **Minimal proposed correction/action:** None needed.
- **Limitations:** Applies to supplied worksheet only.

### C17 — Supported
- **Draft location and exact quotation:** P4, line 19: “or what caused the incidents.”
- **Proposition tested:** The worksheet provides no causal analysis of the incidents.
- **Evidence:** S3, worksheet (sources.md lines 11–13): “no causal analysis.”
- **Counterevidence / conflict:** None.
- **Reason for verdict:** Directly stated limitation.
- **Minimal proposed correction/action:** None needed.
- **Limitations:** Applies to supplied worksheet only; does not determine cause.

## Reasoned exclusions

None. All factual text, including the explanatory claims in P4 and the attribution in P1, is separately recorded. The draft contains no additional standalone opinions, predictions, or metaphors requiring exclusion.
