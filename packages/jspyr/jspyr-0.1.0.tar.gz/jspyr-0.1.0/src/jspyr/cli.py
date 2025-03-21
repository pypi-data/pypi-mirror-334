"""CLI interface for jspyr."""

from __future__ import annotations

import argparse
import os.path
import sys

from jspyr import combine


class CLIArgs:
    py_path: str
    js_path: str
    out: str


def cli(argv: list[str] | None = None) -> int:
    """CLI interface."""
    parser = argparse.ArgumentParser()
    parser.add_argument("py_path")
    parser.add_argument("js_path")
    parser.add_argument("--out", default=None)
    args = parser.parse_args(argv, namespace=CLIArgs())

    if not os.path.isfile(args.py_path):
        parser.error(f"file not found: {args.py_path}")
    if not os.path.isfile(args.js_path):
        parser.error(f"file not found: {args.js_path}")

    with open(args.py_path, "rb") as py_file:
        py_source = py_file.read()

    with open(args.js_path, "rb") as js_file:
        js_source = js_file.read()

    if args.out is None:
        sys.stdout.buffer.write(combine(py_source, js_source))
    else:
        with open(args.out, "wb") as out_file:
            out_file.write(combine(py_source, js_source))

    py_name = os.path.basename(args.py_path)
    js_name = os.path.basename(args.js_path)

    if args.out is not None:
        print(f"Created {args.out} from {py_name} and {js_name}!", file=sys.stderr)

    return 0
