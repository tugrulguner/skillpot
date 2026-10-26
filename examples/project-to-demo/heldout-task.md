# Reserved task: unit conversion

Protocol status: specified after the initial record-grouper prototype, before implementing
or executing this reserved task. No held-out success or evaluation is claimed. Do not
change this brief to accommodate results; record a protocol amendment if it changes.

## Input

A separate browser application with a labeled numeric input, source-unit selection,
destination-unit selection, a Convert button, and a visible result. Use public fixture
data: convert 100 centimeters to meters. The expected result is 1 meter. Start empty,
enter the value through visible UI controls, select the units, click Convert, and show
the actual result. Do not inject application state or hard-code the expected result
into the recording.

## Same acceptance criteria

- Record the real empty/input/action/result journey in causal order.
- Verify the actual output independently against the conversion definition.
- Preserve raw capture and source identity; deliver a silent landscape MP4, captions,
  transcript, claims mapped to inspected encoded frames, and full-decode verification.
- Refuse overwriting prior runs; clean up owned fixture/browser processes on failure.
- Clearly identify fixture data and editorial explanation. Do not present viewing holds
  or edited duration as latency.

Freeze the same model, host, tool versions, permissions, and budget before comparative
trials; predeclare trial count and rubric. Reserve this task for evaluation, rather than
using it to tune the record-grouper example. Its application and agent trials are not
implemented in this change.
