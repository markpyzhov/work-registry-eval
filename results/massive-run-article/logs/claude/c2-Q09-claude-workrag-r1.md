# Has the fixed-bucket histogram optimization in `opentelemetry-go` pull request `#7474` been released?

<!-- RESPONSE_START -->

## Answer: No — not per this dataset's evidence.

**PR #7474** ("Use sync.Map and atomics for fixed bucket histograms", open-telemetry/opentelemetry-go) is **merged but not established as released** in the assigned dataset.

### Key facts

**The PR itself** (`opentelemetry/pulls/opentelemetry-go-7474.md`, SRC-PR-06):
- Author: dashpole; opened 2025-10-08; **merged 2025-12-11T16:56:04Z** (branch `optimize_syncmap_histogram` → `main`)
- Milestone: **v1.40.0** (moved there from v1.39.0 on 2025-12-04)
- Content: lockless histogram via atomics + `sync.Map` for attribute access, ~2x measure-path improvement (~-53% geomean on parallel `SyncMeasure` benchmarks); collect path ~+20% slower, accepted as a tradeoff
- Approvals: MrAlias 2025-12-04, dmathieu 2025-12-09

**Authoritative work state** (`work-states/WS-02-metrics-performance.md`, status `in_progress`, owner dashpole, last updated 2025-12-15):
- Task `T003` (mapped to #7474): "Optimize fixed-bucket histogram (`sync.Map` / atomics). **Merged; not released in included Sources.**"
- Blockers section: "No `v1.40.0` release Source is in the package, so **release completion is not established**."
- Active Work: "None. Remaining open question is release delivery of `T002` / `T003`."
- Next Update Needed: "Evidence of a `v1.40.0` (or later) release that includes `#7443` and `#7474`, if/when available."

### Why the dataset can't confirm a release
The only release record present is **v1.39.0** (`opentelemetry/releases/release-v1.39.0.md`, SRC-REL-01), published **2025-12-08** — three days *before* #7474 merged, so it cannot contain it. Its changelog confirms this: it lists the related sum optimization #7427 and selector functions #7434, but not #7474. There is no v1.40.0 release document in the dataset.

### One nuance worth flagging
The v1.40.0 milestone record (`opentelemetry/milestones/milestone-13661613.md`, SRC-MILE-03) shows **State: closed, 120 closed / 0 open**, last updated 2026-02-02. A closed milestone is suggestive that v1.40.0 shipped, but a closed milestone is not a release record, and the work state explicitly declines to treat it as release evidence. So: almost certainly delivered in v1.40.0, but **not provable from this dataset**.

### Companion item
The sibling PR **#7443** (histogram reservoir, T002) is in the same position — merged 2025-12-15, milestone v1.40.0, not released in included sources.
