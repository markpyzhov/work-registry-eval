# Has the concurrent sum performance work in `opentelemetry-go` pull request `#7427` been released?

<!-- RESPONSE_START -->

Yes — PR #7427 has been released, in `v1.39.0`.

## Answer

**Yes.** The concurrent sum performance work ("Use sync.Map and atomics to improve sum performance", open-telemetry/opentelemetry-go#7427, by `dashpole`) was merged and shipped in `v1.39.0`.

## Evidence

- **Work State `WS-02: Metrics Performance`** (`work-states/WS-02-metrics-performance.md`, authoritative for current status, last updated 2025-12-15) records task `T001` (mapped to PR `#7427`) as complete, with Done/Evidence stating: opened 2025-09-29 by `dashpole`; approach accepted by the SIG 2025-10-02; merged 2025-10-07; **released in `v1.39.0`** `(SRC-PR-04, SRC-REL-01)`.
- **PR Source `SRC-PR-04`** (`opentelemetry/pulls/opentelemetry-go-7427.md`): state **merged** 2025-10-07T13:40:23Z, branch `optimize_counter_syncmap` → `main`, +437/-121 across 14 files, label `area:metrics`, **milestone `v1.39.0`**. Approved by `MrAlias` (2025-10-07) and `dmathieu` (2025-10-07).
- **Release Source `SRC-REL-01`** (`opentelemetry/releases/release-v1.39.0.md`): tag `v1.39.0` (Release v1.39.0/v0.61.0/v0.15.0/v0.0.14), authored by `MrAlias`, **published 2025-12-08T16:45:46Z**. Its changelog Changed section includes "Improve performance of concurrent measurements in `go.opentelemetry.io/otel/sdk/metric`. (#7427)", and the commit list includes "Use sync.Map and atomics to improve sum performance by @dashpole ... /pull/7427".

## Contrast with the sibling performance PRs

The other two Metrics Performance items are **not** established as released in this dataset:

- `#7443` (histogram exemplar reservoir, per-measurement lock) — moved from `v1.39.0` to `v1.40.0` on 2025-12-04; merged 2025-12-15; release not established.
- `#7474` (fixed-bucket histogram via `sync.Map`/atomics) — moved to `v1.40.0` on 2025-12-04; merged 2025-12-11; release not established.

The Work State's Blockers section notes no `v1.40.0` release Source exists in the package, so `WS-02` overall remains `in_progress` even though `#7427` itself has shipped. The `work-state-index` navigation aid corroborates the split: `#7427` "merged and released in v1.39.0", while `#7443` and `#7474` are "merged; release not established".
