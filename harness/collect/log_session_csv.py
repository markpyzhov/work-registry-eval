#!/usr/bin/env python3
"""
Analyze a Claude Code or Codex session log and append one metrics row to a CSV.

Reuses the same accounting as analyze_session.py: rates are looked up per model
from the id the log itself names, so Opus 5 / Opus 4.8 / terra / sol sessions in
one run each price correctly. Each invocation appends a single row; the CSV is
created with a header if it does not exist.

Usage:
    # Whole session -> one row
    python log_session_csv.py <session.jsonl> --csv usage.csv

    # Single prompt -> one row
    python log_session_csv.py <session.jsonl> --csv usage.csv --prompt-index 0

    # Override Codex rates (USD per 1M tokens); unset ones keep model defaults
    python log_session_csv.py <session.jsonl> --csv usage.csv \\
        --price-input 2.0 --price-cached 0.20 --price-cache-write 2.5 \\
        --price-output 12

Session log locations:
  Claude: ~/.claude/projects/*/*.jsonl
  Codex:  ~/.codex/sessions/*/*/*/*.jsonl
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Allow `python path/to/log_session_csv.py` from any cwd.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from analyze_session import (  # noqa: E402
    build_codex_price_override,
    aggregate_results,
    analyze_session,
    detect_format,
    load_records,
)

# Wide schema covering both formats. Unused fields are left empty.
# Optional identity fields (run_id / corpus / key / instance) are filled by
# collect_massive_run.py so CSV rows line up with <corpus>-<key>-<n> filenames.
CSV_FIELDS = [
    "run_id",
    "corpus",
    "key",
    "instance",
    "arm",
    "round",
    "logged_at",
    "session_path",
    "session_id",
    "format",
    "model",
    "prompt_index",
    "num_prompts",
    "prompt",
    "prompt_ts",
    "end_ts",
    "duration_seconds",
    "duration_wall_seconds",
    "approval_wait_seconds",
    "num_steps",
    # Token counts (per type)
    "tokens_input",
    "tokens_cache_read",
    "tokens_cache_write_5m",
    "tokens_cache_write_1h",
    "tokens_cached_input",
    "tokens_uncached_input",
    "tokens_cache_write",
    "tokens_output",
    "tokens_reasoning_output",
    "tokens_total",
    # Spend per token type (USD)
    "spend_input",
    "spend_cache_read",
    "spend_cache_write_5m",
    "spend_cache_write_1h",
    "spend_input_uncached",
    "spend_input_cached",
    "spend_cache_write",
    "spend_output",
    "spend_total",
]


def session_id_from_path(path: str) -> str:
    name = Path(path).name
    if name.endswith(".jsonl"):
        name = name[:-6]
    if name.startswith("rollout-"):
        # rollout-2026-07-22T16-30-43-<uuid>
        parts = name.split("-")
        if len(parts) >= 5:
            return "-".join(parts[-5:])
    return name


def _get(d, *keys, default=""):
    cur = d
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    if cur is None:
        return default
    return cur


def result_to_row(result, session_path: str, prompt_index, meta=None,
                  prompt_override=None) -> dict:
    tokens = result.get("tokens") or {}
    cost = result.get("cost_usd") or {}
    fmt = result.get("format")
    meta = meta or {}
    prompt = (result.get("prompt") or "").strip()
    if not prompt and prompt_override:
        prompt = prompt_override
    if isinstance(prompt, str):
        prompt = prompt.replace("\n", " ").strip()

    row = {k: "" for k in CSV_FIELDS}
    row.update({
        "run_id": meta.get("run_id", ""),
        "corpus": meta.get("corpus", ""),
        "key": meta.get("key", ""),
        "instance": meta.get("instance", ""),
        "arm": meta.get("arm", ""),
        "round": meta.get("round", ""),
        "logged_at": datetime.now(timezone.utc).isoformat(),
        "session_path": os.path.abspath(session_path),
        "session_id": session_id_from_path(session_path),
        "format": fmt or "",
        "model": result.get("model") or "",
        "prompt_index": prompt_index if prompt_index is not None else result.get("prompt_index", ""),
        "num_prompts": result.get("num_prompts", 1),
        "prompt": prompt,
        "prompt_ts": result.get("prompt_ts") or "",
        "end_ts": result.get("end_ts") or "",
        "duration_seconds": (
            f"{result['duration_seconds']:.3f}"
            if result.get("duration_seconds") is not None else ""
        ),
        "duration_wall_seconds": (
            f"{result['duration_wall_seconds']:.3f}"
            if result.get("duration_wall_seconds") is not None else ""
        ),
        "approval_wait_seconds": (
            f"{float(result.get('approval_wait_seconds') or 0):.3f}"
        ),
        "num_steps": result.get("num_steps", ""),
        "tokens_total": tokens.get("total_tokens", ""),
        "spend_total": (
            f"{cost['total']:.8f}" if "total" in cost else ""
        ),
    })

    if fmt == "claude_code":
        row.update({
            "tokens_input": tokens.get("input", 0),
            "tokens_cache_read": tokens.get("cache_read", 0),
            "tokens_cache_write_5m": tokens.get("cache_write_5m", 0),
            "tokens_cache_write_1h": tokens.get("cache_write_1h", 0),
            "tokens_output": tokens.get("output", 0),
            "spend_input": f"{_get(cost, 'input', default=0):.8f}",
            "spend_cache_read": f"{_get(cost, 'cache_read', default=0):.8f}",
            "spend_cache_write_5m": f"{_get(cost, 'cache_write_5m', default=0):.8f}",
            "spend_cache_write_1h": f"{_get(cost, 'cache_write_1h', default=0):.8f}",
            "spend_output": f"{_get(cost, 'output', default=0):.8f}",
        })
    elif fmt == "codex":
        row.update({
            "tokens_input": tokens.get("input", 0),
            "tokens_cached_input": tokens.get("cached_input", 0),
            "tokens_uncached_input": tokens.get("uncached_input", 0),
            "tokens_cache_write": tokens.get("cache_write", 0),
            "tokens_output": tokens.get("output", 0),
            "tokens_reasoning_output": tokens.get("reasoning_output", 0),
            "spend_input_uncached": f"{_get(cost, 'input_uncached', default=0):.8f}",
            "spend_input_cached": f"{_get(cost, 'input_cached', default=0):.8f}",
            "spend_cache_write": f"{_get(cost, 'cache_write', default=0):.8f}",
            "spend_output": f"{_get(cost, 'output', default=0):.8f}",
        })
    return row


def append_csv(csv_path: str, row: dict) -> None:
    path = Path(csv_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not path.exists() or path.stat().st_size == 0
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction="ignore")
        if write_header:
            writer.writeheader()
        writer.writerow(row)


def log_session(
    session_path: str,
    csv_path: str,
    *,
    prompt_index=None,
    codex_prices=None,
    meta=None,
    prompt_override=None,
    dry_run: bool = False,
) -> dict:
    """Analyze a session and append one CSV row. Returns the row dict.

    prompt_override: optional plaintext prompt (e.g. questions.csv text for
    Codex subagents whose NEW_TASK payload is encrypted).
    """
    records = load_records(session_path)
    fmt = detect_format(records)
    # codex_prices stays None unless the caller overrides: rates are then
    # looked up per model, so a terra and a sol session each price correctly.
    fmt, results = analyze_session(
        records, fmt=fmt, prompt_index=prompt_index, codex_prices=codex_prices)
    if not results:
        raise ValueError(f"No user text prompts found (format={fmt})")

    if prompt_index is not None:
        summary = dict(results[0])
        summary["prompt_index"] = prompt_index
        summary["num_prompts"] = 1
        prompt_label = prompt_index
    else:
        summary = aggregate_results(results)
        prompt_label = "all"

    row = result_to_row(
        summary, session_path, prompt_label, meta=meta,
        prompt_override=prompt_override,
    )
    if dry_run:
        return row
    append_csv(csv_path, row)
    return row


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("session", help="path to the .jsonl session log")
    ap.add_argument("--csv", required=True,
                    help="CSV file to append to (created if missing)")
    ap.add_argument("--prompt-index", type=int, default=None,
                    help="0-based prompt index (default: aggregate whole session)")
    ap.add_argument("--run-id", default="", help="optional identity: matches filename stem")
    ap.add_argument("--corpus", default="", help="optional identity field")
    ap.add_argument("--key", default="", help="optional identity field")
    ap.add_argument("--instance", default="", help="optional identity field")
    ap.add_argument("--arm", default="", help="optional scenario/arm label")
    ap.add_argument("--round", default="", help="optional round number")
    ap.add_argument("--prompt", default=None,
                    help="override prompt text (for Codex encrypted NEW_TASK)")
    ap.add_argument("--price-input", type=float, default=None,
                    help="Codex: $/1M uncached input (default: by model)")
    ap.add_argument("--price-cached", type=float, default=None,
                    help="Codex: $/1M cached input (default: by model)")
    ap.add_argument("--price-cache-write", type=float, default=None,
                    help="Codex: $/1M cache write (default: by model)")
    ap.add_argument("--price-output", type=float, default=None,
                    help="Codex: $/1M output (default: by model)")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the row as CSV to stdout without writing")
    args = ap.parse_args()

    codex_prices = build_codex_price_override(args)

    meta = {
        "run_id": args.run_id,
        "corpus": args.corpus,
        "key": args.key,
        "instance": args.instance,
        "arm": args.arm,
        "round": args.round,
    }
    try:
        row = log_session(
            args.session,
            args.csv,
            prompt_index=args.prompt_index,
            codex_prices=codex_prices,
            meta=meta,
            prompt_override=args.prompt,
            dry_run=args.dry_run,
        )
    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        writer = csv.DictWriter(sys.stdout, fieldnames=CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerow(row)
        return

    print(
        f"Appended {row.get('format')}/{row.get('model')} "
        f"run_id={row.get('run_id') or '-'} "
        f"prompt={row.get('prompt_index')} "
        f"tokens={row.get('tokens_total') or 0} "
        f"duration={row.get('duration_seconds')}s "
        f"spend=${row.get('spend_total') or 0} "
        f"-> {args.csv}"
    )


if __name__ == "__main__":
    main()
