# Provenance and maintenance

Original SkillPot procedure and report template, authored for this repository by
Tugrul Guner with Hermes Agent. MIT; see the repository's [license](https://github.com/tugrulguner/skillpot/blob/203e942848b33ca5b1250b99d17536a19c145a5c/LICENSE).
No private skill, kit, third-party instruction pack or product API guide was copied.

The portable entry point follows the public
[Agent Skills specification](https://agentskills.io/specification). Git commands and
repository-specific test tools remain external tools under their own licenses; this
skill bundles no binaries or target repositories. Its standard-library Python helper
records authorized foreground command results; it is not a sandbox. Repository contents used as trial
inputs retain their original license and are identified by immutable public revision.

Canonical source: `skills/repository-readiness/` in
https://github.com/tugrulguner/skillpot. Maintainer: `tugrulguner`.
Keep project-specific setup commands in the target's canonical documentation; inspect
them at the audited revision rather than copying changing API guidance into this skill.
