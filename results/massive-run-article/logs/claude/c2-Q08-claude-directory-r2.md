# What is the status of `opentelemetry-go-contrib` issue `#7254` (otelhttp error recording under the new semantic conventions)?

<!-- RESPONSE_START -->

## Status of `opentelemetry-go-contrib#7254` — otelhttp error recording under new semantic conventions

**Closed as completed on 2026-01-13 by `pellared`. Task `T002` in the Contrib work state is checked off, but no release Source establishes delivery.**

### Current state
- Work State `WS-05: Contrib Modules` (in_progress, P0, owner Damien Mathieu, last updated 2026-03-08) records `T002` (mapped to `#7254`) as done: "Closed as completed; release not established." (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md`)
- The registry index summarizes it identically: `opentelemetry-go-contrib#7254` → "closed; release not established" (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md:33`)
- Issue record: State `closed (completed)`, labels `bug`, `area: instrumentation`, `instrumentation: otelhttp`, milestone `v1.40.0` (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/issues/opentelemetry-go-contrib-7254.md`)

### Chronology
- **2025-04-23** — Opened by `XSAM`: `otelhttp` only calls `span.RecordError(err)` when `errType` is invalid/empty, but `ErrorType` never returns an empty attribute, so the comment and the branch logic conflict.
- **2025-09-18** — Milestoned to `v1.39.0` by `MrAlias`.
- **2025-10-30 SIG meeting** — Discussed as possibly the *only* blocker for otelhttp stabilization; it is a behavioral change (errors as events vs attributes) interacting with semconv/spec wording. Agreement: begin the otelhttp API review; **Robert (`pellared`) takes ownership of #7254** and drafts a clarification document; bugs do not inherently block stabilization. (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3479655348.md:56-65, 98-104`)
- **2025-12-04** — Demilestoned from `v1.39.0`, remilestoned to `v1.40.0` by `MrAlias` (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/milestones/milestone-14282228.md`, milestone now closed, 169 closed / 0 open).
- **2026-01-12** — Cross-referenced from contrib PR `#8386` by `pellared`; **2026-01-13** — closed by `pellared`.

### Technical resolution reached in discussion
`pellared` argued an error result is not an exception, and that per the "recording errors on spans" semantic conventions, **terminating errors should not use `span.RecordError`** — the unrecovered-panic case is already handled by the SDK, and `RecordError`'s stack trace reflects the recording site, not the origin, at a performance cost. `XSAM` converged on this on 2025-08-05: for a terminating error, set `semconv.ErrorType(err)` as an attribute plus `span.SetStatus(codes.Error, err.Error())`, without `RecordError`. `pellared` confirmed. `RecordError` retains value for non-terminating cases. `pellared` also planned OTel-Go-specific "recording errors" guidelines in the Style Guide (scoped to contrib `#7470`) and stated that **stabilization of the semconv `recording-errors.md` (still "Development") is a blocker for otelhttp v1**; `dashpole` agreed provided guidelines stay in line with the current spec rather than getting ahead of it.

### Caveats
- Delivery is **not** established by the evidence: the only release Source is `v1.39.0` (published 2025-12-08, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/releases/release-v1.39.0.md`), which predates the close and is the milestone `#7254` was moved *off* of. The work state's "Next Update Needed" explicitly lists "any release containing `#7254`" as an open follow-up.
- The linked PR `#8386` is present only as a cross-reference in the timeline; no PR record or merge event for it exists in this package.
