# Has the SDK log `Record` mutation fix in `opentelemetry-go` pull request `#7403` been released?

<!-- RESPONSE_START -->

Yes — the fix has been released.

## Answer

**PR #7403** ("sdk/log: Fix `AddAttributes`, `SetAttributes`, `SetBody` on `Record` to not mutate input") shipped in **opentelemetry-go v1.39.0**, released **2025-12-08**.

### Evidence

- **Work State `WS-01: SDK Logs`** (`work-states/WS-01-sdk-logs.md`, path = `work-state`) — Status: **completed**, Owner pellared (Robert Pająk), Last Updated 2025-12-08. Task `T001` (mapped to PR `#7403`) is checked off, Active Work is "None", and the Done/Evidence section states: opened 2025-09-23 by pellared, assigned to milestone `v1.39.0`, approved by `dashpole` and merged 2025-10-16, "Released in `v1.39.0` on 2025-12-08".
- **`SRC-PR-03`** (`opentelemetry/pulls/opentelemetry-go-7403.md`) — State: **merged** 2025-10-16T19:07:08Z, branch `fix-7364` → `main`, milestone **v1.39.0**, +722/−74 across 5 files, labels pkg:SDK / area:logs.
- **`SRC-REL-01`** (`opentelemetry/releases/release-v1.39.0.md`) — Release v1.39.0/v0.61.0/v0.15.0/v0.0.14 by MrAlias, created 2025-12-08T16:32:32Z. Its changelog "Fixed" section lists: "Fix `AddAttributes`, `SetAttributes`, `SetBody` on `Record` in `go.opentelemetry.io/otel/sdk/log` to not mutate input. (#7403)", and the commit list credits the PR to @pellared.

### What the fix does

Adds defensive copying in `sdk/log/record.go` so caller-supplied attributes/body are no longer mutated; allocations occur only when deduplication or limit-based truncation is needed. Tests were expanded in `record_test.go`, and the race-condition workarounds `race_on_test.go` / `race_off_test.go` were deleted since the underlying race is gone. Coverage of `record.go` stayed at 100%.

### Notable history

MrAlias raised a performance concern on 2025-09-29 (the replacement algorithm iterating `attrs` twice); pellared reworked it and posted improved benchstat results on 2025-10-01. dashpole approved on 2025-10-16 and pellared merged the same day, noting that any further performance work should be a follow-up PR (consistent with the SIG meeting consensus recorded in `SRC-NOTE-04`).
