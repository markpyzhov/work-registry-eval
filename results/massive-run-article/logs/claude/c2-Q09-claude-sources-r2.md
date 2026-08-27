# Has the fixed-bucket histogram optimization in `opentelemetry-go` pull request `#7474` been released?

<!-- RESPONSE_START -->

## Answer: Yes — it shipped in v1.40.0, though the dataset contains no v1.40.0 release page to confirm the publish date directly.

**What the sources establish**

- **The PR** — `open-telemetry/opentelemetry-go#7474`, "Use sync.Map and atomics for fixed bucket histograms" by dashpole (`optimize_syncmap_histogram` → `main`, +560/−201 across 7 files). It implements a lockless histogram using atomics plus a sync.Map for attribute access, ~2x faster measure (−53% geomean on parallel `SyncMeasure` benchmarks, zero allocations), at the cost of ~+20% on `Collect`. **State: merged 2025-12-11T16:56:04Z. Milestone: v1.40.0.** [SRC-PR-06]
- **It missed v1.39.0.** The timeline shows it was milestoned v1.39.0 on 2025-10-16, then **demilestoned from v1.39.0 and moved to v1.40.0 on 2025-12-04**, and merged a week later. The v1.39.0 release (tag `v1.39.0`, published 2025-12-08T16:45:46Z) predates the merge, and #7474 does not appear in its changelog — only the sibling sum PR #7427 does ("Improve performance of concurrent measurements in `go.opentelemetry.io/otel/sdk/metric`. (#7427)"). [SRC-PR-06], [SRC-REL-01]
- **v1.40.0 has been cut.** The `opentelemetry-go` v1.40.0 milestone (milestone/76) is **closed, 120 closed / 0 open, last updated 2026-02-02T17:59:40Z**; the contrib v1.40.0 milestone (milestone/34) is likewise closed, updated 2026-02-02T19:23:35Z. Consistent with that, the sibling PR #7443's timeline records a cross-reference from `opentelemetry-go/pull/7859` by MrAlias on 2026-02-02 — matching the pattern of the v1.39.0 release PR (#7676, cross-referenced 2025-12-05, released 2025-12-08). [SRC-MILE-03], [SRC-MILE-04], [SRC-PR-05]

**The one gap:** the dataset's only release record is v1.39.0 [SRC-REL-01]. There is no v1.40.0 release page in it, so the release's exact tag/publish timestamp and its changelog entry for #7474 cannot be quoted from these sources. The conclusion rests on the merge date + v1.40.0 milestone assignment + that milestone being closed out on 2026-02-02.

**Sources cited:** SRC-PR-06 (`opentelemetry/pulls/opentelemetry-go-7474.md`), SRC-REL-01 (`opentelemetry/releases/release-v1.39.0.md`), SRC-MILE-03 (`opentelemetry/milestones/milestone-13661613.md`), SRC-MILE-04 (`opentelemetry/milestones/milestone-14282228.md`), SRC-PR-05 (`opentelemetry/pulls/opentelemetry-go-7443.md`).

One caveat on a related source: the 2025-10-10 SIG meeting note [SRC-NOTE-03] labels "#7474" as "Exemplar reservoir optimization" and "#7443" as "Histogram optimization" — the descriptions are swapped relative to the actual PR titles, so don't rely on that note for identifying which PR is which.
