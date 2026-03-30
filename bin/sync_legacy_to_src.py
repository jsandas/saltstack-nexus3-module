#!/usr/bin/env python3
"""Sync legacy Salt loader folders into the src package tree.

This keeps the transition period maintainable while legacy and package layouts
coexist for one release window.
"""

from __future__ import annotations

import argparse
from pathlib import Path


REWRITES = {
    "import nexus3": "from saltext.nexus3.utils import nexus3",
}


def copy_py_files(source_dir: Path, target_dir: Path) -> int:
    target_dir.mkdir(parents=True, exist_ok=True)
    copied = 0

    for source in sorted(source_dir.glob("*.py")):
        content = source.read_text(encoding="utf-8")
        for old, new in REWRITES.items():
            content = content.replace(old, new)

        target = target_dir / source.name
        target.write_text(content, encoding="utf-8")
        copied += 1

    return copied


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    root = args.root
    mappings = [
        (root / "_modules", root / "src" / "saltext" / "nexus3" / "modules"),
        (root / "_states", root / "src" / "saltext" / "nexus3" / "states"),
        (root / "_utils", root / "src" / "saltext" / "nexus3" / "utils"),
    ]

    total = 0
    for source, target in mappings:
        if not source.exists():
            continue
        total += copy_py_files(source, target)
        print(f"Synced {source.relative_to(root)} -> {target.relative_to(root)}")

    print(f"Synced {total} Python files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
