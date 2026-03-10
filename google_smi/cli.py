from __future__ import annotations

import argparse
import sys
import time

from google_smi import __version__
from google_smi.collector import collect_snapshot
from google_smi.display import format_snapshot, format_json


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="google-smi",
        description="nvidia-smi-style TPU monitor",
    )
    parser.add_argument(
        "-l", "--loop",
        type=float,
        nargs="?",
        const=1,
        default=None,
        metavar="N",
        help="refresh every N seconds (default: 1)",
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

    def _run_once() -> int:
        snap = collect_snapshot()
        if snap.num_chips == 0:
            print("No TPU devices found.", file=sys.stderr)
            return 1
        if args.json:
            print(format_json(snap))
        else:
            print(format_snapshot(snap))
        return 0

    if args.loop is not None:
        try:
            while True:
                sys.stdout.write("\033[2J\033[H")
                sys.stdout.flush()
                _run_once()
                time.sleep(args.loop)
        except KeyboardInterrupt:
            pass
    else:
        sys.exit(_run_once())
