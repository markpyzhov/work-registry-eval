# What is the status of `opentelemetry-go-contrib` issue `#7254` (otelhttp error recording under the new semantic conventions)?

<!-- RESPONSE_START -->

## Status of `opentelemetry-go-contrib` #7254

**Closed (completed)** — closed by **pellared on 2026-01-13T15:23:09Z**, shipped under milestone **v1.40.0** (the contrib v1.40.0 milestone is itself closed, 169/169 done).

**Metadata**
- Title: "otelhttp: Cannot record error for spans when producing new semantic convention" (renamed from "…Cannot record error when producing…" on the day it was filed)
- Author: XSAM · Opened 2025-04-23 · Last updated 2026-01-13
- Labels: `bug`, `area: instrumentation`, `instrumentation: otelhttp`

**The bug**
`otelhttp`'s transport had a branch that only called `span.RecordError(err)` when the `error.type` attribute came back invalid/empty:

```go
if errType := t.semconv.ErrorType(err); errType.Valid() {
    span.SetAttributes(errType)
} else {
    span.RecordError(err)
}
span.SetStatus(codes.Error, err.Error())
```

But the `ErrorType` method never returns an empty attribute (for `errors.New` values it returns e.g. `*errors.errorString`), so the `RecordError` branch was dead — errors could never be recorded as span events. XSAM's point was that the comment and the logic contradicted each other.

**How it was resolved (the design debate)**
The ~15-comment discussion turned into a semantic-conventions question rather than a simple code fix:
- XSAM initially proposed always doing both: `SetAttributes(ErrorType(err))` + `RecordError(err)` + `SetStatus`, citing the OTel exceptions spec and its Java pseudo-code, and arguing `exception.message` / `exception.stacktrace` are valuable for debugging.
- pellared (Robert Pająk) argued the opposite and prevailed: an error *result* is not an exception; only an unrecovered `panic` is an unhandled exception, and the Go SDK already records that in `span.End`. Per the "recording errors on spans" semconv, terminating errors should be recorded as `error.type` attribute + `SetStatus(codes.Error, …)` **without** `span.RecordError`. He also noted `RecordError`'s stack trace points at where the error was recorded, not where it originated, and costs performance.
- XSAM explicitly agreed on 2025-08-05 ("It makes sense"), pellared confirmed ("Correct").
- dashpole asked whether that means `RecordError` should be deprecated; pellared said no — it remains valid for non-terminating errors (retries, multiple errors, e.g. otelgin) and for custom instrumentation.
- pellared's plan (2025-11-03): add OTel-Go-specific "recording errors" guidelines to the CONTRIBUTING Style Guide, following the current Development semconv. dashpole agreed conditional on not getting ahead of the spec; pellared confirmed the guidelines would follow the in-Development semconv.

**Trajectory / related items**
- Milestoned to v1.39.0 by MrAlias 2025-09-18, then demilestoned and moved to v1.40.0 on 2025-12-04.
- Spawned/linked: contrib #7470, opentelemetry-go #6903 and #6904, semantic-conventions PRs #2296 and #3228, contrib #8107, PR #7456.
- Final cross-reference before closure: **contrib PR #8386** (referenced by pellared 2026-01-12, one day before close) — that PR's own record is not in this dataset, so the exact merged diff can't be confirmed from these sources.

**Project impact**
Go SIG meeting notes list #7254 as the *only* identified blocker for `otelhttp` v1 stabilization — a behavioral change around whether errors are marked as events vs. attributes. The SIG agreed to start the otelhttp API review in parallel, assigned Robert ownership of #7254 to draft a clarifying document, and noted that bugs don't inherently block stabilization if fixes are non-breaking or properly versioned. pellared separately stated that stabilization of the semconv "recording errors on spans" doc is itself a blocker for otelhttp v1. Earlier notes (2025-09-25 SIG) show it sat unassigned and needing a volunteer for months before he picked it up.

**Sources cited** (all `path: sources`, dataset `74f29ea88a9c11f197db2303d7337e37`):
- `opentelemetry/issues/opentelemetry-go-contrib-7254.md` — [SRC-ISSUE-02], primary record: state, labels, milestone, description, full 15-comment discussion, timeline
- `opentelemetry/meeting-notes/entry-3479655348.md` — Go SIG notes on otelhttp stabilization, #7254 as sole blocker, ownership assignment
- `opentelemetry/meeting-notes/entry-3389930076.md` — [SRC-NOTE-01], 2025-09-25 SIG: contrib milestone status, unassigned/needs contributor
- `opentelemetry/milestones/milestone-14282228.md` — [SRC-MILE-04], contrib v1.40.0 milestone, closed, 169/169
