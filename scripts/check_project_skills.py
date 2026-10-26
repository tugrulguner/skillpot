"""Validate pinned skill distribution integrity, offline (not runtime qualification)."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import yaml


def check(root):
    errors = []
    catalog = json.loads((root / "catalog/modepot-sources.json").read_text())
    for entry in catalog["skills"]:
        name = entry["name"]
        if (not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)
                or entry["directory"] != f"skills/{name}"):
            errors.append(f"{name}: unsafe directory")
            continue
        if not re.fullmatch(r"[0-9a-f]{40}", entry["upstream_revision"]):
            errors.append(f"{name}: invalid upstream revision")
        directory = root / entry["directory"]
        if not directory.resolve().is_relative_to(root.resolve()):
            errors.append(f"{name}: directory escapes source root")
            continue
        text = (directory / "SKILL.md").read_text()
        metadata = yaml.safe_load(text.split("---", 2)[1])
        description = metadata.get("description")
        if (not text.startswith("---\n") or metadata.get("name") != name
                or not isinstance(description, str) or not 0 < len(description) <= 60
                or metadata.get("license") != entry["license"]):
            errors.append(f"{name}: invalid portable frontmatter")
        values = metadata.get("metadata", {})
        if not isinstance(values, dict) or any(not isinstance(k, str) or not isinstance(v, str)
                                               for k, v in values.items()):
            errors.append(f"{name}: metadata must contain only string values")
        for rel in ("LICENSE", "references/LICENSE.md"):
            path = directory / rel
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != entry["license_sha256"]:
                errors.append(f"{name}: license mismatch or missing notice: {rel}")
        source = directory / "references/upstream.md"
        if hashlib.sha256(source.read_bytes()).hexdigest() != entry["upstream_sha256"]:
            errors.append(f"{entry['name']}: upstream hash mismatch")
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = check(args.root)
    print("\n".join(errors) if errors else "PASS: pinned project skill source integrity")
    raise SystemExit(bool(errors))
