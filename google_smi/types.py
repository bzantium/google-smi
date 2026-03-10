from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DeviceInfo:
    device_id: int
    chip_name: str
    bus_id: str
    hbm_used_mib: float | None = None
    hbm_total_mib: float | None = None
    duty_cycle_pct: float | None = None


@dataclass
class ProcessInfo:
    device_id: int
    pid: int
    process_name: str


@dataclass
class TpuSnapshot:
    tool_version: str
    libtpu_version: str
    chip_type_name: str
    num_chips: int
    devices: list[DeviceInfo] = field(default_factory=list)
    processes: list[ProcessInfo] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
