from __future__ import annotations

import json
from dataclasses import asdict

from google_smi.types import TpuSnapshot

# Column widths (inner content, excluding border chars)
_C1 = 31   # TPU / Chip / Duty Cycle
_C2 = 24   # Bus-Id / Temp / Pwr
_C3 = 26   # HBM-Memory-Usage
_TOTAL = _C1 + _C2 + _C3 + 4  # +4 for the 3 inner `|` chars and adjustment


def _hline(c: str = "-", sep: str = "+") -> str:
    return f"{sep}{c * _C1}{sep}{c * _C2}{sep}{c * _C3}{sep}"


def _full_hline(c: str = "-") -> str:
    w = _C1 + _C2 + _C3 + 2  # +2 for the two inner `|` replaced by `-`
    return f"+{c * w}+"


def _row(a: str, b: str, c: str) -> str:
    return f"|{a:<{_C1}}|{b:<{_C2}}|{c:>{_C3}}|"


def _full_row(text: str) -> str:
    w = _C1 + _C2 + _C3 + 2
    return f"| {text:<{w - 1}}|"


def format_snapshot(snap: TpuSnapshot) -> str:
    lines: list[str] = []

    # Header
    lines.append(_full_hline())
    header = f"Google-SMI {snap.tool_version}                    libtpu: {snap.libtpu_version}          TPU Type: {snap.chip_type_name}"
    lines.append(_full_row(header))

    # Column headers
    lines.append(_hline())
    lines.append(_row(
        " TPU  Chip",
        " Bus-Id",
        "       HBM-Memory-Usage   ",
    ))
    lines.append(_row(
        "  Duty Cycle    TC Util",
        "      Temp    Pwr Usage",
        "",
    ))
    lines.append(f"|{'=' * _C1}+{'=' * _C2}+{'=' * _C3}|")

    # Per-device rows
    for dev in snap.devices:
        # Memory string
        mem = f"{int(dev.hbm_used_mib)}MiB / {int(dev.hbm_total_mib)}MiB"
        mem_str = f"    {mem}     "

        # Duty cycle string
        duty = f"{dev.duty_cycle_pct:.2f}%"

        # Row 1: device id, chip name, bus id, memory
        lines.append(_row(
            f"   {dev.device_id}  {dev.chip_name}",
            f" {dev.bus_id}",
            mem_str,
        ))
        # Row 2: duty cycle, TC util, temp, power
        lines.append(_row(
            f"       {duty}    N/A",
            "      N/A      N/A",
            "",
        ))
        lines.append(_hline())

    # Warnings
    for w in snap.warnings:
        lines.append(_full_row(f"WARNING: {w}"))

    # Process table
    lines.append(_full_hline())
    lines.append(_full_row("Processes:"))
    lines.append(_full_row(" TPU        PID   Process name"))
    lines.append(f"|{'=' * (_C1 + _C2 + _C3 + 2)}|")

    if snap.processes:
        for proc in snap.processes:
            lines.append(_full_row(
                f"   {proc.device_id:<6} {proc.pid:<8} {proc.process_name}"
            ))
    else:
        lines.append(_full_row("  No running processes found"))

    lines.append(_full_hline())

    return "\n".join(lines)


def format_json(snap: TpuSnapshot) -> str:
    return json.dumps(asdict(snap), indent=2)
