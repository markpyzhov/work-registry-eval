# Has the histogram-reservoir optimization in `opentelemetry-go` pull request `#7443` been released?

<!-- RESPONSE_START -->

## Answer: Not confirmed as released — merged, but no release evidence in the dataset.

**Status of PR #7443 ("Optimize histogram reservoir", open-telemetry/opentelemetry-go)**

- **Merged**: 2025-12-15T14:59:34Z, author `dashpole`, branch `optimize_histogram_reservoir` → `main`, +173 / -61 across 8 files (`SRC-PR-05`).
- **Targeted release**: milestone **v1.40.0**. The PR was originally in the v1.39.0 milestone and was moved to v1.40.0 on 2025-12-04 (`SRC-PR-05`, `SRC-MILE-03`).
- **Released?** The authoritative Work State **WS-02: Metrics Performance** (status `in_progress`, last updated 2025-12-15) records `T002` / `#7443` as **"Merged; not released in included Sources."** Its Blockers section states plainly that no v1.40.0 release Source exists in the package, so **release completion is not established**, and its "Next Update Needed" is exactly "Evidence of a `v1.40.0` (or later) release that includes `#7443` and `#7474`."

**Corroborating detail**

- The only release record in the dataset is **v1.39.0** (`SRC-REL-01`) — confirmed against the source index (`integrations/github.md`), which lists a single `release` artifact. There is no v1.40.0 release document to check the changelog against.
- One indirect signal points toward the release having happened, but it is not itself release evidence: the **v1.40.0 milestone (`SRC-MILE-03`, opentelemetry-go milestone 76) is `closed`, 120 closed / 0 open, updated 2026-02-02**. A closed milestone is milestone bookkeeping, not a published release record, and the Work State does not treat it as release confirmation.

**Bottom line**: #7443 is done and merged into `main` and slated for v1.40.0, whose milestone has since closed — but the dataset contains no v1.40.0 release artifact, so within this evidence set the histogram-reservoir optimization cannot be confirmed as shipped in a published release.

**What the change does** (from the PR description, `SRC-PR-05`): improves concurrent performance of the histogram reservoir's `Offer` by ~4x by locking each measurement rather than the entire storage, and deferring trace-context extraction from `context.Context` until collection time. Benchmarks show `HistogramReservoirOffer-24` at -76.40% and exemplar-enabled histogram `SyncMeasure` paths improving 63-74%. Approved by MrAlias (2025-12-11) and dmathieu (2025-12-15); bboreham also approved earlier.

Related: PR **#7474** (fixed-bucket histogram via `sync.Map`/atomics) is in the same position — merged 2025-12-11, same v1.40.0 milestone, also recorded as merged but not released.

Dataset records cited: `work-states/WS-02-metrics-performance.md` (work-state), `opentelemetry/pulls/opentelemetry-go-7443.md` (SRC-PR-05), `opentelemetry/pulls/opentelemetry-go-7474.md` (SRC-PR-06), `opentelemetry/milestones/milestone-13661613.md` (SRC-MILE-03), `opentelemetry/releases/release-v1.39.0.md` (SRC-REL-01), `integrations/github.md` (source index, navigation only).
