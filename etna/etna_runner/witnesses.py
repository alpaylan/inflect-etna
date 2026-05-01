"""Plain-Python witness functions.

Each witness calls a single property with frozen inputs. On the base tree
every witness must return PASS; with the corresponding patch reverse-applied
every witness for that variant must return fail(...).
"""

from __future__ import annotations

from ._result import PropertyResult
from . import properties as P


def witness_plural_apostrophe_no_crash_case_single() -> PropertyResult:
    return P.property_plural_apostrophe_no_crash(1)


def witness_indef_article_abbrev_case_bfm() -> PropertyResult:
    return P.property_indef_article_abbrev("BFM")


def witness_ordinal_accepts_numeric_case_one() -> PropertyResult:
    return P.property_ordinal_accepts_numeric(1)


def witness_plural_shoe_returns_shoes_case_zero() -> PropertyResult:
    return P.property_plural_shoe_returns_shoes(0)


def witness_pound_force_pluralizes_pound_case_zero() -> PropertyResult:
    return P.property_pound_force_pluralizes_pound(0)


def witness_louse_lice_plural_case_zero() -> PropertyResult:
    return P.property_louse_lice_plural(0)
