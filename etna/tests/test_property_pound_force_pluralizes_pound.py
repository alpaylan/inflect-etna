from __future__ import annotations

from hypothesis import given, settings

from etna_runner.properties import property_pound_force_pluralizes_pound
from etna_runner.strategies import strategy_pound_force_pluralizes_pound


@given(strategy_pound_force_pluralizes_pound())
@settings(max_examples=50, deadline=None)
def test_property_pound_force_pluralizes_pound(args) -> None:
    r = property_pound_force_pluralizes_pound(args)
    assert r.kind != "fail", r.message
