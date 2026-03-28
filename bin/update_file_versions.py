#!/usr/bin/env python3
"""Update :version: metadata in _modules, _states, and _utils Python files."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

VERSION_RE = re.compile(r"^:version:\s+\S+\s*$", re.MULTILINE)
RELEASE_BRANCH_RE = re.compile(r"^release/(?P<version>v?\d+\.\d+\.\d+)$")
TARGET_DIRS = ("_modules", "_states", "_utils")


def normalize_version(version: str) -> str:
    version = version.strip()
    if not version:
        raise ValueError("version cannot be empty")
    if not version.startswith("v"):
        version = f"v{version}"
    return version


def detect_version_from_branch(root: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), "branch", "--show-current"],
        check=True,
        capture_output=True,
        text=True,
    )

    branch = result.stdout.strip()
    match = RELEASE_BRANCH_RE.match(branch)
    if not match:
        raise ValueError(
            "Could not detect version from branch name. Expected release/vX.Y.Z, "
            f"got: {branch!r}"
        )

    return normalize_version(match.group("version"))


def update_file(path: Path, normalized_version: str, dry_run: bool) -> bool:
    original = path.read_text(encoding="utf-8")
    replacement = f":version: {normalized_version}"

    if not VERSION_RE.search(original):
        return False

    updated = VERSION_RE.sub(replacement, original, count=1)
    if updated == original:
        return False

    if not dry_run:
        path.write_text(updated, encoding="utf-8")

    return True


def iter_target_files(root: Path):
    for dirname in TARGET_DIRS:
        directory = root / dirname
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.py")):
            if path.name == "__init__.py":
                continue
            yield path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", nargs="?", help="release version (e.g. 0.3.1 or v0.3.1)")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--from-branch",
        action="store_true",
        help="derive version from current git branch release/vX.Y.Z",
    )
    parser.add_argument("--dry-run", action="store_true", help="show changes without writing files")
    args = parser.parse_args()

    root = args.root

    if args.version and args.from_branch:
        raise ValueError("Specify either a version argument or --from-branch, not both")

    if args.version:
        normalized_version = normalize_version(args.version)
    else:
        normalized_version = detect_version_from_branch(root)

    updated_paths = []
    missing_marker = []

    for path in iter_target_files(root):
        if VERSION_RE.search(path.read_text(encoding="utf-8")) is None:
            missing_marker.append(path)
            continue

        if update_file(path, normalized_version, args.dry_run):
            updated_paths.append(path)

    action = "Would update" if args.dry_run else "Updated"

    if updated_paths:
        for path in updated_paths:
            print(f"{action}: {path.relative_to(root)}")
    else:
        print("No files required updates")

    if missing_marker:
        print("Files missing :version: marker:")
        for path in missing_marker:
            print(f"  - {path.relative_to(root)}")

    print(f"Target version: {normalized_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
