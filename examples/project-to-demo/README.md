# Project-to-demo runnable fixture

This original local record-transformer UI is a demonstration fixture, not a SkillPot
feature or a third-party product. `demo-1`, `apples`, and `pears` are public fixture
data. Start with no rows, enter two rows through visible inputs, click **Group rows**,
and inspect one record with two items. No application state is injected by the recorder.

## Requirements and setup

- Node.js 22.x and npm; Python 3.11+ for the small FFmpeg command adapter.
- Separately installed FFmpeg/ffprobe with the `libx264` encoder.
- Run `npm ci` in this directory, then `npx playwright install chromium` to download
  the pinned Playwright package's matching browser. No browser or FFmpeg binaries are
  included. Dependencies retain their own licenses.

## Run checks and capture

From this directory, choose a parent directory you own. Set `RUN` to a new, absent
subdirectory. The POSIX shell commands below were exercised on macOS; Windows shell
instructions and Windows execution are not qualified.

```sh
npm test
RUN="$PWD/demo-run-001"
SKILLPOT_OUTPUT="$RUN" node capture.mjs
python3 render.py "$RUN" "$RUN/render-001"
```

The fixture server binds only loopback on a dynamically assigned port. The recorder
uses explicit 1280×720 recording, public UI actions and an exact visible-JSON assertion.
It closes the browser context to flush the raw WebM. `capture.json` records success or
failure, source identity, and observed action markers. These markers are diagnostics;
wall-clock action timing is not automatically the encoded video timeline.

`render.py` is a small command adapter for this example: it invokes the external FFmpeg
encoder, ffprobe, full decode, and frame extraction. It does not implement a renderer,
compositor, new recipe format, or editing engine. It refuses a failed capture or existing
render directory. The MP4 profile is silent H.264/yuv420p, 1280×720, 30 fps, 30–40 seconds.
The duration includes real recorded viewing holds, not padding or a latency measurement.

A successful media check leaves `visual_review: pending` and status
`media_verified_pending_review` in `render-001/verification.json`. That is not a finished
delivery. Review the actual encoded first, middle, final frames and contact sheet under
`render-001/frames/`, then inspect each input/action/result transition in the video. If
frame zero is loading/blank, locate the first ready raw-video frame and rerender to a
new directory with `--start SECONDS`. No speed changes or freezing are applied. Do not
select a trim that removes the clean input state or makes the capture too short.

## Complete the delivery after encoded-media review

Create the following alongside `demo.mp4` in the selected render directory:

- `brief.md`: audience, public fixture inputs, permitted claims, source fingerprint,
  scope, output profile, and no paid or external application service.
- `capture-plan.md`: empty state → type/add first row → type/add second row → group →
  inspect actual JSON. Link the retained raw recording and `capture.json`.
- `captions.vtt`: actual encoded time ranges, beginning with `WEBVTT`, explaining inputs,
  grouping action, and result. Do not copy unverified wall-clock capture markers.
- `transcript.md`: matching plain-language explanation; label fixture data explicitly.
- `evidence.json`: each claim, observed result, decoded time range/frame, source identity,
  and the reviewed MP4 SHA-256 from `verification.json`.
- `review.json`: reviewer, that same MP4 SHA-256, exact reviewed encoded frame times,
  readability/chronology/claim decisions, and limitations. Leave failed checks failed.
- `reproduce.md`: the exact setup, capture, render commands and tool versions actually
  used. Preserve all earlier takes and renders.

Keep probe/decode evidence separate from visual review. A manifest or a model saying
"success" cannot replace inspecting pixels. Captions, claims, and review must refer to
the final encoded bytes. This is deliberately an agent procedure with explicit review,
not a script that manufactures a complete-looking evidence package.

## Tests and limitations

Run the repository's Python checks from its root:

```sh
python3 scripts/check_docs.py
python3 -m unittest discover -s tests -v
```

The Node tests cover fixture transformation and recorder refusal/cleanup paths; consult
the actual runner output for exercised cases. The Python tests cover render-boundary
refusals. Real media acceptance additionally requires running the capture and external
tools, decoding the MP4, and reviewing it. The [reserved task](heldout-task.md) is a
protocol only, not a completed second example or evaluation.

See [recorded evidence](evidence.md), [provenance](../../skills/project-to-demo/provenance.md),
and [compatibility limits](../../skills/project-to-demo/compatibility.md). Agent-host
installation/activation and repeated comparative trials remain open.
