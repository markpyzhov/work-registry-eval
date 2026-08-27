# Has the histogram-reservoir optimization in `opentelemetry-go` pull request `#7443` been released?

<!-- RESPONSE_START -->

**No — not per the available evidence. The PR is merged but its release is not established in this package.**

## What the records show

**PR #7443 itself** (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-7443.md`, `SRC-PR-05`)
- "Optimize histogram reservoir" by **dashpole**, opened 2025-10-02, **merged 2025-12-15T14:59:34Z** into `main` (+173/−61 across 8 files).
- Approach: lock each measurement rather than the whole storage, and defer trace-context extraction from `context.Context` until collection time. Reported ~76% reduction in `HistogramReservoirOffer` and ~64–74% on `SyncMeasure` exemplar benchmarks.
- **Milestone: v1.40.0.** The timeline shows it was milestoned to `v1.39.0` on 2025-10-16, then **demilestoned from v1.39.0 and milestoned to v1.40.0 on 2025-12-04** by MrAlias — i.e. it missed the v1.39.0 release.

**Authoritative Work State** (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-02-metrics-performance.md`)
- Task `T002` (mapped to `#7443`): "Merged; not released in included Sources."
- Listed under Blockers: release delivery for `#7443` and `#7474` is the remaining open question, because **no `v1.40.0` release Source exists in the package**.
- Next update needed: "Evidence of a `v1.40.0` (or later) release that includes `#7443` and `#7474`, if/when available."

**Index confirmation** (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md`)
- `opentelemetry-go#7443` → "merged; release not established"; and under key blockers: "**Merged but unreleased**: `#7443`, `#7474` (moved to `v1.40.0`; no `v1.40.0` release Source)."

## Corroborating detail

- The only release record in the package is `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/releases/release-v1.39.0.md` (`SRC-REL-01`), which does not contain `#7443` — consistent with the 2025-12-04 milestone move.
- The v1.40.0 milestone record (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/milestones/milestone-13661613.md`, `SRC-MILE-03`) is **closed with 120 closed / 0 open**, last updated 2026-02-02. That indicates the milestone's work was completed, but a closed milestone is not a release record, and the Work State explicitly declines to treat it as release evidence.

## Bottom line

The optimization is **merged (2025-12-15) and slated for v1.40.0**, but the package contains no v1.40.0 release artifact, so **shipment cannot be confirmed** from this evidence. The closed v1.40.0 milestone makes it likely the release has since occurred, but that is an inference, not something the records establish.
