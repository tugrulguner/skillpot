"""Transcode this example's successful capture using external FFmpeg tools.

No editing engine: one real recording, optional reviewed start trim, and probes.
Visual review, captions, and claim verification remain explicit human/agent tasks.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render(capture_dir, output, start=0.0):
    capture_dir, output = Path(capture_dir), Path(output)
    if output.exists():
        raise ValueError("Output exists; choose a new render directory")
    manifest = json.loads((capture_dir / "capture.json").read_text())
    if manifest.get("status") != "success":
        raise ValueError("Refusing a failed or incomplete capture")
    raw = capture_dir / "raw/capture.webm"
    if not raw.is_file():
        raise ValueError("Successful manifest has no raw recording")
    if not 0 <= start < 60:
        raise ValueError("Reviewed start trim must be between 0 and 60 seconds")
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            raise ValueError(f"Missing external tool: {tool}")
    output.mkdir(parents=False)
    record = {"status": "failed", "visual_review": "pending", "commands": [],
              "source_sha256": sha256(raw), "capture_manifest": manifest,
              "start_trim_seconds": start}

    def command(args):
        result = subprocess.run(args, capture_output=True, text=True, timeout=120)
        record["commands"].append({"args": args, "exit_code": result.returncode,
                                   "stderr": result.stderr[-8000:]})
        result.check_returncode()
        return result.stdout

    try:
        record["versions"] = {t: command([t, "-version"]).splitlines()[0]
                              for t in ("ffmpeg", "ffprobe")}
        video = output / "demo.mp4"
        command(["ffmpeg", "-nostdin", "-n", "-ss", str(start), "-i", str(raw),
                 "-an", "-vf", "fps=30,scale=1280:720:flags=lanczos,format=yuv420p",
                 "-c:v", "libx264", "-crf", "20", "-movflags", "+faststart", str(video)])
        probe = json.loads(command(["ffprobe", "-v", "error", "-show_streams",
                                    "-show_format", "-of", "json", str(video)]))
        streams = probe["streams"]
        if len(streams) != 1:
            raise ValueError("Expected exactly one silent video stream")
        stream = streams[0]
        expected = {"codec_name": "h264", "pix_fmt": "yuv420p", "width": 1280,
                    "height": 720, "r_frame_rate": "30/1"}
        if any(stream.get(k) != v for k, v in expected.items()):
            raise ValueError("Encoded stream does not match the example profile")
        duration = float(probe["format"]["duration"])
        if not 30 <= duration <= 40:
            raise ValueError("Example requires 30–40 seconds of actual captured content")
        command(["ffmpeg", "-nostdin", "-v", "error", "-xerror", "-i", str(video),
                 "-f", "null", "-"])
        frames = output / "frames"
        frames.mkdir()
        for name, time in (("first", 0), ("middle", duration / 2), ("final", duration - .1)):
            command(["ffmpeg", "-nostdin", "-v", "error", "-n", "-ss", str(time),
                     "-i", str(video), "-frames:v", "1", str(frames / f"{name}.png")])
        command(["ffmpeg", "-nostdin", "-v", "error", "-n", "-i", str(video),
                 "-vf", "fps=1/4,scale=400:225,tile=2x4", "-frames:v", "1",
                 str(frames / "contact-sheet.png")])
        record.update(status="media_verified_pending_review", probe=probe,
                      full_decode_exit_code=0, output_sha256=sha256(video))
        return record
    except Exception as error:
        record["error"] = str(error)
        raise
    finally:
        (output / "verification.json").write_text(json.dumps(record, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture_dir", type=Path)
    parser.add_argument("output", type=Path, help="new render directory")
    parser.add_argument("--start", type=float, default=0,
                        help="reviewed raw-video start time; no speed changes or padding")
    args = parser.parse_args()
    result = render(args.capture_dir, args.output, args.start)
    print(result["status"])
