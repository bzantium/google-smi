from __future__ import annotations

import glob
import importlib.metadata
import itertools
import os
import re
from pathlib import Path
from typing import Optional

import grpc

from google_smi import __version__
from google_smi.proto import tpu_metric_service_pb2 as tpu_metrics
from google_smi.proto import tpu_metric_service_pb2_grpc as tpu_metrics_grpc
from google_smi.types import (
    GOOGLE_PCI_VENDOR_ID,
    DeviceInfo,
    ProcessInfo,
    TpuChip,
    TpuSnapshot,
)


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


def _scan_pci_devices() -> tuple[Optional[TpuChip], list[dict]]:
    """Scan sysfs for Google TPU PCI devices.

    Returns (chip_type, list_of_device_dicts) where each dict has keys:
    base_addr, full_addr, core_index, device_id, subsystem_id,
    numa_node, iommu_group, vfio_path.
    """
    devices_by_base: dict[str, list[dict]] = {}
    chip_type: Optional[TpuChip] = None

    for device_path in glob.glob("/sys/bus/pci/devices/*"):
        try:
            pci_addr = os.path.basename(device_path)
            vendor_id = Path(os.path.join(device_path, "vendor")).read_text().strip()
            if vendor_id != GOOGLE_PCI_VENDOR_ID:
                continue

            iommu_group_path = os.path.join(device_path, "iommu_group")
            if not os.path.islink(iommu_group_path):
                continue

            iommu_group = int(os.path.basename(os.readlink(iommu_group_path)))
            device_id = Path(os.path.join(device_path, "device")).read_text().strip()
            subsystem_id = Path(os.path.join(device_path, "subsystem_device")).read_text().strip()

            try:
                numa_node = int(Path(os.path.join(device_path, "numa_node")).read_text().strip())
                if numa_node < 0:
                    numa_node = 0
            except (FileNotFoundError, ValueError):
                numa_node = 0

            ct = TpuChip.from_pci_ids(device_id, subsystem_id)
            if ct is not None:
                chip_type = ct

            pci_base = pci_addr.split(".")[0]
            core_index = int(pci_addr.split(".")[-1])

            info = {
                "base_addr": pci_base,
                "full_addr": pci_addr,
                "core_index": core_index,
                "device_id": device_id,
                "subsystem_id": subsystem_id,
                "numa_node": numa_node,
                "iommu_group": iommu_group,
                "vfio_path": f"/dev/vfio/{iommu_group}",
            }
            devices_by_base.setdefault(pci_base, []).append(info)
        except (IOError, ValueError):
            continue

    # Sort each group by core_index, then sort groups by vfio_path of core 0
    chips: list[dict] = []
    for base_addr in sorted(devices_by_base, key=lambda b: _sort_key(devices_by_base[b])):
        cores = sorted(devices_by_base[base_addr], key=lambda c: c["core_index"])
        # Use the first core's info as representative
        chips.append(cores[0])

    return chip_type, chips


def _sort_key(cores: list[dict]) -> str:
    for c in cores:
        if c["core_index"] == 0:
            return c["vfio_path"]
    return cores[0]["vfio_path"] if cores else ""


def _get_grpc_metrics(
    chip_type: TpuChip, addr: str = "localhost:8431"
) -> Optional[list[dict]]:
    """Fetch memory and duty cycle metrics via gRPC. Returns None on failure."""
    try:
        channel = grpc.secure_channel(addr, grpc.local_channel_credentials())
        client = tpu_metrics_grpc.RuntimeMetricServiceStub(channel)

        def sorted_metric(name: str):
            resp = client.GetRuntimeMetric(
                tpu_metrics.MetricRequest(metric_name=name),
                timeout=2,
            )
            return sorted(resp.metric.metrics, key=lambda m: m.attribute.value.int_attr)

        totals = sorted_metric("tpu.runtime.hbm.memory.total.bytes")
        usages = sorted_metric("tpu.runtime.hbm.memory.usage.bytes")
        duty_cycle = sorted_metric("tpu.runtime.tensorcore.dutycycle.percent")

        # Expand duty cycle for multi-device-per-chip types
        duty_expanded = list(
            itertools.chain.from_iterable(
                itertools.repeat(d, chip_type.value.devices_per_chip)
                for d in duty_cycle
            )
        )

        if not (len(totals) == len(usages) == len(duty_expanded)):
            return None

        results = []
        for u, t, d in zip(usages, totals, duty_expanded):
            results.append({
                "memory_usage": u.gauge.as_int,
                "total_memory": t.gauge.as_int,
                "duty_cycle_pct": d.gauge.as_double,
            })
        return results
    except Exception:
        return None


def _get_chip_owners() -> dict[str, int]:
    """Scan /proc/*/fd/* for symlinks to /dev/accel* or /dev/vfio/*."""
    device_owners: dict[str, int] = {}
    for link in glob.glob("/proc/*/fd/*"):
        try:
            target = os.readlink(link)
        except (FileNotFoundError, PermissionError):
            continue
        if re.fullmatch(r"/dev/(?:accel|vfio/)\d+", target):
            match = re.fullmatch(r"/proc/(\d+)/fd/\d+", link)
            if match:
                device_owners[target] = int(match.group(1))
    return device_owners


def _chip_device_path(chip_type: TpuChip, index: int) -> str:
    if chip_type in {TpuChip.V5E, TpuChip.V5P, TpuChip.V6E, TpuChip.V7X}:
        return f"/dev/vfio/{index}"
    else:
        return f"/dev/accel{index}"


def collect_snapshot() -> TpuSnapshot:
    chip_type, pci_devices = _scan_pci_devices()

    if chip_type is None or len(pci_devices) == 0:
        return TpuSnapshot(
            tool_version=__version__,
            libtpu_version=_get_libtpu_version(),
            chip_type_name="N/A",
            num_chips=0,
        )

    chip_type_name = chip_type.value.name
    hbm_total_mib = chip_type.value.hbm_gib * 1024
    num_chips = len(pci_devices)

    # Try gRPC metrics
    grpc_metrics = _get_grpc_metrics(chip_type)

    # Build device list
    devices: list[DeviceInfo] = []
    for i, pci in enumerate(pci_devices):
        if grpc_metrics is not None and i < len(grpc_metrics):
            used = grpc_metrics[i]["memory_usage"] / (1024 * 1024)
            total = grpc_metrics[i]["total_memory"] / (1024 * 1024)
            duty = grpc_metrics[i]["duty_cycle_pct"]
        else:
            used = 0.0
            total = hbm_total_mib
            duty = 0.0

        # Strip leading 0x from PCI IDs for display
        dev_id_hex = pci["device_id"].replace("0x", "")
        sub_id_hex = pci["subsystem_id"].replace("0x", "")

        devices.append(DeviceInfo(
            device_id=i,
            chip_name=f"TPU {chip_type_name}",
            bus_id=pci["full_addr"],
            numa_node=pci["numa_node"],
            iommu_group=pci["iommu_group"],
            pci_device_id=dev_id_hex,
            pci_subsystem_id=sub_id_hex,
            hbm_used_mib=used,
            hbm_total_mib=total,
            duty_cycle_pct=duty,
            tc_util_pct=duty,
        ))

    # Process mapping
    processes: list[ProcessInfo] = []
    try:
        owners = _get_chip_owners()
        for i in range(num_chips):
            path = _chip_device_path(chip_type, i)
            pid = owners.get(path)
            if pid is not None:
                processes.append(ProcessInfo(
                    device_id=i,
                    pid=pid,
                    process_name=_get_process_name(pid),
                ))
    except Exception:
        pass

    # Detect driver
    driver_version = "vfio-pci"
    if pci_devices:
        driver_link = f"/sys/bus/pci/devices/{pci_devices[0]['full_addr']}/driver"
        try:
            driver_version = os.path.basename(os.readlink(driver_link))
        except (FileNotFoundError, OSError):
            pass

    return TpuSnapshot(
        tool_version=__version__,
        libtpu_version=_get_libtpu_version(),
        chip_type_name=chip_type_name,
        num_chips=num_chips,
        driver_version=driver_version,
        devices=devices,
        processes=processes,
    )
