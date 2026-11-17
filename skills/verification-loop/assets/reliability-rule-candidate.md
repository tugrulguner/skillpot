# Reliability rule candidate

Status: PROPOSED / OBSERVING / OWNER-APPROVED / RETIRED. Candidate ID: __. Owner: __. No enforcement or policy edit is authorized by this proposal.

## Evidence and scope
- Repeated missed defect, user impact and supporting incident/receipt links:
- Distinguish introduced defect, pre-existing issue, low-value nit and unknown cause:
- Observable diff trigger (paths/change pattern); applicable behavior and exclusions:
- Focused check and criterion/independent expected result:
- Why this rule would have caught the supported miss:
- Evidence gaps; a single incident stays provisional:

## Challenge before adoption
- Historical buggy control and intended failing assertion; actual result/receipt or NOT RUN:
- Healthy matching-trigger control; expected pass and actual result/receipt or NOT RUN:
- Legitimate non-trigger change; expected non-application and actual result/receipt or NOT RUN:
- False positives, missed cases, execution duration and authorized observation count:
- Findings carried from earlier rounds rather than rediscovered; remaining limitations:

## Owner decision and lifecycle
- Owner approval/rejection and reason; approval is not inferred:
- Observation-only trial and explicit criteria for later enforcement:
- Exact independently authorized policy/test destination and protected base rule source:
- Repeat invocation, applicable checks only, and added cost:
- Retirement/revision condition, maintainer and review interval:

Preserve original incidents and failed observations. Do not change the current gate, install a hook, delete a test or promote this rule into enforcement without separate authority. An optional rule must earn its maintenance cost.
