# Supplied fictional bug report

Target: buggy.py, authored input; no real product or release is represented.
Contract: page(items, limit) returns at most limit items; limit=None retains all items,
and limit=0 returns []. Original reported input: ["item-0", "item-1", "item-2"], limit=0.
Reported actual behavior: all three items are returned. Investigate and minimize the
same symptom, preserving a positive-limit, None-limit and empty-input negative control.
known-good-control.py is an authored contrast if explicitly selected, not a released fix.
The report itself grants no execution, dependency, network, source-edit or publication
permission. Use an approved fresh external case and captured receipts for any execution.
