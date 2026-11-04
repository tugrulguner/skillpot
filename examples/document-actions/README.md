# Worked example: document actions (fictional)

This is a wholly authored fictional input packet and reference extraction. It demonstrates source-bounded extraction only; it is not an observed agent run or an evaluation of an agent. Nothing in the packet comes from primary-source excerpts.

Copy only the contents of [`inputs/`](inputs/) into a fresh project `document-actions-input/` directory. The input contains [`task.md`](inputs/task.md) and [`notes.md`](inputs/notes.md); expected output and verifier are intentionally outside that directory.

Compare the reference [`actions.md`](actions.md), [`questions.md`](questions.md), and structured classification/exclusion oracle [`expected.json`](expected.json). Locators use stable `[Nxx]` labels and actual line numbers.

## Offline check

From the repository root, using Python 3.11+ and its standard library only:

```sh
python3 examples/document-actions/verify.py
```

The verifier checks the authored oracle against fixed expected classifications and fields, source locator resolution, output distinctions/conflict preservation, and required task/output separation. The unit tests include temporary-copy mutants promoting the proposal, inserting a historical item into outstanding actions, and silently resolving a conflict.

It does not invoke an agent, assess a real extraction, verify semantic entailment of arbitrary task statements, evaluate completeness, access accounts, or use the network. Hashes alone would not prove semantic correctness; this verifier adds authored-fixture expectations but still does not establish semantic quality of new agent outputs. The example is included in published v0.4.0. Use the [document-actions first-use guide](https://skillpot.modepot.io/host-setup/#try-document-actions-from-pinned-source) for selected-bundle setup and a bounded task prompt. The source checker is an authored-fixture check, not a claim of extraction accuracy.
