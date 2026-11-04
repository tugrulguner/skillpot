# Field-consistency corrections in current source

These are unreleased source patches for `decision-brief` **0.1.1** and
`document-actions` **0.1.2**. Published collection **v0.4.0** remains at
`3624eaaf2aa6c870e1dad6190ac3466e4e378f35`; it contains decision-brief 0.1.0
and document-actions 0.1.1. Stable clone and first-use instructions still select
that published snapshot. No published tag or existing installation is changed.

## Why these checks changed

Four fresh fictional workplace attempts using the published bundles reached the
expected broad recommendation, deferral or extraction outcome, but parent inspection
found a specific wording/field correction in each draft:

- Both decision briefs named the correct decision owner in their frame but later
  gave the decision to the intended reader. Owner and audience are separate roles;
  neither automatically establishes purchasing authority.
- An extraction combined “Incomplete” with “not reported complete.” Missing completion
  evidence leaves status unknown; an explicit incomplete report must still be retained.
- An extraction marked the approval authority unknown despite a known sponsor approval
  role. A missing individual name must not erase a known role, make that role an action
  owner, or establish that approval occurred.

Follow-up inspection also found an unknown completion date labeled as a failed
hard gate, an incorrect sentence locator, and source-backed frame claims missing
from the ledger. The decision-brief evidence template and final check now explicitly
separate event timing from confirmation timing, verify cited sentence/clause locations,
and register frame/constraint claims alongside recommendation claims.

The corrections place these distinctions in drafting templates and final review,
where the original generic evidence requirements did not prevent the observed drift.
They do not add outputs, authority, dependencies or external actions.

## Evidence boundary

Source/template contract tests check that these instructions are available and that
stable defaults remain release-pinned. They cannot establish agent adherence.

A separate targeted follow-up uses four newly authored fictional packets, one ordinary
host-assisted attempt per packet, with expectations frozen before execution. These are
failure-focused follow-ups, not held-out generalization samples and not a controlled comparison.
Supplementary host guidance and tool failures must be reported from actual traces.
Do not attribute the result solely to the selected SkillPot bundle, replace original
failed outputs with retries, or claim an improvement from unpaired observations.

Original task packets and generated outputs remain preserved. The
[fresh follow-up record](../evaluations/workflow-fields/followup-001/README.md) includes
unchanged fictional inputs, all eight actual outputs and package identities. The
three targeted distinctions held under parent inspection. The original decision drafts
retain their documented gate-label/citation errors, and the archive packet's timing
expectation remains ambiguous. Separately labeled
[assisted corrected copies](../evaluations/workflow-fields/corrections-001/README.md)
repair those artifacts and qualify the frozen expectation without altering the original
attempts or packet. These corrections are not fresh task attempts or evidence of an
improvement caused by the instruction changes. Supplementary host guidance was loaded
in all four original cases.
The published [v0.4.0 record](releases/v0.4.0.md) and earlier repository evaluations
remain historical records at their original identities.
