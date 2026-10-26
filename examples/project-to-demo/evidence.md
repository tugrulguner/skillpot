# Manually exercised demo evidence

This is a single original fixture run, not an agent-host or task-usefulness evaluation.
All application inputs are public fixture values: `demo-1`, `apples`, `pears`.

## Actual media and source identity

- Final MP4 SHA-256: `77487cb7386875087e74d7444743bc1324a6d73ad013d0d7e2c1548a537ea299`.
- Raw WebM SHA-256: `172c3159f7586efe755ea45916c6b2504eb09326ab766a073afd5a4fff26ea3e`.
- `capture.mjs`: `7a035a24852ee020d67953820cbf82ee8a1432db3a41651a783737bae7604840`.
- `index.html`: `8d4662bc79837837c97476304b24cd015b1471837a5309dad1c1857129478d78`.
- `transform.mjs`: `0b8c6e02f8704c8324858f7e15d6b145e23a8e3f42bad23164a172ff9768db1a`.

The three source files were uncommitted when captured; file hashes identify the exact
exercised bytes rather than attributing new behavior to the unchanged base commit.
The run retained capture.json, raw video, MP4, probe/decode commands and reports,
encoded frames/contact sheet, brief, capture plan, VTT, transcript, evidence.json,
AI review.json and reproduction steps outside the checkout. Videos are not committed
as source files or required personal-machine dependencies.

## Actual consumer checks

Playwright 1.58.2 on Node 22.23.3 drove visible inputs and the real Add row/Group rows
buttons. The UI assertion returned exactly:

```json
[{"id":"demo-1","items":["apples","pears"]}]
```

FFmpeg/ffprobe 8.0.1 produced and fully decoded a silent H.264/yuv420p MP4, 1280×720,
30 fps, 31.4 seconds. Full decode exited 0. The duration includes actual viewing holds;
it is not a latency measurement. No trim, speed change, freezing, output injection,
private kit, provider call, spending or upload was used.

## Encoded visual review

The AI reviewer inspected frame 0, sampled 4-second timeline frames, detailed transition
frames at 3.3/3.9/10.2/11/18.7/19.3 seconds and the final 31.3-second frame. The actual
first frame has empty inputs and no output; 8s shows the first row; 12s shows two rows;
20s shows the actual grouped result. Final JSON and closing brackets fit entirely.
Captions use those inspected encoded states rather than assuming that wall-clock
capture markers align exactly with encoded media. Sidecars are evidence for these
particular bytes; reruns require new review and may have different times.

This is AI sampled-frame review, not human acceptance or a complete human playback
review. Browser/UI assertions and media checks do not prove host installation,
activation, third-party project compatibility, safety, or comparative usefulness.
The [reserved task](heldout-task.md) remains unexecuted.
