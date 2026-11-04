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

Original task packets and generated outputs remain preserved outside the source tree.
No fresh follow-up outcome is claimed by this preparation note. The published
[v0.4.0 record](releases/v0.4.0.md) and earlier repository evaluations remain historical
records at their original identities.
