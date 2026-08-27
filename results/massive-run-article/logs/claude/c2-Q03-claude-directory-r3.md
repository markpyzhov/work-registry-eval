# Has the histogram-reservoir optimization in `opentelemetry-go` pull request `#7443` been released?

<!-- RESPONSE_START -->

**Short answer: not established as released — as of the registry's latest state, PR #7443 is merged but no release containing it is documented.**

## What the records show

**The PR itself** (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-7443.md`, `SRC-PR-05`)
- "Optimize histogram reservoir" by `dashpole`, open-telemetry/opentelemetry-go#7443 — locks each measurement instead of the whole storage and defers trace-context extraction to collection time (~76% faster `HistogramReservoirOffer`, ~70% on `Measure` with exemplars enabled).
- **State: merged 2025-12-15T14:59:34Z.**
- Milestone history: milestoned to `v1.39.0` on 2025-10-16, then **demilestoned from v1.39.0 and milestoned to `v1.40.0` on 2025-12-04** by MrAlias.

**Authoritative Work State** (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-02-metrics-performance.md`, task `T002`)
- Records `T002` / `#7443` as "Merged, not released in included Sources."
- Blockers section: "No `v1.40.0` release Source is in the package, so release completion is not established."
- Next Update Needed: "Evidence of a `v1.40.0` (or later) release that includes `#7443` and `#7474`, if/when available."

**Index** (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md`)
- Item coverage table: `opentelemetry-go#7443` → "merged; release not established."
- Key blockers: "**Merged but unreleased**: `#7443`, `#7474` (moved to `v1.40.0`; no `v1.40.0` release Source)."

**Why it isn't confirmed**
- The only release record in the package is `v1.39.0`, published 2025-12-08 (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/releases/release-v1.39.0.md`, `SRC-REL-01`). Its changelog does not list #7443 — and it couldn't, since #7443 merged a week after that release. It does contain the sibling work #7427 and the temporality selectors #7434.
- The `v1.40.0` milestone record for opentelemetry-go (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/milestones/milestone-13661613.md`, `SRC-MILE-03`) is **closed** with 120 closed / 0 open, last updated 2026-02-02. That indicates the milestone was completed, but a closed milestone is not a release record, and no `release-v1.40.0` file exists in the package to confirm the tag shipped or that #7443 appears in its changelog.

**No correcting comment**: the comments file (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/comments/2026-03.md`) contains three human corrections (CMT-2026-03-001 through -003), all against WS-03 and WS-05. None touches WS-02 or the release status of #7443.

## Bottom line

The histogram-reservoir optimization is **done and merged into `main` (2025-12-15) and targeted at `v1.40.0`**, but the corpus contains no release evidence that it has actually shipped. The closed `v1.40.0` milestone is suggestive that the release cycle completed, but it is not proof of release delivery for this PR. The same status applies to its sibling, #7474.
