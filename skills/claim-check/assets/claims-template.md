# Claim ledger

## Scope and coverage

- Draft identity/version: [identify exact draft]
- Cutoff and jurisdiction/product/version: [state or not specified]
- Evidence boundary: [permitted material/retrieval; state no external retrieval if none]
- Read/access limits: [including unreadable/truncated material]
- Coverage status: [complete within readable scope / partial; explain]

### Paragraph-to-claim coverage map

Map **every** draft paragraph to claim IDs, reasoned exclusions, or explicitly unchecked content. IDs must point back to the exact paragraph. Reconcile independently in both directions; report omissions, duplicates, orphan IDs, wrong-paragraph mappings, and split facets. Coverage is semantic, not a count or span-match exercise.

| Draft paragraph/location | Claim IDs | Exclusion IDs and reasons | Unchecked portions and reason |
|---|---|---|---|
| [paragraph ID] | [IDs or none] | [IDs/reasons or none] | [content/reason or none] |

## Standalone source inventory

Give each source a stable ID; every evidence record below cross-links to this inventory. Record identity/title, author or speaker, source type, version/date, retrieval date only when actually retrieved, access/read limits, methods/authority where known, and independence/origin. Identify absent attachments. Distinguish source assertion from independently established fact.

| Source ID | Identity / author or speaker | Type, version/date | Retrieval date (if retrieved) | Read/access limits; authority, methods, independence |
|---|---|---|---|---|
| [S1] | [details] | [details] | [date or not retrieved] | [details] |

## Atomic factual claims

One record per distinct proposition. Preserve the exact draft quotation and precise location. Record all occurrences if identical claims share an ID. Split separate propositions such as an event occurring, independence, a reported finding, and underlying truth. Include conflicting passages and counterevidence; do not vote or silently resolve a conflict.

### [C1] — [Supported / Overstated / Contradicted / Unresolved]

- **Draft location and exact quotation:** [paragraph/sentence/clause ID; exact text]
- **Proposition tested:** [one precise claim]
- **Evidence:** [source ID, exact quotation or labeled faithful paraphrase, precise page/paragraph/section/table locator, source version/date]
- **Counterevidence / conflict:** [source IDs, quotations and locators, or none found within scope]
- **Reason for verdict:** [why these sources support, narrow, directly conflict with, or fail to resolve this exact proposition; qualifications, population, denominator, time, units, scope and attribution]
- **Unresolved reason (if applicable):** [missing / access-limited / ambiguous / stale / scope-mismatch / conflicting, with explanation]
- **Executed calculation (if applicable):** Inputs and units: [values]; formula: [expression]; tool/result: [actual executed result]. If not executable, state why and use Unresolved; never supply a guessed result.
- **Minimal proposed correction/action:** [limited text grounded by evidence, or attribute/remove/verify; proposal only]
- **Limitations:** [independence, methods, source origin, cutoff, access, and what this does not establish]

## Reasoned exclusions

### [E1] — [draft location]

- **Exact quotation:** [text]
- **Reason excluded:** [opinion, value judgment, prediction, metaphor, or other non-factual content]
- **Embedded factual premise checked separately:** [claim ID or none, with reason]
