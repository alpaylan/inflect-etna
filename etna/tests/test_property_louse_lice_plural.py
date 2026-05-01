from __future__ import annotations

from hypothesis import given, settings

from etna_runner.properties import property_louse_lice_plural
from etna_runner.strategies import strategy_louse_lice_plural


@given(strategy_louse_lice_plural())
@settings(max_examples=50, deadline=None)
def test_property_louse_lice_plural(args) -> None:
    r = property_louse_lice_plural(args)
    assert r.kind != "fail", r.message
