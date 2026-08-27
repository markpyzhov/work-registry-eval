# Scoring conventions

Score each response by comparing it directly with the supplied answer key —
the only key in the scoring context. The Sources key reflects the frozen
Sources; the Work Registry key reflects final Work State. Which key applies to
which sessions is decided while preparing the scoring context, never by the
scorer.

## Grade

| Grade | Rule |
| --- | --- |
| **correct** (`1`) | The `Verdict` is right and every bullet under `Required facts` is satisfied. |
| **partial** (`0.5`) | The `Verdict` is right, but one or more `Required facts` bullets are missing or wrong. |
| **incorrect** (`0`) | The operative verdict is wrong, or an `Incorrect if` condition applies. |

### Key fields

- `Verdict`: required conclusion.
- `Required facts`: each bullet is one atomic check and one possible
  `missing_fact`; only indivisible relations or explicit alternatives may share
  a bullet.
- `Optional`: does not affect correctness or `missing_facts`.
- `Partial if`: overrides the general grade rule for the stated case.
- `Incorrect if`: any matching condition makes the answer incorrect.

IDs such as `SRC-SLACK-06` or `WS-03` are audit pointers. Ignore them for
correctness: match facts semantically and never require or retrieve the ID.

## Evidence and citations

- Count citation breadth and validity separately from correctness; citation
  checking cannot add, remove, or change correctness requirements.
- Validate a citation against the cited record. A citation must resolve within
  the supplied key's corpus: frozen Sources under the Sources key, the Work
  Registry package under the Work Registry key.
- Explicitly attributing a fact to a record that does not contain it is
  incorrect when the supplied key identifies that misattribution as material.

Counting:

- `citations_total`: distinct explicit evidence references in the answer body.
  Repeats of the same record count once; an unresolved reference still counts.
  A bare issue/PR/task number mentioned only as the subject of the answer is
  not a citation.
- `citations_valid`: references that resolve under the citation root and
  support the nearby statement in substance. Several citations may jointly
  support one summarized sentence; judge the group semantically. An absolute
  path counts when its relative suffix identifies exactly one record under the
  root.

## Output schema

One CSV per scoring unit, header:

```csv
session_id,correctness,missing_facts,citations_total,citations_valid
```

- `session_id`: the response filename stem;
- `correctness`: 1, 0.5, or 0, per the Grade table;
- `missing_facts`: count of unsatisfied `Required facts` bullets, 0 when the
  key entry has no `Required facts` list;
- `citations_total`, `citations_valid`: per Counting above.

Exactly one row per graded session and nothing else: no arm, model, prose, or
rationale. No blank cells, no duplicate `session_id`, and
`citations_valid <= citations_total`.

## Not scorer inputs

Never use generation, audit, or reporting artifacts to decide correctness.
Comments are also not scorer inputs.

## Reporting

Primary, control, final-state diagnostic, and abstention diagnostic labels are
reporting buckets, not grading rules.

Historical score cards may contain `comment: apply` and
`comment: abstention`. These are legacy reporting values only; they do not tell a
scorer how to grade a new response.
