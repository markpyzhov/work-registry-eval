# On what date will otelgrpc module stabilization be complete?

<!-- RESPONSE_START -->

**No completion date exists in the assigned dataset — the question presupposes a scheduled date that the sources do not support.**

What the sources actually say about otelgrpc stabilization:

- **No date is set, and it is explicitly open-ended.** In the Go SIG meeting of 2025-10-30 (`opentelemetry/meeting-notes/entry-3479655348.md`, SRC-NOTE-06), the conclusion recorded was: "Not likely to stabilize this year; set a goal to finalize a strategy next year once semconv progress is clearer." Note that the goal for the following year is to finalize a *strategy*, not to complete stabilization.

- **The stated blockers are unresolved and have no timeline.** Same note: RPC semantic conventions (semconv) must stabilize first, and an audit of the current otelgrpc API is needed to remove cruft. Action item for David Ashpole: "Monitor semconv RPC stabilization efforts; once stable, drive otelgrpc module stabilization" — i.e., the start is conditional on an external dependency, with no date attached.

- **Maintainers declined to commit to a timeframe.** In issue #8078 (`opentelemetry/issues/opentelemetry-go-contrib-8078.md`, SRC-ISSUE-06), MrAlias on 2025-10-29: "I don't anticipate this stabilization happening within 2025, but I could see us prioritizing it for 2026 if we have community involvement and/or added developer help here." That is a conditional possibility, not a schedule. dashpole on the same issue (2025-10-29) confirms the semconv dependency: naming conventions "are still unstable for gRPC, and prevent us from making the module stable."

- **gRPC-side engagement is uncertain**, described as sporadic and driven by the gRPC team's internal roadmap; David noted only that the semconv SIG "is active and is working towards stabilization," with no date.

- **No later source revises this.** The most recent meeting notes in the dataset (2025-11-20 in `entry-3581463689.md`, and 2026-02-27 in `entry-3974113940.md`) mention otelgrpc only in passing (self-observability PRs, non-release-blocking) and set no stabilization date. Note also that #8078 is closed as *not planned* — it was closed on the separate question of restoring `UnaryClientInterceptor`, which was declined; it is not a stabilization tracking issue that was completed.

For contrast, the dataset does contain concrete milestones for the adjacent **otelhttp** work (issue #7254 was milestoned v1.40.0 and closed 2026-01-13), which makes the absence of any equivalent otelgrpc milestone meaningful rather than merely a retrieval gap.

Sources cited (all `path: sources`, dataset 74f29ea88a9c11f197db2303d7337e37):
- `opentelemetry/meeting-notes/entry-3479655348.md` — SRC-NOTE-06, Go SIG 2025-10-30
- `opentelemetry/issues/opentelemetry-go-contrib-8078.md` — SRC-ISSUE-06
- `opentelemetry/meeting-notes/entry-3581463689.md` — SRC-NOTE-07, Go SIG 2025-11-20
- `opentelemetry/meeting-notes/entry-3974113940.md` — SRC-NOTE-08, Go SIG 2026-02-27
