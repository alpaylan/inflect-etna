# inflect — ETNA workload

Pure-Python English-language inflection from
[jaraco/inflect](https://github.com/jaraco/inflect): plurals, ordinals,
indefinite articles, number-to-word conversion. The base tree is the upstream
fork at HEAD; bug variants live as `patches/*.patch` files. Reverse-applying
each patch installs a real bug previously fixed in upstream history.

## Layout

```
.                              # upstream fork (untouched src + minimal pyproject extension)
inflect/                       # upstream library (importable as `import inflect`)
patches/                       # bug-injection patches (fix → buggy direction; reverse-apply to install)
etna.toml                      # workload manifest (single source of truth)
etna/                          # uv project for the runner (etna_runner package + tests)
BUGS.md                        # generated, do not hand-edit
TASKS.md                       # generated, do not hand-edit
progress.jsonl                 # per-run scratch log (gitignored)
```

## Quickstart

```sh
cd etna
uv sync
uv run pytest                                    # base witnesses + per-property tests
uv run etna-runner etna All                       # JSON-on-stdout per property
uv run etna-runner hypothesis All --max-examples 50
uv run etna-runner crosshair All --max-examples 25
```

## Reproducing a bug

```sh
git apply -R patches/plural_apostrophe_no_crash_498619b_1.patch  # install bug
cd etna && uv run etna-runner hypothesis PluralApostropheNoCrash # status: failed
cd .. && git apply patches/plural_apostrophe_no_crash_498619b_1.patch  # restore base
```

## Provenance

Patches were synthesised against modern HEAD (`262a247d`). Where the upstream
fix commit no longer applies cleanly to the modern tree (file moved from
`inflect.py` to `inflect/__init__.py`, attribute renames, etc.), the patch is
hand-crafted to preserve the *behavioural* delta of the original fix.

## Dropped candidates

See the `[[dropped]]` blocks at the bottom of `etna.toml` for fix commits
that were investigated but found terminally inexpressible on modern HEAD
(bug subsumed by a later refactor; pure refactor with no behaviour change;
no observable public invariant).
