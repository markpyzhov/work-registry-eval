# What is the status of `opentelemetry-go-contrib` issue `#7254` (otelhttp error recording under the new semantic conventions)?

<!-- RESPONSE_START -->

## Status of `opentelemetry-go-contrib` #7254

**Closed as completed** on 2026-01-13 by **pellared** (Robert Pająk). Shipped under milestone **v1.40.0** (contrib milestone 34, now closed: 169/169 done).

### Issue metadata
- Title: "otelhttp: Cannot record error for spans when producing new semantic convention"
- Opened by **XSAM** on 2025-04-23; last updated 2026-01-13
- Labels: `bug`, `area: instrumentation`, `instrumentation: otelhttp`
- Milestone history: milestoned to v1.39.0 (2025-09-18) by MrAlias → demilestoned and moved to **v1.40.0** on 2025-12-04

### The bug
`otelhttp` (transport.go) only called `span.RecordError(err)` in the `else` branch of a check on whether `t.semconv.ErrorType(err)` returned a valid attribute — but `ErrorType` never returns an empty/invalid attribute, so the `RecordError` fallback was dead code. XSAM noted the code comment ("otherwise, record it as an exception") and the actual logic were in conflict. In practice `ErrorType` returns things like `*errors.errorString`, never `ErrorTypeOther`.

### How it was resolved
The long design debate (15 comments) settled on **not** calling `span.RecordError` for terminating errors, per the "recording errors on spans" semantic conventions. pellared's position, which XSAM accepted on 2025-08-05:

```go
span.SetAttributes(semconv.ErrorType(err))
span.SetStatus(codes.Error, err.Error())
```

Key arguments: an error result is not an exception (an unrecovered `panic` is, and the SDK already handles that in `span.End`); `RecordError`'s stack trace points at where the error was *recorded*, not where it originated, and costs performance. `RecordError` was kept in the API for **non-terminating** errors (e.g. retry logic in custom instrumentation), so no deprecation. dashpole's condition was that instrumentation not get ahead of the spec; pellared confirmed the guidelines would follow the current (Development-stage) semconv.

### Spin-off work
pellared filed contrib #7470, opentelemetry-go #6903 and #6904, and cross-referenced semantic-conventions PRs #2296 and #3228 plus opentelemetry-go #6648. Closure was preceded by contrib **PR #8386** (cross-referenced 2026-01-12, one day before close). The plan was to add OTel Go-specific "recording errors" guidelines to the project Style Guide (CONTRIBUTING.md).

### Relationship to otelhttp stabilization
SIG notes record #7254 as "the only blocker I think" for otelhttp v1 — a behavioral change around errors as events vs. attributes. The SIG agreed to start the API review anyway, with Robert taking ownership of #7254 and drafting a clarifying document; they explicitly decided bugs don't inherently block stabilization if fixes are non-breaking or properly versioned. Earlier notes (2025-09-25 / 2025-10-10) show the issue sat unassigned and needing a volunteer for months before pellared picked it up.

### Sources
All from dataset `74f29ea88a9c11f197db2303d7337e37`, `path: sources`:
- `opentelemetry/issues/opentelemetry-go-contrib-7254.md` [SRC-ISSUE-02] — primary
- `opentelemetry/meeting-notes/entry-3479655348.md` — otelhttp stabilization discussion
- `opentelemetry/meeting-notes/entry-3389930076.md` [SRC-NOTE-01] — 2025-09-25 SIG, unassigned status
- `opentelemetry/meeting-notes/entry-3390010099.md` — error recording contrib item
- `opentelemetry/milestones/milestone-14282228.md` [SRC-MILE-04] — contrib v1.40.0 milestone

One caveat: the dataset contains no record of PR #8386's own content, so exactly what code landed is not directly evidenced — only that the issue was closed as completed one day after that PR was cross-referenced.
