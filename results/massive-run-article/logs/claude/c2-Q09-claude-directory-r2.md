# Has the fixed-bucket histogram optimization in `opentelemetry-go` pull request `#7474` been released?

<!-- RESPONSE_START -->

No — not established as released by the evidence in this package.

## Answer

PR **#7474** ("Use sync.Map and atomics for fixed bucket histograms", the fixed-bucket histogram optimization by `dashpole`, ~2x faster `Measure()`) is **merged but its release is not established** in the assigned package.

- Authoritative status: the Work State records `T003` / PR `#7474` as **"Merged; not released in included Sources"**, with the remaining open question being release delivery — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-02-metrics-performance.md` (lines 27, 31, 34, 43, 50). The index repeats this: `opentelemetry-go#7474` → "merged; release not established", and lists it under "Merged but unreleased" — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md` (lines 26, 43).

## Chronology and provenance

- Opened 2025-10-08 by `dashpole`; approved by `MrAlias` (2025-12-04) and `dmathieu` (2025-12-09); **merged 2025-12-11T16:56:04Z** into `main` — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-7474.md`.
- Milestoned to `v1.39.0` on 2025-10-16, then **demilestoned from `v1.39.0` and moved to `v1.40.0` on 2025-12-04** by `MrAlias` (same file, timeline).
- `v1.39.0` was published 2025-12-08, i.e. **before** the merge, and its changelog/"What's Changed" does not include `#7474` (it includes the sibling sum optimization `#7427`) — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/releases/release-v1.39.0.md`.
- The 2025-11-20 SIG discussion noted this sync-map histogram work could safely slip to the next release — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3581463689.md` (cited as SRC-NOTE-07 in WS-02).

## Why it stops short of "released"

The `v1.40.0` milestone for `opentelemetry-go` is **closed** with 120/120 items closed (updated 2026-02-02) — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/milestones/milestone-13661613.md`. But the only release record in the package is `v1.39.0`; there is **no `v1.40.0` release Source**, so publication of a release containing `#7474` cannot be confirmed from this evidence. WS-02's "Next Update Needed" is exactly that: evidence of a `v1.40.0` (or later) release including `#7443` and `#7474`.

Note: the same conclusion applies to the companion PR `#7443` (histogram exemplar reservoir), merged 2025-12-15, also moved to `v1.40.0`.
