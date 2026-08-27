#!/usr/bin/env python3
"""Synthetic fixture checks for approval-wait exclusion (no large session I/O)."""
import json
import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "collect"))
from analyze_session import analyze_session, load_records, openai_prices


def write_jsonl(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


def test_claude_reject_wait():
    rows = [
        {
            "type": "user",
            "timestamp": "2026-07-07T12:00:00.000Z",
            "message": {"role": "user", "content": "do a thing"},
        },
        {
            "type": "assistant",
            "timestamp": "2026-07-07T12:00:05.000Z",
            "message": {
                "role": "assistant",
                "id": "msg_1",
                "content": [{"type": "tool_use", "id": "tool_1", "name": "Bash", "input": {}}],
                "usage": {
                    "input_tokens": 10,
                    "output_tokens": 5,
                    "cache_read_input_tokens": 0,
                    "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0},
                },
            },
        },
        {
            "type": "user",
            "timestamp": "2026-07-07T12:00:25.000Z",
            "message": {
                "role": "user",
                "content": [{"type": "tool_result", "tool_use_id": "tool_1", "content": "User rejected tool use"}],
            },
            "toolUseResult": "User rejected tool use",
        },
        {
            "type": "assistant",
            "timestamp": "2026-07-07T12:00:30.000Z",
            "message": {
                "role": "assistant",
                "id": "msg_2",
                "content": [{"type": "text", "text": "ok"}],
                "usage": {
                    "input_tokens": 3,
                    "output_tokens": 2,
                    "cache_read_input_tokens": 0,
                    "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0},
                },
            },
        },
    ]
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "c.jsonl"
        write_jsonl(path, rows)
        _, results = analyze_session(load_records(path))
    assert len(results) == 1
    r = results[0]
    # wall = 30s (00:00 -> 00:30); reject wait = 20s (00:05 -> 00:25) clipped to last_ts
    assert abs(r["duration_wall_seconds"] - 30.0) < 1e-6, r
    assert abs(r["approval_wait_seconds"] - 20.0) < 1e-6, r
    assert abs(r["duration_seconds"] - 10.0) < 1e-6, r
    assert r["approval_waits"][0]["reason"] == "permission_reject"
    print("claude reject wait OK", r["duration_seconds"], r["approval_wait_seconds"])


def test_claude_ask_user():
    rows = [
        {
            "type": "user",
            "timestamp": "2026-07-07T12:00:00.000Z",
            "message": {"role": "user", "content": "hi"},
        },
        {
            "type": "assistant",
            "timestamp": "2026-07-07T12:00:01.000Z",
            "message": {
                "role": "assistant",
                "id": "msg_1",
                "content": [{"type": "tool_use", "id": "tool_1", "name": "AskUserQuestion", "input": {}}],
                "usage": {
                    "input_tokens": 1,
                    "output_tokens": 1,
                    "cache_read_input_tokens": 0,
                    "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0},
                },
            },
        },
        {
            "type": "user",
            "timestamp": "2026-07-07T12:00:41.000Z",
            "message": {
                "role": "user",
                "content": [{"type": "tool_result", "tool_use_id": "tool_1", "content": "answer"}],
            },
            "toolUseResult": {"answers": ["x"]},
        },
        {
            "type": "assistant",
            "timestamp": "2026-07-07T12:00:45.000Z",
            "message": {
                "role": "assistant",
                "id": "msg_2",
                "content": [{"type": "text", "text": "thanks"}],
                "usage": {
                    "input_tokens": 1,
                    "output_tokens": 1,
                    "cache_read_input_tokens": 0,
                    "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0},
                },
            },
        },
    ]
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "c.jsonl"
        write_jsonl(path, rows)
        _, results = analyze_session(load_records(path))
    r = results[0]
    assert abs(r["duration_wall_seconds"] - 45.0) < 1e-6
    assert abs(r["approval_wait_seconds"] - 40.0) < 1e-6  # 01 -> 41
    assert abs(r["duration_seconds"] - 5.0) < 1e-6
    print("claude ask_user wait OK", r["duration_seconds"], r["approval_wait_seconds"])


def test_codex_cumulative():
    rows = [
        {"type": "session_meta", "payload": {"session_id": "x"}, "timestamp": "2026-07-07T12:00:00.000Z"},
        {"type": "turn_context", "payload": {"model": "gpt-5.6-terra"}, "timestamp": "2026-07-07T12:00:00.100Z"},
        {
            "type": "event_msg",
            "payload": {"type": "user_message", "message": "hi"},
            "timestamp": "2026-07-07T12:00:01.000Z",
        },
        {
            "type": "event_msg",
            "payload": {
                "type": "token_count",
                "info": {
                    "last_token_usage": {
                        "input_tokens": 100,
                        "cached_input_tokens": 40,
                        "cache_write_input_tokens": 0,
                        "output_tokens": 10,
                        "reasoning_output_tokens": 2,
                        "total_tokens": 110,
                    },
                    "total_token_usage": {
                        "input_tokens": 100,
                        "cached_input_tokens": 40,
                        "cache_write_input_tokens": 0,
                        "output_tokens": 10,
                        "reasoning_output_tokens": 2,
                        "total_tokens": 110,
                    },
                },
            },
            "timestamp": "2026-07-07T12:00:05.000Z",
        },
        # stale last_token_usage: total unchanged
        {
            "type": "event_msg",
            "payload": {
                "type": "token_count",
                "info": {
                    "last_token_usage": {
                        "input_tokens": 999,
                        "cached_input_tokens": 0,
                        "cache_write_input_tokens": 0,
                        "output_tokens": 50,
                        "reasoning_output_tokens": 0,
                        "total_tokens": 1049,
                    },
                    "total_token_usage": {
                        "input_tokens": 100,
                        "cached_input_tokens": 40,
                        "cache_write_input_tokens": 0,
                        "output_tokens": 10,
                        "reasoning_output_tokens": 2,
                        "total_tokens": 110,
                    },
                },
            },
            "timestamp": "2026-07-07T12:00:06.000Z",
        },
    ]
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "x.jsonl"
        write_jsonl(path, rows)
        _, results = analyze_session(load_records(path))
    r = results[0]
    assert r["tokens"]["input"] == 100
    assert r["tokens"]["cached_input"] == 40
    assert r["tokens"]["output"] == 10
    assert r["approval_wait_seconds"] == 0.0
    # Priced from the model the fixture's turn_context names, not a constant.
    assert r["pricing_model"] == "gpt-5.6-terra"
    p, _ = openai_prices("gpt-5.6-terra")
    expected = (60 / 1e6) * p["input"] + (40 / 1e6) * p["cached"] + (10 / 1e6) * p["output"]
    assert abs(r["cost_usd"]["total"] - expected) < 1e-12
    print("codex stale-last ignored OK", r["tokens"], r["cost_usd"]["total"])


def _tok(ts, total_in, total_out, last_in, last_out):
    """A codex token_count event: cumulative totals plus this turn's delta."""
    return {
        "type": "event_msg",
        "payload": {
            "type": "token_count",
            "info": {
                "last_token_usage": {
                    "input_tokens": last_in, "cached_input_tokens": 0,
                    "cache_write_input_tokens": 0, "output_tokens": last_out,
                    "reasoning_output_tokens": 0, "total_tokens": last_in + last_out,
                },
                "total_token_usage": {
                    "input_tokens": total_in, "cached_input_tokens": 0,
                    "cache_write_input_tokens": 0, "output_tokens": total_out,
                    "reasoning_output_tokens": 0, "total_tokens": total_in + total_out,
                },
            },
        },
        "timestamp": ts,
    }


def test_codex_resumed_session_excludes_replay():
    """A resumed rollout replays prior history; only post-handoff work counts.

    Regression for a C2 codex-dir run where every question inherited the
    whole codex session's cumulative total (25x over-count).
    """
    rows = [
        {"type": "session_meta", "payload": {"session_id": "s"}, "timestamp": "2026-07-07T12:00:00.000Z"},
        {"type": "session_meta", "payload": {"session_id": "s"}, "timestamp": "2026-07-07T12:00:00.001Z"},
        {"type": "turn_context", "payload": {"model": "gpt-5.6-terra"}, "timestamp": "2026-07-07T12:00:00.002Z"},
        # --- replayed history from earlier prompts in the same codex session ---
        _tok("2026-07-07T12:00:00.003Z", 1000, 100, 1000, 100),
        _tok("2026-07-07T12:00:00.004Z", 2000, 200, 1000, 100),
        _tok("2026-07-07T12:00:00.005Z", 3000, 300, 1000, 100),
        # --- this subagent's turn actually begins here ---
        {"type": "inter_agent_communication_metadata", "payload": {"trigger_turn": True},
         "timestamp": "2026-07-07T12:00:01.000Z"},
        _tok("2026-07-07T12:00:04.000Z", 3500, 340, 500, 40),
        _tok("2026-07-07T12:00:09.000Z", 4200, 390, 700, 50),
    ]
    for replay_user in (False, True):
        test_rows = list(rows)
        if replay_user:
            test_rows.insert(3, {
                "type": "event_msg",
                "payload": {"type": "user_message", "message": "replayed prompt"},
                "timestamp": "2026-07-07T12:00:00.002Z",
            })
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "resumed.jsonl"
            write_jsonl(p, test_rows)
            _, results = analyze_session(load_records(p))
        assert len(results) == 1, results
        r = results[0]
        # Only the two post-handoff turns: 500+700 in, 40+50 out. Not 4200/390.
        assert r["tokens"]["input"] == 1200, r["tokens"]
        assert r["tokens"]["output"] == 90, r["tokens"]
        assert r["num_steps"] == 2, r["num_steps"]
        assert r["duration_seconds"] == 8, r["duration_seconds"]
        # Steps must stay physically plausible: 2 steps over 8s, never 5 in 5ms.
        assert r["num_steps"] / r["duration_seconds"] < 3, r
    print("codex resumed-session replay excluded OK", r["tokens"], r["num_steps"])


def test_codex_fresh_session_unchanged():
    """No handoff marker -> behaviour identical to before the fix."""
    rows = [
        {"type": "session_meta", "payload": {"session_id": "s"}, "timestamp": "2026-07-07T12:00:00.000Z"},
        {"type": "turn_context", "payload": {"model": "gpt-5.6-terra"}, "timestamp": "2026-07-07T12:00:00.100Z"},
        {"type": "event_msg", "payload": {"type": "user_message", "message": "hi"},
         "timestamp": "2026-07-07T12:00:01.000Z"},
        _tok("2026-07-07T12:00:05.000Z", 100, 10, 100, 10),
        _tok("2026-07-07T12:00:09.000Z", 260, 25, 160, 15),
    ]
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "fresh.jsonl"
        write_jsonl(p, rows)
        _, results = analyze_session(load_records(p))
    assert len(results) == 1, results
    r = results[0]
    assert r["tokens"]["input"] == 260, r["tokens"]
    assert r["tokens"]["output"] == 25, r["tokens"]
    assert r["num_steps"] == 2, r["num_steps"]
    print("codex fresh session unchanged OK", r["tokens"])


if __name__ == "__main__":
    test_claude_reject_wait()
    test_claude_ask_user()
    test_codex_cumulative()
    test_codex_resumed_session_excludes_replay()
    test_codex_fresh_session_unchanged()
    print("ALL PASS")
