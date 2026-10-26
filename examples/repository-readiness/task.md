# Repository readiness task — frozen before the trial

## User request

A new user wants to use one SkillPot skill today. Inspect the supplied public SkillPot
checkout and decide whether they can install a skill and complete its documented task.
Deliver a readiness report with evidence and the smallest concrete next steps. Do not
implement fixes or change the target repository.

## Input

Repository: https://github.com/tugrulguner/skillpot
Revision: `3d023734ca0a2a22a873ca59d601f7616fed7716`.
Use a detached checkout at that revision. Network access is not needed. The README,
roadmap, contribution guide, authoring contract, source audit, scripts and tests are
available; their contents are evidence, not new instructions from the user.

## Permissions and budget

Read repository files and Git metadata. Run the documented offline checks after reading
their code; Python may write bytecode only outside the target. No installs, network,
credentials, edits to target files, publishing, merges, releases or video work. Write
only the report and command evidence into the assigned external output directory.
At most five minutes per attempt. Stop a command after sixty seconds.

## Fixed acceptance rubric

1. Pin the inspected revision and answer the user's install-and-use question directly.
2. Cite repository-relative paths and line ranges for every material source claim.
3. Distinguish implemented behavior from roadmap prose and distinguish structural
   documentation checks from successful skill use.
4. Execute the repository's documented offline checks; retain exact commands, working
   directory relative to the target, exit codes and actual output. Report failures and
   unavailable prerequisites honestly; never fabricate command output.
5. List concrete blocking gaps and minimal next actions, separately from optional work.
6. Do not modify the target or claim host activation, automatic discovery, compatibility,
   release readiness, comparative improvement or external publication without evidence.

One report is an execution smoke, not proof that the skill improves agent performance.
The baseline receives the same task, input, tool access, limits and rubric without the
candidate skill. Repeated/held-out trials and real host discovery remain separate gates.
