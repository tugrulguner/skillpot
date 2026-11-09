"""Run the explicitly selected fictional target; not a command sandbox."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, default=ROOT / "buggy.py")
    parser.add_argument("--items", type=int, default=1)
    parser.add_argument("--limit", default="0", help="integer or none")
    args = parser.parse_args()
    if not 0 <= args.items <= 32:
        parser.error("items must be between 0 and 32")
    try:
        limit = None if args.limit.lower() == "none" else int(args.limit)
    except ValueError:
        parser.error("limit must be an integer or none")
    target = args.target.resolve()
    items = [f"item-{i}" for i in range(args.items)]
    expected = items if limit is None else items[:limit]
    record = {"target_path": str(target), "python_executable": sys.executable,
              "python_version": platform.python_version(), "items": args.items, "limit": limit,
              "input_sha256": hashlib.sha256(json.dumps(items).encode()).hexdigest()}
    try:
        record["target_sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
        spec = importlib.util.spec_from_file_location("bug_repro_selected_target", target)
        if spec is None or spec.loader is None:
            raise ImportError("target has no Python source loader")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if module.__file__ is None:
            raise ImportError("target module has no file identity")
        record["imported_module_path"] = str(Path(module.__file__).resolve())
        actual = module.page(items, limit)
        record.update(expected_repr=repr(expected), actual_repr=repr(actual))
        if actual == expected:
            code, status = 0, "Not reproduced"
        elif limit == 0 and items and actual == items:
            code, status = 1, "Reproduced"
        else:
            code, status = 3, "Different failure"
        record["status"] = status
    except Exception as error:
        code = 2
        record.update(status="Blocked", error_type=type(error).__name__, error=str(error))
    print(json.dumps(record, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
