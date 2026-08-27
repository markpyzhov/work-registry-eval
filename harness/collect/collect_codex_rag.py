#!/usr/bin/env python3
"""
Collect a `codex exec --json` RAG run into <run-dir>/logs/codex-rag/.

No discovery here: the runner names its own files after their coordinates in a
dedicated directory:

    c1-q01-raw-r1.jsonl          event stream + tracing log
    c1-q01-raw-r1.status         exit code
    c1-q01-raw-r1-retry1.jsonl   a re-run of the same coordinates

So the job is: parse each name, pick the attempt of record, apply the RAG
filters (no answer, non-zero exit, RAG session touched local files / shell —
contamination), and copy. Rejected attempts go to logs/skipped/codex-rag/ with
a .reason.txt sidecar. Rounds beyond MAX_ROUNDS (3) are skipped as well.

Retries: the ORIGINAL attempt wins whenever it produced an answer — a retry is
for technical failures; re-rolling an answer that merely looked wrong biases
the result. Pass --prefer-retry to invert.

Examples
--------
    python collect_codex_rag.py <src> --run-dir results/massive-run-X
    python collect_codex_rag.py <src> --run-dir results/massive-run-X --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from common import (  # noqa: E402
    canonical_arm, canonical_key, copy_run, copy_skipped, load_questions,
    make_run_id, print_grid, report_skipped,
)

MODEL = "codex-rag"
MAX_ROUNDS = 3

# c1-q01-raw-r1.jsonl / c2-a06-wr-r2-retry1.jsonl
NAME_RE = re.compile(
    r"^(?P<corpus>c\d+)-(?P<key>[qa]\d+)-(?P<arm>raw|wr|dir|wrdir)-r(?P<round>\d+)"
    r"(?:-retry(?P<retry>\d+))?$")

# Items that mean the model reached outside its assigned dataset. RAG arms must
# show none of these.
LOCAL_ITEM_TYPES = frozenset({
    "command_execution", "local_shell_call", "file_change", "patch_apply",
    "web_search",
})


def scan_log(path: Path) -> dict:
    """Minimal read of a `codex exec --json` capture: answer + tool activity.

    `turn_completed` is the log's own end-of-run event; an attempt without it
    was interrupted mid-run, whatever its status file says.
    """
    response, tool_calls, local_items, turn_completed = "", 0, set(), False
    with path.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("{"):
                continue  # interleaved stderr tracing lines
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            if ev.get("type") == "turn.completed":
                turn_completed = True
            if ev.get("type") != "item.completed":
                continue
            item = ev.get("item") or {}
            itype = item.get("type")
            if itype == "agent_message":
                response = item.get("text") or ""
            elif itype == "mcp_tool_call":
                tool_calls += 1
            elif itype in LOCAL_ITEM_TYPES:
                local_items.add(itype)
    return {"response": response.strip(), "tool_calls": tool_calls,
            "local_items": sorted(local_items), "turn_completed": turn_completed}


def read_status(jsonl_path: Path):
    status_path = jsonl_path.with_suffix(".status")
    if not status_path.exists():
        return None
    text = status_path.read_text(encoding="utf-8").strip()
    return int(text) if text.isdigit() else text or None


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", type=Path, help="directory written by the codex runner")
    ap.add_argument("--run-dir", type=Path,
                    required=True, help="run directory to populate")
    ap.add_argument("--questions", type=Path,
                    default=SCRIPT_DIR.parent / "questions.csv")
    ap.add_argument("--prefer-retry", action="store_true",
                    help="keep the newest attempt instead of the original")
    ap.add_argument("--dry-run", action="store_true", help="report, write nothing")
    args = ap.parse_args()
    if not args.src.is_dir():
        ap.error(f"not a directory: {args.src}")

    questions = load_questions(args.questions)

    # Group attempts by coordinates.
    attempts = defaultdict(list)
    skipped = []
    for path in sorted(args.src.glob("*.jsonl")):
        m = NAME_RE.match(path.stem)
        if not m:
            skipped.append(("unparsed_filename", path.name))
            copy_skipped(path, args.run_dir, MODEL, f"{path.name}: unparsed_filename",
                         dry_run=args.dry_run)
            continue
        g = m.groupdict()
        # Rounds here are authoritative (the runner named the file), so a
        # round beyond the cap is skipped, not renumbered.
        if int(g["round"]) > MAX_ROUNDS:
            copy_skipped(path, args.run_dir, MODEL,
                         f"{path.name}: over_max_rounds", dry_run=args.dry_run)
            skipped.append(("over_max_rounds", path.name))
            continue
        coords = (g["corpus"], canonical_key(g["key"]),
                  canonical_arm(g["arm"]), g["round"])
        attempts[coords].append({"path": path, "retry": int(g["retry"] or 0),
                                 "status": read_status(path), "log": scan_log(path)})

    collected = []
    for coords in sorted(attempts):
        corpus, key, arm, round_ = coords
        group = sorted(attempts[coords], key=lambda a: a["retry"],
                       reverse=args.prefer_retry)

        def usable(a):
            return (a["log"]["response"] and a["log"]["turn_completed"]
                    and a["status"] in (0, None))

        chosen = next((a for a in group if usable(a)), group[0])
        for other in group:
            if other is chosen:
                continue
            label = f"retry{other['retry']}" if other["retry"] else "original"
            copy_skipped(other["path"], args.run_dir, MODEL,
                         f"{other['path'].name}: superseded ({label})",
                         dry_run=args.dry_run)
            skipped.append(("superseded", other["path"].name))

        # RAG-specific filters on the attempt of record.
        log = chosen["log"]
        reason = None
        if not log["response"]:
            reason = "no_answer"
        elif not log["turn_completed"]:
            reason = "interrupted_no_turn_completed"
        elif chosen["status"] not in (0, None):
            reason = f"exit={chosen['status']}"
        elif log["local_items"]:
            reason = "contaminated:" + ",".join(log["local_items"])
        if reason:
            copy_skipped(chosen["path"], args.run_dir, MODEL,
                         f"{chosen['path'].name}: {reason}", dry_run=args.dry_run)
            skipped.append((reason, chosen["path"].name))
            continue
        if not log["tool_calls"]:
            print(f"warn: {chosen['path'].name}: no retrieval calls", file=sys.stderr)
        if (corpus, key) not in questions:
            print(f"warn: {chosen['path'].name}: {corpus}-{key} not in questions.csv",
                  file=sys.stderr)

        run_id = make_run_id(corpus, key, MODEL, arm, round_)
        copy_run(chosen["path"], args.run_dir, MODEL, run_id, dry_run=args.dry_run)
        collected.append({"corpus": corpus, "key": key, "arm": arm,
                          "round": round_, "run_id": run_id})

    print(f"{'DRY RUN — ' if args.dry_run else ''}collected {len(collected)} runs "
          f"-> {args.run_dir}/logs/{MODEL}/")
    print_grid(collected)
    report_skipped(skipped)
    return 0 if collected else 1


if __name__ == "__main__":
    raise SystemExit(main())
