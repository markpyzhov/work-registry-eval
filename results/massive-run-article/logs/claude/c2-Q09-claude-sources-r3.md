# Has the fixed-bucket histogram optimization in `opentelemetry-go` pull request `#7474` been released?

<!-- RESPONSE_START -->

## Answer

**Almost certainly yes — it shipped in opentelemetry-go v1.40.0 — but the dataset contains no v1.40.0 release record to confirm publication directly.** Here is what the sources do establish:

**The PR itself** — `opentelemetry/pulls/opentelemetry-go-7474.md` [SRC-PR-06], "Use sync.Map and atomics for fixed bucket histograms":
- **State: merged**, 2025-12-11T16:56:04Z, by dashpole (`optimize_syncmap_histogram` → `main`, +560/−201 across 7 files)
- **Milestone: v1.40.0**. Its timeline shows it was first milestoned to v1.39.0 on 2025-10-16, then **demilestoned from v1.39.0 and milestoned to v1.40.0 on 2025-12-04** by MrAlias.
- Content: lockless histogram using atomics plus a sync.Map for attribute access, ~2x faster measure path (−53% geomean on parallel `SyncMeasure` benchmarks), at the cost of ~20% slower `Collect`.

**Not in v1.39.0** — the only release record in the dataset, `opentelemetry/releases/release-v1.39.0.md` [SRC-REL-01], is tagged `v1.39.0` and **published 2025-12-08T16:45:46Z**, three days *before* #7474 merged. Neither #7474 nor a corresponding changelog line appears in it.

**Indirect evidence that v1.40.0 shipped** — `opentelemetry/milestones/milestone-13661613.md` [SRC-MILE-03]: the opentelemetry-go **v1.40.0 milestone is closed**, 120 closed / 0 open, last updated 2026-02-02. (The parallel contrib milestone [SRC-MILE-04] is likewise closed, 169/0, updated 2026-02-02.) A closed milestone with zero open items is the normal end-state of a completed release, so v1.40.0 was evidently cut around early February 2026 — but the dataset holds **no release record tagged v1.40.0**, so the actual publication date and its changelog entry cannot be cited from these sources.

**Related context** — the companion exemplar work, #7443 "Optimize histogram reservoir" [SRC-PR-05], followed the same path: merged 2025-12-15, also moved from the v1.39.0 to the v1.40.0 milestone. The 2025-11-26 Go SIG note [SRC-NOTE-07] records both items ("Sync map / atomics for fixed bucket histograms" and "Exemplar reservoir changes") as "safe to slip to next release; include if ready," which is what happened.

**Bottom line for a user asking "can I get this?"** — it is not in v1.39.0 or earlier; upgrade to v1.40.0 or later. If you need the exact release date or the changelog wording, that has to come from a source outside this dataset.
