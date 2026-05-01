from __future__ import annotations

from hypothesis import given, settings

from etna_runner.properties import property_plural_shoe_returns_shoes
from etna_runner.strategies import strategy_plural_shoe_returns_shoes


@given(strategy_plural_shoe_returns_shoes())
@settings(max_examples=50, deadline=None)
def test_property_plural_shoe_returns_shoes(args) -> None:
    r = property_plural_shoe_returns_shoes(args)
    assert r.kind != "fail", r.message
