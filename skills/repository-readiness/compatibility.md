# Compatibility and evidence boundaries

Status: experimental procedure, not a released or broadly qualified skill.

The entry point uses portable Agent Skills metadata and host-provided file/search/
command capabilities. Git and the target project's check tools must be available.
No installer, runtime, provider API, network service or media stack is bundled.

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
There is no clean accepted full-task attempt or demonstrated benefit yet.

Host discovery, selective installation/removal, non-trigger behavior, repeated matched
trials, held-out tasks, external users and other OS/model/harness combinations remain
unverified. Source/frontmatter tests validate packaging only, not agent performance.
