# Has the histogram-reservoir optimization in `opentelemetry-go` pull request `#7443` been released?

<!-- RESPONSE_START -->

## Answer

**Not directly confirmable from the dataset — the evidence supports "merged and slated for v1.40.0," with strong indirect (but not direct) evidence that v1.40.0 has since shipped.**

### What the sources establish

**1. The PR is merged, targeting v1.40.0** — `opentelemetry/pulls/opentelemetry-go-7443.md` [SRC-PR-05]
- "Optimize histogram reservoir" (open-telemetry/opentelemetry-go#7443), author dashpole
- State: **merged 2025-12-15T14:59:34Z**, branch `optimize_histogram_reservoir` → `main`, +173/−61 across 8 files
- **Milestone: v1.40.0**
- Approvals: MrAlias (2025-12-11), dmathieu (2025-12-15)
- Content: locks each measurement rather than the whole storage, and defers trace-context extraction to collection time; ~4x (≈75%) faster concurrent `Offer`, ~70% improvement when exemplars are recorded

**2. It is not in v1.39.0, the only release record in the dataset** — `opentelemetry/releases/release-v1.39.0.md` [SRC-REL-01]
- v1.39.0 (v1.39.0/v0.61.0/v0.15.0/v0.0.14) was **published 2025-12-08T16:45:46Z** — a week *before* #7443 merged
- Its changelog and "What's Changed" list sibling optimization PRs (#7427, #7306, #7423, #7371) but **not #7443**

**3. The team explicitly deferred it to the next release** — `opentelemetry/meeting-notes/entry-3581463689.md` [SRC-NOTE-07], SIG meeting 2025-11-20: "Sync map / atomics for fixed bucket histograms. Exemplar reservoir changes. — Safe to slip to next release; include if ready."

**4. The v1.40.0 milestone is closed and complete** — `opentelemetry/milestones/milestone-13661613.md` [SRC-MILE-03]
- Milestone v1.40.0 (opentelemetry-go milestone/76): **State closed, 120 closed / 0 open, updated 2026-02-02T17:59:40Z**
- The corresponding contrib milestone v1.40.0 ([SRC-MILE-04], milestone/34) is likewise closed, 169 closed / 0 open, updated 2026-02-02

### Bottom line

The dataset contains **no release record for v1.40.0** — the only release document is v1.39.0, which predates the merge and does not contain #7443. So the dataset cannot directly confirm publication. However, since the v1.40.0 milestone that #7443 belongs to was fully closed out on 2026-02-02 (0 open items), the histogram-reservoir optimization was almost certainly shipped in v1.40.0 around early February 2026. To state the release date with certainty you would need the v1.40.0 release record, which is not in this dataset.
