# inflect — ETNA Tasks

Total tasks: 24

## Task Index

| Task | Variant | Framework | Property | Witness |
|------|---------|-----------|----------|---------|
| 001 | `a_not_incorrectly_abbreviated_924695c_1` | proptest | `IndefArticleAbbrev` | `witness_indef_article_abbrev_case_bfm` |
| 002 | `a_not_incorrectly_abbreviated_924695c_1` | quickcheck | `IndefArticleAbbrev` | `witness_indef_article_abbrev_case_bfm` |
| 003 | `a_not_incorrectly_abbreviated_924695c_1` | crabcheck | `IndefArticleAbbrev` | `witness_indef_article_abbrev_case_bfm` |
| 004 | `a_not_incorrectly_abbreviated_924695c_1` | hegel | `IndefArticleAbbrev` | `witness_indef_article_abbrev_case_bfm` |
| 005 | `louse_lice_plural_8d610f3_1` | proptest | `LouseLicePlural` | `witness_louse_lice_plural_case_zero` |
| 006 | `louse_lice_plural_8d610f3_1` | quickcheck | `LouseLicePlural` | `witness_louse_lice_plural_case_zero` |
| 007 | `louse_lice_plural_8d610f3_1` | crabcheck | `LouseLicePlural` | `witness_louse_lice_plural_case_zero` |
| 008 | `louse_lice_plural_8d610f3_1` | hegel | `LouseLicePlural` | `witness_louse_lice_plural_case_zero` |
| 009 | `ordinal_accepts_numeric_27b2157_1` | proptest | `OrdinalAcceptsNumeric` | `witness_ordinal_accepts_numeric_case_one` |
| 010 | `ordinal_accepts_numeric_27b2157_1` | quickcheck | `OrdinalAcceptsNumeric` | `witness_ordinal_accepts_numeric_case_one` |
| 011 | `ordinal_accepts_numeric_27b2157_1` | crabcheck | `OrdinalAcceptsNumeric` | `witness_ordinal_accepts_numeric_case_one` |
| 012 | `ordinal_accepts_numeric_27b2157_1` | hegel | `OrdinalAcceptsNumeric` | `witness_ordinal_accepts_numeric_case_one` |
| 013 | `plural_apostrophe_no_crash_498619b_1` | proptest | `PluralApostropheNoCrash` | `witness_plural_apostrophe_no_crash_case_single` |
| 014 | `plural_apostrophe_no_crash_498619b_1` | quickcheck | `PluralApostropheNoCrash` | `witness_plural_apostrophe_no_crash_case_single` |
| 015 | `plural_apostrophe_no_crash_498619b_1` | crabcheck | `PluralApostropheNoCrash` | `witness_plural_apostrophe_no_crash_case_single` |
| 016 | `plural_apostrophe_no_crash_498619b_1` | hegel | `PluralApostropheNoCrash` | `witness_plural_apostrophe_no_crash_case_single` |
| 017 | `pound_force_pluralizes_pound_f87c0b9_1` | proptest | `PoundForcePluralizesPound` | `witness_pound_force_pluralizes_pound_case_zero` |
| 018 | `pound_force_pluralizes_pound_f87c0b9_1` | quickcheck | `PoundForcePluralizesPound` | `witness_pound_force_pluralizes_pound_case_zero` |
| 019 | `pound_force_pluralizes_pound_f87c0b9_1` | crabcheck | `PoundForcePluralizesPound` | `witness_pound_force_pluralizes_pound_case_zero` |
| 020 | `pound_force_pluralizes_pound_f87c0b9_1` | hegel | `PoundForcePluralizesPound` | `witness_pound_force_pluralizes_pound_case_zero` |
| 021 | `shoes_is_plverb_oe_36269c1_1` | proptest | `PluralShoeReturnsShoes` | `witness_plural_shoe_returns_shoes_case_zero` |
| 022 | `shoes_is_plverb_oe_36269c1_1` | quickcheck | `PluralShoeReturnsShoes` | `witness_plural_shoe_returns_shoes_case_zero` |
| 023 | `shoes_is_plverb_oe_36269c1_1` | crabcheck | `PluralShoeReturnsShoes` | `witness_plural_shoe_returns_shoes_case_zero` |
| 024 | `shoes_is_plverb_oe_36269c1_1` | hegel | `PluralShoeReturnsShoes` | `witness_plural_shoe_returns_shoes_case_zero` |

## Witness Catalog

- `witness_indef_article_abbrev_case_bfm` — a('BFM') must be 'a BFM'
- `witness_louse_lice_plural_case_zero` — plural('sealouse') must equal 'sealouses'
- `witness_ordinal_accepts_numeric_case_one` — ordinal(1) must succeed and start with '1'
- `witness_plural_apostrophe_no_crash_case_single` — plural("'") must not raise
- `witness_pound_force_pluralizes_pound_case_zero` — plural('pound-force') must equal 'pounds-force'
- `witness_plural_shoe_returns_shoes_case_zero` — plural('shoe') must equal 'shoes'
