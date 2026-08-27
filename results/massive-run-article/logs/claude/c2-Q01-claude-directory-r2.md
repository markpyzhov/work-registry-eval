# Has the concurrent sum performance work in `opentelemetry-go` pull request `#7427` been released?

<!-- RESPONSE_START -->

Yes — it has been released.

## Answer

**opentelemetry-go PR #7427 ("Use sync.Map and atomics to improve sum performance") was merged and released in v1.39.0.**

**Status details:**
- The PR was opened 2025-09-29 by `dashpole`, approved by `MrAlias` and `dmathieu` on 2025-10-07, and **merged 2025-10-07T13:40:23Z**. It was milestoned to `v1.39.0` on 2025-10-14 by `MrAlias`. (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-7427.md`)
- **Release v1.39.0 was published 2025-12-08T16:45:46Z** and its changelog contains the entry "Improve performance of concurrent measurements in `go.opentelemetry.io/otel/sdk/metric`. (#7427)", plus the merged-PR listing "Use sync.Map and atomics to improve sum performance by @dashpole ... /pull/7427". (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/releases/release-v1.39.0.md`)
- The authoritative Work State records this as task `T001`, marked done: "merged 2025-10-07; released in `v1.39.0`". (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-02-metrics-performance.md`) The registry index likewise lists `opentelemetry-go#7427` as "merged and released in `v1.39.0`". (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md`)
- The `v1.39.0` milestone is closed (335 closed / 0 open). (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/milestones/milestone-13145551.md`)

**Important caveat if you meant the broader metrics-performance effort:** #7427 covers only the concurrent *sum* work. Two sibling performance PRs are **merged but not yet released** per the available evidence — `#7443` (histogram reservoir, merged 2025-12-15) and `#7474` (fixed-bucket histogram, merged 2025-12-11). Both were moved from `v1.39.0` to `v1.40.0` on 2025-12-04, and no `v1.40.0` release record exists in this package, so their release is not established. This is why WS-02 as a whole is still `in_progress`. (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-02-metrics-performance.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/milestones/milestone-13661613.md`)
