#!/usr/bin/env python3
"""
Parse collected Codex logs: markdown transcripts + usage.csv rows.

Covers both Codex log formats in one pass over a run directory:

    logs/codex-dir/<run_id>.jsonl        rollout sessions (~/.codex/sessions)
    logs/codex-baseline/<run_id>.jsonl   rollout sessions (~/.codex/sessions)
    logs/codex-rag/<run_id>.jsonl        `codex exec --json` event streams

For each log it writes the sibling <run_id>.md that scoring reads and upserts
one metrics row into <run-dir>/usage.csv. The markdown headline comes from
questions.csv (the subagent NEW_TASK prompt is encrypted; the exec stream
carries no prompt).

The exec stream does not record its model, so --rag-model names it (pricing).

Examples
--------
    python parse_codex.py --run-dir results/massive-run-X
    python parse_codex.py --run-dir results/massive-run-X --rag-model gpt-5.6-terra
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from analyze_session import (  # noqa: E402
    aggregate_results, analyze_session, load_records, openai_prices, parse_ts,
)
from log_session_csv import CSV_FIELDS, result_to_row  # noqa: E402
from transcript import extract_transcript  # noqa: E402

from common import (  # noqa: E402
    load_questions, parse_run_id, upsert_usage, write_markdown,
)

USAGE_FIELDS = CSV_FIELDS + ["tool"]

# --------------------------------------------------------------------------- #
# `codex exec --json` parsing (codex-rag logs)
# --------------------------------------------------------------------------- #

# The runner redirected stdout (JSON events) and stderr (tracing log) into one
# file; timings come from the stderr timestamps, the events carry none.
_STDERR_TS_RE = re.compile(r"^(\d{4}-\d\d-\d\dT[\d:.]+Z)\s")


def exec_summary(path: Path, model: str) -> dict:
    """Parse an exec capture into the analyze_session result shape, so the
    same CSV row builder serves both formats."""
    events, stamps = [], []
    with path.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            if m := _STDERR_TS_RE.match(line):
                stamps.append(m.group(1))
                continue
            s = line.strip()
            if not s.startswith("{"):
                continue
            try:
                events.append(json.loads(s))
            except json.JSONDecodeError:
                continue

    response, usage, tool_calls = "", {}, 0
    for ev in events:
        etype = ev.get("type")
        if etype == "turn.completed":
            usage = ev.get("usage") or {}
        elif etype == "item.completed":
            item = ev.get("item") or {}
            if item.get("type") == "agent_message":
                response = item.get("text") or ""
            elif item.get("type") == "mcp_tool_call":
                tool_calls += 1

    inp = int(usage.get("input_tokens", 0) or 0)
    cached = int(usage.get("cached_input_tokens", 0) or 0)
    tokens = {
        "input": inp,
        "cached_input": cached,
        "uncached_input": inp - cached,
        "cache_write": int(usage.get("cache_write_input_tokens", 0) or 0),
        "output": int(usage.get("output_tokens", 0) or 0),
        "reasoning_output": int(usage.get("reasoning_output_tokens", 0) or 0),
    }
    tokens["total_tokens"] = inp + tokens["output"]

    prices, pricing_model = openai_prices(model)
    cost = {
        "input_uncached": tokens["uncached_input"] / 1e6 * prices["input"],
        "input_cached": tokens["cached_input"] / 1e6 * prices["cached"],
        "cache_write": tokens["cache_write"] / 1e6 * prices.get("cache_write", 0.0),
        "output": tokens["output"] / 1e6 * prices["output"],
    }
    cost["total"] = sum(cost.values())

    start = parse_ts(stamps[0]) if stamps else None
    end = parse_ts(stamps[-1]) if stamps else None
    wall = (end - start).total_seconds() if (start and end) else None
    return {
        "format": "codex",
        "model": model,
        "prompt": "",
        "prompt_ts": start.isoformat() if start else "",
        "end_ts": end.isoformat() if end else "",
        "duration_seconds": wall,
        "duration_wall_seconds": wall,
        "approval_wait_seconds": 0.0,
        # One exec invocation is one turn; the tool calls it took are the
        # comparable step count across arms.
        "num_steps": tool_calls,
        "tokens": tokens,
        "cost_usd": cost,
        "response": response.strip(),
    }


# --------------------------------------------------------------------------- #
# Parse one model directory
# --------------------------------------------------------------------------- #

def parse_dir(run_dir: Path, model: str, questions: dict, *,
              rag_model: str) -> tuple[list[dict], list[str]]:
    rows, errors = [], []
    for jsonl in sorted((run_dir / "logs" / model).glob("*.jsonl")):
        run_id = jsonl.stem
        coords = parse_run_id(run_id)
        if not coords:
            errors.append(f"{jsonl.name}: filename is not a run_id")
            continue
        question = questions.get((coords["corpus"], coords["key"]), "")

        try:
            if model == "codex-rag":
                summary = exec_summary(jsonl, rag_model)
                response = summary["response"]
            else:
                records = load_records(jsonl)
                _, results = analyze_session(records, fmt="codex")
                summary = aggregate_results(results)
                _, response = extract_transcript(jsonl, "codex")
        except (ValueError, OSError) as e:
            errors.append(f"{jsonl.name}: {e}")
            continue

        write_markdown(jsonl.with_suffix(".md"), question, response)
        row = result_to_row(summary, str(jsonl), "all", meta={
            "run_id": run_id, "corpus": coords["corpus"], "key": coords["key"],
            "instance": coords["round"], "arm": coords["arm"],
            "round": coords["round"],
        }, prompt_override=question)
        row["session_id"] = run_id
        row["tool"] = model
        rows.append(row)
    return rows, errors


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run-dir", type=Path, required=True,
                    help="run directory (holds logs/codex-dir/ and/or logs/codex-rag/)")
    ap.add_argument("--questions", type=Path,
                    default=SCRIPT_DIR.parent / "questions.csv")
    ap.add_argument("--rag-model", default="gpt-5.6-terra",
                    help="model the exec runner used (not recorded in the stream)")
    args = ap.parse_args()

    questions = load_questions(args.questions)
    rows, errors = [], []
    for model in ("codex-dir", "codex-baseline", "codex-rag"):
        r, e = parse_dir(args.run_dir, model, questions, rag_model=args.rag_model)
        rows += r
        errors += e
        if r:
            print(f"parsed {len(r)} {model} runs")
    if not rows:
        print(f"no logs found under {args.run_dir}/logs/codex-*/", file=sys.stderr)
        return 1
    stats = upsert_usage(args.run_dir / "usage.csv", rows, USAGE_FIELDS)
    print(f"usage.csv: +{stats['added']} new, {stats['replaced']} replaced, "
          f"{stats['total']} total")
    for e in errors:
        print(f"error: {e}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
