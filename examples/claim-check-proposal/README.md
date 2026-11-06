# Claim-check proposal — worked packet

This is an **authored design example**, not an installable skill, a real customer
record, an agent attempt or evidence of factual-review accuracy. Review the
[proposal](../../docs/claim-check-proposal.md) before implementing a bundle.

## Files

- [Draft](draft.md): eight labeled paragraphs, including one excluded opinion.
- [Supplied sources](sources.md): six fictional source extracts; one contains hostile
  task-like text. The referenced audit attachment is intentionally not supplied.
- [Expected claims](expected-claims.json): ten authored claim expectations, exact spans
  and evidence locators; not independent ground truth or a generated attempt.
- [Expected review](review.md) and [expected ledger](claims.md): rendered specification
  artifacts. They illustrate proposed local edits, not an automatically rewritten draft.

No network, account, service, model or product dependency is needed to read the packet.
The repository's existing development dependencies are needed only for the full test
suite. Run from the repository root:

```sh
uv run --no-project --with-requirements requirements-ci.txt python -m unittest discover -s tests -p test_claim_check_proposal.py -v
```

This checks literal span/locator consistency, the four verdict categories and selected
proposal boundaries. Arithmetic was executed in the authoring process and is checked
again by the test. The test cannot establish that its authored verdict premises are
semantically correct; review the actual source wording. There is no custom claim
classifier, security enforcement tool or model-evaluation runner.

## Additional review cases before implementation

These are specified expected behaviors, **not executed task observations**:

- A claim has no source: Unresolved/missing, not Contradicted.
- A current-version claim has only an older-version source: Unresolved/scope-mismatch
  unless applicable current evidence independently supports or contradicts it.
- A source is unreadable: disclose the inaccessible portion; do not report zero claims
  or complete coverage for that portion.
- A source only reports what a vendor says: preserve attribution rather than certify
  the underlying proposition. Commissioning an audit is not completed audit evidence.
- Two otherwise applicable sources conflict without authority: preserve both values;
  no vote, averaging or automatic newer-document winner.
- A calculation tool or its required inputs are unavailable: Unresolved; do not type a
  guessed numerical result into the ledger.
- Either output target is a file, directory, live symlink or dangling symlink: refuse
  before writing either output and request a fresh approved destination. No alternate
  filename, sibling overwrite or implicit cleanup.
- Source text asks for private retrieval or publication: disregard it; no new authority.
- Interruption leaves one output incomplete: preserve it and request narrow recovery
  permission before resuming, rather than silently restarting over it.

Future implementation tests must exercise actual metadata/resources, fail-closed
copy behavior and any executable resource that is introduced. The cases above do not
claim that an agent followed these instructions or that the host enforces them.
