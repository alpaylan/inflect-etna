from __future__ import annotations

from hypothesis import given, settings

from etna_runner.properties import property_plural_apostrophe_no_crash
from etna_runner.strategies import strategy_plural_apostrophe_no_crash


@given(strategy_plural_apostrophe_no_crash())
@settings(max_examples=50, deadline=None)
def test_property_plural_apostrophe_no_crash(args) -> None:
    r = property_plural_apostrophe_no_crash(args)
    assert r.kind != "fail", r.message
