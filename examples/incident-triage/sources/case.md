# Case input

## Symptom
A historical public pull-request CI run concluded failure although selected source-job output said 147 tests ran and `OK`.

## Scope
Use only the selected source-job log excerpt and documented run-head source locators in this packet. Run ID 42306065730; source run head `b4d8f6020ca5b9646f68f5dfd915b61bb6e30db7`. Actual checkout identity UNKNOWN; may be a PR synthetic merge. The excerpt is partial, not full incident/workflow coverage.

## Context
The public run URL and exact source provenance are in `manifest.json`. The underlying full original log is retained outside the repository. Selected log output contains check PASS lines, test success output, six trailing-whitespace findings, and exit code 2. Production/customer status and impact are UNKNOWN. This input provides symptoms and scope only; it deliberately contains no expected answers.
