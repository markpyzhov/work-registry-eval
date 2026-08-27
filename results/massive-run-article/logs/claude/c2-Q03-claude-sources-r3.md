# Has the histogram-reservoir optimization in `opentelemetry-go` pull request `#7443` been released?

<!-- RESPONSE_START -->

## Answer

**Not directly confirmable from the dataset — but almost certainly yes, indirectly.** The dataset contains no v1.40.0 release record, so it cannot show the shipped artifact. Here is what the sources do establish:

**The PR is merged, not just open.** `Optimize histogram reservoir` (open-telemetry/opentelemetry-go#7443, author dashpole) is **merged as of 2025-12-15T14:59:34Z** into `main` from branch `optimize_histogram_reservoir` (+173 / -61 across 8 files). Approvals came from MrAlias (2025-12-11), bboreham, and dmathieu (2025-12-15). [SRC-PR-05]

**It missed v1.39.0 and was retargeted to v1.40.0.** The PR timeline shows it was milestoned to v1.39.0 on 2025-10-16, then **demilestoned from v1.39.0 and milestoned to v1.40.0 on 2025-12-04** by MrAlias. Its current milestone is **v1.40.0**. [SRC-PR-05]

**v1.39.0 does not contain it.** The v1.39.0 release (tag `v1.39.0`, published 2025-12-08T16:45:46Z) predates the 2025-12-15 merge, and #7443 does not appear in its changelog. The related sibling PR #7474 (sync.Map/atomics for fixed bucket histograms), also milestoned v1.40.0, likewise is absent. [SRC-REL-01]

**The v1.40.0 milestone has since closed.** Milestone v1.40.0 for opentelemetry-go (milestone/76) is **state: closed, 120 closed / 0 open, last updated 2026-02-02T17:59:40Z**. [SRC-MILE-03] The corresponding contrib milestone v1.40.0 is also closed (169/0, 2026-02-02). [SRC-MILE-04]

### Bottom line

The optimization is merged and assigned to v1.40.0, and that milestone closed fully around 2026-02-02 — which is the normal signature of a shipped release. However, **the dataset contains no v1.40.0 release record** (only v1.39.0 is present), so there is no direct evidence of a published v1.40.0 tag, its publication date, or a changelog entry citing #7443. If you need the release date or the exact changelog wording, that confirmation is outside this dataset.

Supporting context: a SIG meeting note from 2025-11-20 lists "Exemplar reservoir changes" as safe to slip to the next release [SRC-NOTE-07], and the 2025-10-16 note records Tyler Yahn pushing to get the histogram reservoir PR into the milestone for its performance win [SRC-NOTE-04].

**Sources used:** SRC-PR-05 (`opentelemetry/pulls/opentelemetry-go-7443.md`), SRC-REL-01 (`opentelemetry/releases/release-v1.39.0.md`), SRC-MILE-03 (`opentelemetry/milestones/milestone-13661613.md`), SRC-MILE-04 (`opentelemetry/milestones/milestone-14282228.md`), SRC-PR-06 (`opentelemetry/pulls/opentelemetry-go-7474.md`), SRC-NOTE-04, SRC-NOTE-07.
