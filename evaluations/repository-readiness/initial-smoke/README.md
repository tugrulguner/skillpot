# Initial explicit-load smoke — incomplete acceptance, no benefit established

Historical attempts remain below unchanged in disposition. The later
[repaired-version smoke](../repaired-smoke/README.md) used a revised procedure and
recorder; its acceptance does not retroactively pass these attempts.

## Identity and frozen inputs

- Input: public SkillPot revision `3d023734ca0a2a22a873ca59d601f7616fed7716`.
- Task: [frozen brief](frozen-task.md.txt), frozen before the attempts.
- Candidate: [exact entry point](skill-under-test.md.txt) and
  [report template](template-under-test.md.txt); hashes are in [hashes.json](hashes.json).
- Host: macOS 26.5.2 arm64; Python 3.11.6; Git 2.50.1 (Apple Git-155).
- Agent: Hermes delegated workers; tool notification identified both as `gpt-6-luna`.
  Provider version, sampling settings, token usage, service cost and full harness
  version were not retained. Unknown is not zero.
- Conditions: one explicit-load attempt and one no-candidate attempt, run concurrently
  against the same read-only detached target, with the same task, rubric, tools,
  five-minute attempt budget and sixty-second command timeouts. No paid/external
  service calls were part of the repository checks. Model inference cost is unknown.
- The baseline loaded host-local SkillPot development guidance. It was not a blank
  agent, and that guidance mentions repository readiness. Neither isolation nor a
  clean incumbent comparison is established. No held-out task was run.

## Observed outputs

- With skill: [unaltered report](with-skill/report.md.txt) and
  [worker-authored command record](with-skill/commands.txt).
- Without candidate: [unaltered report](without-skill/report.md.txt) and
  [worker-authored command record](without-skill/commands.txt).
- Both concluded that the pinned historical checkout cannot provide an installable
  SkillPot skill. That agrees with its source and the parent verification.
- The with-skill trace shows explicit reads of the entry point and template; the saved
  report identifies their matching hashes. This demonstrates an observed explicit
  instruction load and application, not native installation or automatic discovery.
- Worker reports and records are retained byte-for-byte; `.md.txt` prevents their
  target-relative citations from being mistaken for links in this evaluation directory.
  Read those citations against the input revision, not current SkillPot source.

## Acceptance review and negative findings

The reports answer the concrete question with source citations, distinguish structural
checks from task use, and propose next steps. However, neither attempt is accepted as
a clean pass of the full evidence rubric:

- The no-candidate command record mistypes the `git rev-parse` result as
  `3d023734ca0a0a2a22a873ca59d601f7616fed7716`. It is preserved as written; it is
  not a valid forty-character commit identifier and must not be normalized silently.
  The actual tool result and separate parent check identify the requested input.
- The with-skill record presents an initial multi-command batch as exit 0 even though
  its discovery portion exited 2 on absent paths. Its report acknowledges that error
  but the saved command record omits the failed search/output. Test-output ordering
  was also reconstructed rather than preserved exactly.
- These are authored summaries, **not raw stdout/stderr capture**. Their deficiencies
  fail the task's exact command-evidence requirement. Target-specific tests did run;
  this does not excuse inaccurate recording.
- Full pre-execution script inspection and exhaustive trace completeness are not
  independently established by the retained records. Do not turn missing evidence
  into a passing permission or safety qualification.

The parent's [separate check record](parent-checks.json) captures actual argv, cwd,
environment override, timeouts, exit codes, stdout and stderr directly from subprocesses.
It verifies the exact input, clean status, documentation checker, five tests and
whitespace check. It is not substituted for either worker's flawed attempt record.
Source conclusions were checked against the pinned README, contribution guide,
authoring contract and proposal; quality judgment here is model-assisted and unblinded.

## Assisted retry — also not accepted

A second with-skill attempt received an explicit parent correction to capture actual
subprocess output directly, inspect check scripts before execution and write only to
the assigned external output directory. This intervention is additional assistance,
not an unassisted repetition or a replacement for the first attempt.

Its [unaltered report](with-skill-retry/report.md.txt),
[machine command record](with-skill-retry/commands.json) and
[hashes](with-skill-retry/hashes.json) are retained. It reached the same correct source
decision and ran the documentation checker and five tests. However:

- It accidentally created `commands.json` in the read-only target. A captured status
  explicitly shows that untracked file. Removing it later restores final cleanliness
  but does not undo the permission-boundary violation.
- The report claims correction commands and initial/final status are retained, but
  the JSON has no cleanup or final-status invocation. A failed lookup of the candidate
  skill in the input repository is recorded but not described in its report; another
  failed log lookup described by the report is absent from the JSON. Do not treat this
  as complete execution evidence merely because individual captured results are real.
- The parent separately verified final target cleanliness and the absence of the
  transient log. That verification does not establish that the target was never written.

Total observed attempts: two with-skill (one explicitly assisted retry), one baseline.
None is accepted as a clean pass of the full frozen rubric. The skill and template
bytes did not change between attempts. This negative result limits the candidate's
current status; no further retries were silently substituted for these outcomes.

## Result and boundaries

Explicit-load execution was observed and both reports reached the correct decision;
full acceptance was not achieved. There is no demonstrated advantage over the baseline.
Do not publish a task-success rate, speed/cost improvement, compatibility badge or
qualified release claim from this smoke. Attempt durations in the worker notifications
are orchestration durations, not controlled task timings, and are not compared.

No installs or network actions were needed. The assisted retry violated the read-only
target boundary with a transient evidence file; that deviation is retained above.
The parent rechecked a clean target at the same revision after cleanup. The workers
finished; no attempt process remains running.
Public evidence contains only owned skill text, public-source conclusions and check
output. Private orchestration logs containing local paths remain outside this repository.

Decision: retain the skill as **experimental source**, keep these negative results,
and require faithful command capture, repeated trials, another real repository,
held-out/non-trigger tasks, an applicable incumbent and native host checks before
any usefulness or compatibility qualification. No merge or release is authorized.
