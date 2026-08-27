# Has the fixed-bucket histogram optimization in `opentelemetry-go` pull request `#7474` been released?

<!-- RESPONSE_START -->

## Answer: Not established as released — the record says "merged, but release not confirmed."

**Status of the PR itself**
`opentelemetry-go#7474` ("Use sync.Map and atomics for fixed bucket histograms," author `dashpole`) is **merged**, closed 2025-12-11T16:56:04Z, milestone **v1.40.0**. It implements a lockless atomic histogram with a `sync.Map` for attribute access (~2x faster `Measure`, ~54% latency reduction on the parallel benchmarks; `Collect` gets ~68% slower and allocates more, accepted as a tradeoff).
Source: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-7474.md`

**Why release is not established**
- The authoritative Work State tracks this as task `T003` and records it as **"Merged; not released in included Sources"**, with the open blocker being release delivery for `#7443` / `#7474`, and "Next Update Needed: Evidence of a `v1.40.0` (or later) release that includes `#7443` and `#7474`."
  `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-02-metrics-performance.md`
- The index confirms the as-of state for `opentelemetry-go#7474`: **"merged; release not established"**, and lists it under "Merged but unreleased."
  `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md`
- It was originally milestoned **v1.39.0** (2025-10-16) then **demilestoned and moved to v1.40.0** on 2025-12-04 by `MrAlias`.
  `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-7474.md`
- The only opentelemetry-go release record in the package is **v1.39.0**, published 2025-12-08 — three days *before* `#7474` merged — and its changelog does not include `#7474`.
  `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/releases/release-v1.39.0.md`

**One nuance worth noting**
The v1.40.0 **milestone** record for opentelemetry-go is marked `State: closed` with `120 closed / 0 open` (updated 2026-02-02), which suggests the release work was completed — but a closed milestone is not a release record, and the package contains no v1.40.0 release entry to confirm shipment.
`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/milestones/milestone-13661613.md`

**Bottom line:** the optimization is merged and targeted at v1.40.0, but on the available evidence its release cannot be confirmed. The companion histogram-reservoir PR `#7443` is in the same position.
