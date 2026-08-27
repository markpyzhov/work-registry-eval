# Has the histogram-reservoir optimization in `opentelemetry-go` pull request `#7443` been released?

<!-- RESPONSE_START -->

I have enough to answer.

**No — the evidence in this package does not establish that PR #7443 has been released.** It is merged but its release is not confirmed.

**Current state (authoritative)**
- `WS-02` tracks #7443 as task `T002`: "Optimize histogram reservoir (per-measurement lock). **Merged; not released in included Sources.**" The index records it identically: "merged; release not established," and lists it under "Merged but unreleased."
  - `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-02-metrics-performance.md`
  - `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md`

**Why**
- The PR was milestoned to `v1.39.0` on 2025-10-16, then demilestoned and moved to `v1.40.0` on 2025-12-04 by MrAlias, and merged 2025-12-15T14:59:34Z by dashpole. Its milestone field reads `v1.40.0`.
  - `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-7443.md`
- The only release record in the package is `v1.39.0`, which predates the merge and does not contain #7443.
  - `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/releases/release-v1.39.0.md`
- There is no `v1.40.0` release Source in the package, so release delivery cannot be established. `WS-02` names this explicitly as the remaining open item and its "Next Update Needed."

**Nearest thing to a release signal (not sufficient on its own)**
- The `v1.40.0` milestone record is **closed** with 120 closed / 0 open, last updated 2026-02-02, which is consistent with the release having been cut — but a closed milestone is not a release record, and the Work State does not treat it as delivery.
  - `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/milestones/milestone-13661613.md`

**Supporting context**
- The optimization itself: locking each measurement rather than the whole storage, plus deferring trace-context extraction to collection time — roughly a 76% reduction in `HistogramReservoirOffer`, and ~70% improvement on `Measure` when exemplars are recorded. Approved by MrAlias (2025-12-11), bboreham (2025-10-16), and dmathieu (2025-12-15).
  - `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-7443.md`
- The 2025-11-20 SIG noted this work could safely slip to the next release; the sibling PR #7474 is in the same merged-but-release-unconfirmed position.
  - `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3581463689.md` (per `WS-02` citation)
- The March 2026 Work State Comments contain no corrections touching `WS-02`, so nothing supersedes the "not released" state.
  - `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/comments/2026-03.md`
