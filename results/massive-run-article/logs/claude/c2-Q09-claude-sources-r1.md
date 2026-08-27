# Has the fixed-bucket histogram optimization in `opentelemetry-go` pull request `#7474` been released?

<!-- RESPONSE_START -->

## Answer

**Not confirmable as "released" from this dataset — but it is merged and slated for v1.40.0.** The dataset contains no release record for v1.40.0, so there is no direct evidence of publication.

### What the sources do establish

**The PR is merged** — `opentelemetry/pulls/opentelemetry-go-7474.md` [SRC-PR-06]:
- "Use sync.Map and atomics for fixed bucket histograms" (open-telemetry/opentelemetry-go#7474), author dashpole
- State: **merged 2025-12-11T16:56:04Z** into `main` (branch `optimize_syncmap_histogram`), +560/-201 across 7 files
- Approvals: MrAlias (2025-12-04), dmathieu (2025-12-09)
- **Milestone: v1.40.0** — its timeline shows it was originally milestoned v1.39.0 on 2025-10-16, then **demilestoned from v1.39.0 and milestoned to v1.40.0 on 2025-12-04T18:09:56Z**

**It is definitively *not* in v1.39.0** — `opentelemetry/releases/release-v1.39.0.md` [SRC-REL-01]: v1.39.0 was published **2025-12-08T16:45:46Z**, three days *before* #7474 merged, and #7474 does not appear in its changelog. Note a likely point of confusion: v1.39.0's entry "Improve performance of concurrent measurements in `go.opentelemetry.io/otel/sdk/metric`. (#7427)" refers to the **sum** optimization PR #7427, not the histogram PR #7474.

**Indirect evidence that v1.40.0 shipped** — `opentelemetry/milestones/milestone-13661613.md` [SRC-MILE-03]: milestone v1.40.0 (opentelemetry-go milestone/76) is **closed**, 120 closed / 0 open, last updated **2026-02-02T17:59:40Z**. The parallel contrib milestone [SRC-MILE-04] is likewise closed as of 2026-02-02. A closed, fully-completed v1.40.0 milestone in early Feb 2026 strongly implies the release was cut, but the dataset holds no v1.40.0 release document to confirm the tag was published.

### Supporting context
- `opentelemetry/meeting-notes/entry-3581463689.md` [SRC-NOTE-07] (SIG 2025-11-20) lists "Sync map / atomics for fixed bucket histograms" as an item "safe to slip to next release; include if ready" — consistent with the v1.39.0 → v1.40.0 milestone move.
- The companion optimization, PR #7443 (Optimize histogram reservoir), merged 2025-12-15 and is also milestoned v1.40.0 (`opentelemetry/pulls/opentelemetry-go-7443.md` [SRC-PR-05]).

### Bottom line
The optimization did **not** make v1.39.0 (the most recent release documented in the dataset). It merged 2025-12-11 targeting **v1.40.0**, whose milestone closed complete around 2026-02-02 — so it almost certainly shipped in v1.40.0, but the dataset lacks a v1.40.0 release record to state that as fact.
