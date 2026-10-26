# Exercise repository-readiness on a real repository

The [task](task.md) and rubric were frozen before the initial agent attempts. Input:
https://github.com/tugrulguner/skillpot at
`3d023734ca0a2a22a873ca59d601f7616fed7716`. This predates the new skill; the agent
must judge that actual snapshot rather than silently inspecting the implementation
branch. The task is an installation-and-use readiness decision, not video production.

## Reproduce an explicit-load attempt

1. Obtain that public input revision in a detached checkout separate from this source.
2. Use an agent with repository file/search/command access. Inspect any host-global
   guidance that may affect a comparison; do not assume a blank system prompt.
3. Ask it to read `skills/repository-readiness/SKILL.md` and the linked report template
   from this source, then carry out `examples/repository-readiness/task.md` against
   the detached input checkout. Give it a fresh external output directory.
4. Preserve its report, actual command evidence, source revision, before/after status,
   tool/model/harness details, skill and task hashes, and any failures or interventions.
5. Check the output against the frozen rubric and the pinned input source. Preserve
   missing evidence as missing; do not edit the attempt into an apparent success.

For the no-skill condition, provide the identical frozen task and target but no candidate
entry point or template. Keep permissions and budget equal. One attempt per condition
cannot establish a skill benefit; a good baseline is a legitimate negative finding.
The [proposal](../../docs/repository-readiness-proposal.md) lists further gates.

The [repaired-version result](../../evaluations/repository-readiness/repaired-smoke/README.md)
retains an actual agent's report and machine-captured checks. It passed the bounded
task review after the earlier failures; it does not establish a benefit over the baseline.

No automation framework or fixture app is needed. This example exercises an agent's
procedure and resulting report. It does not claim native installation, automatic
selection, repeated/held-out success or supported compatibility across hosts.
