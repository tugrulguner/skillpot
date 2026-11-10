# Claim ledger

## Scope and coverage

- Draft identity/version: `draft.md`, “Fictional draft for review,” states version 1.2, prepared 3 June (¶1); appendix does not validate it.
- Cutoff and jurisdiction/product/version: No review cutoff, jurisdiction, or product version supplied. Source dates are as transcribed below; only S1 explicitly identifies benchmark year 2025.
- Evidence boundary: Supplied fictional appendix in `sources.md` only; no external retrieval.
- Read/access limits: All supplied draft and appendix text read. No attachments or other source material supplied; S2 explicitly refers to a separate statement of work not included.
- Coverage status: Complete within readable draft and supplied appendix; claims unresolved where the packet is insufficient.

### Paragraph-to-claim coverage map

| Draft paragraph/location | Claim IDs | Exclusion IDs and reasons | Unchecked portions and reason |
|---|---|---|---|
| ¶1 (`draft.md` lines 3–7) | C1–C4 | None | None; C1 unresolved against appendix |
| ¶2 (line 11) | C5–C9 | None | None |
| ¶3 (line 15) | C10–C13 | None | None |
| ¶4 (line 19) | C14–C17 | None | None |

## Standalone source inventory

| Source ID | Identity / author or speaker | Type, version/date | Retrieval date | Read/access limits; authority, methods, independence |
|---|---|---|---|---|
| S1 | AcmeFlow, publisher/vendor | Vendor performance sheet, revision 3, 14 February; reports benchmark for 2025 | Not retrieved; supplied packet | Fully readable supplied excerpt. Interested-party statement. Reports median before/after comparison for 25 customers; no control group; Northstar not identified. No independent corroboration. |
| S2 | Northstar and Cedar Audit Group named in letter | Signed security engagement letter, 2 March | Not retrieved; supplied packet | Fully readable supplied text. Commissioning letter, not an audit report; separate statement of work absent. Explicitly says no fieldwork/completion/findings/security opinion reported. Independence arrangements not included. |
| S3 | Internal worksheet (speaker/author not named) | Pilot tally, 30 April | Not retrieved; supplied packet | Fully readable supplied excerpt. Records counts and duration only; no users, baseline/comparison tally, causal analysis, rate, or impact estimate. Origin internal; independence not established. |

## Atomic factual claims

### C1 — Unresolved
- **Draft location and exact quotation:** ¶1, `draft.md` line 3: “Draft version: 1.2, prepared 3 June.”
- **Proposition tested:** The draft is version 1.2 and was prepared 3 June.
- **Evidence:** None in appendix; no relevant source passage.
- **Counterevidence / conflict:** None found within scope.
- **Reason for verdict:** Draft asserts these metadata, but the supplied appendix neither verifies nor contradicts them.
- **Unresolved reason:** Missing corroborating draft provenance.
- **Executed calculation:** Not applicable.
- **Minimal proposed correction/action:** Verify from draft history/provenance if material.
- **Limitations:** This is not disputed by the appendix; it is simply unverified there.

### C2 — Supported
- **Draft location and exact quotation:** ¶1 line 7, clause: “The vendor says its service reduced processing time by 40% across all customers last year”.
- **Proposition tested:** The vendor says processing time was 40% lower for the described benchmark.
- **Evidence:** S1, `sources.md` ¶1: “median processing time was 40% lower with AcmeFlow enabled than in each customer's prior measurement window.”
- **Counterevidence / conflict:** No conflicting passage in packet. S1 limits this to 25 customers in the 2025 benchmark.
- **Reason for verdict:** Attribution to the vendor and 40% figure are supported, but only for median processing time in the stated benchmark; exact draft scope (“all customers,” “last year”) is tested separately in C3.
- **Minimal proposed correction/action:** Attribute the benchmark as specified in S1; see review.md.
- **Limitations:** Vendor-published, before/after comparison; no control group. Supports a reported result, not independent verification or causation.

### C3 — Overstated
- **Draft location and exact quotation:** ¶1 line 7, “across all customers last year”.
- **Proposition tested:** The 40% comparison applies to all customers in the prior calendar year.
- **Evidence:** S1, `sources.md` ¶1: “Across the 25 customers included in our 2025 benchmark”; measures prior measurement windows, not a stated calendar year.
- **Counterevidence / conflict:** S1’s bounded population and period do not establish “all customers” or “last year.”
- **Reason for verdict:** Narrower support is a vendor-reported result across 25 benchmark customers in 2025. Universal customer scope and an unspecified relative “last year” are not supported.
- **Minimal proposed correction/action:** Say “across 25 customers in its 2025 benchmark.”
- **Limitations:** Benchmark population may not represent all customers; no customer list or underlying data provided.

### C4 — Overstated
- **Draft location and exact quotation:** ¶1 line 7, “and therefore caused a 40% improvement for our team.”
- **Proposition tested:** AcmeFlow caused a 40% processing-time improvement for the draft author’s team.
- **Evidence:** S1, `sources.md` ¶1: before/after comparison, no control group, and “does not identify Northstar as a participant.”
- **Counterevidence / conflict:** No team-specific evidence; no control group reported.
- **Reason for verdict:** The appendix supports only the vendor’s benchmark comparison, not team-specific outcome or causation. “Improvement” is ambiguous; the measured quantity was median processing time.
- **Minimal proposed correction/action:** Remove causal team claim, or obtain team-specific measurements and an appropriate comparison design.
- **Limitations:** No evidence that the team is Northstar or participated; no causal method described.

### C5 — Supported
- **Draft location and exact quotation:** ¶2, `draft.md` line 11, “The company commissioned an independent security audit in March.” (commissioning facet)
- **Proposition tested:** The company commissioned Cedar Audit Group to conduct a review in March.
- **Evidence:** S2, `sources.md` ¶2: “Northstar has commissioned Cedar Audit Group to conduct a review of the AcmeFlow deployment”; signed 2 March; planned start 18 March.
- **Counterevidence / conflict:** None regarding commissioning. The letter says review, not necessarily an “audit.”
- **Reason for verdict:** Commissioning is explicitly documented. This does not establish that the review occurred or was independent (C6–C7).
- **Minimal proposed correction/action:** Use “commissioned Cedar Audit Group to conduct a review”; avoid implying performed audit.
- **Limitations:** S2 is an engagement letter, not completion evidence.

### C6 — Unresolved
- **Draft location and exact quotation:** ¶2 line 11, “independent” in “commissioned an independent security audit”.
- **Proposition tested:** The commissioned review was independent.
- **Evidence:** S2, `sources.md` ¶2: “The scope and independence arrangements will be documented in a separate statement of work.”
- **Counterevidence / conflict:** No statement of work supplied; letter does not establish independence.
- **Reason for verdict:** The draft asserts independence, but the letter defers its arrangements to missing documentation.
- **Unresolved reason:** Missing separate statement of work and evidence of actual independence.
- **Minimal proposed correction/action:** Omit “independent” unless substantiated by the statement of work and relevant facts.
- **Limitations:** Commissioning a named auditor does not itself establish independence.

### C7 — Unresolved
- **Draft location and exact quotation:** ¶2 line 11, “The audit is complete”.
- **Proposition tested:** The review was performed and completed.
- **Evidence:** S2, `sources.md` ¶2: planned to begin 18 March; letter “does not report fieldwork, completion”.
- **Counterevidence / conflict:** The planned start is not evidence that fieldwork began; no report supplied.
- **Reason for verdict:** Commissioning and planned commencement do not establish performance or completion.
- **Unresolved reason:** No fieldwork or completion record/report.
- **Minimal proposed correction/action:** Remove completion claim unless supported by final report or other completion evidence.
- **Limitations:** The letter’s silence is not proof that the review did not happen.

### C8 — Unresolved
- **Draft location and exact quotation:** ¶2 line 11, “found no critical issues”.
- **Proposition tested:** The completed review reported no critical issues.
- **Evidence:** None reporting findings. S2, `sources.md` ¶2, explicitly says the letter does not report findings.
- **Counterevidence / conflict:** No audit report or findings supplied.
- **Reason for verdict:** The packet cannot establish whether a review reported this finding; commissioning alone is not findings evidence.
- **Unresolved reason:** Missing audit report/findings.
- **Minimal proposed correction/action:** Remove pending the actual report; if later supported, attribute the finding to that report.
- **Limitations:** Does not show that the report found issues or that no issues existed.

### C9 — Unresolved
- **Draft location and exact quotation:** ¶2 line 11, “proves the product is secure.”
- **Proposition tested:** The product is secure, established by the purported audit.
- **Evidence:** S2, `sources.md` ¶2: no opinion on product security is reported. No independent security evidence supplied.
- **Counterevidence / conflict:** No security report or testing evidence in packet.
- **Reason for verdict:** Neither an audit opinion nor underlying security evidence is present; even an attributed finding would not automatically prove broad security.
- **Unresolved reason:** Missing audit report and evidence defining product/security scope.
- **Minimal proposed correction/action:** Remove claim; seek qualified review and describe any eventual findings narrowly and with attribution.
- **Limitations:** No universal security conclusion can be drawn from this packet.

### C10 — Supported
- **Draft location and exact quotation:** ¶3, `draft.md` line 15: “The pilot recorded 18 incidents among 60 accounts”.
- **Proposition tested:** The pilot tally records 18 incident tickets across 60 accounts.
- **Evidence:** S3, `sources.md` ¶3: “Accounts included: 60. Incident tickets logged: 18.”
- **Counterevidence / conflict:** None in packet.
- **Reason for verdict:** The count and account denominator match the worksheet; “incidents” should remain attributed as logged incident tickets, not necessarily distinct events.
- **Minimal proposed correction/action:** Say “worksheet logged 18 incident tickets across 60 accounts.”
- **Limitations:** Worksheet supplies no incident definitions or deduplication method.

### C11 — Overstated
- **Draft location and exact quotation:** ¶3 line 15: “so the incident rate was 30%”.
- **Proposition tested:** The incident rate was 30%.
- **Evidence:** S3, `sources.md` ¶3: 18 tickets, 60 accounts, 20 days; no rate or impact estimate.
- **Counterevidence / conflict:** No user count, time-based denominator, baseline, or rate definition supplied.
- **Reason for verdict:** Executed arithmetic from supplied counts: 18 tickets ÷ 60 accounts × 100 = 30 tickets per 100 accounts. This ratio does not establish an incident rate or percentage of accounts/users with incidents.
- **Executed calculation:** Inputs: 18 incident tickets; 60 accounts. Formula: 18 ÷ 60 × 100. Python standard-library arithmetic executed locally; result 30.0 tickets per 100 accounts. It is a count ratio, not a rate.
- **Minimal proposed correction/action:** Replace with “18 incident tickets across 60 accounts”; do not label 30% an incident rate.
- **Limitations:** No unique affected-account count, user denominator, exposure-time rate, or incident definition.

### C12 — Unresolved
- **Draft location and exact quotation:** ¶3 line 15: “this shows the rollout caused a 30% increase”.
- **Proposition tested:** The rollout caused a 30% increase in incidents.
- **Evidence:** S3, `sources.md` ¶3: no baseline/comparison tally or causal analysis.
- **Counterevidence / conflict:** Neither comparison value nor causal evidence is supplied.
- **Reason for verdict:** The observed count ratio in C11 cannot establish an increase without a baseline, or causation without causal analysis.
- **Unresolved reason:** Missing comparison tally and causal analysis; no increase can be calculated from given inputs.
- **Minimal proposed correction/action:** Remove the increase/causation assertion; obtain comparable baseline and suitable causal evidence.
- **Limitations:** Missing evidence does not show that there was no increase.

### C13 — Unresolved
- **Draft location and exact quotation:** ¶3 line 15: “affected 30% of all users.”
- **Proposition tested:** 30% of all users were affected.
- **Evidence:** S3, `sources.md` ¶3: 60 accounts; no number of users; no impact estimate.
- **Counterevidence / conflict:** Account count is not a user count; no affected-user count supplied.
- **Reason for verdict:** Neither numerator of affected users nor denominator of all users is available. C11’s 30 tickets per 100 accounts cannot be transformed into user prevalence.
- **Unresolved reason:** Missing user and affected-user counts.
- **Minimal proposed correction/action:** Remove pending user-level counts and defined impact measure.
- **Limitations:** No supported percentage of accounts affected either, since tickets need not map one-to-one to accounts.

### C14 — Supported
- **Draft location and exact quotation:** ¶4, `draft.md` line 19: “the pilot ran for 20 days”.
- **Proposition tested:** The worksheet states pilot duration was 20 days.
- **Evidence:** S3, `sources.md` ¶3: “Pilot duration: 20 days.”
- **Counterevidence / conflict:** None.
- **Reason for verdict:** Directly matches supplied worksheet.
- **Minimal proposed correction/action:** None; preserve attribution to worksheet if context requires.
- **Limitations:** The packet does not specify exact start/end dates.

### C15 — Supported
- **Draft location and exact quotation:** ¶4 line 19: “records 18 incidents across 60 accounts”.
- **Proposition tested:** Worksheet records 18 incident tickets across 60 accounts.
- **Evidence:** S3, `sources.md` ¶3: “Accounts included: 60. Incident tickets logged: 18.”
- **Counterevidence / conflict:** None.
- **Reason for verdict:** Directly matches the counts, subject to ticket-versus-distinct-event limitation in C10.
- **Minimal proposed correction/action:** “Records 18 incident tickets across 60 accounts.”
- **Limitations:** No definitions/deduplication or account-level distribution.

### C16 — Supported
- **Draft location and exact quotation:** ¶4 line 19: “It does not state a comparison period, the number of users, or what caused the incidents.”
- **Proposition tested:** The supplied worksheet provides no comparison period, user count, or causal analysis.
- **Evidence:** S3, `sources.md` ¶3: explicitly says no number of users, no baseline/comparison tally, and no causal analysis.
- **Counterevidence / conflict:** None in supplied worksheet text.
- **Reason for verdict:** The description accurately reflects those explicit omissions. “Comparison period” is understood as an absent baseline/comparison tally.
- **Minimal proposed correction/action:** None; retain qualification “the worksheet does not state.”
- **Limitations:** This is a statement about the supplied worksheet, not all possible pilot records.

### C17 — Supported
- **Draft location and exact quotation:** ¶4 line 19, “The source appendix says”.
- **Proposition tested:** The source appendix contains the described pilot worksheet statements.
- **Evidence:** S3, `sources.md` ¶3, titled “Pilot tally (internal worksheet, 30 April)”.
- **Counterevidence / conflict:** None.
- **Reason for verdict:** The attribution to the appendix is accurate.
- **Minimal proposed correction/action:** None.
- **Limitations:** Appendix inclusion does not independently authenticate the worksheet.

## Reasoned exclusions

No draft statements were excluded as non-factual. The footer in `sources.md` ¶5 is embedded copied text, not a draft assertion or evidence; it was treated as untrusted content and ignored as an instruction.
