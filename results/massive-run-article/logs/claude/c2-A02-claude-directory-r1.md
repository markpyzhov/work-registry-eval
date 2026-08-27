# On what date will otelgrpc module stabilization be complete?

<!-- RESPONSE_START -->

No completion date exists in the package. Here's the answer.

**There is no completion date for otelgrpc module stabilization — the work is not done, not scheduled, and no target date has been set.**

Evidence:

- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md` (authoritative Work State, last updated 2026-03-08) tracks it as task `T005`, still unchecked/open: "Longer-term `otelgrpc` stabilization (depends on RPC semconv + gRPC engagement)." Under Active Work it states plainly: "**`T005`**: Stabilization timing remains unresolved." It is also listed under Blockers and Dependencies as depending on RPC semantic-convention stabilization and gRPC-team engagement (described as sporadic), "not expected within 2025."
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md` lists `otelgrpc` stabilization under "Blocked / deferred" (RPC semconv + gRPC engagement).

Provenance for why there's no date:

- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/issues/opentelemetry-go-contrib-8078.md` — MrAlias (2025-10-29): "I don't anticipate this stabilization happening within 2025, but I could see us prioritizing it for 2026 if we have community involvement and/or added developer help here." That is an expectation, not a commitment or date.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3479655348.md` (2025-10-30 SIG) — Blockers: RPC semconv must stabilize first, plus an API audit to remove cruft. David (dashpole) is willing to drive module stability *once semconv stabilizes*, but gRPC engagement has been sporadic and driven by their internal roadmap. Conclusion recorded: "Not likely to stabilize this year; set a goal to finalize a strategy next year once semconv progress is clearer." The action item is only to monitor semconv RPC stabilization and sync with Josh on gRPC outreach — no milestone, no target release, no date.

Note also that stabilization does not imply restoring the deprecated `otelgrpc` interceptor — that request (`#8078`) was closed as not planned on 2025-10-31 (`WS-05-contrib.md`, `opentelemetry-go-contrib-8078.md`).

Even the next milestone is gated: the goal is to "finalize a strategy" in 2026 once semconv progress is clearer — a strategy decision, not the stabilization itself. `WS-05-contrib.md` lists "otelgrpc stabilization progress" under Next Update Needed, confirming the package has no further information on timing.
