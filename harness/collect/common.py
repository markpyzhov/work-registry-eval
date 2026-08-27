"""Small helpers shared by the collect_* and parse_* scripts.

Only genuinely common things live here: naming (run_id, arms, keys),
questions.csv loading, the markdown layout scoring reads, usage.csv upsert,
and the skipped-session copier. Everything model-specific stays in the
script that needs it.
"""

from __future__ import annotations

import csv
import re
import shutil
from datetime import datetime
from pathlib import Path

# logs/<model>/ subdirectories; also the value of the usage.csv `tool` column.
MODELS = ("claude", "codex-dir", "codex-rag", "codex-baseline")

ARMS = ("sources", "workrag", "directory", "baseline")

_ARM_ALIASES = {
    "sources": "sources", "source": "sources", "raw": "sources", "rawrag": "sources",
    "workrag": "workrag", "workregistry": "workrag", "workreg": "workrag",
    "wrrag": "workrag", "wr": "workrag",
    "directory": "directory", "dir": "directory", "wrdir": "directory",
    "baseline": "baseline", "base": "baseline",
}

RESPONSE_DELIMITER = "<!-- RESPONSE_START -->"


def canonical_arm(arm: str) -> str:
    a = (arm or "").strip().lower().replace("_", "").replace("-", "")
    return _ARM_ALIASES.get(a, arm or "")


def canonical_key(key: str) -> str:
    """`q1` / `A-05` -> `Q01` / `A05`."""
    m = re.fullmatch(r"([QA])-?(\d+)", (key or "").strip().upper())
    return f"{m.group(1)}{int(m.group(2)):02d}" if m else (key or "").strip().upper()


def make_run_id(corpus: str, key: str, model: str, arm: str, round_) -> str:
    return f"{corpus}-{canonical_key(key)}-{model}-{canonical_arm(arm)}-r{round_}"


_RUN_ID_RE = re.compile(
    r"^(?P<corpus>c\d+)-(?P<key>[QA]\d+)-(?P<model>" + "|".join(MODELS) +
    r")-(?P<arm>[a-z]+)-r(?P<round>\d+)$")


def parse_run_id(run_id: str) -> dict | None:
    m = _RUN_ID_RE.match(run_id)
    return m.groupdict() if m else None


def load_questions(path: Path) -> dict:
    """{(corpus, canonical_key): question_text} from questions.csv."""
    index = {}
    with Path(path).open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            corpus = (row.get("corpus") or "").strip()
            key = (row.get("key") or "").strip()
            if corpus and key:
                index[(corpus, canonical_key(key))] = (row.get("question") or "").strip()
    if not index:
        raise SystemExit(f"error: no questions loaded from {path}")
    return index


def parse_filter_date(s: str, *, end_of_day: bool = False) -> datetime:
    """--min-date/--max-date value -> tz-aware datetime (naive = local tz)."""
    s = s.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        dt = datetime.fromisoformat(s)
        if end_of_day:
            dt = dt.replace(hour=23, minute=59, second=59, microsecond=999_999)
    else:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    return dt.astimezone() if dt.tzinfo is None else dt


def copy_run(src: Path, out_dir: Path, model: str, run_id: str,
             *, dry_run: bool = False) -> Path:
    dest = Path(out_dir) / "logs" / model / f"{run_id}.jsonl"
    if not dry_run:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
    return dest


def copy_skipped(src: Path, out_dir: Path, model: str, reason: str,
                 *, dry_run: bool = False) -> Path:
    """Copy a rejected session into logs/skipped/<model>/ with a reason sidecar."""
    dest = Path(out_dir) / "logs" / "skipped" / model / src.name
    if not dry_run:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        dest.with_suffix(".reason.txt").write_text(reason + "\n", encoding="utf-8")
    return dest


def write_markdown(md_path: Path, prompt: str, response: str) -> None:
    """The layout scoring reads: headline above the delimiter, answer below."""
    headline = (prompt or "").strip() or "(prompt not found — fill in manually)"
    body = (response or "").strip() or "_(final response not found — fill in manually)_"
    md_path.write_text(f"# {headline}\n\n{RESPONSE_DELIMITER}\n\n{body}\n",
                       encoding="utf-8")


def read_response(md_path: Path) -> str:
    text = Path(md_path).read_text(encoding="utf-8")
    _, _, body = text.partition(RESPONSE_DELIMITER)
    return (body or text).strip()


def read_usage_rows(csv_path: Path) -> list[dict]:
    path = Path(csv_path)
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def upsert_usage(csv_path: Path, rows: list[dict], fields: list[str]) -> dict:
    """Merge rows into usage.csv by run_id, so each parser owns its own rows
    and re-running one leaves the others' rows alone."""
    path = Path(csv_path)
    by_id = {r["run_id"]: r for r in read_usage_rows(path) if r.get("run_id")}
    added = replaced = 0
    for row in rows:
        rid = row.get("run_id")
        if not rid:
            raise ValueError("cannot upsert a row without run_id")
        replaced += rid in by_id
        added += rid not in by_id
        by_id[rid] = row
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for rid in sorted(by_id):
            writer.writerow(by_id[rid])
    return {"added": added, "replaced": replaced, "total": len(by_id)}


def print_grid(runs: list[dict]) -> None:
    """runs: dicts with corpus/arm/round/key. Prints unique questions per cell."""
    from collections import defaultdict
    grid = defaultdict(set)
    for r in runs:
        grid[(r["corpus"], r["arm"], r["round"])].add(r["key"])
    print("\ngrid (unique questions per cell):")
    for cell in sorted(grid):
        print(f"  {cell[0]}  {cell[1]:<10} r{cell[2]}  {len(grid[cell])}")


def report_skipped(skipped: list[tuple]) -> None:
    """skipped: [(reason, label), ...]"""
    if not skipped:
        return
    print(f"\nskipped {len(skipped)} session(s) -> logs/skipped/:")
    for reason, label in skipped:
        print(f"  {reason:<28} {label}")
