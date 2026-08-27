# Has the concurrent sum performance work in `opentelemetry-go` pull request `#7427` been released?

<!-- RESPONSE_START -->

Yes — it has been released.

## Answer

**PR #7427, "Use sync.Map and atomics to improve sum performance"** (open-telemetry/opentelemetry-go), authored by `dashpole`, shipped in **v1.39.0**.

**Timeline**
- Opened 2025-09-29, merged **2025-10-07** into `main` (branch `optimize_counter_syncmap`, +437/−121 across 14 files, label `area:metrics`, milestone v1.39.0). Approved by MrAlias (2025-10-07) and dmathieu (2025-10-07).
- Released in tag **v1.39.0** (the combined "Release v1.39.0/v0.61.0/v0.15.0/v0.0.14"), published by MrAlias on **2025-12-08**.

**Release evidence**
- The v1.39.0 changelog "Changed" section contains: "Improve performance of concurrent measurements in `go.opentelemetry.io/otel/sdk/metric`. (#7427)"
- The v1.39.0 "What's Changed" commit list includes: "Use sync.Map and atomics to improve sum performance by @dashpole in .../pull/7427"

**What it did**: replaced lock-based sum storage with a `sync.Map` for attribute-set lookup plus atomic counter values, using a hot/cold waitgroup so measurements are lockless and delta resets stay safe. Known accepted trade-offs recorded in the PR and SIG notes: the cardinality/attribute-set limit becomes a soft limit, and for cumulative sums an exemplar may land in a later batch than its `add()`.

**One caveat if the question is really "is all the concurrent-performance work released?"** — #7427 (sums) is out in v1.39.0, but the sibling work is not: **#7474** (sync.Map/atomics for fixed-bucket histograms, ~2x, merged 2025-12-11) and **#7443** (histogram reservoir optimization, merged 2025-12-15) are both milestoned **v1.40.0**, which does not appear as a published release in this dataset. Note #7474's changelog entry reuses the "(#7427)" reference text, which can make it look like the same item.

**Sources cited** (all `path: sources`, dataset `74f29ea8…`):
- `opentelemetry/pulls/opentelemetry-go-7427.md` [SRC-PR-04]
- `opentelemetry/releases/release-v1.39.0.md` [SRC-REL-01]
- `opentelemetry/pulls/opentelemetry-go-7474.md` [SRC-PR-06]
- `opentelemetry/pulls/opentelemetry-go-7443.md` [SRC-PR-05]
- `opentelemetry/meeting-notes/entry-3389972183.md`, `entry-3389930076.md` [SRC-NOTE-01], `entry-3479584781.md`
