"""Support executing the CLI by doing `python -m jspyr`."""
from __future__ import annotations

from jspyr.cli import cli

if __name__ == "__main__":
    raise SystemExit(cli())
