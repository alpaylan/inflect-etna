from __future__ import annotations

from hypothesis import given, settings

from etna_runner.properties import property_ordinal_accepts_numeric
from etna_runner.strategies import strategy_ordinal_accepts_numeric


@given(strategy_ordinal_accepts_numeric())
@settings(max_examples=50, deadline=None)
def test_property_ordinal_accepts_numeric(args) -> None:
    r = property_ordinal_accepts_numeric(args)
    assert r.kind != "fail", r.message
