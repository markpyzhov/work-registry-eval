# Has the concurrent sum performance work in `opentelemetry-go` pull request `#7427` been released?

<!-- RESPONSE_START -->

Yes — the concurrent sum performance work in `opentelemetry-go` PR #7427 has been released.

**Answer**

PR #7427, "Use sync.Map and atomics to improve sum performance" (author `dashpole`), was merged on 2025-10-07 and shipped in the **v1.39.0** release, published 2025-12-08.

**Evidence**

- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-02-metrics-performance.md` — the authoritative Work State. Task `T001` (mapped to PR #7427, "Optimize concurrent sum performance (`sync.Map` / atomics)") is marked complete, and the Done/Evidence section records: opened 2025-09-29 by `dashpole`, approach accepted by the SIG on 2025-10-02, merged 2025-10-07, **released in `v1.39.0`**.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md` — line 24 lists `opentelemetry-go#7427` under Metrics Performance with status "merged and released in `v1.39.0`".
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/releases/release-v1.39.0.md` (SRC-REL-01) — tag `v1.39.0`, published 2025-12-08T16:45:46Z. Changelog "Changed" section: "Improve performance of concurrent measurements in `go.opentelemetry.io/otel/sdk/metric`. (#7427)", and the commit list includes "Use sync.Map and atomics to improve sum performance by @dashpole ... /pull/7427".
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-7427.md` (SRC-PR-04) — State: merged 2025-10-07T13:40:23Z, milestone `v1.39.0`, +437/-121 across 14 files. Reported parallel benchmarks show roughly 70–77% reduction in sec/op for counter and up-down-counter measurements.

**Related context (not released)**

The two sibling performance PRs in the same work state are *not* covered by any release record in this package: #7443 (histogram exemplar reservoir, merged 2025-12-15) and #7474 (fixed-bucket histogram, merged 2025-12-11) were both moved from `v1.39.0` to the `v1.40.0` milestone on 2025-12-04, and no `v1.40.0` release source exists in the package, so their release delivery is not established (`WS-02-metrics-performance.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-7443.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-7474.md`).
