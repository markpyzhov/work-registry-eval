# On what date will otelgrpc module stabilization be complete?

<!-- RESPONSE_START -->

The dataset does not contain a completion date for otelgrpc module stabilization — no target date, milestone, or release was ever committed to in these sources.

What the sources do say:

**No date exists; the work is blocked on prerequisites, not scheduled.**

- **MrAlias (2025-10-29)**, on issue open-telemetry/opentelemetry-go-contrib#8078: "I don't anticipate this stabilization happening within 2025, but I could see us prioritizing it for 2026 if we have community involvement and/or added developer help here." That is a hedged possibility, not a commitment.
- **dashpole (2025-10-29)**, same issue: otelgrpc depends on gRPC telemetry naming conventions that "are still unstable," which "prevent us from making the module stable."
- **Go SIG meeting 2025-10-30** (notes posted 2025-11-03) recorded two blockers — RPC semantic conventions must stabilize first, and the otelgrpc API needs an audit — and concluded: "Not likely to stabilize this year; set a goal to finalize a strategy next year once semconv progress is clearer." The goal for 2026 is to finalize a *strategy*, not to complete stabilization.
- The action item assigned to David Ashpole is conditional: "Monitor semconv RPC stabilization efforts; once stable, drive otelgrpc module stabilization." Gating is compounded by sporadic gRPC-team engagement driven by their internal roadmap; outreach via Josh and KubeCon was proposed.

Sources cited (all `path: sources`, dataset 74f29ea88a9c11f197db2303d7337e37):
- `opentelemetry/meeting-notes/entry-3479655348.md` [SRC-NOTE-06] — Go SIG meeting 2025-10-30
- `opentelemetry/issues/opentelemetry-go-contrib-8078.md` [SRC-ISSUE-06] — issue closed not_planned 2025-10-31

Note: a later meeting note (`entry-3581463689.md`, 2025-11-20) mentions ongoing self-observability PRs for OTel gRPC, but those are unrelated to module stabilization and carry no stabilization date.
