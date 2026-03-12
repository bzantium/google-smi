from __future__ import annotations

import json
from io import StringIO

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


def test_write_tty_frame_clears_stale_line_content(monkeypatch):
    buf = StringIO()

    monkeypatch.setattr(cli, "_move_cursor_home", lambda: buf.write("\033[H"))
    monkeypatch.setattr(cli, "_clear_to_end", lambda: buf.write("\033[J"))
    monkeypatch.setattr(cli.sys, "stdout", buf)

    line_count = cli._write_tty_frame(
        "header\nrow pid(5758M) train.py(5758M)\n",
        previous_line_count=0,
    )
    line_count = cli._write_tty_frame(
        "header\nrow idle\n",
        previous_line_count=line_count,
    )

    output = buf.getvalue()
    assert line_count == 2
    assert "\033[2Krow idle\n" in output
    assert "idle5758M) train.py(5758M)" not in output


def test_watch_returns_zero_on_keyboard_interrupt(monkeypatch):
    monkeypatch.setattr(cli, "_render", lambda as_json=False, show_detail=False: 0)
    monkeypatch.setattr(cli.time, "sleep", lambda _: (_ for _ in ()).throw(KeyboardInterrupt()))
    monkeypatch.setattr(cli.sys.stdout, "isatty", lambda: False, raising=False)

    assert cli._watch(0.1, show_detail=False) == 0
