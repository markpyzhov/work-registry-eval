# On what date will otelgrpc module stabilization be complete?

<!-- RESPONSE_START -->

## Answer

**There is no completion date.** The dataset does not contain any target or completed date for `otelgrpc` module stabilization — the work is not finished and its timing is explicitly unresolved.

### What the records say

**Work State (authoritative, `work-states/WS-05-contrib.md`, WS-05: Contrib Modules, Status `in_progress`, Last Updated 2026-03-08):**
- `T005` — "Longer-term `otelgrpc` stabilization (depends on RPC semconv + gRPC engagement)" is an **unchecked / open** task.
- Blockers and Dependencies: "`T005` / otelgrpc stabilization: Depends on RPC semantic-convention stabilization and active gRPC-team engagement (described as sporadic); not expected within 2025."
- Done / Evidence: "`T005`: Stabilization timing remains unresolved."
- Next Update Needed still lists "otelgrpc stabilization progress" as outstanding.

**Work State Index (`work-states/index.md`, source cutoff 2026-02-27, final Work State through 2026-03-11):** lists `otelgrpc` stabilization under "Blocked / deferred (RPC semconv + gRPC engagement)", and records `opentelemetry-go-contrib#8078` as "restoration not planned; stabilization timing unresolved."

### Provenance / why there is no date

- `SRC-NOTE-06` — OpenTelemetry Go SIG meeting note of 2025-10-30 (`opentelemetry/meeting-notes/entry-3479655348.md`): the SIG concluded it is "Not likely to stabilize this year; set a goal to finalize a **strategy** next year once semconv progress is clearer." Blockers named: RPC semconv must stabilize first, plus an audit of the current otelgrpc API. David Ashpole is willing to drive module stabilization once semconv stabilizes; gRPC-team engagement has been sporadic. Note that what was scheduled for "next year" is a **strategy decision**, not stabilization completion.
- `SRC-ISSUE-06` — `opentelemetry-go-contrib#8078` (`opentelemetry/issues/opentelemetry-go-contrib-8078.md`), closed as *not planned* on 2025-10-31. That closure covers only the request to restore the deprecated `UnaryClientInterceptor`; the Work State explicitly records that stabilizing otelgrpc does not imply restoring that interceptor.
- The 2026-03 Comments file (`work-states/comments/2026-03.md`) contains no correction touching `T005` — the three comments cover WS-03/T001, WS-03/T002, and WS-05/T001 only.

### Bottom line
As of the latest Work State (2026-03-08, index through 2026-03-11), otelgrpc stabilization is **open and deferred with no scheduled or actual completion date**, gated on RPC semantic-convention stabilization and gRPC-team engagement.
