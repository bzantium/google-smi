from __future__ import annotations

import json
import time
from dataclasses import asdict

from google_smi.types import TpuSnapshot

# Column widths (inner content, excluding border chars)
# C1=41, C2=22, C3=22  →  total inner = 87, with borders = 89
_C1 = 41
_C2 = 22
_C3 = 22
_W = _C1 + _C2 + _C3 + 2  # +2 for the two inner `|` chars = 87


def _full_hline(c: str = "-") -> str:
    return f"+{c * _W}+"


def _col_hline(c: str = "-") -> str:
    return f"+{c * _C1}+{c * _C2}+{c * _C3}+"


def _header_sep() -> str:
    return f"|{'-' * _C1}+{'-' * _C2}+{'-' * _C3}|"


def _full_eq_sep() -> str:
    return f"|{'=' * _W}|"


def _col_eq_sep() -> str:
    return f"|{'=' * _C1}+{'=' * _C2}+{'=' * _C3}|"


def _full_row(text: str) -> str:
    return f"| {text:<{_W - 1}}|"


def _row(a: str, b: str, c: str) -> str:
    return f"|{a:<{_C1}s}|{b:<{_C2}s}|{c:<{_C3}s}|"


def _cell(content: str, width: int) -> str:
    """Pad or truncate content to exact width."""
    return content[:width].ljust(width)


def format_snapshot(snap: TpuSnapshot) -> str:
    lines: list[str] = []

    # Timestamp above the box
    lines.append(time.strftime("%a %b %d %H:%M:%S %Y"))

    # Header box
    lines.append(_full_hline())
    header = f"Google-SMI {snap.tool_version}"
    driver = f"Driver: {snap.driver_version}"
    libtpu = f"libtpu Version: {snap.libtpu_version}"
    mid = f"{header:<30}{driver:<17}{libtpu}"
    lines.append(_full_row(mid))

    # Column header separator (nvidia-smi style with outer |)
    lines.append(_header_sep())

    # Column headers
    lines.append(_row(
        " TPU  Name                   NUMA Node",
        " Bus-Id         IOMMU",
        " Device / Subsystem  ",
    ))
    lines.append(_row(
        " Duty Cycle",
        "     Memory-Usage    ",
        "                     ",
    ))
    lines.append(_col_eq_sep())

    # Per-device rows
    for dev in snap.devices:
        used = int(dev.hbm_used_mib)
        total = int(dev.hbm_total_mib)

        # Build C1 row 1: "   {id}  {name}...{numa}   "
        idx_name = f"   {dev.device_id}  {dev.chip_name}"
        numa = str(dev.numa_node)
        gap1 = _C1 - len(idx_name) - len(numa) - 3
        c1r1 = f"{idx_name}{' ' * max(gap1, 1)}{numa}   "

        # Build C2 row 1: " {bus_id}...{iommu} "
        bus = dev.bus_id
        iommu = str(dev.iommu_group)
        gap2 = _C2 - 1 - len(bus) - len(iommu) - 1
        c2r1 = f" {bus}{' ' * max(gap2, 1)}{iommu} "

        # Build C3 row 1: "         {dev_id} / {sub_id}  "
        dev_sub = f"{dev.pci_device_id:>4s} / {dev.pci_subsystem_id:<4s}"
        c3r1 = f"         {dev_sub}  "

        # Build C1 row 2: "      {duty}..."
        duty_str = f"{dev.duty_cycle_pct:5.1f}%"
        c1r2 = f"      {duty_str}"

        # Build C2 row 2: right-aligned memory
        mem_content = f"{used}MiB / {total}MiB"
        c2r2 = f"{mem_content:>{_C2 - 2}}  "

        # Build C3 row 2: empty
        c3r2 = " " * _C3

        lines.append(_row(_cell(c1r1, _C1), _cell(c2r1, _C2), _cell(c3r1, _C3)))
        lines.append(_row(_cell(c1r2, _C1), _cell(c2r2, _C2), c3r2))
        lines.append(_col_hline())

    # Process table
    lines.append("")
    lines.append(_full_hline())
    lines.append(_full_row("Processes:"))
    lines.append(_full_row(
        " TPU        PID   Type   Process name                             Memory Usage       "
    ))
    lines.append(_full_eq_sep())

    if snap.processes:
        for proc in snap.processes:
            mem_str = f"{proc.memory_usage_mib}MiB"
            lines.append(_full_row(
                f"  {proc.device_id:<6}    {proc.pid:<6} {proc.process_type:<6} "
                f"{proc.process_name:<40s} {mem_str}"
            ))
    else:
        lines.append(_full_row(" No running processes found"))

    lines.append(_full_hline())

    return "\n".join(lines)


def format_json(snap: TpuSnapshot) -> str:
    return json.dumps(asdict(snap), indent=2)
