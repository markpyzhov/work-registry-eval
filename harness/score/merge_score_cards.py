#!/usr/bin/env python3
"""Merge per-scorer score cards into one analysis table.

Implements merge-score-cards.md:

  1. Metadata + performance stats  -> <run>/usage.csv (the manifest)
  2. Accuracy stats                -> <run>/scores/<scorer>.csv, medianed per session
  3. Human review (optional)       -> <run>/scores/human.csv supersedes the
                                      medianed correctness per session

Fail-closed: exits 1 without writing when a scorer's flat file is missing, a
scorer misses a manifest session or adds an unknown/duplicate session_id, or a
cell violates the Output schema in scoring-conventions.md. Run
validate_score_run.py first for a per-cell diagnosis.

Outputs (into <run>/):
  - score-cards.csv       one row per session: metadata + performance + medianed
                          accuracy + scorer diagnostics
  - score-cards-long.csv  one row per (session, scorer): the raw un-medianed union

Pure stdlib. Usage:
    python3 merge_score_cards.py --run-dir DIR [--scorers a,b,c]
"""

from __future__ import annotations

import argparse
import csv
import os
import statistics
import sys
from collections import defaultdict

# --- config -----------------------------------------------------------------

DEFAULT_SCORERS = ["claude", "codex", "cursor"]

SCORE_HEADER = ["session_id", "correctness", "missing_facts",
                "citations_total", "citations_valid"]
HUMAN_HEADER = ["session_id", "correctness", "description"]
NUMERIC_SCORE_FIELDS = ["correctness", "missing_facts",
                        "citations_total", "citations_valid"]
COUNT_FIELDS = ["missing_facts", "citations_total", "citations_valid"]
CORRECTNESS_VALUES = {"0", "0.5", "1"}

# Manifest columns carried into the merged card. A column not listed here stays
# in usage.csv and never reaches the analysis table, so a new manifest column
# cannot appear in a report until it is added here deliberately.
USAGE_IDENTITY = [  # placed before the scores
    "run_id", "corpus", "key", "instance", "arm", "round", "model", "format",
]
USAGE_METRICS = [  # placed after the scores
    # provenance
    "logged_at", "session_path", "prompt_index", "num_prompts",
    "prompt_ts", "end_ts",
    # performance
    "duration_seconds", "duration_wall_seconds", "approval_wait_seconds",
    "num_steps",
    # tokens
    "tokens_input", "tokens_cache_read", "tokens_cache_write_5m",
    "tokens_cache_write_1h", "tokens_cached_input", "tokens_uncached_input",
    "tokens_cache_write", "tokens_output", "tokens_reasoning_output",
    "tokens_total",
    # spend
    "spend_input", "spend_cache_read", "spend_cache_write_5m",
    "spend_cache_write_1h", "spend_input_uncached", "spend_input_cached",
    "spend_cache_write", "spend_output", "spend_total",
]

WARN = "[warn]"
INFO = "[info]"
ERROR = "[error]"


def log(*a):
    print(*a, file=sys.stderr)


def die(msg):
    log(f"{ERROR} {msg}")
    sys.exit(1)


# --- loaders ----------------------------------------------------------------

def load_scorer_rows(scores_dir, scorer):
    """Load the scorer's assembled flat file; anything else is fatal."""
    flat = os.path.join(scores_dir, f"{scorer}.csv")
    if not os.path.isfile(flat):
        die(f"scorer '{scorer}' has no assembled flat file: {flat} "
            f"(assemble per score-rounds.md before merging)")
    with open(flat, newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != SCORE_HEADER:
            die(f"{flat}: bad header {reader.fieldnames!r}, "
                f"expected {SCORE_HEADER!r}")
        return list(reader)


def load_human_overrides(scores_dir, usage_by_sid):
    """Optional human-review file: scores/human.csv supersedes correctness.

    Covers any subset of sessions (unlike scorer files, which must be
    complete). Absent file -> no overrides. Same fail-closed validation.
    """
    path = os.path.join(scores_dir, "human.csv")
    if not os.path.isfile(path):
        return {}
    with open(path, newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != HUMAN_HEADER:
            die(f"{path}: bad header {reader.fieldnames!r}, "
                f"expected {HUMAN_HEADER!r}")
        rows = list(reader)
    overrides = {}
    for r in rows:
        sid = (r.get("session_id") or "").strip()
        if not sid:
            die("human: blank session_id row")
        if sid in overrides:
            die(f"human: duplicate session_id {sid}")
        if sid not in usage_by_sid:
            die(f"human: unknown session_id {sid} (not in usage.csv)")
        val = (r.get("correctness") or "").strip()
        if val not in CORRECTNESS_VALUES:
            die(f"human: session {sid}: correctness {val!r} not in 0/0.5/1")
        if not (r.get("description") or "").strip():
            die(f"human: session {sid}: empty description")
        overrides[sid] = float(val)
    return overrides


def parse_score(scorer, sid, field, raw):
    """Strictly parse one score cell -> float; invalid cells are fatal."""
    s = (raw or "").strip()
    if field == "correctness":
        if s not in CORRECTNESS_VALUES:
            die(f"{scorer}: session {sid}: correctness {raw!r} not in 0/0.5/1")
    elif not s.isdigit():
        die(f"{scorer}: session {sid}: {field} {raw!r} is not a "
            f"non-negative integer")
    return float(s)


def fmt_num(x):
    """Render a float without a trailing .0 when it is integral."""
    if x is None:
        return ""
    if x == int(x):
        return str(int(x))
    return f"{x:g}"


# --- main -------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run-dir", required=True,
                    help="dir with usage.csv and scores/")
    ap.add_argument("--scorers", default=",".join(DEFAULT_SCORERS),
                    help="comma list of scorer names (default: claude,codex,cursor)")
    args = ap.parse_args()

    run_dir = args.run_dir
    scores_dir = os.path.join(run_dir, "scores")
    usage_path = os.path.join(run_dir, "usage.csv")
    scorers = [s.strip() for s in args.scorers.split(",") if s.strip()]

    if not os.path.isfile(usage_path):
        die(f"missing required input: {usage_path}")

    # 1. usage manifest --------------------------------------------------
    with open(usage_path, newline="") as fh:
        reader = csv.DictReader(fh)
        usage_cols = list(reader.fieldnames)
        usage_rows = list(reader)
    usage_by_sid = {}
    for r in usage_rows:
        sid = r["session_id"]
        if sid in usage_by_sid:
            die(f"duplicate session_id in usage.csv: {sid}")
        usage_by_sid[sid] = r
    log(f"{INFO} usage.csv: {len(usage_rows)} sessions, {len(usage_cols)} columns")
    absent = [c for c in USAGE_IDENTITY + USAGE_METRICS if c not in usage_cols]
    if absent:
        die(f"usage.csv lacks {len(absent)} column(s) this merge carries: {absent}")
    extra = [c for c in usage_cols
             if c not in USAGE_IDENTITY + USAGE_METRICS and c != "session_id"]
    if extra:
        log(f"{INFO} manifest columns not carried into the card: {extra}")

    # 2. scorer tables (fail-closed) --------------------------------------
    # scores_by_sid[sid] = { scorer: {field: float} }
    scores_by_sid = defaultdict(dict)
    long_rows = []  # for score-cards-long.csv
    for scorer in scorers:
        rows = load_scorer_rows(scores_dir, scorer)
        seen = set()
        for r in rows:
            sid = (r.get("session_id") or "").strip()
            if not sid:
                die(f"{scorer}: blank session_id row")
            if sid in seen:
                die(f"{scorer}: duplicate session_id {sid}")
            if sid not in usage_by_sid:
                die(f"{scorer}: unknown session_id {sid} (not in usage.csv)")
            seen.add(sid)
            vals = {f: parse_score(scorer, sid, f, r.get(f))
                    for f in NUMERIC_SCORE_FIELDS}
            if vals["citations_valid"] > vals["citations_total"]:
                die(f"{scorer}: session {sid}: citations_valid > citations_total")
            scores_by_sid[sid][scorer] = vals
            lr = {"session_id": sid, "scorer": scorer}
            lr.update({f: r.get(f, "") for f in NUMERIC_SCORE_FIELDS})
            long_rows.append(lr)
        missed = sorted(s for s in usage_by_sid if s not in seen)
        if missed:
            die(f"scorer '{scorer}' did NOT score {len(missed)} manifest "
                f"session(s), e.g. {missed[:5]}")
        log(f"{INFO} scorer '{scorer}': {len(seen)} rows — complete")

    # 2b. human review overrides (optional) -------------------------------
    human = load_human_overrides(scores_dir, usage_by_sid)
    for sid, val in sorted(human.items()):
        long_rows.append({"session_id": sid, "scorer": "human",
                          "correctness": fmt_num(val), "missing_facts": "",
                          "citations_total": "", "citations_valid": ""})
    if human:
        log(f"{INFO} human review: {len(human)} correctness override(s) "
            f"from scores/human.csv")

    # 3. build merged rows ----------------------------------------------
    out_cols = (["session_id"]
                + USAGE_IDENTITY
                + NUMERIC_SCORE_FIELDS
                + ["citation_validity_rate", "n_scorers", "scorers",
                   "correctness_values", "all_scorers_agree", "spread_flag"]
                + USAGE_METRICS)

    merged = []
    agree_num = agree_den = 0
    spread_rows = []

    # iterate over every manifest session (base = usage; coverage is complete)
    for sid, urow in usage_by_sid.items():
        # ---- accuracy: median across all scorers
        per_scorer = scores_by_sid[sid]
        contributing = [s for s in scorers if s in per_scorer]
        n_scorers = len(contributing)
        med = {f: statistics.median(per_scorer[s][f] for s in contributing)
               for f in NUMERIC_SCORE_FIELDS}

        correctness_vals = [per_scorer[s]["correctness"] for s in contributing]
        all_agree = len(set(correctness_vals)) == 1
        spread = (min(correctness_vals) == 0 and max(correctness_vals) == 1)
        agree_den += 1
        if all_agree:
            agree_num += 1
        if spread:
            spread_rows.append((sid, correctness_vals))

        cit_total, cit_valid = med["citations_total"], med["citations_valid"]
        val_rate = (cit_valid / cit_total) if cit_total > 0 else None

        row = {"session_id": sid}
        for c in USAGE_IDENTITY + USAGE_METRICS:
            row[c] = urow.get(c, "")
        for f in NUMERIC_SCORE_FIELDS:
            row[f] = fmt_num(med[f])
        if sid in human:  # human review supersedes the medianed correctness
            row["correctness"] = fmt_num(human[sid])
        row["citation_validity_rate"] = ("" if val_rate is None else f"{val_rate:.4f}")
        row["n_scorers"] = n_scorers
        row["scorers"] = ";".join(contributing)
        row["correctness_values"] = ";".join(fmt_num(v) for v in correctness_vals)
        row["all_scorers_agree"] = str(all_agree)
        row["spread_flag"] = "1" if spread else ""
        merged.append(row)

    # sort by session identity for a stable, readable file
    def sort_key(r):
        inst = r["instance"]
        # (0, int) sorts numeric instances numerically; (1, str) keeps any
        # non-numeric instance comparable without mixing int and str.
        inst_key = (0, int(inst)) if inst.isdigit() else (1, inst)
        return (r["corpus"], r["key"], inst_key)
    merged.sort(key=sort_key)

    # 4. write outputs ---------------------------------------------------
    out_card = os.path.join(run_dir, "score-cards.csv")
    with open(out_card, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=out_cols)
        w.writeheader()
        w.writerows(merged)

    out_long = os.path.join(run_dir, "score-cards-long.csv")
    long_rows.sort(key=lambda r: (r["session_id"], r["scorer"]))
    with open(out_long, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["session_id", "scorer"] + NUMERIC_SCORE_FIELDS)
        w.writeheader()
        w.writerows(long_rows)

    # 5. report ----------------------------------------------------------
    log("")
    log(f"{INFO} wrote {out_card}  ({len(merged)} sessions x {len(out_cols)} cols)")
    log(f"{INFO} wrote {out_long}  ({len(long_rows)} session-scorer rows)")
    log(f"{INFO} scorers: {', '.join(scorers)} ({len(scorers)}) — "
        f"all complete over {len(merged)} sessions")
    if agree_den:
        log(f"{INFO} correctness agreement rate (all scorers equal): "
            f"{agree_num}/{agree_den} = {agree_num/agree_den:.3f}")
    log(f"{INFO} full-spread rows (a scorer said correct AND another incorrect): "
        f"{len(spread_rows)}")
    for sid, vals in spread_rows[:20]:
        log(f"{INFO}   spread {sid}: {[fmt_num(v) for v in vals]}")
    if len(spread_rows) > 20:
        log(f"{INFO}   ... and {len(spread_rows)-20} more")


if __name__ == "__main__":
    main()
