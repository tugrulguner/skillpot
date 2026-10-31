# Worked example: an evidence-bounded decision

This example accompanies the unreleased [decision-brief skill](../../skills/decision-brief/SKILL.md) in current source. It is **not included in published v0.3.0**.

Read [the task](task.md), inspect [the pinned source packet](sources.json), then compare the parent-authored [brief](brief.md) and [evidence ledger](evidence.md).
The [failure cases](cases.md) show expected responses to conflict, missing evidence, source instructions and an occupied output location. None is an observed agent trace.

To use the workflow, choose a reviewed source checkout containing this directory, copy the complete selected skill using the documented [host setup](../../docs/quickstart.md), and provide the task with a fresh owned output location. The stable v0.3.0 clone command does not supply this unreleased directory.
Keep all supplied documents within the offline scope. The skill depends on host file tools, not a specific agent or an executable research service.

The separate [observed task record](../../evaluations/decision-brief/offline-tasks-001/README.md) archives actual new outputs from three explicitly loaded attempts. It does not reclassify the authored reference files here as agent output.

## Offline example check

From the repository root, with Python 3.11+ (standard library only):

```sh
python3 examples/decision-brief/verify.py
```

This reads the committed artifacts and checks claim references, excerpt hashes, pinned source metadata and the four case labels without network, database creation or writes.
It does not generate a brief, invoke an agent, prove a quote supports a conclusion, authenticate remote source provenance from hashes alone, or establish better decisions.
The original upstream files were inspected at authoring time; full-file hashes in the packet identify those originals, while excerpt hashes cover only the bundled excerpts.

## Source and rights boundary

The primary material is selected documentation from Python v3.14.0, not generic search results. Original file hashes and immutable URLs are preserved in `sources.json`.
[NOTICE.md](NOTICE.md) identifies the selection and the unchanged full [CPython license](LICENSE-PYTHON.txt). No private documents, third-party skills or copied ADR templates are included.
No storage benchmark, migration, target runtime check or professional-advice certification has been performed.
