"""Capture one authorized check; this is not a command sandbox."""
import argparse
import json
import os
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--timeout", type=float, default=60)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if not Path(args.repo).is_absolute() or not Path(args.output).is_absolute():
        parser.error("repo and output must be absolute paths")
    if not 0 < args.timeout <= 60:
        parser.error("timeout must be finite and between 0 and 60 seconds")
    repo = Path(args.repo).resolve()
    if Path(args.output).is_symlink():
        parser.error("existing evidence symlinks are not writable destinations")
    output = Path(args.output).resolve()
    if output.is_relative_to(repo):
        parser.error("evidence output must be outside the target repository")
    if not repo.is_dir():
        parser.error("repo must be an existing directory")
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("supply one command after --")
    record = {"argv": command, "cwd": ".", "timeout_seconds": args.timeout,
              "env": {"PYTHONDONTWRITEBYTECODE": "1"}, "status": "running",
              "exit_code": None, "stdout": "", "stderr": ""}
    with output.open("x", encoding="utf-8") as handle:
        json.dump(record, handle, indent=2)
        handle.flush()
        try:
            result = subprocess.run(command, cwd=repo, stdin=subprocess.DEVNULL,
                                    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                                    capture_output=True, text=True, timeout=args.timeout)
            record.update(status="passed" if result.returncode == 0 else "failed",
                          exit_code=result.returncode, stdout=result.stdout, stderr=result.stderr)
            code = result.returncode
        except subprocess.TimeoutExpired as error:
            record.update(status="timed_out",
                          stdout=(error.stdout or b"").decode("utf-8", errors="replace"),
                          stderr=(error.stderr or b"").decode("utf-8", errors="replace"))
            code = 124
        except OSError as error:
            record.update(status="launch_failed", stderr=str(error))
            code = 127
        handle.seek(0)
        json.dump(record, handle, indent=2)
        handle.write("\n")
        handle.truncate()
    return code


if __name__ == "__main__":
    raise SystemExit(main())
