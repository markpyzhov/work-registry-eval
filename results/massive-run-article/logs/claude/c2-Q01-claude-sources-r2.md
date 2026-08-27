# Has the concurrent sum performance work in `opentelemetry-go` pull request `#7427` been released?

<!-- RESPONSE_START -->

**Yes — it shipped in opentelemetry-go v1.39.0, published 2025-12-08.**

## Evidence chain

**The PR itself** — `opentelemetry/pulls/opentelemetry-go-7427.md` [SRC-PR-04], "Use sync.Map and atomics to improve sum performance" by dashpole:
- Created 2025-09-29, **merged 2025-10-07T13:40:23Z** into `main` (branch `optimize_counter_syncmap`)
- **Milestone: v1.39.0**, label `area:metrics`, +437/-121 across 14 files
- Approved by MrAlias (2025-10-07) and dmathieu (2025-10-07)

**The release** — `opentelemetry/releases/release-v1.39.0.md` [SRC-REL-01], tag `v1.39.0` (Release v1.39.0/v0.61.0/v0.15.0/v0.0.14), published **2025-12-08T16:45:46Z**:
- "What's Changed" lists: "Use sync.Map and atomics to improve sum performance by @dashpole in .../pull/7427"
- Changelog "Changed" section: "Improve performance of concurrent measurements in `go.opentelemetry.io/otel/sdk/metric`. (#7427)"

So the merge-to-release gap was about two months (Oct 7 → Dec 8).

## What the change does

Replaces lock-based sum storage with a `sync.Map` plus atomics for the counter value, using a hot/cold waitgroup swap so delta aggregations can reset safely without dropping concurrent measurements. Two known trade-offs discussed in the PR and the SIG meeting notes (`opentelemetry/meeting-notes/entry-3389972183.md`):
- The attribute-set cardinality limit becomes a **soft** limit (race between map-size accounting and map updates). dashpole explicitly rejected MrAlias's pre-increment-with-rollback suggestion because it could split one attribute set's observations between the real set and the overflow set.
- For cumulative sums, an exemplar may land in a later export batch than its `Add()`. Deemed acceptable since cumulative exemplars persist across collection cycles.

## Related follow-on work (not in v1.39.0)

Two sibling PRs from the same optimization sequence went to **v1.40.0**, not v1.39.0:
- **#7474** "Use sync.Map and atomics for fixed bucket histograms" — merged 2025-12-11, ~2x faster (~53% reduction on parallel `SyncMeasure`). Explicitly modeled on #7427's design.
- **#7443** "Optimize histogram reservoir" — merged 2025-12-15, ~76% reduction on `HistogramReservoirOffer`.

Worth flagging if the underlying question is about metric hot-path performance generally: only the **sum** half of that work is in v1.39.0; the histogram half requires v1.40.0.

No revert or post-release regression for #7427 appears anywhere in the dataset.
