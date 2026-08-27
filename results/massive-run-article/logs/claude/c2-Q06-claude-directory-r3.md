# Has the SDK log `Record` mutation fix in `opentelemetry-go` pull request `#7403` been released?

<!-- RESPONSE_START -->

**Yes — it was released in `v1.39.0` on 2025-12-08.**

## Details

**The fix**: PR [#7403](https://github.com/open-telemetry/opentelemetry-go/pull/7403), "sdk/log: Fix AddAttributes, SetAttributes, SetBody on Record to not mutate input," authored by `pellared` (Robert Pająk). It fixes issue #7364, where the `Record` type in `sdk/log` mutated caller-supplied input when `AddAttributes`, `SetAttributes`, or `SetBody` were called. Allocations now happen only when necessary (deduplication or limit-driven truncation).

**Timeline**:
- Opened 2025-09-23, milestoned to `v1.39.0` on 2025-09-25
- Went through several draft cycles (an incomplete first fix, then a `MrAlias` review flagging a two-pass dedup algorithm as a performance regression, addressed 2025-10-01)
- Approved by `dmathieu` (2025-09-26) and `dashpole` (2025-10-16); merged by `pellared` on 2025-10-16
- Released in `v1.39.0` (tag published 2025-12-08T16:45:46Z, released by `MrAlias` alongside v0.61.0/v0.15.0/v0.0.14)

The release notes list it under **Fixed**: "Fix `AddAttributes`, `SetAttributes`, `SetBody` on `Record` in `go.opentelemetry.io/otel/sdk/log` to not mutate input. (#7403)".

The tracking Work State **WS-01: SDK Logs** is marked `completed`, with its single task `T001` (mapped to #7403) done, no active work, and no blockers.

## Sources

- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-01-sdk-logs.md` — authoritative status (completed; released in v1.39.0)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-7403.md` — PR detail, merge date, review history
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/releases/release-v1.39.0.md` — release date and changelog entry
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/milestones/milestone-13145551.md` — v1.39.0 milestone, closed
