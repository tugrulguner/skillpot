# Fresh field-consistency follow-up

**Status:** completed bounded observations, with remaining manual corrections recorded.

Four fictional packets were authored after the first v0.4.0 observations to inspect
owner/reader consistency, unknown completion status and known approval roles. They
used complete candidate bundles from commit
`6a3d6950a40e2fc6bec236741b59085e02486f8a`: decision-brief 0.1.1 and
document-actions 0.1.2. These versions are unreleased; stable v0.4.0 is unchanged.

## Observed outcomes

- **Archive decision:** the recommendation and owner action keep Nessa as decision
  owner, Luis as reader and Imani as separate purchase authorizer. The locked workspace
  stays an unresolved dependency. A separate gate-label inconsistency remains: the
  brief calls volunteer timing a failure while its ledger says actual completion
  timing is unknown. The input's “confirms completion only after the exhibition” can
  describe confirmation timing rather than when repairs finish. The defensible label
  is not established, rather than a proven timing failure. The prewritten expectation
  also overstates this distinction; neither source nor original expectation was edited.
- **Reading-room decision:** Rafi remains owner, Sera reader, purchasing/reservation
  authority unknown, and the decision is deferred. One precise locator needs repair:
  claim C4 cites B4's third sentence for the inspection note, but that note appears in
  its second compound sentence. The frame's owner and constraint claims also lack
  explicit ledger entries despite being supported by B1/B2; register those for a more
  complete audit trail.
- **Garden extraction:** no completion report stays Unknown for the grounds team and
  Bea, while Kiran's explicitly incomplete status is retained. Bea's acceptance is
  separate from completion. The sponsor approval role is retained, its individual
  representative unknown, Marta remains proposer, and all six source items have a
  canonical record including the unassigned diagrams and Jo's historical completion.
- **Harbor extraction:** unreported notice-posting completion stays Unknown while the
  explicitly not-started review retains that source wording. The grant-panel approval
  role stays known with unnamed members Unknown; Tomas is not made owner. Duplicate
  references merge, the photo has its own unassigned record, and Dalia remains attached
  to the cancelled historical task.

The targeted distinctions held in these four outputs under parent inspection. That
is narrower than claiming four error-free drafts: the decision drafts still need
manual edits, and the archive packet has an ambiguous expectation. The extraction
drafts had no additional material field correction identified in this inspection.

## Evidence and limitations

- Exactly eight expected regular output files were created and reopened. All 41
  frozen input/task/control/package files matched their pre-execution hashes.
- Supplementary guidance was actually loaded: `hermes-agent` in both decision cases
  and `document-to-action-items` in both extraction cases. Those host instruction
  contents are not published here. No visible tool-error preview was found in the
  worker logs; their output previews are truncated, so that is not a complete command
  journal or a guarantee that every underlying command was captured.
- The parent audit's first inline invocation had a SyntaxError before execution; a
  separate corrected script completed the hash/output/trace checks. This was parent
  verification, not a worker retry or change to generated outputs.
- These were one host-assisted attempt per targeted packet, with no matched baseline,
  repeated sampling, native-client activation or controlled improvement comparison.
  Additional host guidance differs from earlier observations. No result is attributed
  solely to the candidate instruction edits.
- No real user acceptance or editing time was measured. No original generated artifact
  was repaired. Source-contract tests and independent source review are separate from
  these observed-task findings.

Inputs and outputs are fictional and preserved byte-for-byte. Original location-bound
task envelopes, complete package copies, frozen controls and runner logs remain in the
private local observation directory. The source identity above identifies the bundles
that ran; a later documentation-only delivery commit is not substituted as execution
identity.

## Delivery boundary

The source change is prepared for review, not merged or published. Stable installation
still selects published v0.4.0. The findings support keeping the concise template/review
corrections while retaining manual review; they do not establish that adding further
warnings will repair the remaining adherence errors.
