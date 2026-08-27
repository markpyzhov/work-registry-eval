# Large-file chunking was merged in mid-August. As of **2026-09-22**, has that completion held? Reconstruct the completion → reopen timeline, the technical root cause, and who owns the next engineering action.

<!-- RESPONSE_START -->

No evidence exists after 2026-08-27 on this thread. I have the full picture.

## Answer

**No — the completion did not hold.** As of the 2026-09-22 work state (`work-states/WS-05-performance.md`, WS-05: Performance Benchmarking and System Optimization, Status `in_progress`, Owner Charlie / Bob, Project CipherDoc), large-file chunking (**T031**, mapped to **CIPH-41**) is **Reopened/active** and remains an unchecked item on the task list. ClickUp CIPH-41 (`SRC-CU-CIPH-41`) independently carries status **Active (Reopened)**, assignee Charlie. The mid-August "done" call was reversed two days later and has never been re-closed.

### Completion → reopen timeline

- **2026-08-12** — Alice opens CIPH-41 ("Stream-chunk multi-GB PDF loads without retaining buffers") because chunking is needed for multi-GB documents. (`SRC-CU-CIPH-41`)
- **2026-08-14** — Charlie starts stream-based chunked reads; adds an overlap window between chunks so entities spanning a boundary aren't missed. Design note DOC-2025 records the "Stream-and-Split" pre-processing layer (100-page blocks → temp sub-documents → worker pool → re-merge), and flags a pending 10,000-page stress test to confirm the re-merge step doesn't re-introduce OOM. (`SRC-SLACK-42`, `SRC-GDOC-25`)
- **2026-08-16** — **Merge and first completion claim.** Charlie merges the stream-chunking implementation to mainline: "Calling this done." Bob asks whether the memory concerns from testing are fully clean; Charlie answers that testing showed clean, "We'll see if anything shows up on longer runs." (`SRC-SLACK-44`; merge date confirmed in `SRC-GDOC-42`)
- **2026-08-18** — **Reopen, two days later.** Bob reopens: on long-running batches with files over 2GB, memory is still leaking despite the chunked-read path being nominally done. He notes it is not the page buffers themselves — something else is holding a reference and preventing them from being freed. Diana reproduces it in QA: memory climbs steadily and the process is eventually killed on larger inputs. Charlie reopens the task pending root cause. (`SRC-SLACK-43`)
- **2026-08-18** — Same day, **CMT-2026-08-003** (Bob, correction, WS-05/T031): the MedFirst pilot hit OOM on a 4.7GB PDF with only 8GB RAM on a clinic workstation. Escalated as a **pilot-blocker**, to be prioritized ahead of nice-to-have perf work and tied explicitly to the **T011 release gate**. Applied to WS-05/T031 Active Work and Blockers.
- **2026-08-20** — Charlie posts the root cause and starts the fix: chunk buffers were not being explicitly released once a worker moved past them; he is refactoring the buffer-release path to release **eagerly, right after each chunk is processed**, rather than at end of file. He explicitly declines to re-close: "Still working through it, not ready to call it done again yet." Diana asks to be told when there's a build to re-run the stress case against. CIPH-41 activity history logs a **2026-08-20 Charlie — Buffer Release Refactor** transition into Active (Reopened). (`SRC-SLACK-44`, `SRC-CU-CIPH-41`)
- **2026-08-23** — Design review DOC-2042 ("Large-File Chunking — Post-Merge Reopen") records the state: chunking mechanism merged and in place; the per-chunk buffer-release refactor is still Active. Early local testing on a 2.3GB sample shows flat memory across chunks instead of the previous climb, **but the fix has not been validated against the full large-file test corpus**. (`SRC-GDOC-42`)
- **2026-08-23** — A **separate, distinct** leak is closed: Bob's profiling report DOC-2044 traces retained allocations to the PDF loader's internal page-object cache holding fully-parsed page objects after each page's redaction pass finished. He patched the loader to drop the cache entry immediately, and re-profiling showed peak memory on a 2GB+ run matching the chunk-bounded footprint. That loader-side work (**T033 / CIPH-43**) is Completed and checked off. Because tooling was air-gapped, the team superseded the commercial cloud profiler with Python's stdlib `tracemalloc`. (`SRC-GDOC-44`, `SRC-CU-CIPH-43`)
- **2026-09-22** — Work state last updated; T031 still listed under Active Work as Reopened/active, with the MedFirst pilot OOM still recorded. No later record in the dataset shows the buffer-release fix validated or the task re-closed.

### Technical root cause

Two related but **distinct** memory leaks surfaced on 2GB+ files, and only one is closed:

1. **The T031/CIPH-41 leak (still open).** The chunking layer allocated a buffer per chunk but never explicitly released it once the chunk finished processing — it relied on the buffer falling out of scope, and something was still holding a reference that kept it from being freed. Peak memory therefore climbed roughly **linearly with file size** instead of staying bounded by the chunk size, which defeats the entire purpose of chunking on exactly the largest files it was built for. The fix is to make the stream-chunk handler explicitly release each chunk's buffer eagerly, immediately after processing, rather than waiting for the whole file to finish. Acceptance criteria on CIPH-41 require buffers released after each chunk with **no leak on files 2GB and larger**. (`SRC-SLACK-43`, `SRC-SLACK-44`, `SRC-GDOC-42`, `SRC-CU-CIPH-41`)

2. **The T033/CIPH-43 loader leak (closed).** Independently, the PDF loader's internal page-object cache retained fully-parsed page objects long after each page's redaction pass completed, releasing only at document close. Patched and verified. (`SRC-GDOC-44`)

The design work also flagged a standing trade-off, not a defect: splitting at page boundaries breaks regex matches that span pages, trading context-awareness for memory stability (mitigated by the overlap window), plus disk I/O and chunk-ordering overhead on re-merge. (`SRC-GDOC-25`, `SRC-SLACK-42`)

### Who owns the next engineering action

**Charlie** owns it. He is the CIPH-41 assignee and is personally refactoring the stream-chunk buffer-release logic; the work state names him explicitly ("Charlie is refactoring stream buffer release logic"). The concrete next action is to **finish and validate the per-chunk eager buffer-release refactor against the full large-file test corpus** — early local results on a 2.3GB sample are promising but not end-to-end verified.

Supporting ownership: **Diana** (QA) holds the verification step and has asked to be handed a build so she can re-run the stress case, including the MedFirst 4.7GB / 8GB-RAM scenario. **Bob** reported and reproduced the leak and owns the already-completed loader-side patch. WS-05 overall is jointly owned by **Charlie / Bob**.

### Cited records

`work-states/WS-05-performance.md` (WS-05, last updated 2026-09-22) · `work-states/comments/2026-08.md` (CMT-2026-08-003) · `med-synth/tasks/CIPH-41-Large-File-Chunking.md` (`SRC-CU-CIPH-41`) · `med-synth/communication/sources/slack/2026-08-14-large-file-chunking.md` (`SRC-SLACK-42`) · `med-synth/communication/sources/slack/2026-08-16-large-file-chunking-merge.md` (`SRC-SLACK-44`) · `med-synth/communication/sources/slack/2026-08-18-large-file-chunking-reopen.md` (`SRC-SLACK-43`) · `med-synth/documentation/sources/2026-08-14-Large-File-Chunking-Review.md` (`SRC-GDOC-25`, DOC-2025) · `med-synth/documentation/sources/2026-08-23-Large-File-Chunking-Design-Review.md` (`SRC-GDOC-42`, DOC-2042) · `med-synth/documentation/sources/2026-08-23-Memory-Leak-Profiling-Report.md` (`SRC-GDOC-44`, DOC-2044)

One caveat: the most recent chunking-specific source in the dataset is dated 2026-08-23. The "still reopened as of 2026-09-22" conclusion rests on the authoritative work state's own last-updated date, not on a September-dated source document.
