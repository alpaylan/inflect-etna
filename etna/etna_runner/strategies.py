"""Hypothesis strategies for the inflect workload.

Strategies stick to the CrossHair-friendly subset: integers, plain text,
booleans, simple ranges. No @composite, no st.data.
"""

from __future__ import annotations

from hypothesis import strategies as st


def strategy_plural_apostrophe_no_crash():
    return st.integers(min_value=1, max_value=3)


def strategy_indef_article_abbrev():
    # 3-letter all-caps abbreviations: first char is a SPECIAL_A consonant,
    # second is from FHLMNRSX (so the buggy regex finds an interior match),
    # third is any uppercase letter.
    first = st.sampled_from(list("BCDGJKPQTVWYZ"))
    second = st.sampled_from(list("FHLMNRSX"))
    third = st.sampled_from(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
    return st.builds(lambda a, b, c: a + b + c, first, second, third)


def strategy_ordinal_accepts_numeric():
    return st.integers(min_value=0, max_value=9999)


def strategy_plural_shoe_returns_shoes():
    return st.integers(min_value=0, max_value=1)


def strategy_pound_force_pluralizes_pound():
    return st.integers(min_value=0, max_value=1)


def strategy_louse_lice_plural():
    return st.integers(min_value=0, max_value=1)
