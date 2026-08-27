# Has the concurrent sum performance work in `opentelemetry-go` pull request `#7427` been released?

<!-- RESPONSE_START -->

Yes — it shipped in **opentelemetry-go v1.39.0**.

## What the sources show

**The PR** — `open-telemetry/opentelemetry-go#7427`, "Use sync.Map and atomics to improve sum performance" by dashpole:
- Opened 2025-09-29, **merged 2025-10-07T13:40:23Z** (branch `optimize_counter_syncmap` → `main`)
- +437 / −121 across 14 files, label `area:metrics`, **milestone v1.39.0**
- Approved by MrAlias (2025-10-07) and dmathieu (2025-10-07)

**The release** — v1.39.0 (tag `v1.39.0`, released as v1.39.0/v0.61.0/v0.15.0/v0.0.14, published by MrAlias):
- **Published 2025-12-08T16:45:46Z**
- The commit list includes: "Use sync.Map and atomics to improve sum performance by @dashpole in .../pull/7427"
- The changelog "Changed" section carries the entry: `Improve performance of concurrent measurements in go.opentelemetry.io/otel/sdk/metric. (#7427)`

No revert, rollback, or regression follow-up on #7427 appears anywhere in the dataset.

## Related, not yet in v1.39.0

Two follow-on optimizations built on the same design landed later and are milestoned **v1.40.0** (i.e. not part of the v1.39.0 release):
- `#7474` "Use sync.Map and atomics for fixed bucket histograms" — merged 2025-12-11, ~2x improvement, explicitly modeled on #7427
- `#7443` "Optimize histogram reservoir" — merged 2025-12-15

Note one wrinkle worth flagging: a CHANGELOG suggestion inside PR #7474 (dashpole, 2025-12-09) reuses the same wording and the `(#7427)` reference, so the string "#7427" also appears in the histogram PR's changelog discussion. That's a copied line, not a second release of the sum work.

## Sources
- `opentelemetry/pulls/opentelemetry-go-7427.md` — [SRC-PR-04]
- `opentelemetry/releases/release-v1.39.0.md` — [SRC-REL-01]
- `opentelemetry/pulls/opentelemetry-go-7474.md` — [SRC-PR-06]
- `opentelemetry/pulls/opentelemetry-go-7443.md` — [SRC-PR-05]
- `opentelemetry/meeting-notes/entry-3389972183.md` (background on the design and PR sequencing)
