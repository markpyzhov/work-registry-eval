# What is the status of `opentelemetry-go-contrib` issue `#7254` (otelhttp error recording under the new semantic conventions)?

<!-- RESPONSE_START -->

## Status of `opentelemetry-go-contrib` #7254

**Closed as completed** on 2026-01-13 by `pellared`. Per the authoritative Work State, the task (`T002`) is done, but **no release is established** in the record.

### Current state
- **State**: `closed (completed)`; **Milestone**: `v1.40.0`; **Labels**: `bug`, `area: instrumentation`, `instrumentation: otelhttp` (`c2/opentelemetry/issues/opentelemetry-go-contrib-7254.md`)
- Work State `T002` is checked off: "Resolve otelhttp error-recording behavior for new semantic conventions. Closed as completed; release not established." (`c2/work-states/WS-05-contrib.md`)
- The v1.40.0 milestone itself is closed (169 closed / 0 open), but the Work State explicitly notes "No release Source after `v1.39.0` establishes delivery" (`c2/opentelemetry/milestones/milestone-14282228.md`, `c2/work-states/WS-05-contrib.md`)

### The problem
`otelhttp`'s transport only called `span.RecordError(err)` when `errType` was *invalid*, but `ErrorType` never returns an empty/invalid attribute — so the comment and the logic contradicted each other, and errors were effectively never recorded as exceptions. Reported by `XSAM` on 2025-04-23 (`c2/opentelemetry/issues/opentelemetry-go-contrib-7254.md`).

### How it was resolved (the substantive decision)
The discussion converged on **not** calling `RecordError` for terminating errors. `pellared` argued an error result is not an exception — unhandled panics are already covered by the SDK's `span.End`, and `RecordError`'s stack trace reflects where the error was *recorded*, not where it originated, at a performance cost. `XSAM` accepted this on 2025-08-05, agreeing the pattern should be:

```go
span.SetAttributes(semconv.ErrorType(err))
span.SetStatus(codes.Error, err.Error())
```

`RecordError` remains valuable for **non-terminating** errors (e.g. retry visibility in custom instrumentation), so no deprecation. `dashpole` conditioned agreement on the guidelines matching the current Development spec rather than getting ahead of it; `pellared` confirmed they would follow the in-Development semconv.

### Chronology
| Date | Event |
|---|---|
| 2025-04-23 | Opened by `XSAM` |
| 2025-06-16 | `pellared` spins off follow-ups: contrib `#7470`, go `#6903`/`#6904` |
| 2025-09-18 | Milestoned to `v1.39.0` by `MrAlias` |
| 2025-10-30 | SIG meeting: flagged as possibly the **only blocker** to otelhttp stabilization; Robert takes ownership to draft a clarification doc |
| 2025-11-03 | `pellared` states semconv "recording errors on spans" must go Stable before otelhttp v1 |
| 2025-12-04 | Demilestoned from `v1.39.0`, moved to `v1.40.0` |
| 2026-01-12 | Cross-referenced from PR `#8386` |
| 2026-01-13 | **Closed** by `pellared` |

(`c2/opentelemetry/issues/opentelemetry-go-contrib-7254.md`, `c2/opentelemetry/meeting-notes/entry-3479655348.md`)

### Caveats worth flagging
- **Delivery not confirmed.** PR `#8386` appears only as a cross-reference immediately before closure; the records contain no merge event for it and no release Source proving the fix shipped. The Work State lists "any release containing `#7254`" under *Next Update Needed*.
- **Stabilization link.** The 2025-10-30 SIG treated #7254 as the likely sole blocker for otelhttp stabilization, though the group also agreed bugs don't inherently block stabilization if fixes are non-breaking or properly versioned. The broader guideline work continues under contrib `#7470`, gated on the semconv error-recording doc moving from Development to Stable (`c2/opentelemetry/meeting-notes/entry-3479655348.md`).

**Files cited**: `c2/work-states/WS-05-contrib.md`, `c2/opentelemetry/issues/opentelemetry-go-contrib-7254.md`, `c2/opentelemetry/meeting-notes/entry-3479655348.md`, `c2/opentelemetry/milestones/milestone-14282228.md`, `c2/opentelemetry/milestones/milestone-13145551.md` (all under `/Users/markpyzhov/VSCodeProjects/corpuses-arms/`)
