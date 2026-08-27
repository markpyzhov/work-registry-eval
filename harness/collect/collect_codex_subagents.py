#!/usr/bin/env python3
"""
Collect Codex subagent sessions (directory + baseline arms) in one pass.

Both arms run as Codex subagents whose NEW_TASK payload is encrypted, so there
is no plaintext prompt to match on. What identifies a run is the subagent's
`agent_path` in the first session_meta record; it carries the corpus, question,
round, arm, and any retry marker. Observed spellings:

    /root/c1_q01_r1_wrdir       directory arm
    /root/c2_r02_a05_directory  directory arm
    /root/baseline_q01b         baseline arm (2026-08: `b` suffix on the key)
    /root/baseline_c2_r2_q09    baseline arm (explicit corpus + round)
    /root/baseline_a01_retry    baseline arm (retry marker)

One scan of ~/.codex/sessions fills both model directories:

    logs/codex-dir/<run_id>.jsonl        directory runs
    logs/codex-baseline/<run_id>.jsonl   baseline runs

Filters (skipped to logs/skipped/<model>/ with a .reason.txt sidecar):
turn_aborted / unfinished subagent, handoff-only answer, attempts superseded
by a retry, rounds beyond MAX_ROUNDS (3). Baseline only: contamination — a
parametric-knowledge run that made ANY tool call.

ALWAYS bound the scan with --min-date: historical batches share un-numbered
path spellings, and mixing them collides order-inferred rounds with explicit
ones (the collector then exits 1 with a duplicate-run_id report).

Examples
--------
    python collect_codex_subagents.py --run-dir results/massive-run-X --min-date 2026-08-04
    python collect_codex_subagents.py --run-dir results/massive-run-X --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from analyze_session import parse_ts  # noqa: E402
from transcript import extract_transcript  # noqa: E402

from common import (  # noqa: E402
    canonical_key, copy_run, copy_skipped, load_questions, make_run_id,
    parse_filter_date, print_grid, report_skipped,
)

SESSIONS = Path.home() / ".codex" / "sessions"
MAX_ROUNDS = 3

MODEL_FOR_ARM = {"directory": "codex-dir", "baseline": "codex-baseline"}
# Un-prefixed round paths belong to Corpus 1; baseline batches to Corpus 2.
DEFAULT_CORPUS = {"directory": "c1", "baseline": "c2"}

_CORPUS_TOKEN = re.compile(r"^c(\d+)$", re.IGNORECASE)
_ROUND_TOKEN = re.compile(r"^r(\d+)$", re.IGNORECASE)
# The 2026-08 baseline harness appends `b` to the key token (q01b); tolerated.
_KEY_TOKEN = re.compile(r"^([qa]-?\d+)b?$", re.IGNORECASE)
_ARM_WORDS = {
    "directory": "directory", "dir": "directory", "wrdir": "directory",
    "baseline": "baseline", "base": "baseline",
}
_RERUN_WORDS = frozenset({"rerun", "retry"})


def parse_agent_path(agent_path: str) -> dict | None:
    """-> {corpus, key, arm, round, retry}, else None.

    The last path segment is an underscore-joined bag of tokens whose order
    varies between harness generations, so each token is classified on its own.
    Requires EXACTLY ONE question key (a bundle like c1_q10_q15_r3_wrdir is one
    session answering six questions) and an arm word.
    """
    seg = agent_path.rstrip("/").rsplit("/", 1)[-1]
    corpus, round_num, keys, arm, retry = None, None, [], None, False
    for tok in seg.split("_"):
        if not tok:
            continue
        if m := _CORPUS_TOKEN.match(tok):
            corpus = f"c{int(m.group(1))}"
        elif m := _ROUND_TOKEN.match(tok):
            round_num = int(m.group(1))
        elif m := _KEY_TOKEN.match(tok):
            keys.append(canonical_key(m.group(1)))
        elif tok.lower() in _ARM_WORDS:
            arm = _ARM_WORDS[tok.lower()]
        elif tok.lower() in _RERUN_WORDS:
            retry = True
    if len(keys) != 1 or arm is None:
        return None
    return {"corpus": corpus or DEFAULT_CORPUS[arm], "key": keys[0],
            "arm": arm, "round": round_num, "retry": retry}


def read_agent_path(path: Path) -> str | None:
    try:
        with path.open(encoding="utf-8") as f:
            rec = json.loads(f.readline())
    except (OSError, json.JSONDecodeError, ValueError):
        return None
    if rec.get("type") != "session_meta":
        return None
    src = (rec.get("payload") or {}).get("source")
    spawn = (src.get("subagent") or {}).get("thread_spawn") if isinstance(src, dict) else None
    return spawn.get("agent_path") if isinstance(spawn, dict) else None


def failure_reason(path: Path, arm: str) -> str | None:
    """Aborted/unfinished run; for baseline also any tool call (contamination:
    the parametric-knowledge arm must not look anything up)."""
    try:
        records = [json.loads(s) for s in path.read_text(encoding="utf-8").splitlines()
                   if s.strip()]
    except (OSError, json.JSONDecodeError) as e:
        return f"unreadable ({e})"
    task_complete = aborted = has_message = False
    abort_reason = None
    tool_calls = set()
    for rec in records:
        p = rec.get("payload") or {}
        if rec.get("type") == "response_item" and p.get("type") == "function_call":
            tool_calls.add(p.get("name") or "?")
        if rec.get("type") != "event_msg":
            continue
        pt = p.get("type")
        if pt == "task_complete":
            task_complete = True
        elif pt == "turn_aborted":
            aborted, abort_reason = True, p.get("reason") or "aborted"
        elif pt == "agent_message" and (p.get("message") or "").strip():
            has_message = True
    if aborted and not task_complete:
        return f"turn_aborted:{abort_reason}"
    if not task_complete:
        return "incomplete_no_response" if not has_message else "incomplete_no_task_complete"
    if arm == "baseline" and tool_calls:
        return "contaminated:" + ",".join(sorted(tool_calls))
    return None


# The run finished but the exported answer is a handoff line ("findings sent to
# the parent"), not the answer itself.
_HANDOFF_MARKERS = (
    "to the parent", "to parent", "parent agent", "findings sent", "sent the",
    "delivered the", "reported findings", "to `/root`",
)


def answer_defect_reason(text: str) -> str | None:
    body = (text or "").strip()
    if not body:
        return "no_answer_text"
    if len(body) < 500 and any(m in body.lower() for m in _HANDOFF_MARKERS):
        return "handoff_no_answer"
    return None


def session_start(path: Path) -> datetime:
    try:
        with path.open(encoding="utf-8") as f:
            for _ in range(50):
                line = f.readline()
                if not line:
                    break
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(rec, dict) and rec.get("timestamp"):
                    dt = parse_ts(rec["timestamp"])
                    if dt is not None:
                        return dt
    except OSError:
        pass
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run-dir", type=Path,
                    required=True, help="run directory to populate")
    ap.add_argument("--questions", type=Path,
                    default=SCRIPT_DIR.parent / "questions.csv")
    ap.add_argument("--min-date", default=None, metavar="YYYY-MM-DD")
    ap.add_argument("--max-date", default=None, metavar="YYYY-MM-DD")
    ap.add_argument("--dry-run", action="store_true", help="report, write nothing")
    args = ap.parse_args()

    questions = load_questions(args.questions)
    date_lo = parse_filter_date(args.min_date) if args.min_date else None
    date_hi = parse_filter_date(args.max_date, end_of_day=True) if args.max_date else None

    files = sorted(SESSIONS.rglob("rollout-*.jsonl"))
    print(f"Scanning {len(files)} Codex session files...")

    # (arm, corpus, key, round) -> [{path, mtime, retry}]  (oldest first)
    slots = defaultdict(list)
    skipped = []
    for path in files:
        agent_path = read_agent_path(path)
        if not agent_path:
            continue
        parsed = parse_agent_path(agent_path)
        if not parsed:
            continue
        if (parsed["corpus"], parsed["key"]) not in questions:
            print(f"warn: {agent_path} names unknown question "
                  f"{parsed['corpus']}-{parsed['key']}", file=sys.stderr)
            continue
        if date_lo or date_hi:
            start = session_start(path)
            if (date_lo and start < date_lo) or (date_hi and start > date_hi):
                continue
        slots[(parsed["arm"], parsed["corpus"], parsed["key"], parsed["round"])].append(
            {"path": path, "mtime": path.stat().st_mtime, "retry": parsed["retry"]})

    collected = []
    for (arm, corpus, key, round_num) in sorted(
            slots, key=lambda k: (k[0], k[1], k[2], k[3] or 0)):
        model = MODEL_FOR_ARM[arm]
        group = sorted(slots[(arm, corpus, key, round_num)], key=lambda h: h["mtime"])
        # A retry supersedes the attempt it repeats in the same slot; keeping
        # both would double-weight the cell.
        if any(h["retry"] for h in group):
            for h in [h for h in group if not h["retry"]]:
                label = f"{corpus}-{key}-r{round_num} {h['path'].name}"
                copy_skipped(h["path"], args.run_dir, model,
                             f"{label}: superseded_by_retry", dry_run=args.dry_run)
                skipped.append(("superseded_by_retry", label))
            group = [h for h in group if h["retry"]]
        for hit in group:
            label = f"{corpus}-{key}-r{round_num} {hit['path'].name}"
            reason = failure_reason(hit["path"], arm)
            if reason is None:
                _, answer = extract_transcript(hit["path"], "codex")
                reason = answer_defect_reason(answer)
            if reason:
                copy_skipped(hit["path"], args.run_dir, model, f"{label}: {reason}",
                             dry_run=args.dry_run)
                skipped.append((reason, label))
                continue
            hit["ok"] = True
        group = [h for h in group if h.get("ok")]
        # Cap at MAX_ROUNDS. The agent_path round is authoritative, so a round
        # beyond the cap is skipped, not renumbered; where several sessions
        # share one slot (or carry no round) the NEWEST win, older extras skip.
        if round_num is not None and round_num > MAX_ROUNDS:
            drop, group = group, []
        elif round_num is not None:
            drop, group = group[:-1], group[-1:]
        else:
            drop, group = group[:-MAX_ROUNDS], group[-MAX_ROUNDS:]
        for h in drop:
            reason = ("over_max_rounds" if round_num is None or round_num > MAX_ROUNDS
                      else "superseded_by_newer")
            label = f"{corpus}-{key}-r{round_num} {h['path'].name}"
            copy_skipped(h["path"], args.run_dir, model, f"{label}: {reason}",
                         dry_run=args.dry_run)
            skipped.append((reason, label))
        for i, hit in enumerate(group, 1):
            rnd = round_num if round_num is not None else i
            run_id = make_run_id(corpus, key, model, arm, rnd)
            copy_run(hit["path"], args.run_dir, model, run_id, dry_run=args.dry_run)
            collected.append({"corpus": corpus, "key": key, "arm": arm,
                              "round": rnd, "run_id": run_id, "model": model})

    dupes = defaultdict(int)
    for r in collected:
        dupes[r["run_id"]] += 1
    by_model = defaultdict(int)
    for r in collected:
        by_model[r["model"]] += 1
    counts = ", ".join(f"{n} -> logs/{m}/" for m, n in sorted(by_model.items()))
    print(f"{'DRY RUN — ' if args.dry_run else ''}collected {len(collected)} runs "
          f"({counts or 'none'})")
    print_grid(collected)
    report_skipped(skipped)
    duplicated = {rid: n for rid, n in dupes.items() if n > 1}
    if duplicated:
        print(f"\nERROR: duplicate run ids (two sessions claim one cell, last "
              f"write wins): {duplicated}", file=sys.stderr)
    return 1 if duplicated or not collected else 0


if __name__ == "__main__":
    raise SystemExit(main())
