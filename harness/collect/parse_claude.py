#!/usr/bin/env python3
"""
Parse collected Claude logs: markdown transcripts + usage.csv rows.

Reads every <run-dir>/logs/claude/<run_id>.jsonl (written by collect_claude.py),
writes the sibling <run_id>.md that scoring reads, and upserts one metrics row
per run into <run-dir>/usage.csv (tokens, spend, duration — via analyze_session).

Safe to re-run: rows are keyed by run_id, markdown is rewritten in place.

Examples
--------
    python parse_claude.py --run-dir results/massive-run-X
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from analyze_session import aggregate_results, analyze_session, load_records  # noqa: E402
from log_session_csv import CSV_FIELDS, result_to_row  # noqa: E402
from transcript import extract_transcript  # noqa: E402

from common import (  # noqa: E402
    load_questions, parse_run_id, upsert_usage, write_markdown,
)

MODEL = "claude"
USAGE_FIELDS = CSV_FIELDS + ["tool"]


def parse_dir(run_dir: Path, questions: dict) -> tuple[list[dict], list[str]]:
    rows, errors = [], []
    for jsonl in sorted((run_dir / "logs" / MODEL).glob("*.jsonl")):
        run_id = jsonl.stem
        coords = parse_run_id(run_id)
        if not coords:
            errors.append(f"{jsonl.name}: filename is not a run_id")
            continue
        question = questions.get((coords["corpus"], coords["key"]), "")
        try:
            records = load_records(jsonl)
            _, results = analyze_session(records, fmt="claude_code")
            summary = aggregate_results(results)
        except (ValueError, OSError) as e:
            errors.append(f"{jsonl.name}: {e}")
            continue
        prompt, response = extract_transcript(jsonl, "claude",
                                              prompt_override=question or None)
        write_markdown(jsonl.with_suffix(".md"), prompt, response)
        row = result_to_row(summary, str(jsonl), "all", meta={
            "run_id": run_id, "corpus": coords["corpus"], "key": coords["key"],
            "instance": coords["round"], "arm": coords["arm"],
            "round": coords["round"],
        }, prompt_override=question or prompt)
        row["session_id"] = run_id
        row["tool"] = MODEL
        rows.append(row)
    return rows, errors


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run-dir", type=Path, required=True,
                    help="run directory (holds logs/claude/)")
    ap.add_argument("--questions", type=Path,
                    default=SCRIPT_DIR.parent / "questions.csv")
    args = ap.parse_args()

    questions = load_questions(args.questions)
    rows, errors = parse_dir(args.run_dir, questions)
    if not rows:
        print(f"no logs found under {args.run_dir}/logs/{MODEL}/", file=sys.stderr)
        return 1
    stats = upsert_usage(args.run_dir / "usage.csv", rows, USAGE_FIELDS)
    print(f"parsed {len(rows)} runs -> md + usage.csv "
          f"(+{stats['added']} new, {stats['replaced']} replaced, "
          f"{stats['total']} total)")
    for e in errors:
        print(f"error: {e}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
