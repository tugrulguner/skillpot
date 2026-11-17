# Change verification checklist

- [ ] Confirm the requested change, acceptance criteria and explicit permissions.
- [ ] Agree fresh external output directory; refuse existing paths/live or dangling symlinks and preserve partial work.
- [ ] Record base, exact candidate HEAD, actual source/input/check hashes, dirty state, diff and changed paths.
- [ ] Map each user-visible criterion to a check and independent expected result.
- [ ] Identify criteria/checks that the candidate can modify; disclose that risk.
- [ ] Select checks matching the claim: E2E user flow, property/invariant, differential baseline, focused unit/integration.
- [ ] Define comparison normalization and approved differences before differential runs.
- [ ] Run authorized cheap deterministic checks first; record exact command, cwd, exit and receipts.
- [ ] Exercise actual user flow when authorized/available; don't substitute unit pass for it.
- [ ] Preserve failures; classify setup, flaky, blocked, not-run and stale separately.
- [ ] After any code edit, rerun affected checks against the new exact head.
- [ ] Repair only with explicit authorization; never weaken/bypass checks; stop after at most three rounds.
- [ ] Complete `verification.md`; state remaining uncertainty and human decision needed.
