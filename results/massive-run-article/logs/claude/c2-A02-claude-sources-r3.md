# On what date will otelgrpc module stabilization be complete?

<!-- RESPONSE_START -->

## Answer

**There is no completion date.** The dataset contains no target, projected, or actual completion date for otelgrpc module stabilization — the question presupposes a date that the sources do not support.

What the sources do say:

**It is explicitly not scheduled.** In the OTel Go SIG meeting of 2025-10-30, the conclusion on otelgrpc stabilization was that it is "Not likely to stabilize this year; set a goal to finalize a strategy next year once semconv progress is clearer." Note that even the *next year* goal is to finalize a **strategy**, not to complete stabilization.

**It is blocked on an unscheduled upstream dependency.** Two blockers were recorded:
1. RPC semantic conventions (semconv) must stabilize first — dashpole (2025-10-29): telemetry naming conventions "are still unstable for gRPC, and prevent us from making the module stable."
2. An audit of the current otelgrpc API to remove cruft.

**Ownership is conditional, not dated.** David Ashpole's action item is to "Monitor semconv RPC stabilization efforts; once stable, drive otelgrpc module stabilization" — a trigger condition, not a deadline. gRPC team engagement was described as "sporadic and driven by their internal roadmap."

**The closest thing to a timeframe** is MrAlias (2025-10-29), which is a hedge rather than a commitment: "I don't anticipate this stabilization happening within 2025, but I could see us prioritizing it for 2026 if we have community involvement and/or added developer help here."

The most recent source touching gRPC (SIG meeting 2025-11-20) mentions only ongoing, non-release-blocking self-observability PRs for OTel gRPC — no stabilization progress or date.

## Sources cited

- `opentelemetry/meeting-notes/entry-3479655348.md` — [SRC-NOTE-06], Go SIG meeting 2025-10-30 (blockers, "not likely to stabilize this year," dashpole action item)
- `opentelemetry/issues/opentelemetry-go-contrib-8078.md` — [SRC-ISSUE-06], "Restore deprecated `UnaryClientInterceptor`" (MrAlias on 2026 prioritization; dashpole on semconv blocking; closed not_planned 2025-10-31)
- `opentelemetry/meeting-notes/entry-3581463689.md` — [SRC-NOTE-07], Go SIG meeting 2025-11-20 (most recent gRPC mention; no stabilization date)
