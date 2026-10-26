# Compatibility and exercised environment

Status: experimental source example, manually exercised only. No host compatibility or agent activation is claimed.

| Component | Observed environment |
| --- | --- |
| OS / architecture | macOS 26.5.2, Apple Silicon (arm64) |
| Node.js / npm | Node v22.23.3; npm 10.9.9 |
| Playwright npm package | 1.58.2, pinned in `examples/project-to-demo/package-lock.json` |
| Browser | Playwright Chromium 145.0.7632.6, revision v1208 |
| FFmpeg / ffprobe | 8.0.1; local build enables GPL, version3, and libx264 |
| Capture fixture | Local HTTP server, real Chromium UI click, UI output assertion |
| MP4 | H.264, yuv420p, 1280×720, 30/1 fps, silent; 31.4 seconds |

The capture and rendered artifact were retained in the current session's scratch directory as external verification evidence; that location is deliberately not embedded here as a required skill path or machine-specific compatibility claim.

Exercised failure cases: missing dependency resolution, absent browser executable,
unavailable local app (HTTP 503), missing UI action target, existing destination,
and SIGTERM interruption. These are controlled fixture cases, not general crash or
power-loss qualification. Failed/partial captures remain failed; renderer refusal
and invalid-media tests are also included. SIGINT uses the same handler but was not
separately signal-tested.

Not exercised: clean host installation/removal, actual agent loading or activation,
non-trigger behavior in a host, Linux/Windows locally, a representative third-party
project, the reserved unit-converter task, repeated paired trials, incumbent comparison,
paid/external services, publication, or distribution rights for binaries. The experimental
source/example is not a qualified release. The added CI workflow is configured to
exercise the fixture on Linux; its actual run result must be checked separately and
is not an agent-compatibility claim.
