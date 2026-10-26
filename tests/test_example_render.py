import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "example_render", Path(__file__).resolve().parents[1] / "examples/project-to-demo/render.py"
)
assert SPEC is not None and SPEC.loader is not None
renderer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(renderer)


class RenderBoundaryTests(unittest.TestCase):
    def test_existing_output_is_untouched(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "existing"
            out.mkdir()
            (out / "keep").write_text("original")
            with self.assertRaisesRegex(ValueError, "Output exists"):
                renderer.render(Path(d) / "missing", out)
            self.assertEqual((out / "keep").read_text(), "original")

    def test_failed_capture_never_renders(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "capture.json").write_text(json.dumps({"status": "failed"}))
            with patch.object(renderer.subprocess, "run") as run:
                with self.assertRaisesRegex(ValueError, "failed or incomplete"):
                    renderer.render(root, root / "render")
                run.assert_not_called()
            self.assertFalse((root / "render").exists())

    @unittest.skipUnless(renderer.shutil.which("ffmpeg") and renderer.shutil.which("ffprobe"),
                         "media tools not installed")
    def test_invalid_media_records_failed_render(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "capture.json").write_text(json.dumps({"status": "success"}))
            (root / "raw").mkdir()
            (root / "raw/capture.webm").write_bytes(b"deliberately invalid media")
            with self.assertRaises(renderer.subprocess.CalledProcessError):
                renderer.render(root, root / "render")
            report = json.loads((root / "render/verification.json").read_text())
            self.assertEqual(report["status"], "failed")
            self.assertNotEqual(report["commands"][-1]["exit_code"], 0)
            self.assertNotIn("full_decode_exit_code", report)

    def test_missing_tool_never_creates_output(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "capture.json").write_text(json.dumps({"status": "success"}))
            (root / "raw").mkdir()
            (root / "raw/capture.webm").write_bytes(b"test-only placeholder; not media")
            with patch.object(renderer.shutil, "which", return_value=None):
                with self.assertRaisesRegex(ValueError, "Missing external tool"):
                    renderer.render(root, root / "render")
            self.assertFalse((root / "render").exists())


if __name__ == "__main__":
    unittest.main()
