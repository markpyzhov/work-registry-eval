# Has the fixed-bucket histogram optimization in `opentelemetry-go` pull request `#7474` been released?

<!-- RESPONSE_START -->

## Answer: No — not in the assigned dataset's evidence.

PR #7474 ("Use sync.Map and atomics for fixed bucket histograms") is **merged but not established as released**.

### What the records show

**The PR itself** (`opentelemetry/pulls/opentelemetry-go-7474.md`, SRC-PR-06):
- Author: dashpole; opened 2025-10-08
- State: **merged 2025-12-11T16:56:04Z** (branch `optimize_syncmap_histogram` → `main`)
- Milestone: **v1.40.0**
- Changes: +560 / −201 across 7 files; approvals from MrAlias (2025-12-04) and dmathieu (2025-12-09)
- Implements a lockless histogram using atomics plus a `sync.Map` for attribute access — roughly 2x faster measure path (~53% geomean reduction on parallel `SyncMeasure` benchmarks), at the cost of ~20% slower `Collect`

**The Work State** (`work-states/WS-02-metrics-performance.md`, status `in_progress`, last updated 2025-12-15) is explicit:
- `T003 / PR #7474` — "moved to `v1.40.0` 2025-12-04; merged 2025-12-11. **Merged, not released** in included Sources"
- Blockers section: "No `v1.40.0` release Source is in the package, so release completion is not established."
- Next Update Needed: "Evidence of a `v1.40.0` (or later) release that includes `#7443` and `#7474`, if/when available."

### Supporting context

- The only release record in the dataset is **v1.39.0** (published 2025-12-08, `opentelemetry/releases/release-v1.39.0.md`). Since #7474 merged on 2025-12-11 — three days *after* v1.39.0 shipped — it is definitively not in that release. Its changelog does contain the earlier related work: #7175 map-key hashing and #7434 temporality selector functions.
- The **v1.40.0 milestone** record (`opentelemetry/milestones/milestone-13661613.md`, SRC-MILE-03) is **closed** with 120 closed / 0 open, updated 2026-02-02 — which suggests the release cycle completed, but a closed milestone is not a release record, and the Work State does not treat it as establishing delivery.
- The companion PR #7443 (histogram reservoir optimization, merged 2025-12-15) is in the same position: same milestone, same unestablished release status.

### Bottom line

The optimization is merged into `main` and slated for v1.40.0, but the dataset contains no v1.40.0 release record, so shipment cannot be confirmed from this evidence. To close the question you'd need a v1.40.0 (or later) release source added to the package.
