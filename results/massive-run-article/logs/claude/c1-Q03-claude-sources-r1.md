# Large-file chunking was merged in mid-August. As of **2026-09-22**, has that completion held? Reconstruct the completion → reopen timeline, the technical root cause, and who owns the next engineering action.

<!-- RESPONSE_START -->

## Answer

**No — the completion did not hold.** As of 2026-09-22 the large-file chunking task is still open. Its last recorded status is **Active (Reopened)**, assigned to **Charlie**, and no source in the dataset shows it being closed again after the reopen.

### Completion → reopen timeline

| Date | Event | Source |
|---|---|---|
| 2026-08-12 | Alice opens the task (CIPH-41 / referenced elsewhere as T031), "Stream-chunk multi-GB PDF loads without retaining buffers," assigned to Charlie | SRC-CU-CIPH-41 |
| 2026-08-14 | Charlie starts stream-based chunked reads; adds an overlap window between chunks so entities spanning a boundary aren't missed. Design note DOC-2025 records the "Stream-and-Split" layer (100-page blocks → temp sub-documents → worker pool → re-merge) and flags a *pending* 10,000-page stress test to check whether the final re-merge step re-introduces OOM | SRC-SLACK-42, SRC-GDOC-25 |
| **2026-08-16** | **Charlie merges stream chunking to mainline and calls it done.** Bob asks whether the memory concerns are fully cleared; Charlie answers "As far as testing showed, clean. We'll see if anything shows up on longer runs." | SRC-SLACK-44, SRC-GDOC-42 |
| 2026-08-17 | Bob begins leak-hotspot identification in the PDF loader; blocked for several days because the usual commercial profiler is unavailable in the offline lab (network-gated license check) | SRC-GDOC-27 |
| **2026-08-18** | **Bob reopens the task.** On long-running batches with files >2GB memory still leaks despite the chunked-read path; Bob notes it is not the page buffers themselves but "something else holding a reference." Diana reproduces in QA — memory climbs steadily and the process is eventually killed. Charlie: "Reopening this until we find it." | SRC-SLACK-43 |
| 2026-08-20 | Charlie posts root cause and starts the buffer-release refactor; task status recorded as **Active (Reopened)** | SRC-SLACK-44, SRC-CU-CIPH-41 |
| 2026-08-21 | Profiling switched to Python stdlib `tracemalloc` (works offline); it points at the PDF loader page-buffer / page-tree retention | SRC-GDOC-27, SRC-SLACK-49 |
| 2026-08-23 | Bob's loader-side patch lands (PR #84); Diana's 6-hour soak test shows flat memory; Evan rolls it to dev clusters. CIPH-43 (loader leak) closes as **Completed**. But CIPH-41's own buffer-release refactor is still **Active**, validated only on a 2.3GB local sample, "not yet verified end-to-end" against the full large-file test corpus | SRC-SLACK-49, SRC-GDOC-44, SRC-CU-CIPH-43, SRC-GDOC-42 |
| 2026-09-15 | Pre-release audit lists open gates (Docker slim/CVE, Windows signing, high-DPI, audit-log schema) — chunking is not mentioned either as cleared or as a gate | SRC-MEET-10 |
| 2026-09-22 | No further source records. Last known state of CIPH-41 remains Active (Reopened) | — |

### Technical root cause

The dataset records **two distinct but related retention problems**, and it's worth keeping them apart:

1. **Chunk-buffer non-release (the CIPH-41/T031 reopen cause, still open).** Buffers allocated per chunk were not explicitly released once the chunk finished processing — the code relied on them falling out of scope. Peak memory therefore climbed roughly **linearly with file size** instead of staying bounded by chunk size, defeating the purpose of chunking on the largest files. Charlie's fix refactors the stream-chunk handler to release each chunk's buffer **eagerly, immediately after each chunk is processed** rather than at end-of-file. (SRC-GDOC-42, SRC-SLACK-44, SRC-CU-CIPH-41)

2. **Loader-side page-object retention (CIPH-43, closed).** `tracemalloc` traced retained allocations to the PDF loader's internal page-object cache / the full page-tree held in `RedactionEngine` even after the document object was closed. Bob patched the loader's context manager to drop the cache entry once a page's redaction pass finishes, instead of waiting for document close. Post-patch profiling brought peak memory on a 2GB+ run down to the chunk-bounded footprint. (SRC-GDOC-44, SRC-SLACK-49, SRC-GDOC-27)

Bob explicitly characterized these as "same family of fix — builds on the chunking buffer-release work," and DOC-2044 states the loader leak is "distinct from the T031 buffer-release issue." So closing #2 did **not** close #1.

One caveat on the record itself: SRC-GDOC-27 attributes the tracemalloc switch to Charlie on 2026-08-21 (consistent with SRC-SLACK-49, where Charlie runs the capture), while the CIPH-43 task record and DOC-2044 credit the profiling/patch work to Bob as owner. The substance is consistent; the attribution of the tooling switch is not.

### Who owns the next engineering action

**Charlie** owns it. He is the assignee of CIPH-41 (Active/Reopened) and is the one refactoring the per-chunk buffer-release path. The outstanding action is **end-to-end validation of the buffer-release refactor against the full large-file test corpus** — as of the last record it had only been checked on a 2.3GB local sample showing flat memory. Two supporting owners are named:

- **Diana (QA)** is waiting on a build to re-run the stress case against ("Let me know when there's a build") and reproduced the original leak in QA.
- The **10,000-page re-merge stress test** flagged as *pending* in Charlie's 2026-08-14 design note (DOC-2025) — verifying the final PDF re-merge step doesn't re-introduce the OOM — has no completion record anywhere in the dataset.

The acceptance criteria that remain unmet: "Memory buffers are released after each chunk, with **no leak on files 2GB and larger**."

### Coverage gap

The dataset contains **no source records dated between 2026-08-23 and 2026-09-22 that touch large-file chunking**. The 2026-09-15 pre-release audit — the closest-dated status record to the question's cutoff — reviews release gates without mentioning chunking at all. So the "as of 2026-09-22" answer rests on the absence of any closing event after 2026-08-23 rather than on a positive 2026-09-22 status record. If the task was quietly closed in that window, this dataset would not show it.

### Sources cited

- `med-synth/tasks/CIPH-41-Large-File-Chunking.md` (SRC-CU-CIPH-41)
- `med-synth/tasks/CIPH-43-Memory-Leak-Profiling.md` (SRC-CU-CIPH-43)
- `med-synth/documentation/sources/2026-08-14-Large-File-Chunking-Review.md` (SRC-GDOC-25, DOC-2025)
- `med-synth/documentation/sources/2026-08-23-Large-File-Chunking-Design-Review.md` (SRC-GDOC-42, DOC-2042)
- `med-synth/documentation/sources/2026-08-23-Memory-Leak-Profiling-Report.md` (SRC-GDOC-44, DOC-2044)
- `med-synth/documentation/sources/2026-08-27-Memory-Leak-Profiling-Review.md` (SRC-GDOC-27, DOC-2027)
- `med-synth/communication/sources/slack/2026-08-14-large-file-chunking.md` (SRC-SLACK-42)
- `med-synth/communication/sources/slack/2026-08-16-large-file-chunking-merge.md` (SRC-SLACK-44)
- `med-synth/communication/sources/slack/2026-08-18-large-file-chunking-reopen.md` (SRC-SLACK-43)
- `med-synth/communication/sources/slack/2026-08-21-memory-leak-tracemalloc.md` (SRC-SLACK-49)
- `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (SRC-MEET-10)
