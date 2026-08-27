# WS-05: Contrib Modules
**Status**: in_progress
**Priority**: P0
**Owner**: Damien Mathieu (contrib SIG context)
**Project**: opentelemetry-go-contrib / community
**Last Updated**: 2026-03-08

## Sources
- `SRC-ISSUE-01` — [opentelemetry-go-contrib-5946.md](../opentelemetry/issues/opentelemetry-go-contrib-5946.md)
- `SRC-PR-01` — [opentelemetry-go-contrib-6609.md](../opentelemetry/pulls/opentelemetry-go-contrib-6609.md)
- `SRC-ISSUE-02` — [opentelemetry-go-contrib-7254.md](../opentelemetry/issues/opentelemetry-go-contrib-7254.md)
- `SRC-ISSUE-05` — [opentelemetry-go-contrib-8059.md](../opentelemetry/issues/opentelemetry-go-contrib-8059.md)
- `SRC-ISSUE-06` — [opentelemetry-go-contrib-8078.md](../opentelemetry/issues/opentelemetry-go-contrib-8078.md)
- `SRC-PR-02` — [community-3000.md](../opentelemetry/pulls/community-3000.md)
- `SRC-PR-07` — [opentelemetry-go-contrib-8014.md](../opentelemetry/pulls/opentelemetry-go-contrib-8014.md)
- `SRC-NOTE-04` — [entry-3479584781.md](../opentelemetry/meeting-notes/entry-3479584781.md)
- `SRC-NOTE-05` — [entry-3479626706.md](../opentelemetry/meeting-notes/entry-3479626706.md)
- `SRC-NOTE-06` — [entry-3479655348.md](../opentelemetry/meeting-notes/entry-3479655348.md)
- `SRC-MILE-02` — [milestone-13145551.md](../opentelemetry/milestones/milestone-13145551.md)
- `SRC-MILE-04` — [milestone-14282228.md](../opentelemetry/milestones/milestone-14282228.md)

## Applied Comments
- `CMT-2026-03-002` — [2026-03.md](comments/2026-03.md) — `RemoveAll()` adopted; cleanup work complete locally, pending publication.

## Request / Context
Track open contrib instrumentation work and related community proposals: otelgin cleanup and context behavior, otelhttp error recording, otelconf config-file support, otelgrpc interceptor restoration vs longer stabilization, and the Ecosystem Explorer proposal.

## Task List
- [x] `T001` (mapped to `#5946` / PR `#6609`) — Automatic `MultipartForm.RemoveAll()` adopted; conflict resolution and tests complete locally; publication pending. `(SRC-ISSUE-01, SRC-PR-01, SRC-NOTE-04, CMT-2026-03-002)`
- [x] `T002` (mapped to `#7254`) — Resolve otelhttp error-recording behavior for new semantic conventions. Closed as completed; release not established. `(SRC-ISSUE-02, SRC-NOTE-06, SRC-MILE-02, SRC-MILE-04)`
- [x] `T003` (mapped to `#8059`) — Add `OTEL_EXPERIMENTAL_CONFIG_FILE` support via contrib `otelconf`. Issue closed; linked implementation PR `#8106` merge not in Sources. `(SRC-ISSUE-05, SRC-NOTE-05)`
- [x] `T004` (mapped to `#8078`) — Restore deprecated otelgrpc interceptor: closed as not planned. `(SRC-ISSUE-06, SRC-NOTE-06)`
- [ ] `T005` (mapped to otelgrpc stabilization) — Longer-term `otelgrpc` stabilization (depends on RPC semconv + gRPC engagement). `(SRC-ISSUE-06, SRC-NOTE-06)`
- [x] `T006` (mapped to `community#3000`) — Ecosystem Explorer **project proposal** PR. Merged. `(SRC-PR-02, SRC-NOTE-06)`
- [ ] `T007` (mapped to PR `#8014`) — otelgin context save/restore data-race PR. **Status: `closed_without_merge`** (not done under PR done convention). `(SRC-PR-07, SRC-NOTE-04)`

## Active Work
- **`T001` publication follow-up**: Automatic `MultipartForm.RemoveAll()` is the adopted approach and the cleanup implementation is complete locally. Final commits have not been pushed, so issue `#5946` and PR `#6609` remain open/unmerged on GitHub. `(SRC-ISSUE-01, SRC-PR-01, SRC-NOTE-04, CMT-2026-03-002)`
- **`T005`**: Stabilization timing remains unresolved `(SRC-ISSUE-06, SRC-NOTE-06)`.
- **`T007` / `#8014`**: Closed without merge on 2025-10-17 after the SIG treated current context-restore behavior as intentional; users should explicitly pass context into spawned goroutines `(SRC-PR-07, SRC-NOTE-04)`. Remains unchecked — not done.

## Blockers and Dependencies
- **`T005` / otelgrpc stabilization**: Depends on RPC semantic-convention stabilization and active gRPC-team engagement (described as sporadic); not expected within 2025 `(SRC-ISSUE-06, SRC-NOTE-06)`.

## Decisions and Superseded Directions
- **MultipartForm cleanup (`T001`)**: The earlier unresolved choice among `RemoveAll()`, reattach, and user cleanup is superseded. Automatic `MultipartForm.RemoveAll()` is adopted. `(SRC-PR-01, SRC-NOTE-04, CMT-2026-03-002)`
- **otelgrpc interceptor restoration (`T004`)**: Stabilizing `otelgrpc` does not imply restoring the deprecated interceptor; restoration request closed as not planned on 2025-10-31 `(SRC-ISSUE-06, SRC-NOTE-06)`.
- **otelgin context reversal (`T007`)**: On 2025-10-16, Damien and Tyler treated the current context-restore behavior as correct; users should explicitly pass context into spawned goroutines `(SRC-NOTE-04)`. PR `#8014` was closed 2025-10-17 **without a merge event** `(SRC-PR-07)` — `closed_without_merge`, not done.
- **`OTEL_EXPERIMENTAL_CONFIG_FILE` (`T003`)**: On 2025-10-23 the SIG rejected short-term SDK-level support in favor of a contrib `otelconf` prototype path `(SRC-NOTE-05)`. Issue `#8059` was closed 2025-12-04 by `MrAlias` after being cross-referenced to PR `#8106` `(SRC-ISSUE-05)`. The frozen Sources do not include `#8106` or a merge event for it.

## Done / Evidence
- `T001 / #5946 / #6609` — Conflict resolution and tests are complete locally using automatic `MultipartForm.RemoveAll()`. The work is treated as done internally, but final commits are not pushed and the GitHub issue/PR remain open/unmerged. `(CMT-2026-03-002, SRC-ISSUE-01, SRC-PR-01)`
- `T002 / #7254` — Opened 2025-04-23 by `XSAM`; milestoned to `v1.39.0` on 2025-09-18; discussed 2025-10-30 as a possible otelhttp stabilization blocker with Robert assigned to draft clarification `(SRC-NOTE-06)`; moved to `v1.40.0` on 2025-12-04 `(SRC-MILE-04)`; closed 2026-01-13 `(SRC-ISSUE-02)`. No release Source after `v1.39.0` establishes delivery.
- `T003 / #8059` — Closed 2025-12-04 `(SRC-ISSUE-05)`. Linked PR `#8106` appears only as a cross-reference; merge/release not established in Sources.
- `T004 / #8078` — Closed as not planned 2025-10-31 `(SRC-ISSUE-06)`.
- `T006 / community#3000` — Proposal opened 2025-09-19 by `jaydeluca`; 2025-10-30 meeting required semconv alignment, Weaver compatibility, and schema validation `(SRC-NOTE-06)`; merged/closed 2025-12-01 `(SRC-PR-02)`. Explorer product delivery not established.

## Needs Manual Triage
- Whether any in-tree follow-up replaced `#8014` after `closed_without_merge` (`T007`).

## Next Update Needed
- Publication of the completed `#6609` work and GitHub issue update; any release containing `#7254`; whether `#8106` merged; otelgrpc stabilization progress; Explorer implementation beyond the proposal PR.
