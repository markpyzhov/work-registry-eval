#!/usr/bin/env python3
"""Generate the analysis report and chart-ready aggregate CSVs from score-cards.csv.

Reads the merged score cards produced by merge_score_cards.py and writes:

  <run>/report/report.md            - full human-readable report
  <run>/report/accuracy_by_arm.csv  - tidy accuracy table
  <run>/report/cost_by_arm.csv      - tidy cost table
  <run>/report/cost_deltas.csv      - within-model relative savings
  <run>/report/cost_per_correct.csv - spend/tokens per fully-correct answer
  <run>/report/per_question.csv     - per-question means

Rows with corpus='all' pool both corpora. Aggregate CSVs are the single source
for any chart in the article; the article itself should only quote numbers that
appear here.

Usage: python3 generate_report.py --run-dir results/massive-run-X
"""

import argparse
import csv
import math
import random
import statistics as st
from collections import defaultdict
from pathlib import Path

ARM_LABELS = {
    "baseline": "Baseline (no retrieval)",
    "sources": "Sources RAG",
    "workrag": "Work Registry RAG",
    "directory": "Work Registry Directory",
}
MODEL_LABELS = {
    "claude-opus-5": "Claude Opus 5",
    "claude-opus-4-8": "Claude Opus 4.8",
    "claude-fable-5": "Claude Fable 5",
    "claude-sonnet-5": "Claude Sonnet 5",
    "gpt-5.6-sol": "GPT-5.6 Sol",
    "gpt-5.6-terra": "GPT-5.6 Terra",
}
ARM_ORDER = ["baseline", "sources", "workrag", "directory"]
CORPUS_ORDER = ["all", "c1", "c2"]

BOOTSTRAP_N = 10_000
SEED = 20260724


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def wilson(successes, n, z=1.96):
    """Wilson 95% interval for a proportion."""
    if n == 0:
        return (0.0, 0.0)
    p = successes / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, center - half), min(1.0, center + half))


def boot_ci(values, rng, n_boot=BOOTSTRAP_N):
    """Bootstrap 95% CI for the mean of graded scores (0 / 0.5 / 1)."""
    if not values:
        return (0.0, 0.0)
    means = []
    k = len(values)
    for _ in range(n_boot):
        means.append(st.mean(rng.choices(values, k=k)))
    means.sort()
    return (means[int(0.025 * n_boot)], means[int(0.975 * n_boot)])


def cv(values):
    m = st.mean(values)
    return 100 * st.pstdev(values) / m if m else 0.0


def group_rows(rows, keys, corpus):
    """Group rows by keys; corpus='all' pools, otherwise filters to one corpus."""
    groups = defaultdict(list)
    for r in rows:
        if corpus != "all" and r["corpus"] != corpus:
            continue
        groups[tuple(r[k] for k in keys)].append(r)
    return groups


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True,
                        help="run directory containing score-cards.csv")
    args = parser.parse_args()
    cards = args.run_dir / "score-cards.csv"
    if not cards.is_file():
        parser.error(f"missing score cards: {cards}")
    outdir = cards.parent / "report"
    outdir.mkdir(exist_ok=True)
    rng = random.Random(SEED)

    with cards.open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    human_path = cards.parent / "scores" / "human.csv"
    human_ids = set()
    if human_path.is_file():
        with human_path.open(newline="") as fh:
            human_ids = {r["session_id"] for r in csv.DictReader(fh)}

    # ---------------- accuracy: (corpus | all) x model x arm ----------------
    acc_recs = []
    for corpus in CORPUS_ORDER:
        for key, rs in sorted(
            group_rows(rows, ["model", "arm"], corpus).items()
        ):
            scores = [fnum(r["correctness"]) for r in rs]
            strict = sum(1 for s in scores if s == 1)
            lo_w, hi_w = wilson(strict, len(scores))
            lo_b, hi_b = boot_ci(scores, rng)
            acc_recs.append(
                dict(
                    corpus=corpus,
                    model=key[0],
                    arm=key[1],
                    n=len(scores),
                    mean_correctness=round(st.mean(scores), 4),
                    mean_ci_lo=round(lo_b, 4),
                    mean_ci_hi=round(hi_b, 4),
                    strict_correct=strict,
                    strict_rate=round(strict / len(scores), 4),
                    strict_wilson_lo=round(lo_w, 4),
                    strict_wilson_hi=round(hi_w, 4),
                )
            )

    # ---------------- cost aggregation helper ----------------
    def cost_record(base, rs):
        dur = [fnum(r["duration_seconds"]) for r in rs]
        tok = [fnum(r["tokens_total"]) for r in rs]
        spend = [fnum(r["spend_total"]) for r in rs]
        steps = [fnum(r["num_steps"]) for r in rs]
        cites = [
            fnum(r["citation_validity_rate"])
            for r in rs
            if r["citation_validity_rate"] not in ("", "None")
        ]
        rec = dict(base)
        rec.update(
            n=len(rs),
            duration_mean_s=round(st.mean(dur), 1),
            duration_median_s=round(st.median(dur), 1),
            duration_cv_pct=round(cv(dur), 1),
            tokens_mean=round(st.mean(tok)),
            tokens_median=round(st.median(tok)),
            tokens_cv_pct=round(cv(tok), 1),
            spend_mean_usd=round(st.mean(spend), 4),
            spend_median_usd=round(st.median(spend), 4),
            spend_total_usd=round(sum(spend), 2),
            steps_mean=round(st.mean(steps), 1),
            citation_validity_mean=round(st.mean(cites), 4) if cites else "",
            citation_rows=len(cites),
        )
        return rec

    # cost by (corpus | all) x model x arm
    cost_recs = []
    for corpus in CORPUS_ORDER:
        for (model, arm), rs in sorted(
            group_rows(rows, ["model", "arm"], corpus).items()
        ):
            cost_recs.append(cost_record(dict(corpus=corpus, model=model, arm=arm), rs))

    # within-model deltas, pooled and per corpus
    delta_recs = []
    for corpus in CORPUS_ORDER:
        by_model = defaultdict(dict)
        for rec in cost_recs:
            if rec["corpus"] == corpus:
                by_model[rec["model"]][rec["arm"]] = rec

        def deltas(a, b):
            return dict(
                duration_saving_pct=round(
                    100 * (1 - a["duration_mean_s"] / b["duration_mean_s"]), 1
                ),
                tokens_saving_pct=round(
                    100 * (1 - a["tokens_mean"] / b["tokens_mean"]), 1
                ),
                spend_saving_pct=round(
                    100 * (1 - a["spend_mean_usd"] / b["spend_mean_usd"]), 1
                ),
                steps_saving_pct=round(
                    100 * (1 - a["steps_mean"] / b["steps_mean"]), 1
                ),
            )

        for model, arms in sorted(by_model.items()):
            # deltas only where both arms exist (a baseline-only run has none)
            if "sources" in arms:
                for arm in ("workrag", "directory"):
                    if arm in arms:
                        delta_recs.append(
                            dict(corpus=corpus, model=model, arm=arm, vs="sources")
                            | deltas(arms[arm], arms["sources"])
                        )
            if "directory" in arms and "workrag" in arms:
                delta_recs.append(
                    dict(corpus=corpus, model=model, arm="directory", vs="workrag")
                    | deltas(arms["directory"], arms["workrag"])
                )

    # cost per fully-correct answer, pooled and per corpus
    cpc_recs = []
    for corpus in CORPUS_ORDER:
        for (model, arm), rs in sorted(
            group_rows(rows, ["model", "arm"], corpus).items()
        ):
            n_correct = sum(1 for r in rs if fnum(r["correctness"]) == 1)
            spend_sum = sum(fnum(r["spend_total"]) for r in rs)
            tok_sum = sum(fnum(r["tokens_total"]) for r in rs)
            dur_sum = sum(fnum(r["duration_seconds"]) for r in rs)
            cpc_recs.append(
                dict(
                    corpus=corpus,
                    model=model,
                    arm=arm,
                    n_runs=len(rs),
                    n_fully_correct=n_correct,
                    spend_per_correct_usd=round(spend_sum / n_correct, 4)
                    if n_correct
                    else "",
                    tokens_per_correct=round(tok_sum / n_correct) if n_correct else "",
                    seconds_per_correct=round(dur_sum / n_correct, 1)
                    if n_correct
                    else "",
                )
            )

    # ---------------- per-question means (heatmap input) ----------------
    pq_recs = []
    pq_groups = defaultdict(list)
    for r in rows:
        pq_groups[(r["corpus"], r["key"], r["arm"], r["model"])].append(
            fnum(r["correctness"])
        )
    for key in sorted(pq_groups):
        vals = pq_groups[key]
        pq_recs.append(
            dict(
                corpus=key[0],
                key=key[1],
                arm=key[2],
                model=key[3],
                n=len(vals),
                mean_correctness=round(st.mean(vals), 4),
            )
        )

    # ---------------- scorer agreement ----------------
    agree = sum(1 for r in rows if r["all_scorers_agree"] == "True")
    spread = sum(1 for r in rows if r["spread_flag"] not in ("", "None", "0"))

    # ---------------- write CSVs ----------------
    written = []

    def write_csv(name, recs):
        if not recs:
            return
        written.append(name)
        with open(outdir / name, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(recs[0].keys()))
            w.writeheader()
            w.writerows(recs)

    write_csv("accuracy_by_arm.csv", acc_recs)
    write_csv("cost_by_arm.csv", cost_recs)
    write_csv("cost_deltas.csv", delta_recs)
    write_csv("cost_per_correct.csv", cpc_recs)
    write_csv("per_question.csv", pq_recs)

    # ---------------- write markdown report ----------------
    def md_table(recs, cols, headers=None):
        headers = headers or cols
        lines = ["| " + " | ".join(headers) + " |"]
        lines.append("|" + "|".join([" --- "] * len(headers)) + "|")
        for rec in recs:
            lines.append("| " + " | ".join(str(rec[c]) for c in cols) + " |")
        return "\n".join(lines)

    def label(rec):
        out = dict(rec)
        if out.get("arm") in ARM_LABELS:
            out["arm"] = ARM_LABELS[out["arm"]]
        if out.get("model") in MODEL_LABELS:
            out["model"] = MODEL_LABELS[out["model"]]
        return out

    def sort_key(r):
        return (
            CORPUS_ORDER.index(r["corpus"]) if r.get("corpus") in CORPUS_ORDER else 9,
            r.get("model", ""),
            ARM_ORDER.index(r["arm"]) if r.get("arm") in ARM_ORDER else 9,
        )

    def pick(recs, corpus):
        return [label(r) for r in sorted(recs, key=sort_key) if r["corpus"] == corpus]

    L = []
    L.append(f"# {cards.parent.name} analysis report\n")
    L.append(
        f"Generated by `generate_report.py` from `{cards.name}` "
        f"({len(rows)} scored sessions). Bootstrap CIs use seed {SEED}.\n"
    )
    # A human review that agrees with the scorers changed nothing.
    human_n = 0
    for r in rows:
        if r["session_id"] not in human_ids:
            continue
        scorer_grades = [float(v) for v in r["correctness_values"].split(";")]
        if st.median(scorer_grades) != float(r["correctness"]):
            human_n += 1

    grade_rule = "The final grade is the scorer median."
    if human_n:
        grade_rule = (
            f"The final grade is the scorer median, except {human_n} "
            "sessions where human review changed it."
        )
    L.append(
        "Design: 30 questions across 2 corpora (C1 synthetic CipherDoc "
        "project, C2 real OpenTelemetry sources), 3 retrieval arms, 2 models, "
        "and 3 rounds. Each session was graded by 3 independent scorers "
        f"(Claude, Codex, Cursor). {grade_rule} Stats are pooled and split by "
        "corpus.\n"
    )
    L.append(
        f"Scorer agreement: all three scorers agreed on correctness in "
        f"{agree}/{len(rows)} sessions ({100 * agree / len(rows):.1f}%); "
        f"{spread} sessions had full spread (one scorer correct, another "
        f"incorrect). Scorer agreement describes the raw scorer judgments.\n"
    )

    acc_cols = [
        "model",
        "arm",
        "n",
        "mean_correctness",
        "mean_ci_lo",
        "mean_ci_hi",
        "strict_rate",
        "strict_wilson_lo",
        "strict_wilson_hi",
    ]
    cost_cols = [
        "model",
        "arm",
        "n",
        "duration_mean_s",
        "duration_median_s",
        "duration_cv_pct",
        "tokens_mean",
        "tokens_median",
        "tokens_cv_pct",
        "spend_mean_usd",
        "steps_mean",
        "citation_validity_mean",
    ]
    delta_cols = [
        "model",
        "arm",
        "vs",
        "duration_saving_pct",
        "tokens_saving_pct",
        "spend_saving_pct",
        "steps_saving_pct",
    ]
    cpc_cols = [
        "model",
        "arm",
        "n_runs",
        "n_fully_correct",
        "spend_per_correct_usd",
        "tokens_per_correct",
        "seconds_per_correct",
    ]
    L.append("\n## Accuracy by arm\n")
    L.append(
        "`mean_correctness` averages graded scores (correct=1, partial=0.5, "
        "incorrect=0). `strict_rate` counts only fully-correct answers, with a "
        "Wilson 95% interval.\n"
    )
    for corpus in CORPUS_ORDER:
        L.append(f"\n### Accuracy — {'both corpora pooled' if corpus == 'all' else corpus.upper()}\n")
        L.append(md_table(pick(acc_recs, corpus), acc_cols))

    L.append("\n\n## Cost and performance by arm\n")
    L.append(
        "Token totals are not comparable across models (different caching and "
        "accounting); compare arms **within** a model only.\n"
    )
    for corpus in CORPUS_ORDER:
        L.append(f"\n### Cost — {'both corpora pooled' if corpus == 'all' else corpus.upper()}\n")
        L.append(md_table(pick(cost_recs, corpus), cost_cols))

    L.append("\n\n## Within-model savings\n")
    for corpus in CORPUS_ORDER:
        L.append(f"\n### Savings — {'both corpora pooled' if corpus == 'all' else corpus.upper()}\n")
        L.append(md_table(pick(delta_recs, corpus), delta_cols))

    L.append("\n\n## Cost per fully-correct answer\n")
    for corpus in CORPUS_ORDER:
        L.append(f"\n### Cost per correct — {'both corpora pooled' if corpus == 'all' else corpus.upper()}\n")
        L.append(md_table(pick(cpc_recs, corpus), cpc_cols))

    (outdir / "report.md").write_text("\n".join(L) + "\n")
    print(f"Wrote {outdir}/report.md and {len(written)} aggregate CSVs")


if __name__ == "__main__":
    main()
