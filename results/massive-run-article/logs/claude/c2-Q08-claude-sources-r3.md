# What is the status of `opentelemetry-go-contrib` issue `#7254` (otelhttp error recording under the new semantic conventions)?

<!-- RESPONSE_START -->

## Status: Closed (completed)

**Issue:** [otelhttp: Cannot record error for spans when producing new semantic convention (open-telemetry/opentelemetry-go-contrib#7254)](https://github.com/open-telemetry/opentelemetry-go-contrib/issues/7254)

| Field | Value |
|---|---|
| Author | XSAM |
| Created | 2025-04-23 |
| **State** | **closed (completed)** — closed by `pellared` on 2026-01-13 |
| Last updated | 2026-01-13 |
| Labels | bug, area: instrumentation, instrumentation: otelhttp |
| Milestone | **v1.40.0** (contrib milestone 34, now closed: 169 closed / 0 open) |

### The original bug
`otelhttp` called `span.RecordError(err)` only when `errType` was *not* empty, but the `ErrorType` method never returns an empty attribute — so the fallback branch was dead code and errors were effectively never recorded as exceptions. XSAM's point was that the comment and the logic were in conflict.

### How the discussion resolved the design question
The 15-comment thread converged on **not** calling `span.RecordError` for terminating errors:

- **pellared** argued an error result is not an exception; only an unrecovered `panic` is an unhandled exception, and that is already handled by the SDK in `sdk/trace/span.go`. He also noted `RecordError` captures a stack trace from where the error was *recorded*, not where it originated, at a performance cost.
- The agreed pattern (XSAM proposed, pellared confirmed "Correct"):
  ```go
  span.SetAttributes(semconv.ErrorType(err))
  span.SetStatus(codes.Error, err.Error())
  ```
- `RecordError` was kept in the API (not deprecated) for **non-terminating** errors, e.g. retry logic in custom instrumentation.
- **dashpole** asked that the guidelines not get ahead of the spec; pellared confirmed they would follow the current (Development-stage) semantic conventions. pellared's plan was to add OTel Go-specific "recording errors" guidelines to the project Style Guide.

### Timeline highlights
- 2025-09-18 milestoned v1.39.0 → 2025-12-04 demilestoned and moved to **v1.40.0**
- Cross-referenced by spin-off work: contrib #7470, opentelemetry-go #6903 / #6904 / #6648, semantic-conventions PRs #2296 and #3228, contrib #8107
- 2026-01-12 cross-referenced by contrib **PR #8386** (pellared) — the last change referenced before closure
- 2026-01-13 closed by pellared

### Why it mattered beyond otelhttp
Go SIG meeting notes list #7254 as **the only blocker** for otelhttp stabilization — a behavioral change around whether errors are marked as events vs. attributes. The SIG agreed to begin the otelhttp API review, with Robert (pellared) taking ownership of #7254 and drafting a clarifying document, while noting that bugs do not inherently block stabilization if fixes are non-breaking or properly versioned. Earlier notes (2025-09-25) show the issue sitting unassigned and needing a volunteer, which explains the long gap between April 2025 and the eventual January 2026 close.

**Caveat:** the dataset contains the issue's metadata, description, full discussion, and timeline, but not the text of the closing comment itself or the contents of PR #8386, so the exact final code change is inferred from the agreed proposal rather than directly evidenced.

**Sources:** `opentelemetry/issues/opentelemetry-go-contrib-7254.md` [SRC-ISSUE-02]; `opentelemetry/meeting-notes/entry-3479655348.md`; `opentelemetry/meeting-notes/entry-3389930076.md` [SRC-NOTE-01]; `opentelemetry/milestones/milestone-14282228.md` [SRC-MILE-04].
