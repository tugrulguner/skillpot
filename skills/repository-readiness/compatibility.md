# Compatibility and evidence boundaries

Status: experimental procedure, not a released or broadly qualified skill.

The entry point uses portable Agent Skills metadata and host-provided file/search/
command capabilities. Git and the target project's check tools must be available.
The bundled command recorder requires Python 3.10+ and uses only its standard library.
It guards its own output path and records actual subprocess results, but does not
sandbox commands or manage background servers/descendant process trees. No installer,
agent runtime, provider API, network service or media stack is bundled.

An initial explicit-load attempt and a no-candidate attempt ran against the frozen
public task in [the example](../../examples/repository-readiness/task.md). Both reached
the correct decision, but saved command records failed the full evidence rubric.
The [record](../../evaluations/repository-readiness/initial-smoke/README.md) preserves
those failures and a separate parent verification, without claiming improvement.
A worker reading and applying the entry point is explicit loading, not automatic
catalogue selection, native host installation or trigger behavior. An assisted retry
also failed full acceptance: it transiently wrote a command log into the read-only
target and its saved evidence omitted the cleanup/final status commands. Final target
cleanliness was separately verified; it does not erase the boundary violation.
Those attempts used the original procedure without the new recorder. A revised
procedure now requires absolute external destinations and the bundled recorder;
regressions exercise actual refusal, overwrite, symlink, failure and timeout behavior.
The [repaired-version smoke](../../evaluations/repository-readiness/repaired-smoke/README.md)
was accepted for its frozen bounded audit task: the agent explicitly read the skill,
ran the checks through the recorder, and delivered the cited report. All six project
command records were retained; target hashes and modification times were unchanged,
with no target write observed in the trace. This is one model-assisted, unblinded
acceptance decision, not native installation/discovery or a demonstrated usefulness benefit.

Host discovery, selective installation/removal, non-trigger behavior, repeated matched
trials, held-out tasks, external users and other OS/model/harness combinations remain
unverified. Source/frontmatter tests validate packaging only, not agent performance.
