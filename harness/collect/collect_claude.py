#!/usr/bin/env python3
"""
Collect Claude Code benchmark sessions into <run-dir>/logs/claude/.

Claude sessions live in one per-user tree (~/.claude/projects/**) with nothing
tying a session to a question, so each session's first user prompts are matched
against the question text from questions.csv. The arm is read from the prompt's
instruction clause. Failed sessions (cut off by a session/token limit, no real
answer, handoff-only answer, ...) are copied to logs/skipped/claude/ with a
.reason.txt sidecar instead.

Rounds: Claude sessions do not record a round, so rounds are assigned by
execution order within an arm (oldest first). At most MAX_ROUNDS (3) runs are
kept per (question, arm) cell — the NEWEST ones; older extras go to skipped.

Examples
--------
    python collect_claude.py --run-dir results/massive-run-X --min-date 2026-08-04
    python collect_claude.py --run-dir results/massive-run-X --dry-run
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

from analyze_session import cc_is_user_prompt, cc_prompt_text, parse_ts  # noqa: E402
from transcript import extract_transcript  # noqa: E402

from common import (  # noqa: E402
    canonical_key, copy_run, copy_skipped, load_questions, make_run_id,
    parse_filter_date, print_grid, report_skipped,
)

MODEL = "claude"
SESSIONS = Path.home() / ".claude" / "projects"
MAX_PROMPTS_SCAN = 8
MAX_ROUNDS = 3

# --------------------------------------------------------------------------- #
# Question matching
# --------------------------------------------------------------------------- #

# Fold smart quotes / dashes / nbsp to ASCII so questions.csv text matches what
# was actually typed into the session.
_NORMALIZE = {
    0x2018: "'", 0x2019: "'", 0x201A: "'", 0x201B: "'", 0x02BC: "'",
    0x201C: '"', 0x201D: '"', 0x201E: '"', 0x201F: '"',
    0x2013: "-", 0x2014: "-", 0x2015: "-", 0x2212: "-",
    0x2192: "->", 0x00A0: " ", 0x2007: " ", 0x202F: " ", 0x2026: "...",
}

# A session that DISCUSSES a question is not a run of it: harness wrappers,
# prompt-review chats, and authoring sessions that quote the question.
_META_MARKERS = (
    "is it ok to send", "is it okay to send", "such prompts", "these prompts",
    "can i send", "should i send", "is this prompt", "review this prompt",
    "what do you think of this prompt",
)
_HARNESS_PREFIXES = ("the following is the codex agent history", "<")


def _normalize(s: str) -> str:
    return s.translate(_NORMALIZE)


def _is_meta_prompt(prompt: str, qtext: str) -> bool:
    low = prompt.lstrip().lower()
    if any(low.startswith(p) for p in _HARNESS_PREFIXES):
        return True
    idx = prompt.find(qtext)
    if idx <= 0:
        return False
    # A question quoted as a markdown blockquote is being edited, not asked.
    if prompt[prompt.rfind("\n", 0, idx) + 1:idx].lstrip().startswith(">"):
        return True
    prefix = prompt[:idx].lower()
    return any(m in prefix for m in _META_MARKERS)


def extract_user_prompts(path: Path, limit: int = MAX_PROMPTS_SCAN) -> list[str]:
    out = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if cc_is_user_prompt(rec):
                out.append(cc_prompt_text(rec) or "")
                if len(out) >= limit:
                    break
    return out


# --------------------------------------------------------------------------- #
# Arm classification (see run-rounds.md)
# --------------------------------------------------------------------------- #

# Fixed RAGFlow datasets used by this evaluation. These are part of the
# experiment definition, not runtime configuration.
_SOURCES_IDS = frozenset({
    "REPLACE_C1_SOURCES_DATASET_ID",  # C1 Sources
    "REPLACE_C2_SOURCES_DATASET_ID",  # C2 Sources
})
_WORKREG_IDS = frozenset({
    "REPLACE_C1_WORK_REGISTRY_DATASET_ID",  # C1 Work Registry
    "REPLACE_C2_WORK_REGISTRY_DATASET_ID",  # C2 Work Registry
})
_SOURCES_MARKERS = ("sources rag entry point", "sources rag arm")
_WORKREG_MARKERS = ("work registry rag entry point", "work registry rag arm")
_BASELINE_MARKERS = ("internal/parametric knowledge", "parametric knowledge")
_RAG_MARKERS = ("ragflow_retrieval", "tl-v1")


def classify_arm(prompt: str) -> str:
    """'sources' | 'workrag' | 'directory' | 'baseline' | '' (unknown).

    Fixed dataset IDs identify the published RAG arms. The explicit arm label is
    a readable fallback. An unrecognized RAG prompt returns '' so the session is
    skipped and surfaced — guessing here once relabelled a whole corpus.
    """
    low = prompt.lower()
    if any(m in low for m in _BASELINE_MARKERS):
        return "baseline"
    if ("directory to answer" in low
            or "follow it as your operating instructions" in low):
        return "directory"
    if any(dataset_id in prompt for dataset_id in _SOURCES_IDS):
        return "sources"
    if any(dataset_id in prompt for dataset_id in _WORKREG_IDS):
        return "workrag"
    if any(marker in low for marker in _SOURCES_MARKERS):
        return "sources"
    if any(marker in low for marker in _WORKREG_MARKERS):
        return "workrag"
    return ""


# --------------------------------------------------------------------------- #
# Failure filters (Claude-specific)
# --------------------------------------------------------------------------- #

_LIMIT_MARKERS = (
    "you've hit your session limit", "session limit", "rate limit",
    "prompt is too long", "exceeds the maximum", "context length",
    "too many tokens",
)


def _assistant_text(rec) -> tuple[str | None, str]:
    if rec.get("type") != "assistant":
        return None, ""
    msg = rec.get("message") if isinstance(rec.get("message"), dict) else {}
    content = msg.get("content")
    if isinstance(content, str):
        text = content.strip()
    elif isinstance(content, list):
        text = "\n".join(b.get("text") or "" for b in content
                         if isinstance(b, dict) and b.get("type") == "text").strip()
    else:
        text = ""
    return msg.get("model"), text


def failure_reason(path: Path) -> str | None:
    """Reason string if the session failed (limit cutoff, no answer, cut off
    mid-tool-request), else None."""
    try:
        records = [json.loads(s) for s in path.read_text(encoding="utf-8").splitlines()
                   if s.strip() and s.lstrip().startswith("{")]
    except (OSError, json.JSONDecodeError) as e:
        return f"unreadable ({e})"

    has_answer = False
    cut_off_by_limit = False  # true when a limit error is the terminal event
    last_stop_reason = None
    for rec in records:
        model, text = _assistant_text(rec)
        if model is None:
            continue
        if rec.get("isApiErrorMessage") or model == "<synthetic>":
            if any(m in (text or "").lower() for m in _LIMIT_MARKERS):
                cut_off_by_limit = True
            continue
        if text:
            has_answer = True
            cut_off_by_limit = False  # a real answer came after the error
        last_stop_reason = (rec.get("message") or {}).get("stop_reason")
    if cut_off_by_limit:
        return "session_or_token_limit"
    if not has_answer:
        return "no_assistant_response"
    if last_stop_reason == "tool_use":
        return "incomplete_tool_use"
    return None


# Answers that completed cleanly but contain no answer:
# a handoff line ("findings sent to the parent") or a tool refusal.
_HANDOFF_MARKERS = (
    "to the parent", "to parent", "parent agent", "findings sent", "sent the",
    "delivered the", "reported findings", "to `/root`",
)
_REFUSAL_VERBS = (
    "rejected", "blocked", "denied", "refused", "declined", "not permitted",
    "not allowed", "approval is needed", "requires approval",
    "unable to retrieve", "explicit user authoriz",
)
_REFUSAL_SUBJECTS = ("retrieval", "query", "lookup", "tool call", "dataset call", "mcp")


def answer_defect_reason(text: str) -> str | None:
    body = (text or "").strip()
    if not body:
        return "no_answer_text"
    if body.startswith("{"):
        try:
            obj = json.loads(body)
            if isinstance(obj, dict) and "outcome" in obj:
                return "approval_decision_json"  # leaked approval-hook verdict
        except json.JSONDecodeError:
            pass
    low = body.lower()
    # A refusal leads the answer AND names the refused retrieval; real answers
    # about rejected proposals satisfy neither test in the opening window.
    head = low[:200]
    if (len(body) < 800 and any(v in head for v in _REFUSAL_VERBS)
            and any(s in head for s in _REFUSAL_SUBJECTS)):
        return "tool_refusal"
    if len(body) < 500 and any(m in low for m in _HANDOFF_MARKERS):
        return "handoff_no_answer"
    return None


# --------------------------------------------------------------------------- #
# Collect
# --------------------------------------------------------------------------- #

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


def find_matches(questions: dict, date_lo, date_hi) -> dict:
    """{(corpus, key): [{path, mtime, arm, prompt}, ...]} across the tree."""
    # Longest question first so a question quoting another matches correctly.
    by_text = sorted(((_normalize(q), ck) for ck, q in questions.items()),
                     key=lambda t: len(t[0]), reverse=True)
    files = sorted(SESSIONS.rglob("*.jsonl"))
    print(f"Scanning {len(files)} Claude session files...")

    matches = defaultdict(list)
    for i, path in enumerate(files, 1):
        if i % 200 == 0:
            print(f"  ... {i}/{len(files)}")
        if date_lo or date_hi:
            start = session_start(path)
            if (date_lo and start < date_lo) or (date_hi and start > date_hi):
                continue
        try:
            prompts = extract_user_prompts(path)
        except OSError as e:
            print(f"warn: skip {path}: {e}", file=sys.stderr)
            continue
        hit = set()
        for prompt in prompts:
            nprompt = _normalize(prompt)
            for qtext, ck in by_text:
                if ck in hit or qtext not in nprompt or _is_meta_prompt(nprompt, qtext):
                    continue
                matches[ck].append({"path": path, "mtime": path.stat().st_mtime,
                                    "arm": classify_arm(prompt)})
                hit.add(ck)
                break
    return matches


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
    matches = find_matches(
        questions,
        parse_filter_date(args.min_date) if args.min_date else None,
        parse_filter_date(args.max_date, end_of_day=True) if args.max_date else None,
    )

    collected, skipped, missing = [], [], []
    for ck in sorted(questions):
        corpus, key = ck
        kept = []
        for hit in sorted(matches.get(ck, []), key=lambda h: h["mtime"]):
            label = f"{corpus}-{key} {hit['path'].name}"
            reason = None
            if not hit["arm"]:
                reason = "arm_unclassified"
            if reason is None:
                reason = failure_reason(hit["path"])
            if reason is None:
                _, answer = extract_transcript(hit["path"], "claude")
                reason = answer_defect_reason(answer)
            if reason:
                copy_skipped(hit["path"], args.run_dir, MODEL, f"{label}: {reason}",
                             dry_run=args.dry_run)
                skipped.append((reason, label))
                continue
            kept.append(hit)
        if not kept:
            missing.append(f"{corpus}-{key}")
            continue
        by_arm = defaultdict(list)  # kept is oldest-first
        for hit in kept:
            by_arm[hit["arm"]].append(hit)
        for arm in sorted(by_arm):
            hits = by_arm[arm]
            # Cap at MAX_ROUNDS per cell, keeping the NEWEST sessions.
            for hit in hits[:-MAX_ROUNDS]:
                label = f"{corpus}-{key} {hit['path'].name}"
                copy_skipped(hit["path"], args.run_dir, MODEL,
                             f"{label}: over_max_rounds (kept newest {MAX_ROUNDS})",
                             dry_run=args.dry_run)
                skipped.append(("over_max_rounds", label))
            # Execution order within the arm is the round.
            for rnd, hit in enumerate(hits[-MAX_ROUNDS:], 1):
                run_id = make_run_id(corpus, key, MODEL, arm, rnd)
                copy_run(hit["path"], args.run_dir, MODEL, run_id, dry_run=args.dry_run)
                collected.append({"corpus": corpus, "key": canonical_key(key),
                                  "arm": arm, "round": rnd, "run_id": run_id})

    print(f"{'DRY RUN — ' if args.dry_run else ''}collected {len(collected)} runs "
          f"-> {args.run_dir}/logs/{MODEL}/")
    print_grid(collected)
    report_skipped(skipped)
    if missing:
        print(f"\nquestions with no usable session ({len(missing)}): {missing}")
    return 0 if collected else 1


if __name__ == "__main__":
    raise SystemExit(main())
