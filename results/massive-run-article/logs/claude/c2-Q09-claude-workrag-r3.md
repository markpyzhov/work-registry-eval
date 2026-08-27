# Has the fixed-bucket histogram optimization in `opentelemetry-go` pull request `#7474` been released?

<!-- RESPONSE_START -->

**No — release is not established. PR #7474 is merged but not shown as released in the dataset.**

## Status

`opentelemetry-go#7474` — "Use sync.Map and atomics for fixed bucket histograms" (author: dashpole) — **merged 2025-12-11T16:56:04Z** into `main` from branch `optimize_syncmap_histogram` (+560/−201 across 7 files), carrying **milestone v1.40.0**.

The authoritative Work State (`WS-02: Metrics Performance`, status `in_progress`, owner dashpole, last updated 2025-12-15) records this as:

- Task `T003` (mapped to `#7474`) — "Optimize fixed-bucket histogram (`sync.Map` / atomics). **Merged; not released in included Sources.**"
- Done/Evidence: opened 2025-10-08; discussed as safe to slip on 2025-11-20; **moved to `v1.40.0` on 2025-12-04**; merged 2025-12-11. "**Merged, not released** in included Sources."
- Blockers and Dependencies: "No `v1.40.0` release Source is in the package, so **release completion is not established**."
- Active Work: "None. Remaining open question is release delivery of `T002` / `T003`."
- Next Update Needed: "Evidence of a `v1.40.0` (or later) release that includes `#7443` and `#7474`, if/when available."

The Work State Index corroborates: under "Merged but unreleased — `#7443`, `#7474` (moved to `v1.40.0`; no `v1.40.0` release Source)."

## Important nuance

The v1.40.0 milestone record itself (github.com/open-telemetry/opentelemetry-go/milestone/76) is **closed**, 120 closed / 0 open, updated 2026-02-02 — which suggests the release cycle concluded, but the dataset contains **no v1.40.0 release document**. The only release Source present is `v1.39.0`, which shipped the earlier sibling PR `#7427` (concurrent sum) and temporality selector functions `#7434`. So the dataset cannot confirm the shipped artifact for #7474.

## Related context

- `#7474` was originally targeted at v1.39.0 and moved to v1.40.0 on 2025-12-04, alongside `#7443` (histogram reservoir, merged 2025-12-15) — both in the same unreleased bucket.
- The change implements a lockless atomic histogram with a `sync.Map` for attribute access: ~2x faster Measure (−53% geomean on parallel benchmarks), zero allocations, at the cost of ~20% slower Collect.
- No Work State Comment (the human-correction layer, current through 2026-03-11) revises WS-02 — the three comments on file address WS-03 and WS-05 only. So nothing supersedes the "merged, not released" status.

**Bottom line:** as of the registry's final Work State (2026-03-11), #7474 is complete and merged, slated for v1.40.0, but the dataset holds no evidence of a release containing it.

Dataset records cited: `work-states/WS-02-metrics-performance.md`, `work-states/index.md`, `opentelemetry/pulls/opentelemetry-go-7474.md` (SRC-PR-06), `opentelemetry/milestones/milestone-13661613.md` (SRC-MILE-03), `work-states/comments/2026-03.md`.
