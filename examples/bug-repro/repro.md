# Reproduction report: fictional zero-limit bug

Status: **Reproduced**, for the supplied authored target and recorded inputs only.
This report summarizes parent-executed scripts, not an autonomous agent evaluation.
Target identity: buggy.py SHA-256 is bound by receipts/manifest.json; the reproducer
records its observed imported-module location, interpreter/version and input hash.
Runtime and operating-system observations are in receipts/cases/environment.json.
No third-party dependency was installed. Case execution used isolated-mode Python,
bytecode disabled, an owned external cwd and a ten-second timeout per command. Those
settings are not a sandbox for arbitrary target code.

## Expected and observed behavior

The authored contract says page(items, 0) returns an empty list. The target instead
returns every supplied item. The exact original three-item command returned 1 and
reported Reproduced; reducing to one item retained that symptom. Zero items returned
0 and Not reproduced: this is a negative control, not an even smaller reproduction.
Positive and None limits also returned 0. No statistical or flaky-reproduction claim
is made from these deterministic observations.

## Reduction and regression evidence

- Original three items: receipts/cases/original.json, exit 1, same reported symptom.
- Reduced one item: receipts/cases/minimal.json, exit 1, same reported symptom.
- Empty non-trigger: receipts/cases/empty.json, exit 0, Not reproduced.
- Positive/None controls: receipts/cases/positive.json and none.json, exit 0.
- Bug target regression: receipts/cases/regression_bug.json, exit 1; exactly the
  zero-limit contract assertion fails, while three legitimate controls pass.
- Authored contrast regression: receipts/cases/regression_good.json, exit 0; four pass.
- Authored contrast reproducer: receipts/cases/good_control.json, exit 0.
- Missing target: receipts/cases/missing_target.json, exit 2, Blocked—not reproduction.

Runnable minimal artifact: reproduce.py --items 1; regression: regression.py. Exact
argv/cwd, stdout, stderr, exit status and finite timeout are in the captured records.
README.md gives portable commands. Public paths are explicitly redacted and originals
retained privately; source equivalence is not substituted for final-artifact execution.

## Limits

known-good-control.py is an authored comparison, not a released version or remediation
of user source. No real target was changed, root cause certified, external issue posted,
package published, or native agent/model invoked. Broader target/runtime coverage and
agent usefulness are untested. Not reproduced elsewhere would not establish no bug.
