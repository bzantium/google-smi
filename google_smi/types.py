from __future__ import annotations

import enum
import sys
import typing
from dataclasses import dataclass, field
from typing import Literal, Optional

_T = typing.TypeVar("_T")
_identity = lambda item: item
nonmember = enum.nonmember if sys.version_info >= (3, 11) else _identity

GOOGLE_PCI_VENDOR_ID = "0x1ae0"


class TpuChip(enum.Enum):
    @nonmember
    class Info(typing.NamedTuple):
        name: str
        hbm_gib: int
        devices_per_chip: Literal[1, 2]

    V2 = Info("v2", hbm_gib=8, devices_per_chip=2)
    V3 = Info("v3", hbm_gib=16, devices_per_chip=2)
    V4 = Info("v4", hbm_gib=32, devices_per_chip=1)
    V5E = Info("v5e", hbm_gib=16, devices_per_chip=1)
    V5P = Info("v5p", hbm_gib=95, devices_per_chip=1)
    V6E = Info("v6e", hbm_gib=32, devices_per_chip=1)
    V7X = Info("7x", hbm_gib=192, devices_per_chip=2)

    @classmethod
    def from_pci_ids(cls, device_id: str, subsystem_id: str) -> Optional[TpuChip]:
        if device_id == "0x0027":
            if subsystem_id == "0x004e":
                return cls.V2
            elif subsystem_id == "0x004f":
                return cls.V3
        return {
            "0x005e": cls.V4,
            "0x0063": cls.V5E,
            "0x0062": cls.V5P,
            "0x006f": cls.V6E,
            "0x0076": cls.V7X,
        }.get(device_id)


@dataclass
class DeviceInfo:
    device_id: int
    chip_name: str
    bus_id: str
    numa_node: int = 0
    iommu_group: int = 0
    pci_device_id: str = ""
    pci_subsystem_id: str = ""
    pcie_gen: str = ""
    pcie_width: str = ""
    power_draw_w: float = 0.0
    power_cap_w: float = 0.0
    hbm_used_mib: float = 0.0
    hbm_total_mib: float = 0.0
    duty_cycle_pct: float = 0.0


@dataclass
class ProcessInfo:
    device_id: int
    pid: int
    process_name: str
    process_type: str = "C"
    memory_usage_mib: int = 0


@dataclass
class TpuSnapshot:
    tool_version: str
    libtpu_version: str
    chip_type_name: str
    num_chips: int
    driver_version: str = "vfio-pci"
    devices: list[DeviceInfo] = field(default_factory=list)
    processes: list[ProcessInfo] = field(default_factory=list)
