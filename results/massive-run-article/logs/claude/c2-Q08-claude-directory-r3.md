# What is the status of `opentelemetry-go-contrib` issue `#7254` (otelhttp error recording under the new semantic conventions)?

<!-- RESPONSE_START -->

## Status of `opentelemetry-go-contrib` #7254

**Closed as completed.** Closed 2026-01-13 by `pellared`; milestone `v1.40.0`. In the Work Registry it is task `T002` in WS-05 (Contrib Modules), marked done — but with the caveat that **no Source establishes a release containing the fix**.

### Key facts

- **Issue**: "otelhttp: Cannot record error for spans when producing new semantic convention", opened 2025-04-23 by `XSAM`. Labels: `bug`, `area: instrumentation`, `instrumentation: otelhttp`. State: `closed (completed)`.
- **The bug**: `otelhttp`'s transport only calls `span.RecordError(err)` when `t.semconv.ErrorType(err)` returns an invalid/empty attribute — but `ErrorType` never returns an empty attribute (it falls back to e.g. `*errors.errorString`), so the `else` branch was effectively dead. The code comment and the logic conflicted.
- **Resolution direction** (settled in-thread, 2025-08-05): follow the "recording errors on spans" semantic conventions — set `error.type` as an attribute and set span status, and do **not** call `span.RecordError` for *terminating* errors. `pellared` argued an error result is not an exception; `RecordError` remains appropriate for non-terminating cases (e.g. panics handled by the SDK, multiple errors). `XSAM` accepted this. Note this reversed XSAM's original proposal, which was to always call both `SetAttributes(ErrorType(err))` and `RecordError(err)`.

### Chronology

| Date | Event |
|---|---|
| 2025-04-23 | Opened by XSAM |
| 2025-08-05 | Resolution approach agreed (error.type attribute + status, no `RecordError`) |
| 2025-09-18 | Milestoned to `v1.39.0` by `MrAlias` |
| 2025-10-30 | SIG meeting: flagged as possibly the **only blocker** to otelhttp stabilization; **Robert (`pellared`) took ownership** and agreed to draft a clarification doc on error marking / semconv alignment |
| 2025-11-03 | `pellared` proposed adding OTel-Go "recording errors" guidance to the Style Guide, scoped under contrib `#7470`; noted semconv `recording-errors.md` is still "Development" and must go Stable — and that this is a **blocker for otelhttp v1**. `dashpole` agreed provided guidelines stay in line with the current spec |
| 2025-12-04 | Demilestoned from `v1.39.0`, remilestoned to `v1.40.0` by `MrAlias` |
| 2026-01-12 | Cross-referenced from contrib PR `#8386` |
| 2026-01-13 | **Closed** by `pellared` |

### Caveats

- The `v1.40.0` milestone is itself closed (169 closed / 0 open), but the registry explicitly records that **no release Source establishes delivery** of the fix. WS-05's "Next Update Needed" lists "any release containing `#7254`" as still outstanding.
- Note the SIG's position that bugs do not inherently block stabilization if fixes are non-breaking or properly versioned — so otelhttp stabilization was not necessarily gated on this closing.
- PR `#8386` appears only as a cross-reference in the timeline; no merge event for it is in the frozen Sources.

### Files

- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md` (authoritative status; `T002`, lines 30, 53)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/issues/opentelemetry-go-contrib-7254.md` (`SRC-ISSUE-02` — full discussion and timeline)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3479655348.md` (`SRC-NOTE-06` — 2025-10-30 SIG, stabilization blocker + Robert's ownership)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/milestones/milestone-13145551.md` (`SRC-MILE-02`, v1.39.0) and `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/milestones/milestone-14282228.md` (`SRC-MILE-04`, v1.40.0)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md` (line 33) and `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/integrations/github.md` (line 20)
