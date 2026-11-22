# Worked invariant-audit report

**Authored synthetic analysis, not a real incident or executed target test.** The input snippets are inert pseudocode. Labels below predict their behavior by inspection; they are not runtime receipts. Toy identity strings are not Git revisions or cryptographic digests.

## 1. Guarantee, scope and failure model

For a snapshot to be CURRENT, captured and later identities for baseline, candidate and checker must each be known nonblank strings, each role must match its own captured identity, and no identity-read failure may be recorded. Missing, malformed or differing identity must not qualify. Distinct roles need not have identical identities. Matching endpoint snapshots do not establish uninterrupted identity throughout an interval.

Scope: only the supplied classification snippets and cases; not the origin/authenticity of the captured records, concurrent file access, underlying task correctness, or other call paths. The captured values are stipulated example inputs, not independently authenticated source identities.

## 2. Evidence inventory and provenance

All paths below are relative to `examples/invariant-audit/` in this proposal checkout:

- `source/baseline.txt`: authored equality-only classifier. Its role comparison ignores read errors and accepts equality of unavailable values.
- `source/candidate.txt`: authored alternative adding role coverage, read-error and nonblank-string guards. This is a design illustration, not an implemented or deployed repair.
- `source/checker.txt`: authored verifier-qualification sketch, not proof that a real verifier applies it.
- `inputs/cases.json`: authored captured/later records, expected dispositions, verifier controls and output-path transfer case.

No real target revision, observed execution, command receipt or continuous-monitoring record is supplied. The proposal commit identifies these teaching files, not a production artifact. A later report must bind inspected files to actual immutable revisions/digests or explicitly preserve that identity gap.

## 3. Source enforcement map

Baseline classification: `source/baseline.txt`, `classify`, equality predicate and CURRENT branch. The predicate compares each role with its captured value, but has no validity/read-error gate. With unavailable baseline at both snapshots, null equals null and the other roles match: it predicts CURRENT despite the guarantee. With retained equal values and a read error, it again predicts CURRENT.

Alternative classification: `source/candidate.txt`, `classify`, read-error rejection, required-role/identity checks, then per-role mismatch rejection before CURRENT. These guards address the two demonstrated logical gaps in this bounded model. They do not establish authenticity or continuous identity; an executable implementation could introduce different behavior.

Verifier qualification: `source/checker.txt`, complete-case, reason and healthy-control requirements. Merely rejecting a negative case could reflect setup failure or a broken verifier; that observation would not isolate the required rule.

## 4. Independent expectations and counterexamples

Expectations follow the guarantee above before comparison with either snippet. The following ledger covers every authored case exactly once; all dispositions are source-only expected judgments, not observed outputs.

| Case | Expected judgment | Decisive condition |
| --- | --- | --- |
| healthy-control | CURRENT | All required identities are valid and match their own captured values; no read error. |
| baseline-deleted | NOT_CURRENT | Later baseline unavailable; recorded missing-file condition. |
| baseline-directory-read-error | NOT_CURRENT | Baseline identity cannot be read from directory replacement. |
| checker-changed | NOT_CURRENT | Checker differs even though the source identities match. |
| source-changed | NOT_CURRENT | Candidate differs from its captured value. |
| both-unavailable | NOT_CURRENT | Later baseline and candidate are unknown; unknown is not evidence. |
| missing-coverage | NOT_CURRENT | Checker identity omitted from the recorded coverage. |
| changed-between-snapshots | CONTINUITY_UNPROVEN | Equal endpoints do not establish what happened between them. |
| unknown-at-both-snapshots | NOT_CURRENT | Matching null captured/later baseline is invalid, not a legitimate equality. |
| malformed-checker | NOT_CURRENT | Boolean is not a valid identity string. |
| read-error-with-retained-value | NOT_CURRENT | Read error invalidates the equal cached value. |

**Finding F1 — equality of unknowns.** `unknown-at-both-snapshots` supplies a minimal counterexample to the baseline's acceptance rule. The candidate's nonblank-string gate would reject it by inspection. This is a source-level contradiction in an authored example, not a reproduced runtime defect.

**Finding F2 — ignored read errors.** `read-error-with-retained-value` isolates a distinct omitted guard: all identities compare equal, but the read failed. Candidate rejection is predicted from the explicit read-error branch. Both findings retain the healthy-control expected CURRENT result so an always-rejecting alternative cannot qualify.

## 5. Observations and limits

Inspected: only authored source text and input records. Calculated: the expected ledger from the stipulated contract. Executed against target: **none**. No test was run on the illustrated classifier, no actual source was deleted or replaced, and no runtime correctness or deployed repair is claimed.

Fixture consistency tests can recompute these stipulated judgments and catch ledger drift. They do not establish arbitrary report semantics, model task accuracy, historical incident truth or the behavior of an executable translation. Endpoint identity observations are snapshots, not continuous monitoring.

## 6. Proposed tests and controls — not executed target checks

For each case in section 4, propose a disposable test at a separately authorized executable classifier, retaining command, source/checker identity, exact input/output, status and the relevant reason. A missing-file rejection must name missing baseline; a checker-change rejection must name changed checker. A crash, unrelated setup error or another role's rejection does not qualify the intended test.

Two verifier-quality cases are mandatory: `wrong-reason` (checker-change rejected as missing baseline) and `control-failure` (healthy control rejected). Both invalidate verifier qualification. Account for every required case exactly once; omitted negative cases remain untested, not passed. Pair any negative execution with the unchanged healthy control and distinguish proposed, blocked, failed-setup and executed results.

## 7. Decision and prioritized handoff

1. **Decidable now:** the authored equality-only source does not support the named guarantee; F1 and F2 give concrete source-level counterexamples. The alternative appears to address those local conditions by inspection only. Do not endorse a real system from either snippet.
2. **Prerequisite:** identify the actual decision-maker's guarantee, target source, authoritative captured identities and bounded read/execute authority. If those are absent, deliver this gap rather than inventing a target or requesting broad access.
3. **Smallest additional evidence if needed:** under existing explicit scope, inspect the real classification boundary and reuse an adequate existing test; otherwise propose permission for an isolated healthy/negative pair. Do not require another approval when the user has already authorized that exact bounded execution. Stop when the decision is resolved or the budget expires.
4. **Separate transfer:** for an existing-destination refusal guarantee, trace the pre-write guard; expected refusal preserves original bytes, whereas truncate-before-refusal is a counterexample. The isolated test needs an owned pre-existing destination, its byte snapshot, an allowed invocation and after-state comparison. Symlink targets need separate coverage. Identity labels do not answer this different guarantee.

No target repair, hook, policy installation, dependency change, merge or publication is authorized by this report.
