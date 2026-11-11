# Authored claims to audit against a historical record

These are **newly authored review inputs**, not quotations from Dexpot's maintainers,
a published announcement, or an observed agent task. The upstream record itself
retains the failed screen; this deliberately misleading draft must not be attributed
to upstream. The owner requests review of C1–C6 only. C7 is explicitly deferred.

- **C1:** The published JSON contains one trial record for each of the eight planned
  cells, including two smoke cells and six screen cells.
- **C2:** All eight trial records report zero timeout errors.
- **C3:** Both 30-second flat pairs demonstrate candidate/control goodput above 1.0
  and adjusted closed-loop p99 ratios at most 1.10.
- **C4:** For the archived `item-2` pair, the candidate's recorded goodput is lower
  and its recorded adjusted closed-loop p99 is higher than the control's.
- **C5:** The wheel bytes actually loaded in every recorded trial match that side's
  declared wheel digest.
- **C6:** At 10,000 offered requests per second, the candidate's scheduled-arrival
  p99 latency is at most 20 ms.
- **C7:** The candidate is faster on macOS as well. **Outside the requested scope:**
  the owner deferred other platforms; do not silently widen this Linux-record review.
