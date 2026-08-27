# Score rounds

Orchestration for scoring a run's responses; `<RUN>` is the run directory,
for example `results/massive-run-article`. All grading rules and the
output schema live in `harness/score/scoring-conventions.md`; merge and
reporting in `harness/score/merge-score-cards.md`. Relative paths resolve from
the repository root.

Scorers: Claude Code, Codex, and Cursor. Each scorer, via its own parent
agent, runs the job below over every unit.

## Units

- A unit is one `(corpus, question, key group)`.
- Key groups, slugs as used in filenames: **`sources`** (arms `sources`,
  `baseline`) and **`work-registry`** (arms `workrag`, `directory`). The
  `baseline` arm exists for C2 only; its grading context is
  `harness/score/score-baseline.md`.
- A unit's sessions are the `usage.csv` rows where:
  - `corpus` = the unit's corpus;
  - `key` = the unit's question ID (C1 `Q01`…`Q15`; C2 `Q01`…`Q09`,
    `A01`…`A06` — not an answer key);
  - `arm` ∈ the key group's arms.
- C2 IDs: `usage.csv`, filenames, and the run's `questions.csv` snapshot drop
  the hyphen (`Q01`, `A01`); the C2 answer-key `##` headings keep it
  (`## Q-01`, `## A-01`) — insert the hyphen when extracting the key section.
  C1 IDs match everywhere as-is.
- Example: unit (c2, Q01, sources) → rows with `corpus = c2`, `key = Q01`,
  `arm ∈ {sources, baseline}`.
- The `arm` column is the only valid source of a session's arm; never infer it
  from answer text or filenames.
- A session's response file is `logs/<tool>/<session_id>.md` — the run splits
  logs into per-tool subdirectories (`claude/`, `codex-dir/`, `codex-rag/`,
  `codex-baseline/`); match by the filename stem, which is the `session_id`.
  `logs/skipped/` holds excluded transcripts — never grade from it.

## Parent-agent job

For every unit:

1. Fill the prompt template below: the session list with each session's
   response-file path, question text from the run's frozen snapshot
   `<RUN>/questions.csv` (never the current
   `harness/questions.csv`), the unit's `## <QUESTION_ID>` section pasted
   verbatim from the answer key (C2 headings hyphenate the ID: `Q01` →
   `## Q-01`), citation root, and the unit's output file
   `<RUN>/scores/<scorer>/<corpus>-<question>-<key group>.csv`
   (for example `<RUN>/scores/claude/c1-Q01-sources.csv`;
   create the scorer's directory first). Derive the session list and paths
   with a script, not by reading `usage.csv` — its `prompt` cells are large
   quoted blobs that break eyeball CSV parsing.
2. Send it to a fresh subagent. The subagent gets read access only to its
   listed inputs — never the other key group's key. Without a sandbox this is
   an instruction boundary, not physical blindness, so list nothing extra.
3. Verify the file the subagent wrote: expected header, exactly one row per
   listed `session_id`, no extra rows, values per the Output schema. On
   failure rerun the unit once with a fresh subagent; if it fails again, stop
   the unit and report.

After all units: concatenate the unit files into
`<RUN>/scores/<scorer>.csv` — header once at the top, no edits
or re-grading. The scorer's file is complete when every session in `usage.csv`
has exactly one row; check with
`python3 harness/score/validate_score_run.py --run-dir <RUN>`.

Subagents share nothing with each other; the three scorers stay blind to one
another until all score files are complete. `usage.csv` is a parent-agent
input only — subagents never see it.

## Paths

Answer keys:

| Corpus | `sources` | `work-registry` |
| --- | --- | --- |
| C1 | `corpora/corpus-1/ground-truth/scoring/answer-key-sources.md` | `corpora/corpus-1/ground-truth/scoring/answer-key-work-registry.md` |
| C2 | `corpora/corpus-2/ground-truth/scoring/answer-key-sources.md` | `corpora/corpus-2/ground-truth/scoring/answer-key-work-registry.md` |

Citation roots:

| Corpus | `sources` | `work-registry` |
| --- | --- | --- |
| C1 | `corpora/corpus-1/work-registry/med-synth/` | `corpora/corpus-1/work-registry/` |
| C2 | `corpora/corpus-2/work-registry/opentelemetry/` | `corpora/corpus-2/work-registry/` |

Citation roots are read-only allowlists for validating citations made in a
response. They are not generation inputs and do not decide correctness. The C2
Sources root is exactly the 26 frozen converted Source records packaged under
`work-registry/opentelemetry/`. `corpora/corpus-2/sources/` is not a benchmark
input and must not be opened by runners or scorers.

Responses: `<RUN>/logs/`. Session metadata (`arm`, `corpus`,
`key`): `<RUN>/usage.csv`.

## Subagent prompt

```text
Score the responses for corpus <CORPUS>, question <QUESTION_ID>. Relative
paths resolve from the repository root.

The unit's sessions and their response files are exactly:

<SESSION_ID: RESPONSE_PATH — one line per session>

The question: <QUESTION_TEXT>

Each response file holds the generation prompt as a heading, then the final
answer; the boundary is marked with <!-- RESPONSE_START -->. Grade only the
final answer; prompt content receives no credit.

Grade every listed response against the answer-key entry at the end of this
prompt by applying the grading rules in harness/score/scoring-conventions.md. To
validate citations you may open records under <CITATION_ROOT>, but only
records a response actually cites. Open nothing else: no other keys, corpora,
or run files.

Write your scores to <OUT_FILE> as CSV per the Output schema in
scoring-conventions.md:

session_id,correctness,missing_facts,citations_total,citations_valid

one row per listed session, nothing else. If an input is missing or the
prompt/answer boundary is unclear, report the blocking session ID instead of
guessing.

Answer-key entry (grade against this alone):

<KEY_ENTRY>
```
