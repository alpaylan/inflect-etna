# inflect — Injected Bugs

Pure-Python English-language inflection (jaraco/inflect): plurals, ordinals, indefinite articles, number-to-word conversion. Bug fixes mined from upstream history; modern HEAD is the base, each patch reverse-applies a fix to install the original bug.

Total mutations: 6

## Bug Index

| # | Variant | Name | Location | Injection | Fix Commit |
|---|---------|------|----------|-----------|------------|
| 1 | `a_not_incorrectly_abbreviated_924695c_1` | `a_not_incorrectly_abbreviated` | `inflect/__init__.py:1857` | `patch` | `924695c2de9d1dcfde0c1bd4c4cb054e32fd8273` |
| 2 | `louse_lice_plural_8d610f3_1` | `louse_lice_plural` | `inflect/__init__.py:2833` | `patch` | `8d610f30f24bcdc524bcb8c734801fbb311eeeec` |
| 3 | `ordinal_accepts_numeric_27b2157_1` | `ordinal_accepts_numeric` | `inflect/__init__.py:3648` | `patch` | `27b2157907ae7f18feec5cf1b600a09e65e78420` |
| 4 | `plural_apostrophe_no_crash_498619b_1` | `plural_apostrophe_no_crash` | `inflect/__init__.py:1989` | `patch` | `498619bf7a658d127c8be1e7e7e465b69dcf6800` |
| 5 | `pound_force_pluralizes_pound_f87c0b9_1` | `pound_force_pluralizes_pound` | `inflect/__init__.py:1510` | `patch` | `f87c0b9e76ad97d564a8fd3a3b2e75e765e193f5` |
| 6 | `shoes_is_plverb_oe_36269c1_1` | `shoes_is_plverb_oe` | `inflect/__init__.py:1825` | `patch` | `36269c1111add4c247d83389b874005fc3526994` |

## Property Mapping

| Variant | Property | Witness(es) |
|---------|----------|-------------|
| `a_not_incorrectly_abbreviated_924695c_1` | `IndefArticleAbbrev` | `witness_indef_article_abbrev_case_bfm` |
| `louse_lice_plural_8d610f3_1` | `LouseLicePlural` | `witness_louse_lice_plural_case_zero` |
| `ordinal_accepts_numeric_27b2157_1` | `OrdinalAcceptsNumeric` | `witness_ordinal_accepts_numeric_case_one` |
| `plural_apostrophe_no_crash_498619b_1` | `PluralApostropheNoCrash` | `witness_plural_apostrophe_no_crash_case_single` |
| `pound_force_pluralizes_pound_f87c0b9_1` | `PoundForcePluralizesPound` | `witness_pound_force_pluralizes_pound_case_zero` |
| `shoes_is_plverb_oe_36269c1_1` | `PluralShoeReturnsShoes` | `witness_plural_shoe_returns_shoes_case_zero` |

## Framework Coverage

| Property | proptest | quickcheck | crabcheck | hegel |
|----------|---------:|-----------:|----------:|------:|
| `IndefArticleAbbrev` | ✓ | ✓ | ✓ | ✓ |
| `LouseLicePlural` | ✓ | ✓ | ✓ | ✓ |
| `OrdinalAcceptsNumeric` | ✓ | ✓ | ✓ | ✓ |
| `PluralApostropheNoCrash` | ✓ | ✓ | ✓ | ✓ |
| `PoundForcePluralizesPound` | ✓ | ✓ | ✓ | ✓ |
| `PluralShoeReturnsShoes` | ✓ | ✓ | ✓ | ✓ |

## Bug Details

### 1. a_not_incorrectly_abbreviated

- **Variant**: `a_not_incorrectly_abbreviated_924695c_1`
- **Location**: `inflect/__init__.py:1857` (inside `A_abbrev`)
- **Property**: `IndefArticleAbbrev`
- **Witness(es)**:
  - `witness_indef_article_abbrev_case_bfm` — a('BFM') must be 'a BFM'
- **Source**: [#136](https://github.com/jaraco/inflect/issues/136) — fix a/an issue 136 as indicated by tonywu7
  > A_abbrev was a verbose regex with no `^` anchor: when invoked through re.search() the negative lookahead group could bind to any interior position, so words like 'BFM' (a consonant followed by [FHLMNRSX][A-Z]) were classified as 'an BFM' through an interior match. The fix prepends `^` so the lookahead binds only to the start of the word.
- **Fix commit**: `924695c2de9d1dcfde0c1bd4c4cb054e32fd8273` — fix a/an issue 136 as indicated by tonywu7
- **Invariant violated**: For an all-caps abbreviation whose first character is a consonant from SPECIAL_A's class (b,c,d,g,j,k,p,q,t,v,w,y,z), engine().a(word) starts with 'a ' (not 'an ').
- **How the mutation triggers**: Reverse-applying the patch removes the leading `^` anchor in A_abbrev. re.search() can then locate `[FHLMNRSX][A-Z]` at an interior position; the consonant-leading abbreviation 'BFM' matches at offset 1 and is incorrectly classified as 'an BFM'.

### 2. louse_lice_plural

- **Variant**: `louse_lice_plural_8d610f3_1`
- **Location**: `inflect/__init__.py:2833` (inside `engine._plnoun_louse_branch`)
- **Property**: `LouseLicePlural`
- **Witness(es)**:
  - `witness_louse_lice_plural_case_zero` — plural('sealouse') must equal 'sealouses'
- **Source**: internal — Update handling of louse/lice plurals to treat it as the exception rather than the norm.
  > The original 'louse' branch in plural() pluralized every word ending in '..louse' to '..lice' wholesale (e.g. 'sealouse' → 'sealice'), even though only four canonical compounds (booklouse, grapelouse, louse, woodlouse) actually take that form. The fix gates the substitution on membership in pl_sb_U_louse_lice_bysize and falls back to the regular '+s' path otherwise.
- **Fix commit**: `8d610f30f24bcdc524bcb8c734801fbb311eeeec` — Update handling of louse/lice plurals to treat it as the exception rather than the norm.
- **Invariant violated**: For any non-canonical louse compound (e.g. 'sealouse'), engine().plural(w) appends 's' rather than substituting 'louse' → 'lice'.
- **How the mutation triggers**: Reverse-applying the patch reverts the louse branch to the unguarded substitution `return f"{word[:-5]}lice"`. plural('sealouse') then returns 'sealice' instead of 'sealouses'.

### 3. ordinal_accepts_numeric

- **Variant**: `ordinal_accepts_numeric_27b2157_1`
- **Location**: `inflect/__init__.py:3648` (inside `engine.ordinal`)
- **Property**: `OrdinalAcceptsNumeric`
- **Witness(es)**:
  - `witness_ordinal_accepts_numeric_case_one` — ordinal(1) must succeed and start with '1'
- **Source**: [#178](https://github.com/jaraco/inflect/issues/178) — Handle numeric inputs to ordinal without first casting to string. Fixes #178.
  > engine.ordinal() was annotated `num: Word` (an Annotated[str,...] alias). Once typeguard begain enforcing this annotation at call time, ordinal(1) — documented as accepting an int per the docstring — raised TypeCheckError. The fix widens the parameter to Union[Number, Word] (and adapts the body to coerce non-str via str(num)).
- **Fix commit**: `27b2157907ae7f18feec5cf1b600a09e65e78420` — Handle numeric inputs to ordinal without first casting to string. Fixes #178.
- **Invariant violated**: For any int n in [-9999, 9999], engine().ordinal(n) returns a string starting with str(n) and ending in one of {'st','nd','rd','th'}.
- **How the mutation triggers**: Reverse-applying the patch narrows `num: Union[Number, Word]` back to `num: Word`. typeguard's @typechecked decorator then rejects integer arguments and ordinal(1) raises TypeCheckError.

### 4. plural_apostrophe_no_crash

- **Variant**: `plural_apostrophe_no_crash_498619b_1`
- **Location**: `inflect/__init__.py:1989` (inside `ENDS_WITH_APOSTROPHE_S`)
- **Property**: `PluralApostropheNoCrash`
- **Witness(es)**:
  - `witness_plural_apostrophe_no_crash_case_single` — plural("'") must not raise
- **Source**: [#218](https://github.com/jaraco/inflect/pull/218) — Handle a single apostrophe more gracefully
  > ENDS_WITH_APOSTROPHE_S used `^(.*)'s?$` which lets the empty stem case match for the bare-apostrophe input "'". The downstream typeguarded plural_noun() then crashes on the empty Word. The fix tightens the regex to `^(.+)'s?$` so the apostrophe-only string falls through and is returned unchanged.
- **Fix commit**: `498619bf7a658d127c8be1e7e7e465b69dcf6800` — Handle a single apostrophe more gracefully
- **Invariant violated**: engine().plural(s) returns a string for any non-empty str s; in particular, plural("'") must not raise.
- **How the mutation triggers**: Reverse-applying the patch loosens ENDS_WITH_APOSTROPHE_S back to `^(.*)'s?$`. plural("'") then matches with an empty stem; the typeguard-checked plural_noun() rejects the empty Word and raises TypeCheckError.

### 5. pound_force_pluralizes_pound

- **Variant**: `pound_force_pluralizes_pound_f87c0b9_1`
- **Location**: `inflect/__init__.py:1510` (inside `_pl_sb_postfix_adj_defn`)
- **Property**: `PoundForcePluralizesPound`
- **Witness(es)**:
  - `witness_pound_force_pluralizes_pound_case_zero` — plural('pound-force') must equal 'pounds-force'
- **Source**: internal — Fix plural of 'pound-force'
  > _pl_sb_postfix_adj_defn lacked a 'force' postfix-adjective entry. plural('pound-force') therefore fell through to the generic hyphenated-compound path and pluralized the wrong word, returning 'pound-forces' instead of 'pounds-force'. The fix adds ('force', enclose('pound')) so 'force' is recognized as a postfix adjective.
- **Fix commit**: `f87c0b9e76ad97d564a8fd3a3b2e75e765e193f5` — Fix plural of 'pound-force'
- **Invariant violated**: engine().plural('pound-force') == 'pounds-force'.
- **How the mutation triggers**: Reverse-applying the patch removes the ('force', enclose('pound')) entry from _pl_sb_postfix_adj_defn. plural('pound-force') then falls through to the generic compound path and returns 'pound-forces'.

### 6. shoes_is_plverb_oe

- **Variant**: `shoes_is_plverb_oe_36269c1_1`
- **Location**: `inflect/__init__.py:1825` (inside `pl_v_oes_oe_endings_size5`)
- **Property**: `PluralShoeReturnsShoes`
- **Witness(es)**:
  - `witness_plural_shoe_returns_shoes_case_zero` — plural('shoe') must equal 'shoes'
- **Source**: [#43](https://github.com/jaraco/inflect/issues/43) — Restore missing comma. Fixes #43.
  > `pl_v_oes_oe_endings_size5 = "shoes"` (no trailing comma) made the constant a bare string instead of a one-element tuple. Downstream code that iterates the tuple to invert a 'shoes' plural treats each character as a member, breaking the round-trip. plural('shoe') then returns 'sho'. The fix restores the trailing comma so the value is `("shoes",)`.
- **Fix commit**: `36269c1111add4c247d83389b874005fc3526994` — Restore missing comma. Fixes #43.
- **Invariant violated**: engine().plural('shoe') == 'shoes'.
- **How the mutation triggers**: Reverse-applying the patch turns `pl_v_oes_oe_endings_size5 = ("shoes",)` back into the bare string `"shoes"`. The tuple-iteration code in the singular/plural lookup then treats each character as a member, so the inverse-lookup fails for 'shoe' and plural('shoe') is computed as 'sho'.

## Dropped Candidates

- `31b9339` (Don't crash on a suffix-only number_to_words) — modern HEAD's _chunk_num('') no longer raises; both buggy and fixed paths return 'zero'.
- `76150f9` (Replace enconium with encomium. Fixes #67.) — no observable public invariant on modern HEAD: singular_noun('encomia') returns False even on the fixed tree, so the bug isn't exposed via the engine API.
- `e2d02d2` (Apply a minimal fix to allow the test cases to pass) — no observable public invariant; this commit is a workaround scope-narrowing of an existing typeguard issue and not an independent bug.
- `8e2f1cf` (_plequal: marginally reduce cyclomatic complexity (#223)) — pure refactor, no behavior change.
- `0bf9533` (engine: migrate from py3.14-removed `ast` classes) — ast.Num/ast.Str still exist on py3.10-3.13 (even though deprecated), so reverting the migration on those Pythons is not observably broken.
- `c58609b` (Construct the _gend_sing dictionary statically.) — pure refactor, no behavior change.
