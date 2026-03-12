from __future__ import annotations

import json

from google_smi.display import format_json, format_snapshot


def test_format_snapshot_renders_devices_and_processes(sample_snapshot, monkeypatch):
    monkeypatch.setattr("google_smi.display.time.strftime", lambda fmt: "Thu Mar 12 01:44:36 2026")

    output = format_snapshot(sample_snapshot)

    assert "Google-SMI 0.1.0" in output
    assert "0000:00:04.0" in output
    assert "5120MiB /   32768MiB" in output
    assert "23.4%" in output
    assert "python3" in output
    assert "jax_worker" in output
    assert "Pwr:Usage/Cap" not in output


def test_format_json_contains_snapshot_payload(sample_snapshot):
    payload = json.loads(format_json(sample_snapshot))

    assert payload["chip_type_name"] == "v6e"
    assert payload["devices"][0]["device_id"] == 0
    assert payload["processes"][1]["process_name"] == "jax_worker"
