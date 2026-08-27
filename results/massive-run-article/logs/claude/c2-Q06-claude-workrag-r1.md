# Has the SDK log `Record` mutation fix in `opentelemetry-go` pull request `#7403` been released?

<!-- RESPONSE_START -->

Yes — it has been released.

## Answer

PR **open-telemetry/opentelemetry-go#7403** ("sdk/log: Fix `AddAttributes`, `SetAttributes`, `SetBody` on `Record` to not mutate input") shipped in **v1.39.0**, published **2025-12-08**.

## Current status (authoritative)

Work State **WS-01: SDK Logs** — status **completed**, owner **pellared (Robert Pająk)**, last updated **2025-12-08**. Task `T001` (mapped to PR #7403) is checked off; Active Work, Blockers, and Next Update Needed are all "None". The Done/Evidence entry states directly: "Released in `v1.39.0` on 2025-12-08."

## Provenance and chronology

- **Opened** 2025-09-23 by `pellared`, branch `fix-7364` → `main`, fixing issue #7364. Labeled `pkg:SDK`, `area:logs`, assigned to milestone **v1.39.0**. Changes: +722 / -74 across 5 files (`sdk/log/record.go`, `sdk/log/record_test.go`, removed `race_on_test.go` and `race_off_test.go`, plus `CHANGELOG.md`). [SRC-PR-03, SRC-MILE-02]
- **Review**: approved by `dmathieu` (2025-09-26) and `dashpole` (2025-10-16). `MrAlias` raised a concern that the replacement algorithm iterates `attrs` twice; `pellared` responded that this only happens when a duplicate exists, has the same O-performance, and that benchmarks showed no significant overhead, proposing a separate performance PR. On 2025-10-16 in the SIG meeting context, Robert asked whether Tyler's review was required; Tyler encouraged other reviewers and David Ashpole offered to review. [SRC-PR-03, SRC-NOTE-04]
- **Merged** 2025-10-16T19:07:08Z. `pellared` noted he merged it himself because he was out the following week, inviting follow-up performance issues/PRs — which he said matched the SIG meeting consensus. [SRC-PR-03, SRC-NOTE-04]
- **Released**: tag `v1.39.0` (release "v1.39.0/v0.61.0/v0.15.0/v0.0.14", author MrAlias), published 2025-12-08T16:45:46Z. The changelog's Fixed section lists: "Fix `AddAttributes`, `SetAttributes`, `SetBody` on `Record` in `go.opentelemetry.io/otel/sdk/log` to not mutate input. (#7403)", and the What's Changed list credits the PR to @pellared. [SRC-REL-01]

## What the fix does

`Record`'s `AddAttributes`, `SetAttributes`, and `SetBody` were mutating caller-supplied input, causing race conditions when the same input data was used concurrently across goroutines. The fix adds defensive copying, with allocations occurring only when necessary — i.e. when deduplication happens or data is truncated due to limits. Coverage of `sdk/log/record.go` remained at 100%.

## Dataset records cited

- `work-states/WS-01-sdk-logs.md` (path = work-state) — authoritative status
- `opentelemetry/pulls/opentelemetry-go-7403.md` (SRC-PR-03)
- `opentelemetry/releases/release-v1.39.0.md` (SRC-REL-01)
- `opentelemetry/milestones/milestone-13145551.md` (SRC-MILE-02)
- `opentelemetry/meeting-notes/entry-3479584781.md` (SRC-NOTE-04)
- `work-states/index.md` (navigation aid only; corroborates "merged and released in v1.39.0")
