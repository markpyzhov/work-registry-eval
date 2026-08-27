# Has the histogram-reservoir optimization in `opentelemetry-go` pull request `#7443` been released?

<!-- RESPONSE_START -->

## Answer: No — not established as released. The PR is merged, but the dataset contains no release evidence for it.

**PR #7443 "Optimize histogram reservoir"** (`opentelemetry/pulls/opentelemetry-go-7443.md`, SRC-PR-05):
- Author: dashpole; opened 2025-10-02; **merged 2025-12-15T14:59:34Z** (`optimize_histogram_reservoir` → `main`, +173/-61 across 8 files)
- **Milestone: v1.40.0** — it was moved from v1.39.0 to v1.40.0 on 2025-12-04
- Approvals: MrAlias (2025-12-11), dmathieu (2025-12-15), bboreham (2025-10-16)

**Release status** — the authoritative Work State `WS-02: Metrics Performance` (`work-states/WS-02-metrics-performance.md`, status `in_progress`, owner dashpole, last updated 2025-12-15) records:
- `T002` (mapped to PR `#7443`) — "Optimize histogram reservoir (per-measurement lock). **Merged; not released in included Sources.**"
- Blockers section: "No `v1.40.0` release Source is in the package, so **release completion is not established**."
- Next Update Needed: "Evidence of a `v1.40.0` (or later) release that includes `#7443` and `#7474`, if/when available."

The only release Source in the package is `release-v1.39.0.md` (SRC-REL-01, tag v1.39.0, published 2025-12-08), which predates the merge and does not contain #7443. Its sibling PR #7474 (fixed-bucket histogram, merged 2025-12-11) is in the same position.

One nuance worth flagging: the v1.40.0 milestone Source (`opentelemetry/milestones/milestone-13661613.md`, SRC-MILE-03) shows **State: closed, 120 closed / 0 open**, last updated 2026-02-02 — so the milestone itself was completed after the merge. But a closed milestone is not a release record, and the Work State explicitly declines to treat it as one.

**What the change does** (from the PR description): improves concurrent performance of the histogram reservoir's `Offer` by ~4x (~75% reduction) by locking each measurement rather than the entire storage, and deferring trace-context extraction from `context.Context` until collection time. Benchmarks: `HistogramReservoirOffer` 200.85n → 47.41n (-76.40%); `SyncMeasure/.../Int64Histogram/Attributes/0` 436.7n → 114.8n (-73.72%). Files touched include `sdk/metric/exemplar/histogram_reservoir.go`, `fixed_size_reservoir.go`, and `storage.go`.

**Bottom line:** merged into `main` on 2025-12-15 and targeted at v1.40.0, but the dataset holds no v1.40.0 release record, so I cannot confirm it has shipped.
