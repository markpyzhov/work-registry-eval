# Has the concurrent sum performance work in `opentelemetry-go` pull request `#7427` been released?

<!-- RESPONSE_START -->

Yes — PR #7427 has been released, in opentelemetry-go **v1.39.0**.

## Answer

**Status: merged and released.**

- **PR #7427** — "Use sync.Map and atomics to improve sum performance" by `dashpole`, labeled `area:metrics`, milestone `v1.39.0`. Opened 2025-09-29, merged 2025-10-07 (approved by MrAlias 2025-10-07 and dmathieu 2025-10-07). Changes: +437 / −121 across 14 files.
- **Released in v1.39.0**, tag `v1.39.0` (release "v1.39.0/v0.61.0/v0.15.0/v0.0.14" by MrAlias), **published 2025-12-08**. The release notes list it both in the commit list ("Use sync.Map and atomics to improve sum performance by @dashpole ... /pull/7427") and in the Changed section: "Improve performance of concurrent measurements in `go.opentelemetry.io/otel/sdk/metric`. (#7427)".
- The authoritative Work State **WS-02: Metrics Performance** (status `in_progress`, owner `dashpole`, last updated 2025-12-15) records task `T001` (mapped to #7427) as complete: "Opened 2025-09-29 by `dashpole`; approach accepted 2025-10-02; merged 2025-10-07; released in `v1.39.0`."

### Useful context
The workstream as a whole is still `in_progress`, but not because of #7427. The two sibling performance PRs have **not** been established as released:
- **#7443** (histogram reservoir, per-measurement lock) — moved from v1.39.0 to v1.40.0 on 2025-12-04, merged 2025-12-15; merged, release not established.
- **#7474** (fixed-bucket histogram, sync.Map/atomics) — moved to v1.40.0 on 2025-12-04, merged 2025-12-11; merged, release not established.

WS-02 notes there is no v1.40.0 release source in the package, so those two remain the open item ("Next Update Needed: evidence of a v1.40.0 or later release that includes #7443 and #7474").

### Dataset records cited
- `work-states/WS-02-metrics-performance.md` (path `work-state`) — Task List `T001`, Done/Evidence, Blockers and Dependencies
- `opentelemetry/pulls/opentelemetry-go-7427.md` — SRC-PR-04
- `opentelemetry/releases/release-v1.39.0.md` — SRC-REL-01
- `work-states/index.md` (navigation aid only) — lists `opentelemetry-go#7427` as "merged and released in v1.39.0"
