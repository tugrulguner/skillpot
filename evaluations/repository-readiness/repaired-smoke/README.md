# Repaired procedure: accepted bounded execution smoke

## Identity and task

Input: public SkillPot revision `3d023734ca0a2a22a873ca59d601f7616fed7716`, using the
unchanged [frozen task](../../../examples/repository-readiness/task.md). The user asked
whether that historical checkout lets a new user install and use one SkillPot skill.
The correct audit answer is **not ready**; this is different from whether the new
audit skill successfully produced its requested readiness report.

Candidate revision: `06b4392685ebfb9030acadc550ece30060b1da61`. Retained exact bytes:
[entry point](skill-under-test.md.txt), [template](template-under-test.md.txt), and
[command recorder](recorder-under-test.py.txt). See [hashes](hashes.json).
The candidate adds a small standard-library resource, not a new runtime or evaluation
framework. It refuses relative/in-target/existing evidence paths and records real
subprocess results. It is explicitly not a sandbox or process-tree supervisor.

This is a fresh repaired-version attempt after the failed original and assisted retry.
It is not an unassisted original-condition repetition, held-out task or efficacy trial.
The same small in-project input and host guidance remain important limitations.

## Observed execution and review

The worker notification identified `gpt-6-luna` on Hermes delegated execution. The
host is macOS 26.5.2 arm64. Full harness/provider versions, inference parameters,
token use and model cost were not retained and remain unknown. No paid repository
service, installation or network operation was needed.

The trace shows explicit file reads of the skill, template and helper, then target
check scripts/tests before execution. An initial native catalogue lookup failed;
the worker then read the supplied skill path. This establishes explicit loading only,
not successful native catalogue discovery or installation. Two read-only directory
inspection commands preceded the project checks; they were source discovery, not
claimed project-verification results.

The agent produced the [readiness report](report.md) and these six unedited machine
records, each with argv, cwd, timeout, environment override, exit code and stdout/stderr:

- [Source revision](01-revision.json): exact requested commit.
- [Initial worktree status](02-initial-status.json): clean.
- [Documentation checker](03-doc-check.json): exit 0.
- [Target unit tests](04-unittest.json): five passed, exit 0.
- [Whitespace check](05-diff-check.json): exit 0.
- [Final worktree status](99-final-status.json): clean.

All project checks passed. This does not mean the audited historical repository is
ready for installation; its structural checks do not supply an implemented skill.
The report's references to unexecuted installation/task behavior concern that target,
not the readiness-audit task which the worker actually carried out.

The parent read the report, all records and the agent trace, checked material source
citations against the frozen checkout, and compared its before/after snapshots.
The [separate parent verification](parent-verification.json) shows the same file set,
content hashes and modification times for all twenty target files, plus clean final
Git status. No target write was observed in the trace. This supports the observed
attempt; neither clean Git status nor timestamps alone prove a sandbox guarantee.
No process was left running. No later cleanup was needed to restore target cleanliness.

The report's private original is retained outside the repository. For the public copy,
only three machine-local absolute locations were replaced with labeled placeholders.
The original hash and exact redaction description are in parent-verification.json.
No finding, check result or JSON command record was rewritten to appear successful.

## Frozen rubric disposition

Parent review, model-assisted and unblinded:

1. **Pass:** exact input pinned; direct answer to the install-and-use question.
2. **Pass:** material conclusions have target-relative source citations, checked against
   the specified source, not the newer implementation branch.
3. **Pass:** implemented behavior, roadmap prose and structural checks are distinguished.
4. **Pass:** documented offline checks actually ran; all six project command records
   are retained directly rather than reconstructed.
5. **Pass:** blocking consumer gaps and minimal next actions are stated separately
   from optional future work.
6. **Pass for the observed trace:** no target write or unauthorized action observed;
   no host compatibility, comparative improvement or release claim is made.

The separate independent repair review found no concrete blocker at candidate revision
06b4392 and executed all nineteen source/helper tests. That is code review evidence,
not independent confirmation of efficacy or human acceptance of the report.

## Result and remaining limits

Accepted as one bounded explicit-load execution of the repaired skill. The original
[failed attempts](../initial-smoke/README.md) remain unchanged and are not retroactively
passed. This result clears the demonstrated command-evidence/output-location defects
for the exercised path. Eleven helper subprocess regressions cover actual refusal,
overwrite/symlink controls, success, failure, missing executable and timeout behavior.

No usefulness advantage over the baseline, broad safety/compatibility, native
installation/discovery, other repository, held-out/non-trigger task or qualified
release is established. Repeated paired trials and applicable incumbent comparison
remain open. Experimental source may be reviewed separately from those release gates.
