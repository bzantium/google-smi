from __future__ import annotations

import json

import pytest

from google_smi import cli


def test_cli_json_output(monkeypatch, capsys, sample_snapshot):
    monkeypatch.setattr(cli, "collect_snapshot", lambda: sample_snapshot)

    with pytest.raises(SystemExit) as exc:
        cli.main(["--json"])
    captured = capsys.readouterr()

    assert exc.value.code == 0
    payload = json.loads(captured.out)
    assert payload["num_chips"] == 2


def test_cli_text_output(monkeypatch, capsys, sample_snapshot):
    monkeypatch.setattr(cli, "collect_snapshot", lambda: sample_snapshot)

    with pytest.raises(SystemExit) as exc:
        cli.main([])
    captured = capsys.readouterr()

    assert exc.value.code == 0
    assert "Google-SMI 0.1.0" in captured.out
    assert "python3" in captured.out
    assert "Bus-Id" not in captured.out


def test_cli_detail_output(monkeypatch, capsys, sample_snapshot):
    monkeypatch.setattr(cli, "collect_snapshot", lambda: sample_snapshot)

    with pytest.raises(SystemExit) as exc:
        cli.main(["--detail"])
    captured = capsys.readouterr()

    assert exc.value.code == 0
    assert "Bus-Id" in captured.out
    assert "0000:00:04.0" in captured.out


def test_cli_rejects_json_watch(monkeypatch, sample_snapshot):
    monkeypatch.setattr(cli, "collect_snapshot", lambda: sample_snapshot)

    with pytest.raises(SystemExit):
        cli.main(["--json", "-i", "1"])


def test_cli_no_devices_returns_error(monkeypatch, capsys, sample_snapshot):
    sample_snapshot.num_chips = 0
    monkeypatch.setattr(cli, "collect_snapshot", lambda: sample_snapshot)

    with pytest.raises(SystemExit) as exc:
        cli.main([])
    captured = capsys.readouterr()

    assert exc.value.code == 1
    assert "No TPU devices found." in captured.err


def test_watch_returns_zero_on_keyboard_interrupt(monkeypatch):
    monkeypatch.setattr(cli, "_render", lambda as_json=False, show_detail=False: 0)
    monkeypatch.setattr(cli.time, "sleep", lambda _: (_ for _ in ()).throw(KeyboardInterrupt()))
    monkeypatch.setattr(cli.sys.stdout, "isatty", lambda: False, raising=False)

    assert cli._watch(0.1, show_detail=False) == 0
