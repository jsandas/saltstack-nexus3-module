#!/usr/bin/env python3
"""Generate docs markdown from function docstrings in _modules and _states.

This script scans top-level Python files under _modules and _states, extracts
top-level function signatures and docstrings, then writes markdown files under:
  - docs/modules/<name>.md
  - docs/states/<name>.md

Where <name> is derived from source filename by removing the nexus3_ prefix.
"""

from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent
from typing import Iterable, List


@dataclass
class FunctionDoc:
    name: str
    signature: str
    doc: str


def normalize_docstring(doc: str) -> str:
    """Normalize docstrings for current markdown style."""
    normalized = dedent(doc).strip("\n")
    normalized = normalized.replace(".. note::", "Note:")
    normalized = normalized.replace(".. note:", "Note:")
    return normalized


def _format_default(node: ast.AST) -> str:
    if isinstance(node, ast.Constant):
        return repr(node.value)
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _format_default(node.value)
        return f"{base}.{node.attr}"
    try:
        return ast.unparse(node)
    except Exception:
        return "..."


def _format_arg(arg: ast.arg, default: ast.AST | None) -> str:
    if default is None:
        return arg.arg
    return f"{arg.arg}={_format_default(default)}"


def build_signature(fn: ast.FunctionDef) -> str:
    args = fn.args
    parts: List[str] = []

    positional = args.posonlyargs + args.args
    defaults = [None] * (len(positional) - len(args.defaults)) + list(args.defaults)

    if args.posonlyargs:
        posonly_count = len(args.posonlyargs)
        for i, arg in enumerate(positional):
            parts.append(_format_arg(arg, defaults[i]))
            if i + 1 == posonly_count:
                parts.append("/")
    else:
        for i, arg in enumerate(positional):
            parts.append(_format_arg(arg, defaults[i]))

    if args.vararg:
        parts.append(f"*{args.vararg.arg}")
    elif args.kwonlyargs:
        parts.append("*")

    for kwarg, default in zip(args.kwonlyargs, args.kw_defaults):
        parts.append(_format_arg(kwarg, default))

    if args.kwarg:
        parts.append(f"**{args.kwarg.arg}")

    return ",".join(parts)


def iter_python_files(folder: Path) -> Iterable[Path]:
    for path in sorted(folder.glob("*.py")):
        if path.name == "__init__.py":
            continue
        yield path


def extract_functions(py_path: Path) -> list[FunctionDoc]:
    source = py_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(py_path))

    functions: list[FunctionDoc] = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            doc = ast.get_docstring(node)
            if not doc:
                continue
            functions.append(
                FunctionDoc(
                    name=node.name,
                    signature=build_signature(node),
                    doc=normalize_docstring(doc),
                )
            )
    return functions


def source_to_doc_name(source_file: Path) -> str:
    stem = source_file.stem
    prefix = "nexus3_"
    if stem.startswith(prefix):
        return stem[len(prefix) :]
    return stem


def render_markdown(module_name: str, functions: list[FunctionDoc]) -> str:
    chunks: list[str] = []
    for func in functions:
        chunks.append(f"{module_name}.**{func.name}**(*{func.signature}*):")
        chunks.append("")
        for line in func.doc.splitlines():
            if line:
                chunks.append(f"    {line}")
            else:
                chunks.append("")
        chunks.append("")
        chunks.append("")

    return "\n".join(chunks).rstrip() + "\n"


def write_docs(source_dir: Path, docs_dir: Path, check_only: bool = False) -> list[Path]:
    changed: list[Path] = []

    for py_file in iter_python_files(source_dir):
        functions = extract_functions(py_file)
        if not functions:
            continue

        module_name = py_file.stem
        doc_name = source_to_doc_name(py_file)
        output_file = docs_dir / f"{doc_name}.md"

        rendered = render_markdown(module_name, functions)
        existing = output_file.read_text(encoding="utf-8") if output_file.exists() else None

        if existing != rendered:
            changed.append(output_file)
            if not check_only:
                output_file.write_text(rendered, encoding="utf-8")

    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--check", action="store_true", help="Only check whether docs are up-to-date")
    args = parser.parse_args()

    root = args.root
    updates: list[Path] = []

    updates.extend(write_docs(root / "_modules", root / "docs" / "modules", check_only=args.check))
    updates.extend(write_docs(root / "_states", root / "docs" / "states", check_only=args.check))

    if updates:
        action = "Would update" if args.check else "Updated"
        for path in updates:
            print(f"{action}: {path.relative_to(root)}")
        return 1 if args.check else 0

    print("Docs are already up-to-date")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
