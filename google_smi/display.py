from __future__ import annotations

import json
import time
from dataclasses import asdict

from google_smi.types import TpuSnapshot

# Column widths (inner content, excluding border chars)
# C1=41, C2=22, C3=22  →  total inner = 87, with borders = 89
_C1 = 37
_C2 = 26
_C3 = 22
_W = _C1 + _C2 + _C3 + 2  # +2 for the two inner `|` chars = 87
_D1 = 56
_D2 = 30
_DW = _D1 + _D2 + 1  # +1 for the inner `|` char = 87


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


def _detail_hline(c: str = "-") -> str:
    return f"+{c * _D1}+{c * _D2}+"


def _detail_header_sep() -> str:
    return f"|{'-' * _D1}+{'-' * _D2}|"


def _detail_eq_sep() -> str:
    return f"|{'=' * _D1}+{'=' * _D2}|"


def _detail_row(a: str, b: str) -> str:
    return f"| {a:<{_D1 - 1}s}| {b:<{_D2 - 1}s}|"


def _cell(content: str, width: int) -> str:
    """Pad or truncate content to exact width."""
    return content[:width].ljust(width)


def format_snapshot(snap: TpuSnapshot, *, show_detail: bool = False) -> str:
    lines: list[str] = []

    # Timestamp above the box
    lines.append(time.strftime("%a %b %d %H:%M:%S %Y"))

    # Header box
    lines.append(_full_hline())
    header = f"Google-SMI {snap.tool_version}"
    driver = f"Driver Version: {snap.driver_version}"
    libtpu = f"LIBTPU Version: {snap.libtpu_version}"
    mid = f"{header:<24}{driver}   {libtpu}"
    lines.append(_full_row(mid))

    if show_detail:
        lines.extend(_format_detail_table(snap))
    else:
        lines.extend(_format_default_table(snap))

    # Process table
    lines.append("")
    lines.append(_full_hline())
    lines.append(_full_row("Processes:"))
    lines.append(_full_row(
        "TPU         PID    Type      Process Name                         Memory Usage"
    ))
    lines.append(_full_eq_sep())

    if snap.processes:
        for proc in snap.processes:
            mem_str = f"{proc.memory_usage_mib}MiB"
            lines.append(_full_row(
                f"{proc.device_id:>3}     {proc.pid:>7}       "
                f"{proc.process_type}      {proc.process_name:<42}{mem_str:>7}"
            ))
    else:
        lines.append(_full_row("  No running processes found"))

    lines.append(_full_hline())

    return "\n".join(lines)


def format_json(snap: TpuSnapshot) -> str:
    return json.dumps(asdict(snap), indent=2)


def _format_default_table(snap: TpuSnapshot) -> list[str]:
    lines: list[str] = []
    lines.append(_col_hline())
    lines.append(_row(
        " TPU  Name               NUMA Node   ",
        "       Memory-Usage       ",
        "      TPU-Util        ",
    ))
    lines.append(_col_eq_sep())

    for dev in snap.devices:
        idx_name = f"   {dev.device_id}  {dev.chip_name}"
        numa = str(dev.numa_node)
        gap = _C1 - len(idx_name) - len(numa) - 3
        left = f"{idx_name}{' ' * max(gap, 1)}{numa}   "
        used = int(dev.hbm_used_mib)
        total = int(dev.hbm_total_mib)
        middle = f" {used:7d}MiB / {total:7d}MiB "
        right = f"{dev.duty_cycle_pct:.1f}%"
        lines.append(_row(
            _cell(left, _C1),
            _cell(middle, _C2),
            _cell(f"{right:>{_C3 - 8}}        ", _C3),
        ))
        lines.append(_col_hline())

    return lines


def _format_detail_table(snap: TpuSnapshot) -> list[str]:
    lines: list[str] = []
    has_pcie_info = any(
        (f"{device.pcie_gen} {device.pcie_width}".strip())
        for device in snap.devices
    )

    lines.append(_header_sep())
    lines.append(_row(
        "",
        " Bus-Id            IOMMU ",
        "          PCIe        " if has_pcie_info else "",
    ))
    lines.append(_row(
        " TPU  Name               NUMA Node   ",
        "       Memory-Usage      ",
        "      TPU-Util        ",
    ))
    lines.append(_col_eq_sep())

    for dev in snap.devices:
        used = int(dev.hbm_used_mib)
        total = int(dev.hbm_total_mib)

        idx_name = f"   {dev.device_id}  {dev.chip_name}"
        numa = str(dev.numa_node)
        gap1 = _C1 - len(idx_name) - len(numa) - 3
        c1r1 = f"{idx_name}{' ' * max(gap1, 1)}{numa}   "

        bus = dev.bus_id
        iommu = str(dev.iommu_group)
        gap2 = _C2 - 1 - len(bus) - len(iommu) - 2
        c2r1 = f" {bus}{' ' * max(gap2, 1)}{iommu}  "

        c1r1 = ""
        c1r2 = f"{idx_name}{' ' * max(gap1, 1)}{numa}   "
        c2r2 = f" {used:7d}MiB / {total:7d}MiB "
        pcie_text = f"{dev.pcie_gen} {dev.pcie_width}".strip() if has_pcie_info else ""
        c3r1 = f"{pcie_text:>{_C3 - 8}}        " if pcie_text else ""
        c3r2 = f"{dev.duty_cycle_pct:.1f}%"
        c3r2 = f"{c3r2:>{_C3 - 8}}        "

        lines.append(_row(_cell(c1r1, _C1), _cell(c2r1, _C2), _cell(c3r1, _C3)))
        lines.append(_row(_cell(c1r2, _C1), _cell(c2r2, _C2), _cell(c3r2, _C3)))
        lines.append(_col_hline())

    return lines
