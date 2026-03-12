from __future__ import annotations

import json

from google_smi.display import format_json, format_snapshot


def test_format_snapshot_renders_devices_and_processes(sample_snapshot, monkeypatch):
    monkeypatch.setattr("google_smi.display.time.strftime", lambda fmt: "Thu Mar 12 01:44:36 2026")

    output = format_snapshot(sample_snapshot)
    header_line = next(line for line in output.splitlines() if "Memory-Usage" in line)

    assert "Google-SMI 0.1.0" in output
    assert "Memory-Usage" in output
    assert "| TPU  Name" in header_line
    assert "|       Memory-Usage" in header_line
    assert "|      TPU-Util" in header_line
    assert "|    5120MiB /   32768MiB  |" in output
    assert "23.4%" in output
    assert "python3" in output
    assert "jax_worker" in output
    assert "Pwr:Usage/Cap" not in output
    assert "Bus-Id" not in output
    assert "0000:00:04.0" not in output


def test_format_snapshot_detail_renders_bus_and_pcie(sample_snapshot, monkeypatch):
    monkeypatch.setattr("google_smi.display.time.strftime", lambda fmt: "Thu Mar 12 01:44:36 2026")

    output = format_snapshot(sample_snapshot, show_detail=True)
    lines = output.splitlines()
    bus_header = next(line for line in lines if "Bus-Id" in line)
    metric_header = next(line for line in lines if "Memory-Usage" in line)
    first_bus_row = next(line for line in lines if "0000:00:04.0" in line)
    first_metric_row = next(line for line in lines if "5120MiB" in line)

    assert "Bus-Id" in output
    assert "0000:00:04.0" in output
    assert "PCIe" in output
    assert "TPU  Name" not in bus_header
    assert "TPU  Name" in metric_header
    assert "TPU v6e" not in first_bus_row
    assert "TPU v6e" in first_metric_row


def test_format_json_contains_snapshot_payload(sample_snapshot):
    payload = json.loads(format_json(sample_snapshot))

    assert payload["chip_type_name"] == "v6e"
    assert payload["devices"][0]["device_id"] == 0
    assert payload["processes"][1]["process_name"] == "jax_worker"


def test_format_snapshot_hides_unavailable_pcie(sample_snapshot, monkeypatch):
    monkeypatch.setattr("google_smi.display.time.strftime", lambda fmt: "Thu Mar 12 01:44:36 2026")
    for device in sample_snapshot.devices:
        device.pcie_gen = ""
        device.pcie_width = ""

    output = format_snapshot(sample_snapshot, show_detail=True)

    assert "PCIe" not in output
    target_line = next(line for line in output.splitlines() if "0000:00:04.0" in line)
    assert "x0" not in target_line
    assert "Gen" not in target_line
