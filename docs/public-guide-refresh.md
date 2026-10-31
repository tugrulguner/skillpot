# Public project-guide refresh

This audit compares the seven packaged public project guides with immutable snapshots
of their four canonical repositories. It is source maintenance, not a runtime trial,
a new collection release or a promise to follow moving `main` automatically.

## Scope and retained pins

- **Intpot CLI and Python:** refresh to
  [`470584e21ee518e983087175f217c65664bd0ec5`](https://github.com/tugrulguner/intpot/commit/470584e21ee518e983087175f217c65664bd0ec5).
  The guides add bounded binding-chain explanations, exact body-reference locations
  and source digests, plus explicitly unreleased numeric-range conversion guidance.
- **Summonpot consumer:** refresh to
  [`739d980dca48657a839e8f6a19649bfb6f54da80`](https://github.com/tugrulguner/summonpot/commit/739d980dca48657a839e8f6a19649bfb6f54da80).
  The guide adds application-authenticated context and version-specific producer-choice
  execution boundaries, including an explicitly unreleased multiple-choice extension.
  It does not provide built-in login or grant operation authority.
- **Dexpot consumer:** refresh to
  [`409df5b68a2386bd04e1f2cf0f057773142e0759`](https://github.com/tugrulguner/dexpot/commit/409df5b68a2386bd04e1f2cf0f057773142e0759).
  The added lifecycle guidance describes synchronous process-scoped resources,
  bounded shutdown and deferred-cleanup/thread-affinity limits.
- **Summonpot's two contributor guides and Refpot:** their guide bytes match the
  audited default-branch snapshots, so keep their existing reviewed pins, package
  versions and notices. Refpot remains a preview; repository-readiness remains
  experimental and is outside this upstream-guide audit.

All four repository trees were complete (`truncated: false`). All seven upstream
license comparisons were unchanged. Preserve complete notices and exact upstream
reference bytes; clarify stale historical availability wording in the adapted entry
points and compatibility records, not by editing archived upstream text.

The earlier seven-repository [discovery inventory](../catalog/source-inventory.json)
is historical and unchanged. This audit does not newly inventory unrepresented
projects or import private/local workflows.

## Upstream releases versus source

The observed latest public releases are Intpot
[v0.16.0](https://github.com/tugrulguner/intpot/releases/tag/v0.16.0), Summonpot
[v0.14.0](https://github.com/tugrulguner/summonpot/releases/tag/v0.14.0), Dexpot
[v0.8.0](https://github.com/tugrulguner/dexpot/releases/tag/v0.8.0), and Refpot
[v0.1.1](https://github.com/tugrulguner/refpot/releases/tag/v0.1.1).

Dexpot's audited commit is the v0.8.0 release commit. Intpot and Summonpot's audited
main guides differ from their latest published tag guides. In particular, do not
attribute Intpot's unreleased numeric-range guarantees to v0.16.0 or Summonpot's
unreleased multiple-choice optimization to v0.14.0. Match the exact feature and
installed version; copying a guide neither installs a product nor proves behavior.
Refpot's unchanged retained guide also differs from its published tag guide, so its
existing source-preview qualification stays in place.

## SkillPot release boundary

These four refreshed packages are included in published
[SkillPot v0.3.0](https://github.com/tugrulguner/skillpot/releases/tag/v0.3.0),
at commit `b4dabf93e7e4a85a55d947a05eb2989f035a58c1`. The stable
[quickstart](quickstart.md) selects that revision. The v0.2.0 collection keeps its
older reviewed snapshots. Existing user installations are not overwritten or
silently upgraded, and upstream source-only features remain source-only.

The [catalogue](../catalog/modepot-sources.json), affected package metadata,
provenance and compatibility records change together. Historical example and
runtime records retain their original pins and results. This audit executes no
upstream application, product dependency installer, host client, authentication probe or
model call. Offline source/hash/notice checks qualify the distribution surface only.
