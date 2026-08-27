# Has the concurrent sum performance work in `opentelemetry-go` pull request `#7427` been released?

<!-- RESPONSE_START -->

Yes — it shipped in `v1.39.0`.

**Answer**

PR #7427 ("Use sync.Map and atomics to improve sum performance", by `dashpole`) was **merged 2025-10-07** and **released in `v1.39.0`, published 2025-12-08**.

Evidence:

- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-02-metrics-performance.md` — the authoritative Work State (WS-02: Metrics Performance) marks task `T001`, mapped to PR `#7427`, as complete: "Opened 2025-09-29 by `dashpole`; approach accepted 2025-10-02; merged 2025-10-07; released in `v1.39.0`."
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-7427.md` (`SRC-PR-04`) — State: merged 2025-10-07T13:40:23Z; Milestone: v1.39.0.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/releases/release-v1.39.0.md` (`SRC-REL-01`) — Tag `v1.39.0`, published 2025-12-08T16:45:46Z. Changed section: "Improve performance of concurrent measurements in `go.opentelemetry.io/otel/sdk/metric`. (#7427)", and the commit list includes "Use sync.Map and atomics to improve sum performance by @dashpole ... pull/7427".
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/milestones/milestone-13145551.md` (`SRC-MILE-02`) — the v1.39.0 milestone, state closed.

**Related caveat on the rest of the metrics-performance work:** the two sibling optimizations in the same work state are merged but *not* shown as released in this package — `#7443` (histogram reservoir, merged 2025-12-15) and `#7474` (fixed-bucket histogram, merged 2025-12-11) were both moved from `v1.39.0` to the `v1.40.0` milestone on 2025-12-04, and no `v1.40.0` release record exists here. So if "concurrent sum performance work" is meant narrowly as #7427, it is released; the broader histogram follow-ups are not confirmed released. (`WS-02-metrics-performance.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-7443.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-7474.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/milestones/milestone-13661613.md`)
