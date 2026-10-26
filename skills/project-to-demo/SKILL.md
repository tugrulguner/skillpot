---
name: project-to-demo
description: Turn a working browser project into a verified demo recording.
license: MIT
metadata:
  version: "0.1.0"
  maintainer: "tugrulguner"
  status: "experimental"
---

# Project to demo (experimental)

Use this procedure when a user wants a local browser application recorded showing a real, reproducible journey. It orchestrates public Playwright and FFmpeg tools; it is not a video engine, an installer, or an agent-host integration. The checked-in runnable example is a fixture, not evidence of general usefulness or compatibility.

## Trigger and boundaries

- Use for one browser app, one short landscape capture, and a reviewed MP4.
- Do not use for native desktop capture, narration, social posting, uploads, paid services, or broad visual editing.
- Never invent app behavior, pass fabricated data as user data, overwrite an earlier run, or publish without separate approval.

## Requirements and permissions

- Node.js 22.x, npm, the exact pinned Playwright dependency, its installed Chromium browser, FFmpeg with `libx264`, and ffprobe. They are separate user-installed external dependencies; this repository redistributes no tool binaries. FFmpeg builds vary in license; check the local build before use.
- Work only on an authorized local project and approved non-sensitive data. The example's `demo-1`, `apples`, and `pears` are explicitly fixture data.
- Before recording, confirm a new output directory, local app readiness, audience, allowed claims, and capture scope. Do not expose unrelated desktop/browser content or secrets.

## Procedure

1. Inspect the app and identify one small user journey and its expected visible result. Write down what is fixture behavior, actual product behavior, and any claim that needs evidence. Stop if the project cannot be run or the result cannot be independently checked.
2. Start the app with its documented command. Confirm it is reachable and ready before launching capture. Use a fresh, uniquely named run directory; refuse an existing destination.
3. Configure Playwright `recordVideo` with an explicit viewport and output size. Record the actual UI journey; assert the visible final result before treating capture as successful. Close the browser context so the recording is flushed. On action, browser, or process failure, retain diagnostics as failed/incomplete, clean up only processes started for this run, and do not report a completed artifact.
4. Convert the original recording using the locally available FFmpeg encoder, for example:

   ```sh
   ffmpeg -nostdin -n -i raw/capture.webm -an -vf 'fps=30,scale=1280:720:flags=lanczos,format=yuv420p' -c:v libx264 -crf 20 -movflags +faststart demo.mp4
   ```

   Do not infer system latency from holds or edited playback duration. Keep the raw capture. Do not distribute binaries or imply this skill's MIT license applies to FFmpeg, Chromium, or separately installed packages.
5. Probe the encoded output with ffprobe; verify codec, pixel format, dimensions, frame rate, duration, and audio policy. Fully decode it with FFmpeg. Extract and inspect actual encoded frames at the beginning, transitions, and final hold. Reject unreadable, misleading, clipped, or failed outputs and preserve the run for diagnosis.
6. Write captions/transcript and evidence only after reviewing the final encoded media. Map each factual claim to an observed UI state or a specific decoded time range; distinguish fixture data, editorial text, and actual behavior.
7. Report absolute artifact paths, exact commands and tool versions, probe/decode results, review findings, failures, and untested gates. Do not claim host compatibility, installation, activation, usefulness, or release unless each was actually tested.

## Runnable fixture

See [`../../examples/project-to-demo/README.md`](../../examples/project-to-demo/README.md). It starts empty, enters two fixture rows sharing an identifier, clicks the real grouping button, and asserts one output record with two items. It records through official Playwright video capture and uses FFmpeg for H.264 MP4. The example is manually exercised on the environment recorded in `compatibility.md`; it does not test an agent host or a representative third-party project.

## Failure and recovery

- Missing tools/dependencies: stop before capture; report exact missing command/package. Do not silently substitute or install globally.
- Unavailable app or failed action assertion: stop, close the context to flush diagnostics where possible, and mark the run failed.
- Existing destination: refuse without modifying it; choose a new path.
- Interrupted capture: stop only child processes created by the run, close the context when possible, and label raw output incomplete. Never render it as a successful delivery.
- Probe, decode, or visual-review failure: retain originals, report the failing check, and do not claim success.

## Verification

Completion requires the actual UI assertion, flushed raw recording, encoded MP4, ffprobe output, successful full decode, reviewed decoded frames, captions/transcript, and evidence note. This experimental fixture has not passed clean host installation, host activation, held-out tasks, matched evaluation, or a full sensitive-data audit.
