"""Property functions for the inflect workload.

Each property is pure and deterministic: same input always produces the same
PropertyResult. They are referenced from etna.toml and exercised both by the
plain witness functions and by the Hypothesis-driven test suite.
"""

from __future__ import annotations

import inflect

from ._result import DISCARD, PASS, PropertyResult, fail


# Module-level engine: inflect.engine() is heavy to construct; constructing
# once is fine because all calls into it are pure functions of their inputs.
_ENGINE = inflect.engine()


def property_plural_apostrophe_no_crash(suffix_len: int) -> PropertyResult:
    """plural() must not raise on a string consisting solely of apostrophes.

    The buggy ENDS_WITH_APOSTROPHE_S regex used `(.*)'s?$` which matches the
    string "'" with an empty stem; downstream logic then fails the type check
    for an empty Word. The fix tightens the regex to `(.+)'s?$` so the
    apostrophe-only string falls through to a no-op return.
    """
    if not (1 <= suffix_len <= 3):
        return DISCARD
    word = "'" * suffix_len
    try:
        out = _ENGINE.plural(word)
    except Exception as e:
        return fail(f"plural({word!r}) raised {type(e).__name__}: {e}")
    if not isinstance(out, str):
        return fail(f"plural({word!r}) returned non-string {out!r}")
    return PASS


def property_indef_article_abbrev(word: str) -> PropertyResult:
    """For abbreviations whose first letter is a consonant but whose interior
    contains [FHLMNRSX][A-Z], a(...) must start with 'a ' (not 'an ').

    The buggy A_abbrev regex used a non-anchored verbose pattern (no leading
    `^`); the regex's `[FHLMNRSX][A-Z]` clause could match anywhere in the
    word, so a word like 'BFM' gets classified as 'an BFM' even though
    it begins with the consonant 'B'. The fix prepends `^` so the lookahead
    binds to the start of the word.
    """
    if not word:
        return DISCARD
    if len(word) != 3:
        return DISCARD
    if not word.isupper() or not word.isalpha():
        return DISCARD
    # First letter must be in the SPECIAL_A consonant set so the fix correctly
    # produces 'a '.
    if word[0] not in "BCDGJKPQTVWYZ":
        return DISCARD
    # Interior must contain [FHLMNRSX][A-Z] so the buggy regex misfires.
    interior = word[1:]
    if interior[0] not in "FHLMNRSX":
        return DISCARD
    out = _ENGINE.a(word)
    if not isinstance(out, str):
        return fail(f"a({word!r}) returned non-string {out!r}")
    # a() result is always 'a <word>' or 'an <word>'.
    if out.lower().startswith("an "):
        return fail(f"a({word!r}) = {out!r}; expected to start with 'a '")
    if not out.lower().startswith("a "):
        return fail(f"a({word!r}) = {out!r}; expected to start with 'a '")
    return PASS


def property_ordinal_accepts_numeric(value: int) -> PropertyResult:
    """ordinal(int_value) must succeed and produce a numeric ordinal string.

    The buggy version's `validate_arguments` decorator typed the parameter as
    `Word` and the function body indexed `num[-1]` / `num[:-1]` directly,
    which crashes on numeric input or runs through the integer branch only.
    The fix accepts `Union[Number, Word]` and uses `str(num)[-1]` etc.

    Restricted to non-negative ints because negative-int handling is its own
    open bug on modern HEAD (DIGIT.match fails on the leading '-').
    """
    if not (0 <= value <= 9999):
        return DISCARD
    try:
        out = _ENGINE.ordinal(value)
    except Exception as e:
        return fail(f"ordinal({value!r}) raised {type(e).__name__}: {e}")
    if not isinstance(out, str):
        return fail(f"ordinal({value!r}) returned non-string {out!r}")
    expected_suffix_set = {"st", "nd", "rd", "th"}
    if not any(out.endswith(s) for s in expected_suffix_set):
        return fail(
            f"ordinal({value!r}) = {out!r}; expected to end with st/nd/rd/th"
        )
    if not out.startswith(str(value)):
        return fail(
            f"ordinal({value!r}) = {out!r}; expected to start with {str(value)!r}"
        )
    return PASS


def property_plural_shoe_returns_shoes(value: int) -> PropertyResult:
    """plural('shoe') == 'shoes'.

    The buggy revision drops the trailing comma off
    `pl_v_oes_oe_endings_size5 = "shoes"`, making it the bare string.
    Downstream code that iterates the membership tuple to invert plural
    forms then sees individual characters 's','h','o','e','s' instead of
    the single token 'shoes'. plural('shoe') falls into the wrong
    table-driven branch and produces 'sho' instead of 'shoes'.
    """
    if not (0 <= value <= 1):
        return DISCARD
    out = _ENGINE.plural("shoe")
    if out != "shoes":
        return fail(f"plural('shoe') = {out!r}; expected 'shoes'")
    return PASS


def property_pound_force_pluralizes_pound(value: int) -> PropertyResult:
    """plural('pound-force') == 'pounds-force'.

    The buggy version omits the 'force' postfix-adjective entry from
    pl_sb_postfix_adj, so 'pound-force' falls through to the generic
    hyphenated-compound path which pluralizes the wrong word.
    """
    if not (0 <= value <= 1):
        return DISCARD
    out = _ENGINE.plural("pound-force")
    if out != "pounds-force":
        return fail(f"plural('pound-force') = {out!r}; expected 'pounds-force'")
    return PASS


def property_louse_lice_plural(value: int) -> PropertyResult:
    """plural() only pluralizes the four canonical louse compounds to 'lice'.

    Buggy variant: every '..louse' suffix is replaced with '..lice' wholesale,
    even for non-louse words. For 'sealouse' the buggy code returns 'sealice'
    instead of 'sealouses' (sealouse isn't on the canonical
    pl_sb_U_louse_lice_list, so it must take the regular '+s' path). The fix
    gates the 'lice' substitution on membership in the canonical list.

    'value' is a placeholder; the property is deterministic.
    """
    if not (0 <= value <= 1):
        return DISCARD
    out = _ENGINE.plural("sealouse")
    if out == "sealice":
        return fail(
            f"plural('sealouse') = {out!r}; expected 'sealouses' "
            "(non-canonical louse must not be wholesale-pluralized to lice)"
        )
    if out != "sealouses":
        return fail(f"plural('sealouse') = {out!r}; expected 'sealouses'")
    # Sanity: the canonical 'louse' must still pluralize to 'lice'.
    out2 = _ENGINE.plural("louse")
    if out2 != "lice":
        return fail(f"plural('louse') = {out2!r}; expected 'lice'")
    return PASS
