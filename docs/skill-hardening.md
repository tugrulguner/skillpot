# Current-source skill hardening

This pass reviews all fourteen existing skills and hardens their construction,
standalone resources and worked examples. It adds no new skill or collection release.
Published v0.4.1 remains its immutable ten-skill snapshot; these changes are current
source, not an update applied to existing installations.

## Install one reviewed current-source bundle

With Node.js 22.20+ and Git, run in the project where you use your agent:

```sh
npx skills@1.7.6 add https://github.com/tugrulguner/skillpot/tree/66bad57a0a42a4aec2c5d54feee1df8fb242e166 --skill claim-check
```

Replace only the skill name to select another bundle listed below. Keep the full
GitHub tree URL and literal revision. Select your agent in the installer, or append
`--agent claude-code`, `--agent cursor`, `--agent codex` or `--agent hermes-agent`.
The complete selected directory is installed project-locally; selecting several skills
or global scope must be deliberate. Inspect existing destinations and preserve user
edits before approving an update: the installer can replace selected content.

Use the selected skill's first-use guide and bundled inputs, with its exact task
permissions. Installation is not permission to execute targets or examples, retrieve
other records, change a product, spend money or publish. Report-directory collision
refusal is a task rule, not a guarantee about installer update behavior.

The [public distribution record](skill-hardening-distribution.json) binds all 89
current bundle files across fourteen individually tested skills to this source pin.
Its scope is actual public add/list/remove, selected-only placement,
canonical files, agent links, source lock, unrelated project/global sibling
preservation and standalone inline resource destinations. The exercised installer
runtime is Node 22.23.4 with Skills CLI 1.7.6. These checks do not establish native
client activation, automatic skill selection or model/task accuracy.

## Collection coverage

The review covered entry points, linked resources, provenance, compatibility,
representative examples and their declared test/oracle boundaries for each skill:

- `intpot-cli`: consumer instructions and pinned product guide.
- `intpot-python`: Python consumer instructions and pinned product guide.
- `summonpot`: bounded agent-owned API decisions and pinned product guide.
- `dexpot`: synchronous typed API instructions and the retained v0.8.1 source pin.
- `refpot-database`: preview database instructions and explicit qualification limits.
- `summonpot-pr-review`: project-specific contributor review, not merge authority.
- `summonpot-code-review`: project-specific code review, not a general project policy.
- `repository-readiness`: bounded read-only readiness report and command recorder.
- `document-actions`: stated actions, proposals, historical status and unresolved fields.
- `decision-brief`: decision roles, constraints, source evidence and conditional conclusions.
- `claim-check`: claim coverage, attribution, verdicts and precise practice outputs.
- `change-impact`: static evidenced impacts, unknown reachability and proposed verification.
- `bug-repro`: symptom matching, reduction controls, final artifacts and execution permission.
- `incident-triage`: event/source identity, clock uncertainty, impact and investigation handoff.

A review with no demonstrated defect is not a reason to rewrite a working procedure.
The upstream guides and complete notices remain byte-identical to their selected
catalogue pins; twelve distinct public guide/notice objects were fetched at those
immutable revisions and compared with the recorded hashes. This verifies the
retained objects, not that those revisions are today's latest upstream releases.

## Demonstrated repairs

### Validate every existing bundle

The source-integrity command previously inspected only the seven imported catalogue
entries. It now also checks original workflow packages, including complete metadata
and a nonblank instruction body. The common gate rejects duplicate YAML keys,
non-mapping or malformed frontmatter, unsupported host-specific root fields, invalid
optional-field types, invalid names and missing required resources with diagnostics.
A missing catalogue-listed directory cannot silently pass.

All source bundles must contain regular portable resources rather than symlinks.
The bundle gate rejects symlinks before reading linked content. It checks inline
local Markdown destinations within each standalone bundle, not merely within the
larger repository. This does not make the checker a filesystem sandbox or a complete
Markdown/secret scanner: it does not certify reference-style/HTML links, heading
anchors, arbitrary external destinations or resistance to concurrent file changes.

### Keep maintenance references usable after installation

Twenty-eight local links in fourteen supporting files across ten bundles pointed
outside the selected package. Those links worked in the source checkout but broke
when the skill was installed alone. They now point to the corresponding immutable
public maintenance records. Local operational assets remain bundled. Archived setup
commands are historical evidence, not instructions to downgrade a newer installation.

### Make claim-check's practice handoff explicit

Instruction version 0.1.1 states the two fresh practice outputs, `review.md` and
`claims.md`, keeps the packet read-only, and explicitly excludes copying expected
outputs/oracles. The original 0.1.0 installer record is retained unchanged as
[historical evidence](claim-check-distribution.json); the current fourteen-bundle
matrix separately binds the changed bytes. No factual-review efficacy is inferred.

### Align the incident timeline with its template

The current worked timeline now follows the installed seven-column template. It
preserves source timestamps and locators, identifies log-event kinds, separates
precision from unknown clock accuracy, and makes ordering limits explicit. A logged
command echo is not promoted into the command's actual execution time.

This is revised authored analysis of unchanged historical inputs. The original
[three-column authored output](https://github.com/tugrulguner/skillpot/blob/203e942848b33ca5b1250b99d17536a19c145a5c/examples/incident-triage/timeline.md)
remains available at its immutable revision. No historical CI or target was rerun.
The [fixture checks](../tests/test_incident_triage_example.py) exercise template
agreement, source bindings and named mutations, not arbitrary incident reasoning.

## Verification and limits

Run the canonical checks in [CONTRIBUTING](../CONTRIBUTING.md), including all Python
tests, documentation/source validation, repository-tooling lint/types, and the
supported-Node website build/browser gates. The regression suites include positive
controls as well as observed pre-fix failures. The distribution matrix is an executed
artifact boundary, distinct from tests that only inspect command text.

Current-source tests, authored fixtures, installer placement and a source audit do
not establish universal safety, factual correctness or better agent performance.
The host still supplies tools and enforces permissions. Experimental/preview scopes
remain in place. Comparative task-quality evaluation, native client trials, releases,
merges and updates to user installations remain separately scoped actions.
