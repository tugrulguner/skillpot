# Published upstream-guide correction

## Current-source scope

This change refreshes only Dexpot's guide to **Dexpot v0.8.1** at
`a670e626cf73e1c4b21e0529294a87f1aa83e74f`. The SkillPot instruction version is
**0.3.0**, with a Dexpot 0.8.1+ prerequisite for the corrected path-annotation contract.
It is **not included in published SkillPot v0.4.1**: that immutable collection keeps
Dexpot instruction 0.2.0 at upstream v0.8.0 commit
`409df5b68a2386bd04e1f2cf0f057773142e0759`. Stable installation still selects the
verified collection commit `79284b3faa928dc556a9032aa9dbeb059b4ee915`.

The nine other bundles, full notices, source/task observations, original example code,
artwork and active user installations stay unchanged. This does not publish a new
collection or move an existing tag. A future collection must account for the raised
Dexpot prerequisite under the existing release policy; do not assume a patch release.

## Released contract correction

The released guide adds six lines to the held guide:

- Path annotations support only `str`, `int`, unannotated parameters and `Any`.
- Unsupported declarations, including `float`, `bool`, `Enum`, `Annotated`, unions
  and explicit `None`, raise `TypeError` during registration in 0.8.1+. They silently
  received strings in 0.8.0. Supported integer conversions retain their existing 422
  rejection behavior.
- Migrate unsupported path declarations to `str` plus explicit application validation
  or an appropriate typed JSON body. Body/response schema support does not grant
  path-conversion support.

The [released registration implementation](https://github.com/tugrulguner/dexpot/blob/a670e626cf73e1c4b21e0529294a87f1aa83e74f/src/dexpot/_plans.py)
contains this exact identity-based allowlist. Its
[path-annotation tests](https://github.com/tugrulguner/dexpot/blob/a670e626cf73e1c4b21e0529294a87f1aa83e74f/tests/test_path_annotations.py)
and installed-example acceptance test were inspected as source, not executed here.
Existing lifecycle guidance is already in both released snapshots and is retained.
Main-only typed query/header/cookie inputs are excluded; the reference comes from the
release, not the newer default branch.

The full upstream guide is copied byte-for-byte. Guide SHA-256:
`064792cb9897483af66fa1199cbcf4be97cc3e26417533dbb87a36e471a3fa0d`.
The same complete upstream MIT notice remains at both installed notice paths,
SHA-256 `44c84c4f83c7c902b4d7d96ae40b395b4a9c943c1a145e7db92928ba2f21c958`.

## Seven-package audit and retained scope

The [machine-readable inventory](published-upstream-refresh.json) records all seven
catalogue packages across four canonical repositories, each at its held pin, freshly
resolved latest stable release and one immutable default-branch observation. There
are 21 guide/full-notice pairs (42 checked record references), representing 34 unique
repository/path/revision identities. Five held guides differ from their published
release guides; the two Summonpot contributor guides do not. All full notices match.
A guide difference does not establish that its release revision is newer than the pin.

- **Dexpot:** select the released path-annotation correction above; hold main-only
  typed input sources. No lifecycle API addition is being attributed to this refresh.
- **Intpot CLI and Python:** retain both pins. Their existing source-scoped guides
  already cover the applicable released body-reference/binding guidance, while
  source-only package/enum/numeric-range extensions need their own broader review.
- **Summonpot consumer:** retain the existing pin and qualifications. Replacing its
  execution-optimization guidance is a broader contract review; newer choice,
  repetition and checkpoint features remain source-only where labeled.
- **Refpot:** retain its qualified fixed-schema preview rather than mechanically
  replacing it with a different release-era qualification. Newer SQL-preview work
  remains excluded. No durability or performance promotion is made.
- **Summonpot contributor pair:** exact guide parity at held/release/main; no churn.

Inventory snapshot paths refer to durable external audit evidence, not extra files
installed with a skill. Immutable guide/license URLs and hashes permit reproduction.
The catalogue-before-refresh record preserves the previous pin identities; earlier
release inventories and reports are unchanged historical evidence.

## Examples and verification boundary

The existing Dexpot example uses supported integer paths and its command remains at
its historical v0.7.1 source pin. Its code, verifier and recorded outcomes are not
reclassified as new 0.8.1 execution. The example README now makes that distinction
explicit. Source tests cover the new selected guide, entry-point contract, minimum
version, catalogue/reference hashes and release boundary.

No product runtime, native agent client, listener, authentication probe or model
trial was run for this refresh. Source/hash/notice and copy checks qualify instruction
distribution only. A merge needs separate approval; publication needs its own scope.
