from __future__ import annotations

from google_smi.collector import _parse_pcie_gen, _parse_pcie_width


def test_parse_pcie_gen_rejects_unknown_placeholder():
    assert _parse_pcie_gen("Unknown") == ""


def test_parse_pcie_width_rejects_zero_and_255_placeholders():
    assert _parse_pcie_width("0") == ""
    assert _parse_pcie_width("255") == ""


def test_parse_pcie_width_formats_real_width():
    assert _parse_pcie_width("16") == "x16"
