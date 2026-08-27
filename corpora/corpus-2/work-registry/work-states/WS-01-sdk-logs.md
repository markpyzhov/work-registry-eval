# WS-01: SDK Logs
**Status**: completed
**Priority**: P1
**Owner**: pellared (Robert Pająk)
**Project**: opentelemetry-go
**Last Updated**: 2025-12-08

## Sources
- `SRC-PR-03` — [opentelemetry-go-7403.md](../opentelemetry/pulls/opentelemetry-go-7403.md)
- `SRC-NOTE-04` — [entry-3479584781.md](../opentelemetry/meeting-notes/entry-3479584781.md)
- `SRC-MILE-02` — [milestone-13145551.md](../opentelemetry/milestones/milestone-13145551.md)
- `SRC-REL-01` — [release-v1.39.0.md](../opentelemetry/releases/release-v1.39.0.md)

## Request / Context
The `Record` type in `sdk/log` mutated caller input when helper methods such as `AddAttributes`, `SetAttributes`, or `SetBody` were used. The change needed to stop that mutation so callers were not surprised by side effects.

## Task List
- [x] `T001` (mapped to PR `#7403`) — Fix `AddAttributes`, `SetAttributes`, and `SetBody` on `Record` so they do not mutate input. `(SRC-PR-03, SRC-NOTE-04, SRC-MILE-02, SRC-REL-01)`

## Active Work
- None.

## Blockers and Dependencies
- None.

## Decisions and Superseded Directions
- None.

## Done / Evidence
- `T001 / PR #7403` — Opened 2025-09-23 by `pellared` and assigned to milestone `v1.39.0` `(SRC-PR-03, SRC-MILE-02)`. On 2025-10-16, Robert asked whether Tyler's review was required; Tyler encouraged other reviewers and David Ashpole offered to review `(SRC-NOTE-04)`. The PR was approved by `dashpole` and merged the same day `(SRC-PR-03)`. Released in `v1.39.0` on 2025-12-08 `(SRC-REL-01)`.

## Needs Manual Triage
- None.

## Next Update Needed
- None.
