from __future__ import annotations

import importlib.metadata
from pathlib import Path

from google_smi import __version__
from google_smi.types import DeviceInfo, ProcessInfo, TpuSnapshot


def _get_libtpu_version() -> str:
    try:
        return importlib.metadata.version("libtpu")
    except importlib.metadata.PackageNotFoundError:
        return "N/A"


def _get_process_name(pid: int) -> str:
    try:
        return Path(f"/proc/{pid}/comm").read_text().strip()
    except (FileNotFoundError, PermissionError):
        return "unknown"


def collect_snapshot() -> TpuSnapshot:
    from tpu_info.device import get_local_chips, get_actual_chips, get_chip_owners, chip_path
    from tpu_info.metrics import get_chip_usage

    chip_type, num_chips = get_local_chips()
    if chip_type is None or num_chips == 0:
        return TpuSnapshot(
            tool_version=__version__,
            libtpu_version=_get_libtpu_version(),
            chip_type_name="N/A",
            num_chips=0,
            warnings=["No TPU devices found"],
        )

    chip_type_name = chip_type.value.name
    chips = get_actual_chips()

    hbm_total_mib = chip_type.value.hbm_gib * 1024

    # Try gRPC metrics first
    warnings: list[str] = []
    usages: list | None = None
    try:
        usages = get_chip_usage(chip_type)
    except Exception:
        pass  # runtime not active — default to 0

    # Build device list from PCI info + metrics
    devices: list[DeviceInfo] = []
    for i, chip in enumerate(chips):
        if usages is not None and i < len(usages):
            used = usages[i].memory_usage / (1024 * 1024)
            duty = usages[i].duty_cycle_pct
        else:
            used = 0.0
            duty = 0.0
        devices.append(DeviceInfo(
            device_id=i,
            chip_name=f"TPU {chip_type_name}",
            bus_id=chip.base_addr,
            hbm_used_mib=used,
            hbm_total_mib=hbm_total_mib,
            duty_cycle_pct=duty,
        ))

    # Process mapping
    processes: list[ProcessInfo] = []
    try:
        owners = get_chip_owners()
        for i in range(num_chips):
            path = chip_path(chip_type, i)
            pid = owners.get(path)
            if pid is not None:
                processes.append(ProcessInfo(
                    device_id=i,
                    pid=pid,
                    process_name=_get_process_name(pid),
                ))
    except Exception:
        pass  # empty process table on failure

    return TpuSnapshot(
        tool_version=__version__,
        libtpu_version=_get_libtpu_version(),
        chip_type_name=chip_type_name,
        num_chips=num_chips,
        devices=devices,
        processes=processes,
        warnings=warnings,
    )
