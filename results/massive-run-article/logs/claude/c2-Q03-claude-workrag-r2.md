# Has the histogram-reservoir optimization in `opentelemetry-go` pull request `#7443` been released?

<!-- RESPONSE_START -->

## Answer

**No — not according to this dataset. PR #7443 is merged but its release is not established.**

The authoritative Work State `WS-02: Metrics Performance` (`work-states/WS-02-metrics-performance.md`, path = `work-state`, Status: `in_progress`, Owner: dashpole, Last Updated 2025-12-15) records:

- `T002` (mapped to PR `#7443`) — "Optimize histogram reservoir (per-measurement lock). **Merged; not released in included Sources.**"
- Done / Evidence: opened 2025-10-02; moved to the `v1.40.0` milestone on 2025-12-04; **merged 2025-12-15**; "**Merged, not released** in included Sources."
- Blockers and Dependencies: "No `v1.40.0` release Source is in the package, so **release completion is not established**."
- Active Work: "None. Remaining open question is release delivery of `T002` / `T003`."
- Next Update Needed: "Evidence of a `v1.40.0` (or later) release that includes `#7443` and `#7474`, if/when available."

## Supporting provenance

- `SRC-PR-05` (`opentelemetry/pulls/opentelemetry-go-7443.md`) — "Optimize histogram reservoir", author dashpole, branch `optimize_histogram_reservoir` → `main`, **State: merged (2025-12-15T14:59:34Z)**, **Milestone: v1.40.0**, +173/−61 across 8 files. Approvals: MrAlias (2025-10-07, again 2025-12-11), bboreham (2025-10-15, 2025-10-16), dmathieu (2025-12-15). The PR body claims ~4x (≈75% reduction) improvement in concurrent `Offer`, with ~64–74% reductions on `SyncMeasure/.../ExemplarsEnabled` histogram benchmarks.
- `SRC-MILE-03` (`opentelemetry/milestones/milestone-13661613.md`) — the `v1.40.0` milestone for opentelemetry-go is **closed**, 120 closed / 0 open, updated 2026-02-02. This is milestone closure, not a release record.
- `SRC-REL-01` (`opentelemetry/releases/release-v1.39.0.md`) is the only opentelemetry-go release Source in the package, and it covers `#7427` (T001), not `#7443`.
- The comments records (`work-states/comments/2026-03.md`) contain no correction touching WS-02 / `#7443`; all three `CMT-*` entries concern WS-03 and WS-05.

## Caveat

The `v1.40.0` milestone being closed as of 2026-02-02 is suggestive that a v1.40.0 release happened, but no `v1.40.0` release document exists in this dataset, so the dataset does not confirm that #7443 shipped in a published release. Per the Work State, this is exactly the open item flagged under "Next Update Needed."
