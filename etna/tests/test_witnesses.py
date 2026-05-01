"""Pytest collector for the workload's witnesses.

On the base tree, every witness must pass. The tests here run the witness
functions defined in `etna_runner.witnesses` and assert their PropertyResult
kind is "pass".
"""

from __future__ import annotations

import pytest

from etna_runner import witnesses

WITNESS_NAMES = sorted(n for n in dir(witnesses) if n.startswith("witness_"))


@pytest.mark.parametrize("name", WITNESS_NAMES)
def test_witness(name: str) -> None:
    fn = getattr(witnesses, name)
    r = fn()
    assert r.kind == "pass", f"{name}: {r.kind} - {r.message}"
