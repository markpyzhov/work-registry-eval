# Has the concurrent sum performance work in `opentelemetry-go` pull request `#7427` been released?

<!-- RESPONSE_START -->

Yes — PR #7427 has been released.

## Answer

**"Use sync.Map and atomics to improve sum performance" (open-telemetry/opentelemetry-go#7427) shipped in `v1.39.0`.**

Details from the dataset:

- **PR status**: merged 2025-10-07T13:40:23Z, authored by `dashpole`, branch `optimize_counter_syncmap` → `main`, +437/-121 across 14 files, milestone `v1.39.0`. Approved by MrAlias (2025-10-07) and dmathieu (2025-10-07). (`SRC-PR-04`, `opentelemetry/pulls/opentelemetry-go-7427.md`)
- **Release**: `v1.39.0` (tagged release "v1.39.0/v0.61.0/v0.15.0/v0.0.14") was published **2025-12-08T16:45:46Z** by MrAlias, and its "What's Changed" list explicitly includes "Use sync.Map and atomics to improve sum performance by @dashpole in .../pull/7427". The changelog entry reads: "Improve performance of concurrent measurements in `go.opentelemetry.io/otel/sdk/metric`. (#7427)". (`SRC-REL-01`, `opentelemetry/releases/release-v1.39.0.md`)
- **Authoritative work state**: WS-02 "Metrics Performance" (`work-states/WS-02-metrics-performance.md`, last updated 2025-12-15) records task `T001` (mapped to PR #7427) as done: "Opened 2025-09-29 by `dashpole`; approach accepted 2025-10-02; merged 2025-10-07; **released in `v1.39.0`**".

## Important adjacent context (not released)

The other two metrics-performance PRs in the same work stream are merged but **not** established as released in this dataset:

- `#7443` — histogram reservoir (per-measurement lock): merged 2025-12-15, moved from v1.39.0 to **v1.40.0** on 2025-12-04.
- `#7474` — fixed-bucket histogram (sync.Map/atomics, ~2x improvement, design modeled on #7427): merged 2025-12-11, also moved to **v1.40.0**.

WS-02 is still `in_progress` solely because no `v1.40.0` release record exists in the dataset; its only "Next Update Needed" is evidence of a v1.40.0-or-later release containing #7443 and #7474.

No work-state comments (`path = comments`) affect WS-02 — the three recorded corrections apply to WS-03 and WS-05.
