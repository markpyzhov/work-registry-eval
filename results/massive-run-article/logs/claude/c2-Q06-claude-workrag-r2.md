# Has the SDK log `Record` mutation fix in `opentelemetry-go` pull request `#7403` been released?

<!-- RESPONSE_START -->

**Yes — released in `v1.39.0` on 2025-12-08.**

## Answer

PR open-telemetry/opentelemetry-go#7403, "sdk/log: Fix `AddAttributes`, `SetAttributes`, `SetBody` on `Record` to not mutate input," has been merged and shipped.

**Timeline**
- Opened 2025-09-23 by `pellared` (Robert Pająk), assigned to milestone `v1.39.0`, labels `pkg:SDK` / `area:logs`, branch `fix-7364` → `main`, +722/-74 across 5 files. It fixes issue #7364.
- Approved by `dmathieu` (2025-09-26) and `dashpole` (2025-10-16); merged 2025-10-16T19:07:08Z.
- Released in tag `v1.39.0` (release `v1.39.0/v0.61.0/v0.15.0/v0.0.14`, published 2025-12-08T16:45:46Z by MrAlias). The release notes' Fixed section carries the entry: "Fix `AddAttributes`, `SetAttributes`, `SetBody` on `Record` in `go.opentelemetry.io/otel/sdk/log` to not mutate input. (#7403)".

**Work state**: `WS-01: SDK Logs` is **completed** (P1, owner pellared, last updated 2025-12-08). Task `T001` (mapped to `#7403`) is checked off; Active Work, Blockers, and Next Update Needed are all "None."

**Substance of the fix**: `sdk/log/record.go` gained defensive copying with optimization checks, so allocations only occur when deduplication or limit-driven truncation actually happens. Tests were expanded in `record_test.go`, and the race-condition workaround files `race_on_test.go` / `race_off_test.go` were removed as no longer needed. One review thread (MrAlias) raised a deduplication performance regression; pellared reworked it, improved the benchmarks, and merged with the agreement that any further performance work would be a follow-up PR.

## Dataset records cited
- `work-states/WS-01-sdk-logs.md` (path `work-state`) — status, task list, Done/Evidence
- `opentelemetry/pulls/opentelemetry-go-7403.md` (`SRC-PR-03`, path `sources`) — PR metadata, reviews, discussion
- `opentelemetry/releases/release-v1.39.0.md` (`SRC-REL-01`, path `sources`) — release tag, publish date, changelog entry
- `work-states/index.md` (navigation aid) — lists `#7403` as "merged and released in `v1.39.0`"
