from __future__ import annotations

import argparse
import sys

from google_smi import __version__
from google_smi.collector import collect_snapshot
from google_smi.display import format_snapshot, format_json


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="google-smi",
        description="nvidia-smi-style TPU monitor",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="output in JSON format",
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"google-smi {__version__}",
    )
    args = parser.parse_args()

    snap = collect_snapshot()
    if snap.num_chips == 0:
        print("No TPU devices found.", file=sys.stderr)
        sys.exit(1)
    if args.json:
        print(format_json(snap))
    else:
        print(format_snapshot(snap))
