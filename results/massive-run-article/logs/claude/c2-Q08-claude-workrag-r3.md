# What is the status of `opentelemetry-go-contrib` issue `#7254` (otelhttp error recording under the new semantic conventions)?

<!-- RESPONSE_START -->

## Status of `opentelemetry-go-contrib#7254` — otelhttp error recording under new semconv

**Bottom line: Done / closed as completed, but the release delivering it is not established in the dataset.**

### Authoritative work-state position
Tracked as **`WS-05: Contrib Modules` → `T002`** (mapped to `#7254`): *"Resolve otelhttp error-recording behavior for new semantic conventions. Closed as completed; release not established."* — marked `[x]` (done). The parent work state `WS-05` is itself still `in_progress` (P0, owner Damien Mathieu, last updated 2026-03-08) because of other tasks, not this one. `WS-05`'s "Next Update Needed" explicitly lists *"any release containing `#7254`"* as still-open information.

No Comment (`CMT-*`) record corrects or walks back `T002` — the 2026-03 comments touch `WS-05/T001`, `WS-03/T001`, and `WS-03/T002` only.

### Issue facts and chronology (Sources)
From `opentelemetry/issues/opentelemetry-go-contrib-7254.md` (`SRC-ISSUE-02`):
- **State**: closed (completed). **Milestone**: `v1.40.0`. **Labels**: bug, area: instrumentation, instrumentation: otelhttp.
- Opened 2025-04-23 by **XSAM**; updated/closed **2026-01-13T15:23:09Z by pellared** (Robert Pająk).
- Milestoned to `v1.39.0` on 2025-09-18 by MrAlias; **demilestoned from v1.39.0 and moved to `v1.40.0` on 2025-12-04**.
- Cross-referenced shortly before closure by pellared from contrib PR `#8386` (2026-01-12) and from semantic-conventions PRs `#2296` (2025-10-16) and `#3228` (2025-12-19).

### The technical substance
The bug: `otelhttp`'s transport only called `span.RecordError(err)` when the `errType` attribute was invalid/empty, but `ErrorType` never returns an empty attribute — so errors were effectively never recorded as span events. XSAM noted the comment and the logic were in conflict, and that most errors yield `error.type = *errors.errorString`.

Two positions were debated:
- **XSAM** initially proposed always calling both `span.SetAttributes(t.semconv.ErrorType(err))` and `span.RecordError(err)`, arguing `exception.message` / `exception.stacktrace` are valuable for debugging.
- **pellared** argued against `RecordError` for **terminating** errors, per the semconv "recording errors on spans" guidance: an error result is not an exception (only an unrecovered panic is, and the SDK already handles that); the stack trace reflects where the error was recorded, not where it originated, and costs performance. His recommended pattern is `span.SetAttributes(semconv.ErrorType(err))` + `span.SetStatus(codes.Error, err.Error())`, with `RecordError` reserved for non-terminating errors (e.g. retries) — **XSAM agreed on 2025-08-05** ("It makes sense").
- **dashpole** asked that instrumentation not get ahead of the spec; pellared confirmed his guidelines would follow the current (Development-stage) semantic conventions, and planned to add Go-specific "recording errors" guidance to the OTel Go Style Guide.

### Relationship to otelhttp stabilization
Per the SIG meeting notes (`SRC-NOTE-06`, `opentelemetry/meeting-notes/entry-3479655348.md`, 2025-10-30): `#7254` was called out as *possibly the only blocker* for otelhttp stabilization — a behavioral change around whether errors are marked as events vs attributes. The SIG agreed to begin the API review, **Robert (pellared) took ownership of `#7254`** to draft a clarification document, and noted that bugs do not inherently block stabilization if fixes are non-breaking or properly versioned. pellared also stated that stabilization of the semconv "recording errors on spans" doc (still Development) is a blocker for otelhttp v1.

### Caveat
The dataset establishes issue closure, not shipped delivery: milestone is `v1.40.0`, and no release Source after `v1.39.0` confirms the fix is released. Whether contrib PR `#8386` merged is not established in Sources — it appears only as a cross-reference.

**Records cited**: `work-states/WS-05-contrib.md` (path `work-state`); `opentelemetry/issues/opentelemetry-go-contrib-7254.md` (`SRC-ISSUE-02`); `opentelemetry/meeting-notes/entry-3479655348.md` (`SRC-NOTE-06`); `opentelemetry/milestones/milestone-14282228.md` (`SRC-MILE-04`); `opentelemetry/milestones/milestone-13145551.md` (`SRC-MILE-02`); `work-states/comments/2026-03.md` (no entry for `T002`).
