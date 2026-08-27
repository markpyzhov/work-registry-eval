# On what date will otelgrpc module stabilization be complete?

<!-- RESPONSE_START -->

**No completion date exists in the record — the question presumes a scheduled date that has not been set.**

## What the records actually say

**`otelgrpc` module stabilization is unscheduled, blocked, and still open.**

`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md` (authoritative Work State, last updated 2026-03-08) tracks this as task `T005`, unchecked:

- Listed under Active Work as: "Stabilization timing remains unresolved"
- Listed under Blockers and Dependencies: depends on RPC semantic-convention stabilization plus active gRPC-team engagement (characterized as sporadic); "not expected within 2025"
- Listed under Next Update Needed as an item still awaiting progress

`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md` corroborates, listing `otelgrpc` stabilization under "Blocked / deferred" (RPC semconv + gRPC engagement).

## Provenance for why there is no date

`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3479655348.md` (SIG meeting 2025-10-30) records two blockers — RPC semconv must stabilize first, and an API audit to remove cruft — and concludes: not likely to stabilize that year, with a goal only to *finalize a strategy* the following year once semconv progress is clearer. David Ashpole (`dashpole`) is the action-item owner: monitor semconv RPC stabilization, and drive module stabilization once semconv is stable. That is a dependency-gated trigger, not a date.

`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/issues/opentelemetry-go-contrib-8078.md` has `MrAlias` on 2025-10-29 stating he does not anticipate stabilization within 2025, and could see it prioritized for 2026 given community involvement or added developer help — explicitly conditional. `dashpole` adds that unstable gRPC telemetry naming conventions prevent making the module stable.

## Two related clarifications

- Issue `#8078` is closed (2025-10-31, not planned), but that issue was about **restoring the deprecated `UnaryClientInterceptor`**, not stabilization. Per WS-05-contrib (`T004`) and the meeting notes, stabilizing `otelgrpc` explicitly does **not** imply restoring the deprecated interceptor — it stays removed. The closed issue should not be read as stabilization being resolved.
- No record in the package (including `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/comments/2026-03.md`, the only comments file) supplies a target date, milestone, or completion event for `T005`.
