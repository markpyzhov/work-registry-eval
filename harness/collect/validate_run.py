#!/usr/bin/env python3
"""
Check that a collected run directory is complete and self-consistent.

Runs are now filled by several collectors writing into one directory, so the
question "did everything land?" is no longer answerable by looking at one
script's output. This checks the assembled result:

  1. every usage.csv row has its .jsonl and .md, and vice versa
  2. no duplicate run_id
  3. the grid is rectangular — every (corpus, tool, arm, round) cell holds the
     same set of question keys
  4. no run is missing its answer text
  5. run_id, filename, and the row's own coordinate columns agree

Exit code is non-zero when something is wrong, so it can gate a scoring pass.

Examples
--------
    python validate_run.py --run-dir results/massive-run-X
    python validate_run.py --run-dir DIR --expect-rounds 3 --expect-baseline-rounds 1
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from common import (  # noqa: E402
    ARMS, parse_run_id, read_response, read_usage_rows as read_rows,
)

_problems = 0


def err(msg):
    global _problems
    _problems += 1
    print(f"ERROR {msg}")


def warn(msg):
    print(f"warn  {msg}")


def ok(msg):
    print(f"ok    {msg}")


def check(run_dir: Path, *, expect_rounds: int | None,
          expect_baseline_rounds: int | None = None) -> int:
    global _problems
    _problems = 0
    rows = read_rows(run_dir / "usage.csv")
    if not rows:
        err(f"{run_dir}/usage.csv is missing or empty")
        return _problems
    ok(f"usage.csv: {len(rows)} rows")

    _check_ids(rows)
    _check_arms(rows)
    responses = _check_files(run_dir, rows)
    _check_answers(responses)
    _check_grid(rows, expect_rounds=expect_rounds,
                expect_baseline_rounds=expect_baseline_rounds)
    _check_usage_plausible(rows)
    return _problems


# An agent turn costs at least a fraction of a second end to end, so these are
# far above anything real. They exist to catch accounting bugs — e.g. a resumed
# Codex rollout billing one prompt for the whole session's cumulative totals —
# not to police slow or fast runs.
MAX_STEPS_PER_SEC = 3.0
MAX_INPUT_TOKENS_PER_SEC = 500_000


def _check_usage_plausible(rows):
    """Flag physically impossible step / token rates.

    An earlier C2 codex-dir run recorded 93 steps and 3.08M input tokens in 28.7s
    (0.31s per step) because each session inherited the cumulative totals of a
    resumed Codex session. Structural checks all passed; only the rate gave it
    away.
    """
    bad_steps, bad_tokens = [], []
    for row in rows:
        try:
            dur = float(row.get("duration_seconds") or 0)
            steps = int(row.get("num_steps") or 0)
            inp = int(row.get("tokens_input") or 0) + int(row.get("tokens_cache_read") or 0)
        except ValueError:
            continue
        if dur <= 0:
            continue
        if steps / dur > MAX_STEPS_PER_SEC:
            bad_steps.append((row.get("session_id", "?"), steps, dur))
        if inp / dur > MAX_INPUT_TOKENS_PER_SEC:
            bad_tokens.append((row.get("session_id", "?"), inp, dur))

    for label, bad, unit in (("steps", bad_steps, "steps"),
                             ("input tokens", bad_tokens, "tokens")):
        if bad:
            worst = sorted(bad, key=lambda t: -t[1] / t[2])[:3]
            detail = ", ".join(f"{s} ({n:,} {unit} in {d:.1f}s)" for s, n, d in worst)
            err(f"{len(bad)} session(s) report implausible {label}/sec "
                f"— likely cumulative-usage attribution: {detail}")
    if not bad_steps and not bad_tokens:
        ok("usage rates are physically plausible")


def _check_ids(rows):
    seen = defaultdict(int)
    for row in rows:
        seen[row.get("run_id", "")] += 1
    dupes = {k: v for k, v in seen.items() if v > 1}
    if dupes:
        err(f"duplicate run_id in usage.csv: {sorted(dupes)[:5]}")
    else:
        ok("run_id is unique across the manifest")

    mismatched = []
    for row in rows:
        parsed = parse_run_id(row.get("run_id", ""))
        if not parsed:
            continue  # legacy id scheme; nothing to cross-check
        for field, col in (("corpus", "corpus"), ("arm", "arm"),
                           ("round", "round"), ("model", "tool")):
            want, got = parsed[field], (row.get(col) or "")
            if got and want != got:
                mismatched.append(f"{row['run_id']}: {col}={got!r} != {want!r}")
    if mismatched:
        err(f"run_id disagrees with its own columns ({len(mismatched)}): "
            f"{mismatched[:3]}")
    else:
        ok("run_id agrees with corpus/arm/round/tool columns")


def _check_arms(rows):
    """Every row must name a real arm.

    A row landing on an arm outside the known set means classification fell
    back to a guess somewhere upstream — cheap to check, and it is exactly the
    failure that turned a corpus of C2 RAG runs into eight rounds of baseline.
    """
    bad = sorted({(r.get("arm") or "(empty)") for r in rows
                  if (r.get("arm") or "") not in ARMS})
    if bad:
        err(f"rows with an unknown arm: {bad}")
    else:
        ok(f"every row names a known arm ({'/'.join(ARMS)})")


def _check_files(run_dir: Path, rows) -> dict:
    logs = run_dir / "logs"
    on_disk = {}
    for path in list(logs.glob("*.md")) + list(logs.glob("*/*.md")):
        on_disk[path.stem] = path

    responses = {}
    missing_md, missing_jsonl = [], []
    for row in rows:
        rid = row.get("run_id", "")
        md = on_disk.get(rid)
        if md is None:
            missing_md.append(rid)
            continue
        responses[rid] = md
        if not md.with_suffix(".jsonl").exists():
            missing_jsonl.append(rid)

    if missing_md:
        err(f"{len(missing_md)} manifest rows without a .md: {missing_md[:5]}")
    else:
        ok("every manifest row has its .md")
    if missing_jsonl:
        err(f"{len(missing_jsonl)} responses without their .jsonl: {missing_jsonl[:5]}")
    else:
        ok("every response has its .jsonl")

    known = {row.get("run_id") for row in rows}
    orphans = sorted(set(on_disk) - known)
    if orphans:
        warn(f"{len(orphans)} .md files not in the manifest: {orphans[:5]}")
    return responses


def _check_answers(responses: dict):
    empty = [rid for rid, path in responses.items()
             if not read_response(path) or read_response(path).startswith("_(final response")]
    if empty:
        err(f"{len(empty)} runs have no answer text: {empty[:5]}")
    else:
        ok("every run carries an answer")


def _check_grid(rows, *, expect_rounds: int | None,
                expect_baseline_rounds: int | None):
    cells = defaultdict(set)
    for row in rows:
        cell = (row.get("corpus", ""), row.get("tool", ""), row.get("arm", ""),
                row.get("round", ""))
        cells[cell].add(row.get("key", ""))

    print("\ngrid (unique questions per cell):")
    for cell in sorted(cells):
        print(f"  {cell[0]}  {cell[1]:<7} {cell[2]:<10} r{cell[3]}  {len(cells[cell])}")

    # Every cell of one corpus should cover that corpus's whole question set;
    # a short cell is a run that did not finish, not a design choice.
    by_corpus = defaultdict(set)
    for (corpus, _, _, _), keys in cells.items():
        by_corpus[corpus] |= keys
    ragged = []
    for cell, keys in sorted(cells.items()):
        gap = by_corpus[cell[0]] - keys
        if gap:
            ragged.append(f"{'-'.join(cell)} missing {sorted(gap)}")
    if ragged:
        err(f"incomplete cells ({len(ragged)}):")
        for line in ragged[:10]:
            print(f"        {line}")
    else:
        ok("every cell covers its corpus's full question set")

    if expect_rounds is not None:
        rounds = defaultdict(set)
        for corpus, tool, arm, rnd in cells:
            rounds[(corpus, tool, arm)].add(rnd)
        short = {}
        for key, values in rounds.items():
            wanted = (expect_baseline_rounds
                      if key[2] == "baseline" and expect_baseline_rounds is not None
                      else expect_rounds)
            # Count only: some rounds may be naturally skipped by the parent agent
            if len(values) != wanted:
                short[key] = (sorted(values), wanted)
        if short:
            detail = [f"{'-'.join(k)}={','.join(v)} (expected {wanted})"
                      for k, (v, wanted) in sorted(short.items())]
            err(f"arms with the wrong number of rounds: {detail[:5]}")
        else:
            suffix = (f"; baseline has {expect_baseline_rounds}"
                      if expect_baseline_rounds is not None else "")
            ok(f"every main arm has {expect_rounds} rounds{suffix}")


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run-dir", type=Path, required=True,
                    help="run directory (holds usage.csv and logs/)")
    ap.add_argument("--expect-rounds", type=int, default=None,
                    help="expected rounds for non-baseline arms")
    ap.add_argument("--expect-baseline-rounds", type=int, default=None,
                    help="expected baseline rounds (defaults to --expect-rounds)")
    args = ap.parse_args()

    problems = check(args.run_dir, expect_rounds=args.expect_rounds,
                     expect_baseline_rounds=args.expect_baseline_rounds)
    print()
    if problems:
        print(f"{problems} problem(s) found")
        return 1
    print("run directory is complete and consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
