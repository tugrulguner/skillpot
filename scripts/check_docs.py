"""Check local Markdown destinations and accidental personal paths, offline.

Not a skill validator, artwork renderer, or task evaluation runner.
"""
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def check(root):
    errors = []
    for path in sorted(root.rglob("*.md")):
        if {".git", "node_modules", ".venv"}.intersection(path.relative_to(root).parts):
            continue
        text = path.read_text(encoding="utf-8")
        if re.search(r"/(?:Users|home)/[A-Za-z0-9_.-]+(?![A-Za-z0-9_.-])", text):
            errors.append(f"{path.relative_to(root)}: personal absolute path")
        for match in re.finditer(r"!?\[[^\]\n]*\]\(([^\s)]+)(?:\s+[^)]*)?\)", text):
            destination = match.group(1).strip("<>")
            parsed = urlsplit(destination)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (path.parent / unquote(parsed.path)).resolve()
            if not target.is_relative_to(root.resolve()):
                errors.append(f"{path.relative_to(root)}: link escapes repository: {destination}")
            elif not target.exists():
                errors.append(f"{path.relative_to(root)}: missing destination: {destination}")
    return errors


if __name__ == "__main__":
    errors = check(ROOT)
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        sys.exit(1)
    print("PASS: local Markdown destinations and personal-path checks")
