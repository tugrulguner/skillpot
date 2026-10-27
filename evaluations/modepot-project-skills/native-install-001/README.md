# Native selective-install verification

## Scope and identity

Source SkillPot revision: `5b4f695dea0481877ab792e149ae4e8dafc14830`.
Host: macOS arm64. Native CLI reports Hermes Agent v0.22.5, stable build
`bf0203a794a0`, Python 3.14.9. See the last command in [commands.json](commands.json).
No existing registered profile or active user skill directory was selected: an owned
empty temporary `HERMES_HOME` was used, with bundled seeding opted out via the normal
CLI. This is installation/list/removal evidence, not model-driven skill activation.

## Actual results

The native CLI installed each selected immutable raw SKILL.md URL separately, without
`--force`. All seven completed ordinary security scanning with verdict SAFE/ALLOWED.
Those results include medium informational findings (network commands, dependency
installation, subprocess/uv commands) and one low finding; SAFE is not a security
certification and the warnings were not removed or hidden.

The [installation results](installation-results.json) retain SHA-256 for each installed
`SKILL.md`, `references/upstream.md`, and `references/LICENSE.md`. Every installed file
was compared byte-for-byte with the pinned source checkout. After each install, the
active skill names matched exactly the individually selected set: no sibling bundle,
original repository-readiness skill, product package or built-in catalogue was installed
as a dependency. The final native list showed seven enabled hub skills.

All seven were then uninstalled individually with the existing CLI. After every
removal, the other selected skills remained. The final native list was empty.
[Removal results](removal-results.json) retain those exact remaining-name sets.
Native hub scan/audit/cache metadata can remain in the temporary home; empty active
skill state does not mean every host metadata file was deleted. Test processes ended.

## Recorded commands and provenance

[commands.json](commands.json) is captured directly from subprocess argv, exit code,
stdout and stderr. The first skill also used native `inspect`; the other installs
performed their normal install-time scan. Public copies replace only machine-local
absolute locations with labeled placeholders. Exact private-original hashes and the
redaction description are in [provenance.json](provenance.json); originals are retained
outside this repository. No source URL, finding, result or command argument was edited
to manufacture a pass.

Before native installation, a parent Python 3.11 urllib HTTPS byte-fetch probe failed
because its local certificate store could not verify the issuer. Source byte identity
was instead checked through authenticated `gh api` at the exact revision. Native
Hermes' own HTTPS path then succeeded. Certificate verification was not disabled.
This setup failure is distinct from the successful native CLI results.

## Boundaries

This establishes the seven instruction packages' selective native URL installation,
resource/license completeness, host listing and selective removal on this host. It
does not establish automatic model selection, slash-command activation, another host,
all project runtimes, performance, production suitability, safety or usefulness gains.
Each product's installation, credentials, server/data effects and tests remain separate.
The Refpot consumer example is a distinct task check, not implied by these installs.

Upstream ownership and immutable source/license pins remain in the
[collection catalogue](../../../catalog/README.md). No public release, merge, update
of installed user edits, video work or promotion occurred as part of this verification.
