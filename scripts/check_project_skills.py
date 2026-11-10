"""Validate portable bundles and pinned source integrity, offline (not task efficacy)."""
import argparse
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
import yaml


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject shadowed YAML keys instead of accepting the last spelling."""

    def construct_mapping(self, node, deep=False):
        keys = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                if key in keys:
                    raise yaml.constructor.ConstructorError(
                        None, None, "duplicate frontmatter key", key_node.start_mark)
                keys.add(key)
            except TypeError as exc:
                raise yaml.constructor.ConstructorError(
                    None, None, "invalid frontmatter key", key_node.start_mark) from exc
        return super().construct_mapping(node, deep=deep)


def check_entrypoint(directory, name):
    try:
        text = (directory / "SKILL.md").read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None, [f"{name}: cannot read SKILL.md as UTF-8"]
    frontmatter = re.fullmatch(r"---\n(.*?)\n---(?:\n(.*))?", text, re.DOTALL)
    if frontmatter is None:
        return None, [f"{name}: incomplete portable frontmatter"]
    if not (frontmatter.group(2) or "").strip():
        return None, [f"{name}: missing instruction body"]
    try:
        metadata = yaml.load(frontmatter.group(1), Loader=UniqueKeyLoader)
    except yaml.YAMLError as exc:
        reason = "duplicate" if "duplicate frontmatter key" in str(exc) else "invalid YAML"
        return None, [f"{name}: {reason} frontmatter"]
    if not isinstance(metadata, dict):
        return None, [f"{name}: frontmatter must be a mapping"]
    description = metadata.get("description")
    errors = []
    allowed = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
    if any(key not in allowed for key in metadata):
        errors.append(f"{name}: unsupported portable frontmatter field")
    for key in ("compatibility", "allowed-tools", "license"):
        if key in metadata and (not isinstance(metadata[key], str) or not metadata[key].strip()):
            errors.append(f"{name}: invalid portable frontmatter {key}")
    if (metadata.get("name") != name
            or not isinstance(description, str) or not description.strip()
            or not 0 < len(description) <= 60):
        errors.append(f"{name}: invalid portable frontmatter")
    compatibility = metadata.get("compatibility")
    if isinstance(compatibility, str) and len(compatibility) > 500:
        errors.append(f"{name}: portable frontmatter compatibility exceeds 500 characters")
    values = metadata.get("metadata", {})
    if not isinstance(values, dict) or any(not isinstance(k, str) or not isinstance(v, str)
                                           for k, v in values.items()):
        errors.append(f"{name}: metadata must contain only string values")
    return metadata, errors


def check_resources(directory, name):
    """Check inline local Markdown destinations within the installed bundle."""
    errors = []
    for path in sorted(directory.rglob("*.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            errors.append(f"{name}: cannot read resource: {path.relative_to(directory)}")
            continue
        for match in re.finditer(r"!?\[[^\]\n]*\]\(([^\s)]+)(?:\s+[^)]*)?\)", text):
            destination = match.group(1).strip("<>")
            parsed = urlsplit(destination)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (path.parent / unquote(parsed.path)).resolve()
            if not target.is_relative_to(directory.resolve()):
                errors.append(f"{name}/{path.relative_to(directory)}: link escapes bundle: {destination}")
            elif not target.exists():
                errors.append(f"{name}/{path.relative_to(directory)}: missing resource: {destination}")
    return errors


def check(root):
    errors = []
    packages = {}
    for directory in sorted((root / "skills").iterdir()):
        name = directory.name
        if directory.is_symlink():
            errors.append(f"{name}: bundle symlink is not portable")
            continue
        if not directory.is_dir():
            continue
        if any(path.is_symlink() for path in directory.rglob("*")):
            errors.append(f"{name}: bundle symlink is not portable")
            continue
        if not 1 <= len(name) <= 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            errors.append(f"{name}: unsafe directory or invalid portable name")
            continue
        missing = [rel for rel in ("SKILL.md", "provenance.md", "compatibility.md")
                   if not (directory / rel).is_file()]
        if missing:
            errors.extend(f"{name}: missing resource: {rel}" for rel in missing)
            continue
        metadata, problems = check_entrypoint(directory, name)
        errors.extend(problems)
        if metadata is None:
            continue
        errors.extend(check_resources(directory, name))
        packages[name] = metadata
    catalog_path = root / "catalog/modepot-sources.json"
    if catalog_path.is_symlink():
        return errors + ["catalogue symlink is not portable"]
    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return errors + ["cannot read catalogue as UTF-8 JSON"]
    if (not isinstance(catalog, dict) or type(catalog.get("schema_version")) is not int
            or catalog.get("schema_version") != 1 or not isinstance(catalog.get("skills"), list)):
        return errors + ["invalid catalogue schema"]
    seen = set()
    required = ("name", "directory", "upstream_revision", "upstream_sha256", "license", "license_sha256")
    for entry in catalog["skills"]:
        if (not isinstance(entry, dict)
                or any(not isinstance(entry.get(key), str) or not entry[key].strip() for key in required)):
            errors.append("invalid catalogue entry fields")
            continue
        name = entry["name"]
        if name in seen:
            errors.append(f"{name}: duplicate catalogue entry")
            continue
        seen.add(name)
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
        if not directory.is_dir():
            errors.append(f"{name}: missing bundle directory")
            continue
        metadata = packages.get(name)
        if metadata is None:
            continue
        if metadata.get("license") != entry["license"]:
            errors.append(f"{name}: invalid portable frontmatter")
        for rel in ("LICENSE", "references/LICENSE.md"):
            path = directory / rel
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != entry["license_sha256"]:
                errors.append(f"{name}: license mismatch or missing notice: {rel}")
        source = directory / "references/upstream.md"
        if not source.is_file():
            errors.append(f"{name}: missing resource: references/upstream.md")
        elif hashlib.sha256(source.read_bytes()).hexdigest() != entry["upstream_sha256"]:
            errors.append(f"{entry['name']}: upstream hash mismatch")
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = check(args.root)
    print("\n".join(errors) if errors else "PASS: portable bundles and pinned project source integrity")
    raise SystemExit(bool(errors))
