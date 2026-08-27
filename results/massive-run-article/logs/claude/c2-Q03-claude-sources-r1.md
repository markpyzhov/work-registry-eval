# Has the histogram-reservoir optimization in `opentelemetry-go` pull request `#7443` been released?

<!-- RESPONSE_START -->

## Answer

**Not confirmable as released from the dataset's release records — but it was definitively *not* in v1.39.0, and the evidence points to it shipping in v1.40.0.**

### What the sources establish

**PR #7443 "Optimize histogram reservoir"** (`opentelemetry/pulls/opentelemetry-go-7443.md`, SRC-PR-05):
- Author: dashpole; created 2025-10-02, **merged 2025-12-15T14:59:34Z** into `main`
- **Milestone: v1.40.0**
- +173/−61 across 8 files, touching `sdk/metric/exemplar/{storage.go, histogram_reservoir.go, fixed_size_reservoir.go}`
- Effect: per-measurement locking instead of one lock over the whole reservoir, plus deferring trace-context extraction from `context.Context` until collection time; ~4x faster concurrent `Offer` (`HistogramReservoirOffer-24`: 200.85n → 47.41n, −76.40%)
- Approvals: MrAlias (2025-12-11), dmathieu (2025-12-15)

**It missed v1.39.0.** The only release record in the dataset (`opentelemetry/releases/release-v1.39.0.md`, SRC-REL-01) is tagged `v1.39.0`, **published 2025-12-08T16:45:46Z** — a week *before* #7443 merged. Its changelog lists sibling optimization PRs (#7427, #7306, #7423) but not #7443. This matches the 2025-11-20 SIG note (SRC-NOTE-07), which recorded the "exemplar reservoir changes" as "safe to slip to next release," and the timeline showing MrAlias demilestoning related work from v1.39.0 → v1.40.0 on 2025-12-04.

**Indirect evidence v1.40.0 shipped:** the v1.40.0 milestone record (`opentelemetry/milestones/milestone-13661613.md`, SRC-MILE-03, milestone/76) is **closed, 120 closed / 0 open, last updated 2026-02-02**. For comparison, the v1.39.0 milestone (SRC-MILE-02) closed 2025-12-08, the same day v1.39.0 was published — so a closed milestone in this repo coincides with the release being cut.

### Caveat

The dataset contains **no v1.40.0 release record** (no release tag, publication date, or changelog entry for it), so I cannot cite direct confirmation of publication or quote the changelog line for #7443. The conclusion that it has been released rests on the closed v1.40.0 milestone plus the repo's observed pattern of closing a milestone at release time.

**Sources used:** SRC-PR-05 (`opentelemetry/pulls/opentelemetry-go-7443.md`), SRC-REL-01 (`opentelemetry/releases/release-v1.39.0.md`), SRC-MILE-03 (`opentelemetry/milestones/milestone-13661613.md`), SRC-MILE-02 (`opentelemetry/milestones/milestone-13145551.md`), SRC-NOTE-04 (`opentelemetry/meeting-notes/entry-3479584781.md`), SRC-NOTE-07 (`opentelemetry/meeting-notes/entry-3581463689.md`).
