# Has the fixed-bucket histogram optimization in `opentelemetry-go` pull request `#7474` been released?

<!-- RESPONSE_START -->

## Answer: No — not as of the record cutoff

The fixed-bucket histogram optimization (`open-telemetry/opentelemetry-go#7474`, "Use sync.Map and atomics for fixed bucket histograms", by dashpole) is **merged but not established as released** in this package.

### Status detail

**Work State (authoritative)** — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-02-metrics-performance.md` tracks it as `T003`, marked complete-as-merged with the explicit note "Merged; not released in included Sources." The index at `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md` records `opentelemetry-go#7474` as "merged; release not established," and lists it under **Merged but unreleased** alongside `#7443`.

**Timeline** (from `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-7474.md`):
- Opened 2025-10-08 by dashpole; +560/−201 across 7 files; claims ~2x improvement (parallel `SyncMeasure` benchmarks ~-53% geomean)
- Milestoned to **v1.39.0** on 2025-10-16 by MrAlias
- **Demilestoned from v1.39.0 and moved to v1.40.0** on 2025-12-04
- **Merged 2025-12-11T16:56:04Z**

**Why it missed v1.39.0**: the v1.39.0 release (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/releases/release-v1.39.0.md`) was published **2025-12-08**, three days *before* the merge. Its changelog does not mention `#7474`. The 2025-11-20 SIG meeting had already noted the sync-map histogram work could safely slip to the next release (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3581463689.md`, cited as SRC-NOTE-07).

### Caveat worth flagging

The v1.40.0 milestone record (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/milestones/milestone-13661613.md`) is **closed** with 120 closed / 0 open, last updated 2026-02-02 — which suggests v1.40.0 work wrapped up. But milestone closure is not a release record, and **no v1.40.0 release Source exists in this package** (v1.39.0 is the only release file). So the corpus cannot confirm shipment. WS-02's "Next Update Needed" says exactly this: it awaits "evidence of a `v1.40.0` (or later) release that includes `#7443` and `#7474`."

The human-correction comments through 2026-03-11 (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/comments/2026-03.md`) contain no update on `#7474`, so nothing supersedes the above.

**Bottom line**: merged on 2025-12-11 and slated for v1.40.0, but the available evidence does not establish that a release containing it has shipped. Given the v1.40.0 milestone closed in February 2026 and today is August 2026, it has very likely shipped in reality — but confirming that requires a source outside this package.
