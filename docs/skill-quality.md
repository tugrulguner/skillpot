# Existing-skill quality and task observations

SkillPot separates construction, distribution and task quality. A source check,
installer exit status, complete report pair, or favorable grader response does not
establish the others. This work improves the existing fourteen-skill collection;
it adds no skills, agent runtime, installer, required model service or release.

## What changed

- Common source checks reject blank descriptions, compatibility text beyond the
  specification's 500-character limit, malformed catalogue shapes, duplicate
  catalogue identities, invalid JSON and unreadable UTF-8 with bounded diagnostics.
- Authored Markdown source symlinks and the catalogue file symlink are rejected
  before reading linked content. This is a bounded source check, not a filesystem
  sandbox or race-free containment guarantee.
- New offline mutation checks protect authored task inputs, citation identity,
  complete attempt pairs, exact original report bytes, grading coverage and literal
  grading evidence. They do not evaluate semantic truth.

The existing [construction/distribution record](skill-hardening.md) remains separate.
All installable bundle bytes are unchanged by these validation and evaluation
records. Stable v0.4.1 and its ten-skill inventory remain unchanged; current source
contains fourteen skills. No collection release is required for this work.

## Actual task study

The [frozen corpus](../evaluations/skill-quality/cases.json) contains three newly
**authored fictional** offline packets: document-actions, decision-brief and
claim-check. Their eighteen source-linked criteria were frozen before execution.
Two fresh delegated attempts per task produced twelve real reports, retained
[byte-for-byte in a fingerprinted archive](../evaluations/skill-quality/initial-artifacts.json).
Readable Markdown previews disclose whitespace-only adaptations for the unchanged
committed-whitespace gate; raw and preview hashes are separate. The ZIP also retains
the separately labeled assisted reports exactly. No task was rerun or relabeled
because of preview formatting.
Inputs, complete selected bundles and their hashes were frozen at source commit
`abfa31581e7d7c40083cfade9020aa710a52dab7`; controller checks compared each selected
bundle file with that Git snapshot before task execution.

These are explicit-loading observations in an existing configured agent host, not
native-client activation, automatic selection, a clean no-skill comparison, or a
cross-harness study. Supplementary host guidance remained active in every attempt.
Runtime-reported model labels, duration and API-call counters are observations,
not immutable model fingerprints or billing measurements. Token counters were
unavailable and remain null. Retained private runtime logs contain truncated
previews; they are not complete raw journals or proof of full source consumption.
The eleven visible tool-error events include recovered environment/tool mistakes;
they are retained rather than erased by a successful final summary.

## Results must survive review of the grader

Separate agent contexts graded all six attempts. All thirty-six **frozen criterion
judgments** were pass. That is not a six-task correctness certification:

- In document-actions attempt 2, the assigned access-matrix record A3 appears under
  `Unresolved items`, after a statement that none exist. Its deadline is conflicting,
  not its assignment category. The original rubric did not catch this containing-
  section defect. The original reports and scores are preserved.
- The document grader's additional finding conflated A2 and A3; it must be read with
  the source-exact reconciliation, not accepted on the grader's authority.
- Two decision-grader evidence quotations were not literal artifact spans. The
  [citation addendum](../evaluations/skill-quality/grading/decision-brief-citation-addendum.json)
  supplies exact spans and an artifact hash without rewriting the original grade,
  changing its verdicts, or altering the reports.
- Commissioning-date coverage warrants a separate event/date check: a letter's
  signature date and a planned start are not necessarily the commissioning date.
  This is a controller review concern, not a retroactive frozen-score change.

An assisted artifact correction is a new, labeled derivative, never a successful
replacement initial attempt. A placement-only correction proves that relocation,
not the absence of other semantic defects. Additional checks devised after seeing
outputs must be labeled exploratory or prospective; do not quietly add them to the
original rubric or claim they were held out.

## Prospective placement coverage

The original rubric and all six historical attempts remain unchanged. A separate
[prospective cohort](../evaluations/skill-quality/prospective-placement/README.md)
adds two fresh fictional document packets, five expected records and eight critical
criteria per packet, frozen before four new attempts. Writers received the complete
unchanged selected skill and inputs, not expected records or rubrics.

Independent graders recorded **29 pass and 3 fail judgments across 32 criteria**.
Harbor-archive attempt 2 omitted the unaccepted sleeve-chart proposal and placed its
status-conflicted inspection physically under Outstanding, despite calling it
unresolved. Its later cross-reference did not move the canonical record. The new
predeclared placement criterion failed this report; the other three placement
judgments passed. This is coverage of a fresh failure, not evidence that skill
performance improved or that the other tasks were wholly correct.

Source classification, source-to-record identification and structural containment
are checked separately. A grader supplies stable source keys mapped to literal
arbitrary output headings; the bounded test helper checks actual containing H2s,
complete inventories and duplicates without trusting Category labels. Grader maps
are not automatically authoritative: the raw harbor grade incorrectly marks its
present A1 requirement missing, despite passing that requirement's criterion. That
mapping error is retained with a separately hash-bound independent reconciliation
and corrected mapping; raw grades and scores are unchanged.

Replayed controls retain three untouched placement baselines and reject 45
whole-record wrong-section relocations, 15 omissions, 15 duplications and 24 missing
or duplicate category sections. Those are authored mutations of retained reports,
not additional agent attempts. A separate assisted copy restores the omitted
proposal and relocates the inspection while preserving its ID and questions; it
is not included among unassisted successes.

All eight new raw reports are preserved byte-for-byte. The new cohort retains mixed
host guidance, one visible tool-error event, unknown token counts and truncated
runtime-preview limits. Its explicit template-heading and working-directory
instructions differ from the initial cohort; there is no matched causal comparison.
The initial mechanical checker was implemented during task execution, not frozen
with the criteria; missing-record diagnostics and ATX syntax guards were repaired
after grading. A parent
citation review also found a blank-line reference in harbor attempt 1; passing
frozen judgments are not complete source-locator certification.

## Practical quality rules

1. Start with an authorized task, exact outputs, permission boundaries and useful
   recovery. Keep instructions concise; add resources for real work, not a persona.
2. Inventory every distributable bundle independently of imported catalogue entries.
   Preserve immutable upstream sources and historical records; do not refresh sound
   instructions merely to increase the diff or test count.
3. Author realistic inputs and source-grounded expectations. Review source meaning
   before freezing: requester is not assignee, proposal is not commitment, a planned
   event is not an observed event, and a date belongs to a particular proposition.
4. Keep expected answers/rubrics outside installed bundles and task input exports.
   Record complete source/input identities, actual requests and contextual limitations.
5. Retain every attempt, failure and intervention. Verify claimed files, exact names,
   fingerprints, citation spans and physical containing sections. Do not use keyword
   presence or a record's category label as a substitute for its actual placement.
6. Review grader judgments against source meaning and actual artifacts. A literal
   quotation check catches fabricated evidence, not mistaken interpretation. Preserve
   incorrect original grades and publish explicit corrections/addenda.
7. Leave unavailable metrics unknown. Distinguish artifact integrity, observed task
   behavior, comparative benefit and automatic selection. Improvement claims require
   a separately scoped matched comparison and appropriate repeated/held-out tasks.
8. Keep CI offline: validate source, fixtures and retained evidence; do not invoke
   models, native clients, credentials or paid services as a support-format gate.

## Reproduce offline checks

From the repository root:

```sh
uv run --no-project --with-requirements requirements-ci.txt python scripts/check_docs.py
uv run --no-project --with-requirements requirements-ci.txt python scripts/check_project_skills.py
uv run --no-project --with-requirements requirements-ci.txt python -m unittest discover -s tests -v
```

These commands validate recorded artifacts and checker controls. They do not rerun
agents or establish that independent grader judgments are correct. A new task study
needs explicit execution scope, owned workspaces, frozen inputs/rubrics, actual
outputs, honest host-guidance accounting and separate grading/reconciliation.

The methodology draws on official Agent Skills guidance for
[evaluating skills](https://agentskills.io/skill-creation/evaluating-skills),
[best practices](https://agentskills.io/skill-creation/best-practices),
[description optimization](https://agentskills.io/skill-creation/optimizing-descriptions)
and the [portable specification](https://agentskills.io/specification).
These references guide the process; they do not certify this collection.
