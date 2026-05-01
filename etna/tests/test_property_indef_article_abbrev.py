from __future__ import annotations

from hypothesis import given, settings

from etna_runner.properties import property_indef_article_abbrev
from etna_runner.strategies import strategy_indef_article_abbrev


@given(strategy_indef_article_abbrev())
@settings(max_examples=50, deadline=None)
def test_property_indef_article_abbrev(args) -> None:
    r = property_indef_article_abbrev(args)
    assert r.kind != "fail", r.message
