# What is the status of `opentelemetry-go-contrib` issue `#7254` (otelhttp error recording under the new semantic conventions)?

<!-- RESPONSE_START -->

## Status of `opentelemetry-go-contrib#7254` (otelhttp error recording under new semconv)

**Current status: done / closed as completed — but delivery in a release is not established.**

### Authoritative Work State
Per `work-states/WS-05-contrib.md` (path = `work-state`, Last Updated 2026-03-08), this is task **`T002`**, tracked under WS-05 "Contrib Modules" (Status: in_progress overall, Priority P0, Owner Damien Mathieu / contrib SIG context):

> `T002` (mapped to `#7254`) — Resolve otelhttp error-recording behavior for new semantic conventions. **Closed as completed; release not established.** `(SRC-ISSUE-02, SRC-NOTE-06, SRC-MILE-02, SRC-MILE-04)`

The task is checked off `[x]`. It is **not** listed among WS-05's blockers (only `T005`/otelgrpc stabilization is). WS-05's "Next Update Needed" explicitly flags **"any release containing `#7254`"** as still outstanding.

### Provenance / chronology (Sources)
From `opentelemetry/issues/opentelemetry-go-contrib-7254.md` (SRC-ISSUE-02) — State: `closed (completed)`; Labels: bug, area: instrumentation, instrumentation: otelhttp; Milestone: **v1.40.0**; Updated 2026-01-13:

- **2025-04-23** — Opened by **XSAM**. The bug: `otelhttp` only calls `span.RecordError(err)` when `errType` is empty, but the `ErrorType` method never returns an empty attribute — so under the new semconv the error is effectively never recorded on the span. Renamed same day to "…record error **for spans**…".
- **2025-04/06** — Debate on the right fix. XSAM initially proposed always doing `SetAttributes(ErrorType(err))` + `RecordError(err)` + `SetStatus`. **pellared** argued against, per the semconv "recording errors on spans" guidance: an error result is not an exception (only an unrecovered `panic` is, and the SDK already handles that), so instrumentation should **not** call `span.RecordError` for terminating errors. dashpole asked whether that means `RecordError` should essentially never be called by instrumentation.
- **2025-08-05** — Convergence: XSAM restated pellared's proposal as `SetAttributes(semconv.ErrorType(err))` + `SetStatus(codes.Error, err.Error())` (no `RecordError`); pellared replied "Correct". `RecordError` retained for **non-terminating** errors (e.g. retries) and custom instrumentation.
- **2025-09-18** — Milestoned to **v1.39.0** by MrAlias.
- **2025-10-30 SIG meeting** (`meeting-notes/entry-3479655348.md`, SRC-NOTE-06) — In the "Stabilization of otelhttp" discussion, #7254 was called out as **possibly the only blocker** for otelhttp stabilization (a behavioral change around events vs. attributes). Agreement: begin the API review; **Robert (pellared) takes ownership of #7254** and drafts a clarification document; the existence of bugs does not inherently block stabilization.
- **2025-11-03** — pellared's plan: add OTel-Go-specific "recording errors" guidelines to the Style Guide, noting the semconv `recording-errors.md` is still **Development** and would need to be **Stable** first — and that its stabilization is itself a blocker for otelhttp v1. dashpole: fine if in line with the current Development spec, otherwise update the spec first. pellared confirmed the guidelines would follow the current Development semconv.
- **2025-12-04** — Demilestoned from v1.39.0, **milestoned to v1.40.0** by MrAlias (SRC-MILE-04).
- **2026-01-12** — Cross-referenced from contrib PR `#8386` by pellared.
- **2026-01-13** — **Closed by pellared.**

### Caveats
- No release Source after **v1.39.0** exists in the dataset, so the Work State does **not** treat #7254 as shipped — only as closed. Confirming a v1.40.0 (or later) release containing it is the named next update.
- The dataset's Comments file (`work-states/comments/2026-03.md`) contains no correction touching `#7254` / WS-05 `T002` — the only WS-05 comment (CMT-2026-03-002) concerns `T001` / otelgin `MultipartForm.RemoveAll()`. So the closed-as-completed status stands uncorrected.
- Related spin-off issues opened by pellared during the discussion: contrib `#7470`, opentelemetry-go `#6903` and `#6904`.

**Dataset records cited:** `work-states/WS-05-contrib.md`; `opentelemetry/issues/opentelemetry-go-contrib-7254.md` (SRC-ISSUE-02); `opentelemetry/meeting-notes/entry-3479655348.md` (SRC-NOTE-06); milestone Sources SRC-MILE-02 / SRC-MILE-04; `work-states/comments/2026-03.md`.
