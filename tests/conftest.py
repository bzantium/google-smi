from __future__ import annotations

import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from google_smi.types import DeviceInfo, ProcessInfo, TpuSnapshot


@pytest.fixture
def sample_snapshot() -> TpuSnapshot:
    return TpuSnapshot(
        tool_version="0.1.0",
        libtpu_version="0.0.17",
        chip_type_name="v6e",
        num_chips=2,
        driver_version="vfio-pci",
        devices=[
            DeviceInfo(
                device_id=0,
                chip_name="TPU v6e",
                bus_id="0000:00:04.0",
                numa_node=0,
                iommu_group=0,
                pcie_gen="Gen5",
                pcie_width="x16",
                hbm_used_mib=5120,
                hbm_total_mib=32768,
                duty_cycle_pct=23.4,
            ),
            DeviceInfo(
                device_id=1,
                chip_name="TPU v6e",
                bus_id="0000:00:05.0",
                numa_node=0,
                iommu_group=1,
                pcie_gen="Gen5",
                pcie_width="x16",
                hbm_used_mib=12048,
                hbm_total_mib=32768,
                duty_cycle_pct=78.2,
            ),
        ],
        processes=[
            ProcessInfo(
                device_id=0,
                pid=12345,
                process_name="python3",
                memory_usage_mib=5120,
            ),
            ProcessInfo(
                device_id=1,
                pid=67890,
                process_name="jax_worker",
                memory_usage_mib=12048,
            ),
        ],
    )
