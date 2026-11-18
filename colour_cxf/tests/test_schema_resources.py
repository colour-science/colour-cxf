"""Verify that schema validation works outside a source checkout."""

from pathlib import Path

import pytest

from colour_cxf import read_cxf
from colour_cxf.cxf3 import CxF


def test_schema_validation_outside_checkout(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Read a valid document without relying on the current directory."""
    document = (Path(__file__).parent / "resources" / "minimal_cxf.cxf").read_bytes()
    monkeypatch.chdir(tmp_path)
    assert isinstance(read_cxf(document), CxF)
