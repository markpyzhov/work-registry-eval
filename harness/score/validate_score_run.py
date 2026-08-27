#!/usr/bin/env python3
"""Strictly validate a scored run before merging.

Checks the invariants from score-rounds.md and the Output schema in
scoring-conventions.md: unique manifest session_ids, a logs/<sid>.md
per session, and per scorer an assembled flat scores/<scorer>.csv with the
exact header and exactly one valid row per manifest session (correctness in
{0, 0.5, 1}, counts non-negative integers, citations_valid <= citations_total,
no blanks/duplicates/unknowns). Warns when the run has no questions.csv
snapshot; when present, it must name exactly the manifest's (corpus, key) set.

Exit 0 = structurally complete; 1 = errors. Pure stdlib. Usage:
    python3 validate_score_run.py --run-dir DIR [--scorers a,b,c]
"""

from __future__ import annotations

import argparse
import csv
import glob
import os
import re
import sys

DEFAULT_SCORERS = ["claude", "codex", "cursor"]

SCORE_HEADER = ["session_id", "correctness", "missing_facts",
                "citations_total", "citations_valid"]
COUNT_FIELDS = ["missing_facts", "citations_total", "citations_valid"]
CORRECTNESS_VALUES = {"0", "0.5", "1"}

errors = []
warnings = []


def canonical_key(value):
    """Normalize answer-key spelling (Q-01) to run-ID spelling (Q01)."""
    match = re.fullmatch(r"([QA])-?(\d+)", (value or "").strip().upper())
    return f"{match.group(1)}{int(match.group(2)):02d}" if match else value


def err(msg):
    errors.append(msg)
    print(f"[error] {msg}", file=sys.stderr)


def warn(msg):
    warnings.append(msg)
    print(f"[warn]  {msg}", file=sys.stderr)


def info(msg):
    print(f"[info]  {msg}", file=sys.stderr)


def check_scorer(scores_dir, scorer, usage_sids):
    path = os.path.join(scores_dir, f"{scorer}.csv")
    if not os.path.isfile(path):
        err(f"{scorer}: assembled flat file missing: {path}")
        return
    with open(path, newline="") as fh:
        reader = csv.reader(fh)
        try:
            header = next(reader)
        except StopIteration:
            err(f"{scorer}: empty file")
            return
        if header != SCORE_HEADER:
            err(f"{scorer}: bad header {header!r}, expected {SCORE_HEADER!r}")
            return
        seen = set()
        n_bad = 0
        for i, row in enumerate(reader, start=2):
            if len(row) != len(SCORE_HEADER):
                err(f"{scorer}:{i}: expected {len(SCORE_HEADER)} cells, got {len(row)}")
                n_bad += 1
                continue
            r = dict(zip(SCORE_HEADER, row))
            sid = r["session_id"].strip()
            if not sid:
                err(f"{scorer}:{i}: blank session_id")
                n_bad += 1
                continue
            if sid in seen:
                err(f"{scorer}:{i}: duplicate session_id {sid}")
                n_bad += 1
            seen.add(sid)
            if sid not in usage_sids:
                err(f"{scorer}:{i}: unknown session_id {sid} (not in usage.csv)")
                n_bad += 1
            if r["correctness"].strip() not in CORRECTNESS_VALUES:
                err(f"{scorer}:{i}: correctness {r['correctness']!r} not in 0/0.5/1")
                n_bad += 1
            counts = {}
            for f in COUNT_FIELDS:
                v = r[f].strip()
                if not v.isdigit():
                    err(f"{scorer}:{i}: {f} {v!r} is not a non-negative integer")
                    n_bad += 1
                else:
                    counts[f] = int(v)
            if ("citations_valid" in counts and "citations_total" in counts
                    and counts["citations_valid"] > counts["citations_total"]):
                err(f"{scorer}:{i}: citations_valid > citations_total for {sid}")
                n_bad += 1
    missing = usage_sids - seen
    if missing:
        err(f"{scorer}: {len(missing)} manifest sessions unscored, e.g. "
            f"{sorted(missing)[:5]}")
    if not missing and not n_bad:
        info(f"{scorer}: {len(seen)} rows — complete and valid")


def main():
    errors.clear()
    warnings.clear()
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run-dir", required=True,
                    help="dir with usage.csv, logs/ and scores/")
    ap.add_argument("--scorers", default=",".join(DEFAULT_SCORERS),
                    help="comma list of required scorers (default: claude,codex,cursor)")
    args = ap.parse_args()
    run_dir = args.run_dir
    scorers = [s.strip() for s in args.scorers.split(",") if s.strip()]

    # 1. manifest
    usage_path = os.path.join(run_dir, "usage.csv")
    if not os.path.isfile(usage_path):
        err(f"missing manifest: {usage_path}")
        sys.exit(1)
    with open(usage_path, newline="") as fh:
        usage_rows = list(csv.DictReader(fh))
    usage_sids = set()
    for r in usage_rows:
        sid = r["session_id"]
        if sid in usage_sids:
            err(f"usage.csv: duplicate session_id {sid}")
        usage_sids.add(sid)
    info(f"usage.csv: {len(usage_rows)} sessions")

    # 2. response files
    # Runs collected before 2026-08 keep every response directly in logs/;
    # newer ones split them by tool (logs/claude/, logs/codex/). Accept both.
    logs_dir = os.path.join(run_dir, "logs")
    responses = {}  # session_id -> path
    for path in glob.glob(os.path.join(logs_dir, "*.md")) + \
            glob.glob(os.path.join(logs_dir, "*", "*.md")):
        responses.setdefault(os.path.basename(path)[:-3], path)
    missing_logs = [s for s in sorted(usage_sids) if s not in responses]
    if missing_logs:
        err(f"logs/: {len(missing_logs)} manifest sessions without a .md "
            f"response, e.g. {missing_logs[:5]}")
    else:
        info(f"logs/: every manifest session has a response file")
    extra = [s for s in responses if s not in usage_sids]
    if extra:
        warn(f"logs/: {len(extra)} .md files not in the manifest, "
             f"e.g. {sorted(extra)[:5]}")

    # 3-4. scorer files
    scores_dir = os.path.join(run_dir, "scores")
    for scorer in scorers:
        check_scorer(scores_dir, scorer, usage_sids)

    # 5. question snapshot
    snap = os.path.join(run_dir, "questions.csv")
    if not os.path.isfile(snap):
        warn(f"no run-local question snapshot: {snap}")
    else:
        with open(snap, newline="") as fh:
            snap_keys = {(r["corpus"], canonical_key(r["key"]))
                         for r in csv.DictReader(fh)}
        manifest_keys = {(r["corpus"], canonical_key(r["key"]))
                         for r in usage_rows}
        uncovered = manifest_keys - snap_keys
        if uncovered:
            err(f"questions.csv snapshot misses {len(uncovered)} manifest "
                f"(corpus,key) groups: {sorted(uncovered)[:5]}")
        run_corpora = {corpus for corpus, _ in manifest_keys}
        unrun = {k for k in snap_keys if k[0] in run_corpora} - manifest_keys
        if unrun:
            err(f"{len(unrun)} snapshot question(s) never ran: {sorted(unrun)}")
        if not uncovered and not unrun:
            info("questions.csv snapshot and manifest name the same questions")

    print(file=sys.stderr)
    if errors:
        print(f"[fail] {len(errors)} error(s), {len(warnings)} warning(s)",
              file=sys.stderr)
        sys.exit(1)
    print(f"[ok]   run is structurally complete "
          f"({len(warnings)} warning(s))", file=sys.stderr)


if __name__ == "__main__":
    main()
