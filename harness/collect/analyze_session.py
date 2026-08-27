#!/usr/bin/env python3
"""
Analyze an agent session log (.jsonl) to compute the tokens and wall-clock time
spent answering a prompt. Two log formats are auto-detected:

  * "claude_code" -- Claude Code sessions (Anthropic / Opus-family).
        Lines: type=user|assistant with a message.usage object.
        Paths: ~/.claude/projects/*/*.jsonl
  * "codex" -- Codex sessions (OpenAI / GPT-5-family, originator=codex_*).
        Lines: type=event_msg with payload.type=token_count | user_message | ...
        Paths: ~/.codex/sessions/*/*/*/*.jsonl

Usage:
    python analyze_session.py <session.jsonl> [--prompt-index N] [--json]
    python analyze_session.py <session.jsonl> --price-input 2.0 --price-cached 0.20 \\
        --price-output 12 --price-cache-write 2.5

Why each format needs its own accounting:

  Claude Code
    - A user text prompt is a `type:"user"` line whose message.content has a
      `text` block (role=user tool results carry `tool_result` blocks instead).
    - Answering a prompt takes several agentic *steps*, one per API request,
      each a unique assistant `message.id`. The harness writes that message once
      per content block with the SAME final `usage`, so we DEDUPE by message.id.
    - Step tokens = input + cache_read + cache_creation(1h/5m) + output, priced
      with the rates of the model the log names (cache 1h/5m billed
      differently). See ANTHROPIC_PRICING.

  Codex
    - Token usage lives in `event_msg`/`token_count` events.
      `total_token_usage` is cumulative session spend; `last_token_usage` is the
      intended per-step delta. Some events repeat a stale `last_token_usage`
      without advancing the cumulative total, so we take the delta of
      `total_token_usage` across the prompt span (not the sum of lasts).
    - `input_tokens` INCLUDES `cached_input_tokens`; `output_tokens` INCLUDES
      `reasoning_output_tokens` -- so uncached_input = input - cached.
    - Dollar cost uses the Standard API rates of the model named in the log's
      turn_context (see OPENAI_PRICING); override with --price-* flags.

Time = from the prompt's timestamp to the last assistant activity of that
prompt (up to just before the next user prompt). Claude Code human-gate waits
(permission reject / permission-stream failure / AskUserQuestion) are subtracted
from duration_seconds; duration_wall_seconds keeps the raw span. Codex session
logs do not expose approval grant timestamps, so no wait is subtracted there.
"""

import argparse
import json
import sys
from datetime import datetime, timezone

# --------------------------------------------------------------------------- #
# Pricing, USD per 1,000,000 tokens. Verified against the vendors' own pages on
# 2026-08-18; both are keyed BY MODEL because a single run mixes models (the
# benchmark used Opus 4.8 / gpt-5.6-terra, current sessions use Opus 5) and the
# tiers differ by up to 2.5x. Cost is always priced with the model the log says
# produced it, never with a global default.
# --------------------------------------------------------------------------- #

# Anthropic (claude.com/pricing#api). Per model: cache read is 0.1x input, the
# public page's cache-write figure is the 5-minute TTL (1.25x input), and
# extended 1h writes are 2x input. Opus 5 is priced identically to Opus 4.8, so
# the Opus rows below are the same numbers under different ids.
ANTHROPIC_PRICING = {
    # model: (input, output, cache_read, cache_write_5m, cache_write_1h)
    "claude-opus-5":     (5.00, 25.00, 0.50, 6.25, 10.00),
    "claude-opus-4-8":   (5.00, 25.00, 0.50, 6.25, 10.00),
    "claude-opus-4-7":   (5.00, 25.00, 0.50, 6.25, 10.00),
    "claude-opus-4-6":   (5.00, 25.00, 0.50, 6.25, 10.00),
    "claude-fable-5":    (10.00, 50.00, 1.00, 12.50, 20.00),
    "claude-mythos-5":   (10.00, 50.00, 1.00, 12.50, 20.00),
    "claude-sonnet-5":   (2.00, 10.00, 0.20, 2.50, 4.00),
    "claude-sonnet-4-6": (3.00, 15.00, 0.30, 3.75, 6.00),
    "claude-haiku-4-5":  (1.00, 5.00, 0.10, 1.25, 2.00),
}

# OpenAI Standard tier (https://developers.openai.com/api/docs/pricing).
# Cached input is 0.1x input, explicit cache write 1.25x. These are the
# Standard (non-batch, non-flex, non-fast, short-context) rates, which is what
# an interactive Codex session bills at.
OPENAI_PRICING = {
    # model: (input, cached, cache_write, output)
    "gpt-5.6-sol":   (5.00, 0.50, 6.25, 30.00),
    "gpt-5.6-terra": (2.00, 0.20, 2.50, 12.00),
    "gpt-5.6-luna":  (0.20, 0.02, 0.25, 1.20),
}

_ANTHROPIC_KEYS = ("input", "output", "cache_read", "cache_write_5m", "cache_write_1h")
_OPENAI_KEYS = ("input", "cached", "cache_write", "output")

DEFAULT_CODEX_MODEL = "gpt-5.6-terra"
DEFAULT_CLAUDE_MODEL = "claude-opus-5"


def _lookup_prices(model, table, keys, default_model):
    """Return (prices_dict, pricing_label) for `model` from a pricing table.

    Falls back to the longest matching id prefix (so a dated or suffixed
    variant still prices correctly), then to `default_model`. The label names
    the row actually used, so a fallback is visible in output instead of being
    silently priced as something else.
    """
    name = (model or "").strip()
    row = table.get(name)
    if row is None:
        matches = [k for k in table if name.startswith(k)]
        if matches:
            name = max(matches, key=len)
            row = table[name]
    if row is None:
        name = default_model
        row = table[name]
    return dict(zip(keys, row)), name


def anthropic_prices(model):
    return _lookup_prices(model, ANTHROPIC_PRICING, _ANTHROPIC_KEYS,
                          DEFAULT_CLAUDE_MODEL)


def openai_prices(model):
    return _lookup_prices(model, OPENAI_PRICING, _OPENAI_KEYS,
                          DEFAULT_CODEX_MODEL)


def build_codex_price_override(args):
    """Collect --price-* flags into a partial override dict, or None.

    Only the flags actually passed appear; the rest keep the model's own rates.
    """
    override = {}
    for flag, key in (("price_input", "input"), ("price_cached", "cached"),
                      ("price_cache_write", "cache_write"),
                      ("price_output", "output")):
        val = getattr(args, flag, None)
        if val is not None:
            override[key] = val
    return override or None


_IDE_CONTEXT_PREFIX = "# Context from my IDE setup:"
_IDE_REQUEST_MARKER = "## My request for Codex:"


def unwrap_prompt(text):
    """Extract the actual request from the IDE context wrapper, when present."""
    text = text.strip()
    if text.startswith(_IDE_CONTEXT_PREFIX) and _IDE_REQUEST_MARKER in text:
        return text.split(_IDE_REQUEST_MARKER, 1)[1].strip()
    return text


def parse_ts(s):
    """Parse an ISO-8601 timestamp like '2026-07-07T10:28:07.898Z'."""
    if not s:
        return None
    return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc)


def load_records(path):
    records = []
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"warn: skipping unparseable line {i}: {e}", file=sys.stderr)
    return records


def detect_format(records):
    """Return 'codex' or 'claude_code' based on record shapes."""
    for r in records:
        t = r.get("type")
        if t in ("session_meta", "response_item", "turn_context"):
            return "codex"
        if t == "event_msg":
            return "codex"
        if t in ("user", "assistant") and isinstance(r.get("message"), dict):
            return "claude_code"
    # Fallback: if any record carries message.usage -> claude_code
    for r in records:
        msg = r.get("message")
        if isinstance(msg, dict) and isinstance(msg.get("usage"), dict):
            return "claude_code"
    return "claude_code"


# --------------------------------------------------------------------------- #
# Claude Code
# --------------------------------------------------------------------------- #

def cc_is_user_prompt(rec):
    if rec.get("type") != "user":
        return False
    msg = rec.get("message")
    if not isinstance(msg, dict):
        return False
    content = msg.get("content")
    if isinstance(content, str):
        return content.strip() != ""
    if isinstance(content, list):
        return any(isinstance(b, dict) and b.get("type") == "text" for b in content)
    return False


def cc_prompt_text(rec):
    content = rec["message"].get("content")
    if isinstance(content, str):
        return unwrap_prompt(content)
    for b in content:
        if isinstance(b, dict) and b.get("type") == "text":
            return unwrap_prompt(b.get("text", ""))
    return ""


def cc_find_spans(records):
    idxs = [i for i, r in enumerate(records) if cc_is_user_prompt(r)]
    return [(s, idxs[k + 1] if k + 1 < len(idxs) else len(records))
            for k, s in enumerate(idxs)]


# Human-gate tools: the tool_use -> tool_result gap is waiting on the user,
# not model/tool work. AskUserQuestion is always a human wait; Bash/Edit/etc.
# only count when the result is an explicit reject / permission failure
# (approved tools do not log a grant timestamp, so approval+execution cannot
# be separated and those gaps are left in wall-clock time).
_CC_ALWAYS_HUMAN_GATE_TOOLS = frozenset({"AskUserQuestion"})


def _cc_tool_result_text(rec):
    """Flatten tool result text from a user record."""
    parts = []
    tr = rec.get("toolUseResult")
    if isinstance(tr, str):
        parts.append(tr)
    elif isinstance(tr, dict):
        for k in ("message", "error", "content", "text"):
            v = tr.get(k)
            if isinstance(v, str):
                parts.append(v)
    msg = rec.get("message") if isinstance(rec.get("message"), dict) else None
    content = msg.get("content") if msg else None
    if isinstance(content, list):
        for b in content:
            if isinstance(b, dict) and b.get("type") == "tool_result":
                c = b.get("content")
                if isinstance(c, str):
                    parts.append(c)
                elif isinstance(c, list):
                    for sub in c:
                        if isinstance(sub, dict) and isinstance(sub.get("text"), str):
                            parts.append(sub["text"])
    return "\n".join(parts)


def _cc_is_permission_outcome(text):
    """True when the tool_result is a permission reject / stream failure."""
    if not text:
        return False
    t = text.strip()
    if t == "User rejected tool use" or t.startswith("User rejected"):
        return True
    if "Tool permission request failed" in text:
        return True
    return False


def cc_human_gate_waits(records, start, end):
    """
    Find tool_use -> tool_result intervals that are human approval / Q&A waits.

    Returns list of dicts: {start, end, seconds, tool, reason}.
    """
    pending = {}  # tool_use_id -> {ts, name}
    waits = []

    for rec in records[start:end]:
        ts = parse_ts(rec.get("timestamp"))
        msg = rec.get("message") if isinstance(rec.get("message"), dict) else None
        content = msg.get("content") if msg else None

        if rec.get("type") == "assistant" and isinstance(content, list):
            for b in content:
                if not (isinstance(b, dict) and b.get("type") == "tool_use"):
                    continue
                tid = b.get("id")
                if tid and ts is not None:
                    pending[tid] = {"ts": ts, "name": b.get("name") or ""}
            continue

        if rec.get("type") != "user" or not isinstance(content, list) or ts is None:
            continue

        result_text = _cc_tool_result_text(rec)
        is_perm = _cc_is_permission_outcome(result_text)
        for b in content:
            if not (isinstance(b, dict) and b.get("type") == "tool_result"):
                continue
            tid = b.get("tool_use_id")
            meta = pending.pop(tid, None) if tid else None
            if not meta:
                continue
            name = meta["name"]
            reason = None
            if name in _CC_ALWAYS_HUMAN_GATE_TOOLS:
                reason = "ask_user"
            elif is_perm:
                reason = "permission_reject" if "rejected" in result_text.lower() \
                    else "permission_failed"
            if not reason:
                continue
            seconds = (ts - meta["ts"]).total_seconds()
            if seconds > 0:
                waits.append({
                    "start": meta["ts"].isoformat(),
                    "end": ts.isoformat(),
                    "seconds": seconds,
                    "tool": name,
                    "reason": reason,
                })
    return waits


def cc_detect_model(records, start=0, end=None):
    """Model id of the first REAL assistant message in the span, else None.

    Skips <synthetic> and API-error records: those carry a placeholder model
    that is not what the run was billed at.
    """
    for rec in records[start:end]:
        if rec.get("isApiErrorMessage"):
            continue
        msg = rec.get("message")
        if not isinstance(msg, dict) or msg.get("role") != "assistant":
            continue
        model = msg.get("model")
        if model and model != "<synthetic>":
            return model
    return None


def cc_analyze_span(records, start, end, prices=None, model=None):
    prompt_rec = records[start]
    prompt_ts = parse_ts(prompt_rec.get("timestamp"))
    override = prices
    model = model or cc_detect_model(records, start, end)
    prices, pricing_model = anthropic_prices(model)
    if override:
        prices.update(override)
        pricing_model = "custom"

    steps, order = {}, []
    last_ts = prompt_ts
    for rec in records[start:end]:
        ts = parse_ts(rec.get("timestamp"))
        msg = rec.get("message")
        if not isinstance(msg, dict) or msg.get("role") != "assistant":
            continue
        if ts is not None and (last_ts is None or ts > last_ts):
            last_ts = ts
        mid, usage = msg.get("id"), msg.get("usage")
        # A streamed response repeats one message id across records with
        # evolving usage snapshots: the first carries output_tokens=1..3, the
        # final one the real count (input/cache fields are stable throughout).
        # Keep the snapshot with the largest output — first-wins undercounts
        # output by orders of magnitude. Some messages never get their final
        # snapshot logged; nothing in the log recovers those.
        if mid and usage:
            if mid not in steps:
                steps[mid] = usage
                order.append(mid)
            elif (usage.get("output_tokens") or 0) > \
                 (steps[mid].get("output_tokens") or 0):
                steps[mid] = usage

    totals = {k: 0 for k in ("input", "output", "cache_read",
                             "cache_write_5m", "cache_write_1h")}
    per_step = []
    for mid in order:
        u = steps[mid]
        cc = u.get("cache_creation") or {}
        w1h = cc.get("ephemeral_1h_input_tokens", 0)
        w5m = cc.get("ephemeral_5m_input_tokens", 0)
        if not cc and u.get("cache_creation_input_tokens"):
            w5m = u["cache_creation_input_tokens"]
        step = {
            "id": mid,
            "input": u.get("input_tokens", 0),
            "output": u.get("output_tokens", 0),
            "cache_read": u.get("cache_read_input_tokens", 0),
            "cache_write_5m": w5m,
            "cache_write_1h": w1h,
        }
        per_step.append(step)
        for k in totals:
            totals[k] += step[k]
    totals["total_tokens"] = sum(totals[k] for k in
                                 ("input", "output", "cache_read",
                                  "cache_write_5m", "cache_write_1h"))

    cost = {k: totals[k] / 1_000_000 * prices[k] for k in _ANTHROPIC_KEYS}
    cost["total"] = sum(cost.values())

    wall = (last_ts - prompt_ts).total_seconds() if (prompt_ts and last_ts) else None
    waits = cc_human_gate_waits(records, start, end)
    # Only subtract waits that fall inside the measured wall-clock window.
    approval_wait = 0.0
    if wall is not None and prompt_ts and last_ts:
        for w in waits:
            w0, w1 = parse_ts(w["start"]), parse_ts(w["end"])
            if not w0 or not w1:
                continue
            lo = max(w0, prompt_ts)
            hi = min(w1, last_ts)
            if hi > lo:
                approval_wait += (hi - lo).total_seconds()
    dur = max(0.0, wall - approval_wait) if wall is not None else None
    return {
        "format": "claude_code",
        "model": model or DEFAULT_CLAUDE_MODEL,
        "pricing_model": pricing_model,
        "prompt": cc_prompt_text(prompt_rec),
        "prompt_ts": prompt_ts.isoformat() if prompt_ts else None,
        "end_ts": last_ts.isoformat() if last_ts else None,
        "duration_seconds": dur,
        "duration_wall_seconds": wall,
        "approval_wait_seconds": approval_wait,
        "approval_waits": waits,
        "num_steps": len(order),
        "tokens": totals,
        "cost_usd": cost,
        "steps": per_step,
    }


# --------------------------------------------------------------------------- #
# Codex
# --------------------------------------------------------------------------- #

_CX_TOKEN_KEYS = (
    "input_tokens",
    "cached_input_tokens",
    "cache_write_input_tokens",
    "output_tokens",
    "reasoning_output_tokens",
    "total_tokens",
)


def _cx_usage_dict(usage):
    usage = usage or {}
    return {k: int(usage.get(k, 0) or 0) for k in _CX_TOKEN_KEYS}


def _cx_zero_usage():
    return {k: 0 for k in _CX_TOKEN_KEYS}


def cx_is_user_prompt(rec):
    p = rec.get("payload")
    return (rec.get("type") == "event_msg" and isinstance(p, dict)
            and p.get("type") == "user_message")


def cx_prompt_text(rec):
    return unwrap_prompt(rec["payload"].get("message") or "")


def cx_has_token_usage(records):
    for rec in records:
        p = rec.get("payload")
        if (rec.get("type") == "event_msg" and isinstance(p, dict)
                and p.get("type") == "token_count"
                and (p.get("info") or {}).get("total_token_usage")):
            return True
    return False


def cx_find_spans(records):
    idxs = [i for i, r in enumerate(records) if cx_is_user_prompt(r)]
    if idxs:
        return [(s, idxs[k + 1] if k + 1 < len(idxs) else len(records))
                for k, s in enumerate(idxs)]
    # Multi-agent Codex subagent sessions receive an encrypted NEW_TASK and often
    # have no user_message events. Treat the whole file as one span when usage
    # counters are present.
    if records and cx_has_token_usage(records):
        return [(0, len(records))]
    return []


def cx_detect_model(records, start=0, end=None):
    """Best-effort model name from nearby turn_context records."""
    if end is None:
        end = len(records)
    # Prefer turn_context inside / just before the span.
    for rec in records[start:end]:
        if rec.get("type") == "turn_context":
            model = (rec.get("payload") or {}).get("model")
            if model:
                return model
    for rec in reversed(records[:start]):
        if rec.get("type") == "turn_context":
            model = (rec.get("payload") or {}).get("model")
            if model:
                return model
        if rec.get("type") == "session_meta":
            break
    return DEFAULT_CODEX_MODEL


def cx_usage_start(records, start, end):
    """Index where THIS span's own token accounting begins.

    A resumed Codex rollout replays the prior session's history into the file,
    so `total_token_usage` at the end is cumulative for the whole codex session,
    not for this prompt. The subagent handoff
    (`inter_agent_communication_metadata`) marks where this span's real work
    starts; everything before it is replay. Anchoring the usage baseline there
    keeps a resumed session from being billed for its predecessors.

    Returns `start` when there is no handoff marker (fresh, non-subagent
    rollouts), so unaffected sessions are untouched.
    """
    for i in range(end - 1, start - 1, -1):
        if records[i].get("type") == "inter_agent_communication_metadata":
            return i
    return start


def cx_last_total_before(records, start):
    """Cumulative total_token_usage just before index `start`."""
    for rec in reversed(records[:start]):
        p = rec.get("payload")
        if not (rec.get("type") == "event_msg" and isinstance(p, dict)
                and p.get("type") == "token_count"):
            continue
        info = p.get("info") or {}
        if info.get("total_token_usage"):
            return _cx_usage_dict(info["total_token_usage"])
    return _cx_zero_usage()


def cx_analyze_span(records, start, end, prices=None, model=None):
    prompt_rec = records[start]
    usage_start = cx_usage_start(records, start, end)
    override = prices
    model = model or cx_detect_model(records, start, end)
    # `prices` may be a PARTIAL override: unspecified rates still come from the
    # model's own row, so `--price-output 20` doesn't silently reprice input.
    prices, pricing_model = openai_prices(model)
    if override:
        prices.update(override)
        pricing_model = "custom"

    if cx_is_user_prompt(prompt_rec):
        prompt_ts = parse_ts(prompt_rec.get("timestamp"))
        prompt = cx_prompt_text(prompt_rec)
    else:
        # Whole-session / subagent span: no plaintext user_message.
        prompt = ""
        prompt_ts = None
        for rec in records[start:end]:
            prompt_ts = parse_ts(rec.get("timestamp"))
            if prompt_ts is not None:
                break

    # Token accounting and subagent timing start after replayed history. A
    # resumed rollout may replay a user_message, so this applies to both span
    # shapes above.
    if usage_start > start:
        for rec in records[usage_start:end]:
            prompt_ts = parse_ts(rec.get("timestamp"))
            if prompt_ts is not None:
                break
    base = cx_last_total_before(records, usage_start)
    last_total = dict(base)
    per_step = []
    last_ts = prompt_ts
    rate_limits = None
    model_window = None
    n_token_events = 0

    for i, rec in enumerate(records[start:end], start=start):
        ts = parse_ts(rec.get("timestamp"))
        if ts is not None and (last_ts is None or ts > last_ts):
            last_ts = ts
        p = rec.get("payload")
        if not (rec.get("type") == "event_msg" and isinstance(p, dict)
                and p.get("type") == "token_count"):
            continue
        if i < usage_start:
            continue  # replayed history from a prior prompt in this session
        info = p.get("info") or {}
        if p.get("rate_limits"):
            rate_limits = p["rate_limits"]
        model_window = info.get("model_context_window", model_window)
        tu = info.get("total_token_usage")
        if not tu:
            continue
        n_token_events += 1
        cur = _cx_usage_dict(tu)
        delta = {k: cur[k] - last_total[k] for k in _CX_TOKEN_KEYS}
        # Only record a step when the cumulative total advanced. Stale
        # last_token_usage events leave total unchanged and must be ignored.
        if any(delta[k] for k in _CX_TOKEN_KEYS):
            per_step.append({
                "input": delta["input_tokens"],
                "cached_input": delta["cached_input_tokens"],
                "cache_write": delta["cache_write_input_tokens"],
                "output": delta["output_tokens"],
                "reasoning_output": delta["reasoning_output_tokens"],
                "ts": ts.isoformat() if ts else None,
            })
        last_total = cur

    totals_raw = {k: last_total[k] - base[k] for k in _CX_TOKEN_KEYS}
    totals = {
        "input": totals_raw["input_tokens"],
        "cached_input": totals_raw["cached_input_tokens"],
        "cache_write": totals_raw["cache_write_input_tokens"],
        "output": totals_raw["output_tokens"],
        "reasoning_output": totals_raw["reasoning_output_tokens"],
    }
    totals["uncached_input"] = totals["input"] - totals["cached_input"]
    totals["total_tokens"] = totals["input"] + totals["output"]

    uncached = totals["uncached_input"] / 1e6 * prices["input"]
    cached = totals["cached_input"] / 1e6 * prices["cached"]
    cache_write = totals["cache_write"] / 1e6 * prices.get("cache_write", 0.0)
    out = totals["output"] / 1e6 * prices["output"]
    cost = {
        "input_uncached": uncached,
        "input_cached": cached,
        "cache_write": cache_write,
        "output": out,
        "total": uncached + cached + cache_write + out,
    }

    wall = (last_ts - prompt_ts).total_seconds() if (prompt_ts and last_ts) else None
    # Codex session JSONL does not record per-tool approval grant/reject
    # timestamps (approvals, when present, are sidecars / UI-only).
    result = {
        "format": "codex",
        "model": model,
        "prompt": prompt,
        "prompt_ts": prompt_ts.isoformat() if prompt_ts else None,
        "end_ts": last_ts.isoformat() if last_ts else None,
        "duration_seconds": wall,
        "duration_wall_seconds": wall,
        "approval_wait_seconds": 0.0,
        "approval_waits": [],
        "num_steps": len(per_step),
        "token_events": n_token_events,
        "tokens": totals,
        "cost_usd": cost,
        "pricing_model": pricing_model,
        "model_context_window": model_window,
        "steps": per_step,
    }

    if rate_limits:
        result["rate_limits"] = {
            "plan_type": rate_limits.get("plan_type"),
            "primary_used_percent": (rate_limits.get("primary") or {}).get("used_percent"),
            "secondary_used_percent": (rate_limits.get("secondary") or {}).get("used_percent"),
        }
    return result


# --------------------------------------------------------------------------- #
# Aggregation helpers (used by CSV logger too)
# --------------------------------------------------------------------------- #

def analyze_session(records, fmt=None, prompt_index=None, codex_prices=None):
    """Return a list of per-prompt analysis dicts."""
    fmt = fmt or detect_format(records)
    if fmt == "claude_code":
        spans = cc_find_spans(records)
    else:
        spans = cx_find_spans(records)
    if not spans:
        return fmt, []
    if prompt_index is not None:
        spans = [spans[prompt_index]]
    results = []
    for s, e in spans:
        if fmt == "claude_code":
            results.append(cc_analyze_span(records, s, e))
        else:
            results.append(cx_analyze_span(records, s, e, prices=codex_prices))
    return fmt, results


def aggregate_results(results):
    """Collapse per-prompt results into one session-level summary."""
    if not results:
        return None
    if len(results) == 1:
        out = dict(results[0])
        out["prompt_index"] = 0
        out["num_prompts"] = 1
        return out

    fmt = results[0]["format"]
    model = results[0]["model"]
    prompt_ts = results[0]["prompt_ts"]
    end_ts = results[-1]["end_ts"]
    duration = None
    if prompt_ts and end_ts:
        duration = (parse_ts(end_ts) - parse_ts(prompt_ts)).total_seconds()

    token_keys = results[0]["tokens"].keys()
    tokens = {k: sum(r["tokens"].get(k, 0) for r in results) for k in token_keys}
    cost = None
    if all(r.get("cost_usd") for r in results):
        cost_keys = results[0]["cost_usd"].keys()
        cost = {k: sum(r["cost_usd"].get(k, 0.0) for r in results) for k in cost_keys}

    approval_wait = sum(float(r.get("approval_wait_seconds") or 0) for r in results)
    wall = None
    if all(r.get("duration_wall_seconds") is not None for r in results):
        wall = sum(float(r["duration_wall_seconds"]) for r in results)
    # Per-prompt durations already have approval waits removed; summing them
    # is the session active time (not wall clock across idle gaps between prompts).
    active = sum(float(r["duration_seconds"]) for r in results
                 if r.get("duration_seconds") is not None)
    return {
        "format": fmt,
        "model": model,
        "prompt": f"[{len(results)} prompts]",
        "prompt_index": "all",
        "num_prompts": len(results),
        "prompt_ts": prompt_ts,
        "end_ts": end_ts,
        "duration_seconds": active if results else duration,
        "duration_wall_seconds": wall,
        "approval_wait_seconds": approval_wait,
        "approval_waits": [w for r in results for w in (r.get("approval_waits") or [])],
        "num_steps": sum(r.get("num_steps", 0) for r in results),
        "tokens": tokens,
        "cost_usd": cost,
        "pricing_model": results[0].get("pricing_model"),
        "model_context_window": results[-1].get("model_context_window"),
        "rate_limits": results[-1].get("rate_limits"),
    }


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def print_claude(idx, r):
    t, c = r["tokens"], r["cost_usd"]
    print(f"=== Prompt {idx} [claude_code / {r['model']}]: {r['prompt']!r}")
    print(f"  Steps (API requests): {r['num_steps']}")
    if r["duration_seconds"] is not None:
        print(f"  Active time:          {r['duration_seconds']:.1f} s "
              f"({r['prompt_ts']} -> {r['end_ts']})")
        wall = r.get("duration_wall_seconds")
        wait = r.get("approval_wait_seconds") or 0.0
        if wall is not None and wait > 0:
            print(f"    wall-clock:         {wall:.1f} s")
            print(f"    approval/Q&A wait:  {wait:.1f} s "
                  f"({len(r.get('approval_waits') or [])} gate(s), excluded)")
    print("  Tokens:")
    print(f"    uncached input:     {t['input']:>10,}")
    print(f"    cache read:         {t['cache_read']:>10,}")
    print(f"    cache write (5m):   {t['cache_write_5m']:>10,}")
    print(f"    cache write (1h):   {t['cache_write_1h']:>10,}")
    print(f"    output:             {t['output']:>10,}")
    print(f"    TOTAL:              {t['total_tokens']:>10,}")
    label = r.get("pricing_model") or "custom"
    print(f"  Cost ({label}):      ${c['total']:.6f} "
          f"(in ${c['input']:.4f} / read ${c['cache_read']:.4f} / "
          f"w5m ${c['cache_write_5m']:.4f} / w1h ${c['cache_write_1h']:.4f} / "
          f"out ${c['output']:.4f})")
    print()


def print_codex(idx, r):
    t, c = r["tokens"], r["cost_usd"]
    print(f"=== Prompt {idx} [codex / {r['model']}]: {r['prompt']!r}")
    print(f"  Steps (model requests): {r['num_steps']}")
    if r["duration_seconds"] is not None:
        print(f"  Wall-clock time:        {r['duration_seconds']:.1f} s "
              f"({r['prompt_ts']} -> {r['end_ts']})")
    print("  Tokens:")
    print(f"    input (total):        {t['input']:>10,}")
    print(f"      of which cached:    {t['cached_input']:>10,}")
    print(f"      uncached input:     {t['uncached_input']:>10,}")
    print(f"      cache write:        {t['cache_write']:>10,}")
    print(f"    output (total):       {t['output']:>10,}")
    print(f"      of which reasoning: {t['reasoning_output']:>10,}")
    print(f"    TOTAL:                {t['total_tokens']:>10,}")
    if r.get("model_context_window"):
        print(f"  Context window:         {r['model_context_window']:,}")
    if r.get("rate_limits"):
        rl = r["rate_limits"]
        print(f"  Billing plan:           {rl.get('plan_type')} "
              f"(rate-limit metered; cost below is API-equivalent)")
        print(f"    rate limit used:      primary {rl.get('primary_used_percent')}% / "
              f"secondary {rl.get('secondary_used_percent')}%")
    label = r.get("pricing_model") or "custom"
    print(f"  Cost ({label}):         ${c['total']:.6f} "
          f"(uncached ${c['input_uncached']:.4f} / cached ${c['input_cached']:.4f} / "
          f"write ${c['cache_write']:.4f} / out ${c['output']:.4f})")
    print()


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("session", help="path to the .jsonl session log")
    ap.add_argument("--prompt-index", type=int, default=None,
                    help="0-based index of the prompt to analyze (default: all)")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    # Optional per-token pricing override for Codex logs (USD per 1M tokens).
    # Omitted -> rates are looked up from OPENAI_PRICING by the model the log
    # names, so terra and sol sessions each price correctly with no flags.
    ap.add_argument("--price-input", type=float, default=None,
                    help="Codex: $/1M uncached input (default: by model)")
    ap.add_argument("--price-cached", type=float, default=None,
                    help="Codex: $/1M cached input (default: by model)")
    ap.add_argument("--price-cache-write", type=float, default=None,
                    help="Codex: $/1M cache write (default: by model)")
    ap.add_argument("--price-output", type=float, default=None,
                    help="Codex: $/1M output (default: by model)")
    args = ap.parse_args()

    records = load_records(args.session)
    fmt = detect_format(records)

    codex_prices = build_codex_price_override(args)

    fmt, results = analyze_session(
        records, fmt=fmt, prompt_index=args.prompt_index, codex_prices=codex_prices)
    if not results:
        print(f"No user text prompts found (format={fmt}).", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(results, indent=2))
        return

    for idx, r in enumerate(results):
        label = args.prompt_index if args.prompt_index is not None else idx
        if r["format"] == "claude_code":
            print_claude(label, r)
        else:
            print_codex(label, r)


if __name__ == "__main__":
    main()
