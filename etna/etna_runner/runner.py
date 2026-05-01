"""ETNA runner for the inflect Python workload.

Dispatches `<tool> <property>` programmatically. Emits a single JSON line on
stdout per invocation; always exits 0 except on argv-parse errors.

Tools:
  - etna       : witness replay (call every witness for the property once).
  - hypothesis : Hypothesis with the default backend (random + shrinking).
  - crosshair  : Hypothesis with backend="crosshair" (symbolic execution).

The runner adheres to the etna driver JSON contract:
  {"status": "passed|failed|aborted", "tests": N, "discards": M,
   "time": "<us>us", "counterexample": str|None, "error": str|None,
   "tool": "...", "property": "..."}
"""

from __future__ import annotations

import argparse
import json
import sys
import time

from hypothesis import HealthCheck, settings
from hypothesis.errors import HypothesisException

from . import properties, strategies, witnesses

ALL_PROPERTIES = [
    "PluralApostropheNoCrash",
    "IndefArticleAbbrev",
    "OrdinalAcceptsNumeric",
    "PluralShoeReturnsShoes",
    "PoundForcePluralizesPound",
    "LouseLicePlural",
]


def _emit(
    tool: str,
    prop: str,
    status: str,
    tests: int,
    discards: int,
    time_us: int,
    counterexample: str | None = None,
    error: str | None = None,
) -> None:
    sys.stdout.write(
        json.dumps(
            {
                "status": status,
                "tests": tests,
                "discards": discards,
                "time": f"{time_us}us",
                "counterexample": counterexample,
                "error": error,
                "tool": tool,
                "property": prop,
            }
        )
        + "\n"
    )
    sys.stdout.flush()


def _pascal_to_snake(s: str) -> str:
    out = []
    for i, c in enumerate(s):
        if c.isupper() and i and not s[i - 1].isupper():
            out.append("_")
        out.append(c.lower())
    return "".join(out)


def _run_witness(prop: str) -> tuple[str, int, int, str | None]:
    snake = _pascal_to_snake(prop)
    fns = [
        getattr(witnesses, n)
        for n in dir(witnesses)
        if n.startswith(f"witness_{snake}_case_")
    ]
    if not fns:
        return ("aborted", 0, 0, f"no witnesses for {prop}")
    discards = 0
    for fn in fns:
        try:
            r = fn()
        except Exception as e:
            return (
                "failed",
                1,
                discards,
                f"{fn.__name__} raised {type(e).__name__}: {e}",
            )
        if r.kind == "fail":
            return ("failed", 1, discards, r.message)
        if r.kind == "discard":
            discards += 1
    return ("passed", len(fns) - discards, discards, None)


def _run_hypothesis(
    prop: str, backend: str, max_examples: int
) -> tuple[str, int, int, str | None, str | None]:
    snake = _pascal_to_snake(prop)
    strat = getattr(strategies, f"strategy_{snake}")()
    prop_fn = getattr(properties, f"property_{snake}")

    counter = {"n": 0, "discards": 0}
    cex_holder: list[str | None] = [None]
    fail_msg_holder: list[str | None] = [None]

    def _wrapped(args):
        counter["n"] += 1
        try:
            r = prop_fn(args)
        except Exception as e:
            cex_holder[0] = repr(args)
            fail_msg_holder[0] = f"{type(e).__name__}: {e}"
            raise AssertionError(fail_msg_holder[0])
        if r.kind == "fail":
            cex_holder[0] = repr(args)
            fail_msg_holder[0] = r.message
            raise AssertionError(r.message)
        if r.kind == "discard":
            counter["discards"] += 1
            from hypothesis import reject

            reject()

    from hypothesis import given

    test = given(strat)(_wrapped)
    test = settings(
        backend=backend,
        max_examples=max_examples,
        deadline=None,
        derandomize=False,
        suppress_health_check=list(HealthCheck),
        database=None,
    )(test)

    try:
        test()
        return ("passed", counter["n"], counter["discards"], None, None)
    except AssertionError:
        return (
            "failed",
            counter["n"],
            counter["discards"],
            cex_holder[0] or "<unknown>",
            fail_msg_holder[0],
        )
    except HypothesisException as e:
        return (
            "failed",
            counter["n"],
            counter["discards"],
            cex_holder[0] or "<unknown>",
            f"{type(e).__name__}: {e}",
        )
    except Exception as e:
        return (
            "aborted",
            counter["n"],
            counter["discards"],
            cex_holder[0],
            f"{type(e).__name__}: {e}",
        )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("tool", choices=["etna", "hypothesis", "crosshair"])
    p.add_argument("property")
    p.add_argument("--max-examples", type=int, default=200)
    args = p.parse_args(argv)

    targets = ALL_PROPERTIES if args.property == "All" else [args.property]
    overall_status = "passed"
    total_tests = 0
    total_discards = 0
    t0 = time.perf_counter()

    for prop in targets:
        if prop not in ALL_PROPERTIES:
            _emit(
                args.tool,
                prop,
                "aborted",
                0,
                0,
                int((time.perf_counter() - t0) * 1e6),
                None,
                f"unknown property: {prop}",
            )
            return 0
        if args.tool == "etna":
            status, tests, discards, err = _run_witness(prop)
            cex = err if status == "failed" else None
            _emit(
                args.tool,
                prop,
                status,
                tests,
                discards,
                int((time.perf_counter() - t0) * 1e6),
                cex,
                None,
            )
            total_tests += tests
            total_discards += discards
        else:
            backend = "crosshair" if args.tool == "crosshair" else "hypothesis"
            try:
                status, tests, discards, cex, err = _run_hypothesis(
                    prop, backend, args.max_examples
                )
            except Exception as e:
                status, tests, discards, cex, err = (
                    "aborted",
                    0,
                    0,
                    None,
                    f"{type(e).__name__}: {e}",
                )
            _emit(
                args.tool,
                prop,
                status,
                tests,
                discards,
                int((time.perf_counter() - t0) * 1e6),
                cex,
                err,
            )
            total_tests += tests
            total_discards += discards
        if status != "passed" and overall_status == "passed":
            overall_status = status

    return 0


if __name__ == "__main__":
    sys.exit(main())
