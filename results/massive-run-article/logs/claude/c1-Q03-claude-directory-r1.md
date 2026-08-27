# Large-file chunking was merged in mid-August. As of **2026-09-22**, has that completion held? Reconstruct the completion → reopen timeline, the technical root cause, and who owns the next engineering action.

<!-- RESPONSE_START -->

I have everything needed. Here is the complete answer.

---

## No — the completion did not hold. As of 2026-09-22, large-file chunking (CIPH-41 / T031) is still open.

**Authoritative status:** WS-05 (`Last Updated: 2026-09-22`) lists `T031` as an **unchecked** task and describes it as **"Reopened/active"**; the Work State Index (as-of `2026-09-22T12:00:00Z`) lists T031 under "Active / Reopened" as the "large-file memory leak." The ClickUp task itself carries **Status: Active (Reopened)**.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-05-performance.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/index.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-41-Large-File-Chunking.md`

## Completion → reopen timeline

| Date | Event | Evidence |
|---|---|---|
| 2026-08-12 | Alice opens CIPH-41 (large-file chunking needed for multi-GB docs) | `tasks/CIPH-41-Large-File-Chunking.md` |
| 2026-08-14 | Charlie starts stream-based chunked reads; adds an **overlap window** between chunks so entities spanning a boundary aren't missed. Design note documents the "Stream-and-Split" layer (100-page blocks → temp sub-docs → worker pool → re-merge), and flags a *pending* 10,000-page stress test | `slack/2026-08-14-large-file-chunking.md`; `documentation/sources/2026-08-14-Large-File-Chunking-Review.md` |
| **2026-08-16** | **Charlie merges stream chunking to mainline — "Calling this done."** Bob asks if memory concerns are fully clean; Charlie: "As far as testing showed, clean. We'll see if anything shows up on longer runs." | `slack/2026-08-16-large-file-chunking-merge.md`; `2026-08-23-Large-File-Chunking-Design-Review.md` |
| 2026-08-17 | Bob sees RSS climbing after ~4h of processing; Diana confirms a steady upward slope on staging; Evan temporarily bumps the container limit to 2GB | `slack/2026-08-17-memory-leak-hotspots.md` |
| **2026-08-18** | **Bob reopens** — files over 2GB still leak on long-running batches. Bob: "It's not the page buffers themselves — something else is holding a reference." Diana reproduces in QA; process gets OOM-killed on larger inputs | `slack/2026-08-18-large-file-chunking-reopen.md` |
| 2026-08-18 | Bob files `CMT-2026-08-003` (correction): MedFirst pilot hit **OOM on a 4.7GB PDF with 8GB RAM** on a clinic workstation → pilot-blocker, prioritized ahead of nice-to-have perf work and tied to the **T011 release gate** | `work-states/comments/2026-08.md` |
| 2026-08-20 | Charlie posts root cause and starts the **buffer-release refactor** (eager release after each chunk). Diana asks for a build to re-run the stress case; Charlie: "not ready to call it done again yet" | `slack/2026-08-16-large-file-chunking-merge.md` (thread last activity 2026-08-20); `tasks/CIPH-41-...md` activity entry |
| 2026-08-23 | Design review confirms: chunking merged, buffer-release refactor still Active. Early local testing on a 2.3GB sample shows flat memory, **but not yet validated against the full large-file test corpus** | `2026-08-23-Large-File-Chunking-Design-Review.md` |
| 2026-09-02 / 09-15 / 09-22 | Briefs keep T031 listed as an open blocker; on 09-22 it remains "MedFirst pilot OOM still release-coupled" | `briefs/2026-09-02`, `2026-09-15`, `2026-09-22-daily-brief.md` |

## Technical root cause

The chunking mechanism itself works and is merged — the reopen is a **memory-lifetime defect, not a chunking-logic defect**.

- **Root cause (Charlie, 2026-08-20):** chunk buffers were **not explicitly released once a worker moved past them**. They were left to fall out of scope, but something else retained a live reference, so they stayed reachable and were never freed. `slack/2026-08-16-large-file-chunking-merge.md`
- **Effect:** peak memory climbed roughly **linearly with file size** instead of staying bounded by chunk size — defeating the entire point of chunking on the largest files. `2026-08-23-Large-File-Chunking-Design-Review.md`
- **Threshold:** manifests at and above **2GB**; worst observed case is the MedFirst 4.7GB PDF on an 8GB clinic workstation. `CMT-2026-08-003`
- **Fix in flight:** refactor the stream-chunk handler to **eagerly release each chunk's buffer immediately after that chunk is processed**, rather than waiting for whole-file completion. `slack/2026-08-16-...merge.md`, `tasks/CIPH-41-...md`

**Important distinction — a second, separate leak was found and *is* closed.** CIPH-43 / T033 (PDF loader leak) is **Completed**: with the usual commercial profiler unusable on the air-gapped lab box (network-gated license check), the team switched to stdlib `tracemalloc`, which traced retained allocations to the **PDF loader's internal page-object cache** holding fully-parsed page objects after each page's redaction pass. Bob patched it (PR #84, merged 2026-08-23); Diana's 6-hour soak showed flat memory. The profiling report states explicitly this loader-side leak is **"distinct from the T031 buffer-release issue"** and that its result "depends on and complements" the T031 fix. So CIPH-43 being green does *not* mean CIPH-41 is green.
- `tasks/CIPH-43-Memory-Leak-Profiling.md`; `slack/2026-08-21-memory-leak-tracemalloc.md`; `2026-08-23-Memory-Leak-Profiling-Report.md`; `2026-08-27-Memory-Leak-Profiling-Review.md`; `fireflies/2026-08-19-Memory-Leak-Profiling-Blocker.md`

## Ownership of the next engineering action

- **Owner: Charlie** — assignee on CIPH-41 and the engineer performing the stream buffer-release refactor. WS-05 "Next Update Needed" names exactly this: *"T031 stream buffer refactor."* (WS-05 area owner is listed as Charlie / Bob; the 2026-08-19 brief action item reads "Charlie: prioritize stream buffer release patch and clinic 8GB repro.")
- **Next action:** finish the per-chunk eager buffer release and validate it against the **full large-file test corpus** — the 2.3GB local result is not sufficient. Two verification items are explicitly outstanding: Diana is waiting on a build to re-run the QA stress case (`slack/2026-08-16-...merge.md`), and the 09-02 brief says it stays a pilot-blocker "until buffer release is proven **on clinic hardware**" (the 4.7GB / 8GB MedFirst scenario). The original design note also still has an unretired *pending* item: a 10,000-page stress test to confirm the final **re-merge step** doesn't itself re-introduce OOM.
- **Supporting roles:** Bob (reported the leak, filed the pilot-blocker comment, owns the completed loader-side patch), Diana (QA repro and stress/soak validation), Alice (PM prioritization).

## Two caveats worth flagging

1. **Release coupling:** `CMT-2026-08-003` ties T031 explicitly to the **T011 release gate**, and the 2026-09-22 brief still lists T031 under "Blockers / waiting-on items" as "still release-coupled." T011 itself is under a security-gate hold against a hard **2026-10-15 no-ship deadline**. `briefs/2026-09-22-daily-brief.md`
2. **No evidence of progress after 2026-08-23.** The latest substantive source on the buffer-release refactor is the 2026-08-23 design review. From 2026-09-02 onward the briefs restate T031's blocker status by reference to the August comment rather than reporting new work, and T031 does not appear in the 09-22 priority order (which is led by T005/T029, T024, T030). Nothing in the package shows the refactor was completed or verified — the corpus supports "still open and unverified," not "actively progressing."
