# What is the status of `opentelemetry-go-contrib` issue `#7254` (otelhttp error recording under the new semantic conventions)?

<!-- RESPONSE_START -->

## Status of `opentelemetry-go-contrib#7254` — otelhttp error recording under the new semantic conventions

**Bottom line: Done / closed as completed — but delivery in a release is not established in the registry.**

The authoritative Work State entry is `WS-05: Contrib Modules` (`work-states/WS-05-contrib.md`, path = `work-state`, Last Updated 2026-03-08, overall WS status `in_progress`, P0, owner Damien Mathieu). Within it, this issue is task **`T002` (mapped to `#7254`)**, marked **`[x]` complete**: "Resolve otelhttp error-recording behavior for new semantic conventions. Closed as completed; release not established."

### Chronology (from Sources)

From `SRC-ISSUE-02` (`opentelemetry/issues/opentelemetry-go-contrib-7254.md`) and the WS-05 Done/Evidence section:

- **2025-04-23** — Opened by **XSAM**; labeled `bug`, `area: instrumentation`, `instrumentation: otelhttp`. Renamed same day to "otelhttp: Cannot record error for spans when producing new semantic convention".
- **2025-09-18** — Milestoned to **v1.39.0** by MrAlias.
- **2025-10-30 SIG meeting** (`SRC-NOTE-06`, `opentelemetry/meeting-notes/entry-3479655348.md`) — discussed under "Stabilization of otelhttp": #7254 called out as possibly *the only blocker*; **Robert (pellared) took ownership** to draft a clarification document. The meeting also agreed bugs don't inherently block stabilization and the API review should begin.
- **2025-12-04** — Demilestoned from v1.39.0, **milestoned to v1.40.0** (`SRC-MILE-04`, `milestone-14282228.md`).
- **2026-01-13** — **Closed by pellared** (state: `closed (completed)`), preceded by a cross-reference to PR `#8386` on 2026-01-12.

### The technical substance

The bug: `otelhttp`'s transport only called `span.RecordError(err)` when `errType` was empty, but `ErrorType` never returns an empty attribute — so the error was effectively never recorded as an event. XSAM argued the comment and logic were conflicted.

The resolution direction that emerged, driven by **pellared**, is *not* XSAM's original proposal (set `error.type` **and** `RecordError`). Instead, per the "recording errors on spans" semantic conventions, **terminating errors should not use `span.RecordError`** — the pattern is:

```go
span.SetAttributes(semconv.ErrorType(err))
span.SetStatus(codes.Error, err.Error())
```

XSAM agreed ("It makes sense") on 2025-08-05. `span.RecordError` is retained for **non-terminating** errors (e.g. retries) and unrecovered panics (already handled by the SDK's `span.End`). pellared's stated plan was to add OTel-Go-specific error-recording guidelines to the Style Guide, and dashpole asked that the spec not be outrun — pellared confirmed the guidelines follow the current (Development-stage) semconv.

### Caveats and open threads

- **Release not established.** WS-05 explicitly notes "No release Source after `v1.39.0` establishes delivery," and its *Next Update Needed* section lists "**any release containing `#7254`**" as an outstanding item. The issue carries milestone **v1.40.0**, but no source in the dataset confirms that release shipped.
- **otelhttp v1 stabilization remains gated** on semconv: pellared stated that stabilization of the `recording-errors.md` "Recording errors on spans" doc (still **Development**) is a blocker for `otelhttp` v1, and opened `#7470`, `opentelemetry-go#6903`, and `#6904` as related work.
- No Comments-layer records apply to this task — the only applied comment in WS-05 (`CMT-2026-03-002`) concerns `T001`/`#5946`, not `#7254`.

**Dataset records used:** `work-states/WS-05-contrib.md` (work-state, authoritative); `opentelemetry/issues/opentelemetry-go-contrib-7254.md` (SRC-ISSUE-02); `opentelemetry/meeting-notes/entry-3479655348.md` (SRC-NOTE-06); `opentelemetry/milestones/milestone-14282228.md` (SRC-MILE-04) and `milestone-13145551.md` (SRC-MILE-02) as cited by the Work State.
