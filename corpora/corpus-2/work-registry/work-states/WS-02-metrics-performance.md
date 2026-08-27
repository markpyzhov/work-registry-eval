# WS-02: Metrics Performance
**Status**: in_progress
**Priority**: P0
**Owner**: dashpole
**Project**: opentelemetry-go
**Last Updated**: 2025-12-15

## Sources
- `SRC-PR-04` — [opentelemetry-go-7427.md](../opentelemetry/pulls/opentelemetry-go-7427.md)
- `SRC-PR-05` — [opentelemetry-go-7443.md](../opentelemetry/pulls/opentelemetry-go-7443.md)
- `SRC-PR-06` — [opentelemetry-go-7474.md](../opentelemetry/pulls/opentelemetry-go-7474.md)
- `SRC-NOTE-01` — [entry-3389930076.md](../opentelemetry/meeting-notes/entry-3389930076.md)
- `SRC-NOTE-02` — [entry-3389972183.md](../opentelemetry/meeting-notes/entry-3389972183.md)
- `SRC-NOTE-03` — [entry-3390010099.md](../opentelemetry/meeting-notes/entry-3390010099.md)
- `SRC-NOTE-04` — [entry-3479584781.md](../opentelemetry/meeting-notes/entry-3479584781.md)
- `SRC-NOTE-07` — [entry-3581463689.md](../opentelemetry/meeting-notes/entry-3581463689.md)
- `SRC-MILE-02` — [milestone-13145551.md](../opentelemetry/milestones/milestone-13145551.md)
- `SRC-MILE-03` — [milestone-13661613.md](../opentelemetry/milestones/milestone-13661613.md)
- `SRC-REL-01` — [release-v1.39.0.md](../opentelemetry/releases/release-v1.39.0.md)

## Request / Context
Improve metrics SDK performance (concurrent sum, histogram reservoir, fixed-bucket histogram) and settle how temporality selectors should be configured for users.

## Task List
- [x] `T001` (mapped to PR `#7427`) — Optimize concurrent sum performance (`sync.Map` / atomics). `(SRC-PR-04, SRC-NOTE-02, SRC-MILE-02, SRC-REL-01)`
- [x] `T002` (mapped to PR `#7443`) — Optimize histogram reservoir (per-measurement lock). Merged; not released in included Sources. `(SRC-PR-05, SRC-NOTE-02, SRC-NOTE-03, SRC-NOTE-04, SRC-MILE-02, SRC-MILE-03)`
- [x] `T003` (mapped to PR `#7474`) — Optimize fixed-bucket histogram (`sync.Map` / atomics). Merged; not released in included Sources. `(SRC-PR-06, SRC-NOTE-02, SRC-NOTE-03, SRC-NOTE-07, SRC-MILE-02, SRC-MILE-03)`
- [x] `T004` (mapped to temporality-selector configuration) — Custom string selector parsing/configuration rejected; selector functions themselves released in `v1.39.0`. `(SRC-NOTE-01, SRC-NOTE-03, SRC-NOTE-04, SRC-REL-01)`

## Active Work
- None. Remaining open question is release delivery of `T002` / `T003` (no `v1.40.0` release Source).

## Blockers and Dependencies
- **Release delivery for `T002` / `#7443` and `T003` / `#7474`**: Both PRs were moved from `v1.39.0` to `v1.40.0` on 2025-12-04 `(SRC-PR-05, SRC-PR-06, SRC-MILE-03)`. `#7474` merged 2025-12-11; `#7443` merged 2025-12-15 `(SRC-PR-05, SRC-PR-06)`. The 2025-11-20 meeting said the sync-map histogram / exemplar-reservoir work could slip safely to the next release if not ready `(SRC-NOTE-07)`. No `v1.40.0` release Source is in the package, so release completion is not established.

## Decisions and Superseded Directions
- **Temporality selector configuration (`T004`)**: On 2025-10-09 the SIG rejected exposing custom temporality-selector parsing in the SDK in favor of the full OpenTelemetry configuration file format `(SRC-NOTE-03)`. On 2025-10-16 the prior “Exposed Temporality Selector Function” PR was described as API pollution and slated for closure `(SRC-NOTE-04)`. Separately, `v1.39.0` released temporality selector functions `#7434` (`DeltaTemporalitySelector`, `CumulativeTemporalitySelector`, `LowMemoryTemporalitySelector`) `(SRC-REL-01)`.
- **Performance sequencing**: On 2025-10-02 the SIG accepted the concurrent-sum approach and ordered counter work ahead of histogram / fixed-size work `(SRC-NOTE-02)`.

## Done / Evidence
- `T001 / PR #7427` — Opened 2025-09-29 by `dashpole`; approach accepted 2025-10-02 `(SRC-NOTE-02)`; merged 2025-10-07; released in `v1.39.0` `(SRC-PR-04, SRC-REL-01)`.
- `T002 / PR #7443` — Opened 2025-10-02; 2025-10-16 notes describe the simpler per-measurement-lock approach and ~3x–4x improvement `(SRC-NOTE-04)`; moved to `v1.40.0` 2025-12-04; merged 2025-12-15. **Merged, not released** in included Sources `(SRC-PR-05, SRC-MILE-03)`.
- `T003 / PR #7474` — Opened 2025-10-08; discussed as safe to slip on 2025-11-20 `(SRC-NOTE-07)`; moved to `v1.40.0` 2025-12-04; merged 2025-12-11. **Merged, not released** in included Sources `(SRC-PR-06, SRC-MILE-03)`.
- `T004` — Custom configuration approach rejected `(SRC-NOTE-03, SRC-NOTE-04)`; selector functions shipped in `v1.39.0` via `#7434` `(SRC-REL-01)`.

## Needs Manual Triage
- None.

## Next Update Needed
- Evidence of a `v1.40.0` (or later) release that includes `#7443` and `#7474`, if/when available.
