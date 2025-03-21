"""JsPyr - combines Python and JavaScript programs into a single file."""

from __future__ import annotations


def combine(py_source: bytes, js_source: bytes) -> bytes:
    """Combines Python and JavaScript programs into a single file."""
    return (
        b"1 // 1; '''\n"
        + js_source.replace(b"'''", rb"\'\'\'")
        + b"\n/*'''\n"
        + py_source
        + b"\n#*/\n"
    )
