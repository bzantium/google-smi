from __future__ import annotations

import argparse
import sys
import time
from io import StringIO

from google_smi import __version__
from google_smi.collector import collect_snapshot
from google_smi.display import format_snapshot, format_json


def _move_cursor_home() -> None:
    sys.stdout.write("\033[H")


def _clear_screen() -> None:
    sys.stdout.write("\033[H\033[J")


def _clear_to_end() -> None:
    sys.stdout.write("\033[J")


def _hide_cursor() -> None:
    sys.stdout.write("\033[?25l")


def _show_cursor() -> None:
    sys.stdout.write("\033[?25h")


def _render(*, as_json: bool, show_detail: bool) -> int:
    snap = collect_snapshot()
    if snap.num_chips == 0:
        print("No TPU devices found.", file=sys.stderr)
        return 1
    if as_json:
        print(format_json(snap))
    else:
        print(format_snapshot(snap, show_detail=show_detail))
    return 0


def _render_frame(*, show_detail: bool) -> tuple[int, str]:
    snap = collect_snapshot()
    if snap.num_chips == 0:
        return 1, ""
    buf = StringIO()
    buf.write(format_snapshot(snap, show_detail=show_detail))
    buf.write("\n")
    return 0, buf.getvalue()


def _write_tty_frame(frame: str, previous_line_count: int) -> int:
    lines = frame.splitlines()
    _move_cursor_home()
    for line in lines:
        sys.stdout.write("\033[2K")
        sys.stdout.write(line)
        sys.stdout.write("\n")
    for _ in range(max(0, previous_line_count - len(lines))):
        sys.stdout.write("\033[2K\n")
    _clear_to_end()
    return len(lines)


def _watch(interval: float, *, show_detail: bool) -> int:
    is_tty = bool(getattr(sys.stdout, "isatty", lambda: False)())
    previous_line_count = 0
    try:
        if is_tty:
            _clear_screen()
            _hide_cursor()
        while True:
            if is_tty:
                exit_code, frame = _render_frame(show_detail=show_detail)
                if exit_code != 0:
                    print("No TPU devices found.", file=sys.stderr)
                    return exit_code
                previous_line_count = _write_tty_frame(frame, previous_line_count)
            else:
                exit_code = _render(as_json=False, show_detail=show_detail)
                if exit_code != 0:
                    return exit_code
            sys.stdout.flush()
            time.sleep(interval)
    except KeyboardInterrupt:
        return 0
    finally:
        if is_tty:
            _show_cursor()
            sys.stdout.flush()


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv[1:]
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
        "-d", "--detail",
        action="store_true",
        help="show bus and IOMMU detail columns; include PCIe when available",
    )
    parser.add_argument(
        "-i", "--interval", "--watch",
        nargs="?",
        type=float,
        default=0,
        help="refresh continuously with the given interval in seconds",
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"google-smi {__version__}",
    )
    args = parser.parse_args(argv)
    if args.interval is None:
        args.interval = 1.0
    if args.interval and args.interval > 0:
        if args.json:
            parser.error("--json and --interval/-i cannot be used together")
        sys.exit(_watch(max(0.1, args.interval), show_detail=args.detail))
    sys.exit(_render(as_json=args.json, show_detail=args.detail))
