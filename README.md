# Work Registry Evaluation

This repository evaluates the [Work Registry](https://github.com/markpyzhov/work-registry)
method. It measures the cost and accuracy of answering current-status questions from a
maintained Work Registry rather than from raw project Sources alone. It holds the
frozen corpora, the harness that runs and scores the evaluation arms, and the complete
published run so that the article's results can be audited or reproduced.

## `corpora`

The repository contains two corpora, each comprising one project's material frozen at
an as-of timestamp. Each corpus holds the Work Registry package provided to the agents
and the evaluator-only ground truth used to ask and score the questions.

Both corpora share the same layout:

- `work-registry/`: the package under evaluation. Read more about its structure
  in the [work-registry](https://github.com/markpyzhov/work-registry) repository.
- `ground-truth/`: the evaluator-only material:
  - `questions.md`, the corpus questions;
  - `event-ledger.md`, the reconstructed event timeline the answers rest on;
  - `scoring/`, with one answer key per arm group: `answer-key-sources.md` and
    `answer-key-work-registry.md`;
  - Corpus 1 also adds `scenario.md`, the fictional project definition.
- `sources/` (Corpus 2 only): the raw public GitHub payloads, described in
  [`download-plan.md`](corpora/corpus-2/sources/download-plan.md).

### Corpus 1 — CipherDoc

This corpus covers the fictional CipherDoc project from 2026-06-01 to 2026-09-22.

- 168 Sources: ClickUp 39, Google Docs 51, Slack 67, Fireflies 11.
- Work Registry: 7 Work State items, 12 Comments, and 12 Daily Briefs.
- Evaluation: 15 questions.

Corpus generation:

1. Gemini CLI (`gemini-3-flash-preview`) made the first fictional corpus.
2. Cursor (`cursor-grok-4.5-high`, often with `composer-2.5-fast`) rebuilt the
  Sources, Work State, Comments, briefs, questions, and answer keys.

### Corpus 2 — OpenTelemetry

This corpus contains public [OpenTelemetry Go](https://github.com/open-telemetry/opentelemetry-go/)
GitHub activity through `2026-02-27T17:20:46Z`.

- 26 Sources: 8 meeting notes, 6 issues, 7 pull requests, 4 milestones, 1 release.
- Work Registry: 5 Work State items and 3 Comments. It has no Daily Briefs.
- Evaluation: 15 questions.

Corpus generation:

- Public GitHub records were collected and converted into 26 Sources.
- GPT-5.6 Terra (`gpt-5.6-terra`) created the event ledger and question plan.
- Cursor (`cursor-grok-4.5-high`) created the Work State, Comments, questions,
  and answer keys from the frozen material.

## `harness`

The harness is the procedure that runs controlled evaluation arms, collects their
sessions, scores the answers, validates the result, and builds the report.

### Rerun generation and evaluation guide

The steps below reproduce a full run: prepare the datasets and workspaces,
generate answers for every arm, collect and validate the sessions, score them,
and build the report. Run all commands from the repository root.

#### 1. Set the run directory and repository root

Set the destination once for the examples:

```shell
EVAL_RUN="results/massive-run-X"
mkdir -p "$EVAL_RUN"
cp harness/questions.csv "$EVAL_RUN/questions.csv"
```

`harness/questions.csv` is the machine-readable snapshot of both corpora's
questions: its 30 rows carry the verbatim question texts of
[`corpora/corpus-1/ground-truth/questions.md`](corpora/corpus-1/ground-truth/questions.md)
(15 rows, `c1`) and
[`corpora/corpus-2/ground-truth/questions.md`](corpora/corpus-2/ground-truth/questions.md)
(15 rows, `c2`).

Replace `REPLACE_REPO_ROOT` with this repository's absolute path in all files under
`harness/`.

#### 2. Configure RAG and MCP

Set up the RAGFlow fork with the required evaluation fixes and create four datasets by
following the [RAG configuration guide](harness/workspaces/rag-configuration.md).

#### 3. Prepare workspace files

Run from the repository root:

```shell
cp corpora/corpus-1/ground-truth/questions.md harness/workspaces/c1-questions.md
cp corpora/corpus-2/ground-truth/questions.md harness/workspaces/c2-questions.md
cp -R corpora/corpus-1/work-registry/. harness/workspaces/c1/
cp -R corpora/corpus-2/work-registry/. harness/workspaces/c2/
mkdir -p harness/workspaces/baseline
```

#### 4. Run generation rounds

The evaluation uses three comparison arms:

1. Sources RAG
2. Work Registry RAG
3. Work Registry Directory

A separate C2-only no-retrieval baseline tests what the models can answer from prior
knowledge. The comparison arms account for 540 sessions; the baseline adds 30,
producing the article's total of 570 scored sessions.

All runs follow the procedure in
[`harness/run/run-rounds.md`](harness/run/run-rounds.md). For the two RAG arms, Codex
instead follows separate instructions for both corpora:
[`harness/run/run-codex-rag.md`](harness/run/run-codex-rag.md).

The workspace directory of the agents should be `harness/workspaces`.

Run every question-round pair in a fresh subagent session. Each subagent answers the
documented question directly.

#### 5. Collect, parse, and validate

Claude Code and Codex subagent sessions are discovered from their local session
stores.

Note:

- Bind discovery to the evaluation dates. For example, use `--min-date 2026-07-23
  --max-date 2026-07-24` if the sessions ran between July 23 and 24.
- Codex RAG sessions store artifacts outside the common session-log directories.
  Replace `<CODEX_RAG_RAW_DIR>` with the actual output directory.

```shell
python3 harness/collect/collect_claude.py \
  --run-dir "$EVAL_RUN" --min-date YYYY-MM-DD --max-date YYYY-MM-DD
python3 harness/collect/collect_codex_subagents.py \
  --run-dir "$EVAL_RUN" --min-date YYYY-MM-DD --max-date YYYY-MM-DD
python3 harness/collect/collect_codex_rag.py <CODEX_RAG_RAW_DIR> \
  --run-dir "$EVAL_RUN"
python3 harness/collect/parse_claude.py --run-dir "$EVAL_RUN"
python3 harness/collect/parse_codex.py --run-dir "$EVAL_RUN" \
  --rag-model gpt-5.6-terra
python3 harness/collect/validate_run.py --run-dir "$EVAL_RUN" \
  --expect-rounds 3 --expect-baseline-rounds 1
```

Per-session cost is computed by
[`harness/collect/analyze_session.py`](harness/collect/analyze_session.py) from
the Anthropic and OpenAI per-model API list prices embedded in the script,
taken from the vendors' pricing pages as of 2026-08-18.

Inspect `$EVAL_RUN/logs/skipped/` and its reason files before scoring. A validation
failure means the run is incomplete or inconsistent. Fix the collection rather than
silently dropping a session. Because the parent agents may automatically retry failed
subagent sessions, confirm that the expected session is genuinely missing before
rerunning that question-round pair.

#### 6. Score, validate, and merge

Ask three independent parent agents to score the sessions by following
[`harness/score/score-rounds.md`](harness/score/score-rounds.md). Baseline
handling is fully specified in
[`harness/score/score-baseline.md`](harness/score/score-baseline.md). Then run:

```shell
python3 harness/score/validate_answer_keys.py
python3 harness/score/validate_score_run.py --run-dir "$EVAL_RUN"
python3 harness/score/merge_score_cards.py --run-dir "$EVAL_RUN"
```

Scorers may disagree on certain questions — check the `all_scorers_agree`
column in `score-cards.csv`.

For each flagged session, reread the answer against the answer key, adjudicate its
correctness, and save the decision to
`$EVAL_RUN/scores/human.csv` (columns `session_id`, `correctness`,
`description`). This supersedes the scorers' median.

Rerun `merge_score_cards.py`:

```shell
python3 harness/score/merge_score_cards.py --run-dir "$EVAL_RUN"
```

#### 7. Generate the report

```shell
python3 harness/report/generate_report.py --run-dir "$EVAL_RUN"
```

The report and its source tables are written to `$EVAL_RUN/report/`.

#### Smoke test

The test checks all processing stages against the published data and regenerates
the merged and report outputs in a temporary directory:

```shell
python3 harness/tests/smoke_test.py
```

## `results`

### `results/massive-run-article/`

This is the complete evaluation run used by the article. Its question snapshot,
raw and parsed logs, scorer outputs, merged score cards, and report are retained
together so the result can be audited without rerunning model calls.

The package contains:

- `logs/`: raw JSONL and parsed Markdown responses, grouped by runner;
- `scores/`: three scorer tables and human adjudications;
- `usage.csv`: the run manifest and usage metrics;
- `score-cards.csv` and `score-cards-long.csv`: merged scoring data;
- `report/`: the generated report and aggregate CSVs.

From the repository root, verify it with:

```shell
python3 harness/collect/validate_run.py \
  --run-dir results/massive-run-article \
  --expect-rounds 3 --expect-baseline-rounds 1
python3 harness/score/validate_score_run.py \
  --run-dir results/massive-run-article
```

`harness/tests/smoke_test.py` additionally re-merges the scorer files and
regenerates the report in a temporary directory.

## License

Code under `harness/` is licensed under the [MIT License](LICENSE-CODE). Original
research materials and documentation are licensed, to the extent the author holds the
applicable rights, under [CC BY 4.0](LICENSE-DATA). Third-party material retains its
original rights and terms; see [Third-party notices](THIRD_PARTY_NOTICES.md).
