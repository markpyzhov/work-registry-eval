# Large-file chunking was merged in mid-August. As of **2026-09-22**, has that completion held? Reconstruct the completion → reopen timeline, the technical root cause, and who owns the next engineering action.

<!-- RESPONSE_START -->

## Answer

**No — the completion did not hold.** As of **2026-09-22**, large-file stream chunking (`T031` / ClickUp `CIPH-41`) is **Reopened/active**, not done. The Work State `WS-05: Performance Benchmarking and System Optimization` (Last Updated 2026-09-22, Owner Charlie / Bob, P1, in_progress) still carries `T031` as an **unchecked** task, and CIPH-41 sits at status **Active (Reopened)**.

### Completion → reopen timeline

| Date | Event |
|---|---|
| **2026-08-12** | Alice opens CIPH-41 ("Stream-chunk multi-GB PDF loads without retaining buffers") because large-file chunking is needed for multi-GB documents. |
| **2026-08-16** | Charlie merges the stream-chunking implementation to mainline and declares it done ("Calling this done"). Bob asks whether the memory concerns from testing are fully cleared; Charlie replies clean "as far as testing showed… we'll see if anything shows up on longer runs." (SRC-SLACK-44; DOC-2042 confirms merge date 2026-08-16.) |
| **2026-08-17** | Bob reports a slow leak in long-running containers hitting the memory ceiling after ~4h; Diana confirms steady RSS climb on the staging node; Evan bumps the container limit to 2GB as a stopgap. (SRC-SLACK-48) |
| **2026-08-18** | **Reopen.** Bob reopens large-file chunking: on long-running batches with files over 2GB memory still leaks despite the "done" chunked-read path. Bob notes it is *not* the page buffers themselves — something else holds a reference. Diana reproduces in QA; the process gets killed on larger inputs. Charlie: "Reopening this until we find it." (SRC-SLACK-43) |
| **2026-08-18** | Escalation via comment **CMT-2026-08-003** (author Bob): MedFirst pilot hit OOM on a **4.7GB PDF with only 8GB RAM** on a clinic workstation — declared a **pilot-blocker**, to be prioritized ahead of nice-to-have perf work and tied explicitly to the **T011 release gate**. |
| **2026-08-20** | Charlie logs the "Buffer Release Refactor" activity on CIPH-41 (status Active (Reopened)) and states the root cause publicly; fix releases buffers **eagerly after each chunk**, and he explicitly declines to call it done again. Diana asks for a build to re-run the stress case. (CIPH-41 activity history; SRC-SLACK-44) |
| **2026-08-21 → 08-23** | A **separate, adjacent** leak is chased under `T033` / CIPH-43: with the commercial profiler unavailable in the offline lab, Charlie switches to stdlib `tracemalloc`; it points to the PDF loader's page-object cache / full page-tree retained in `RedactionEngine` after document close. Bob patches it (explicit cache/page-tree release), Diana's 6-hour soak shows flat memory, **PR #84 merged**, Evan rolls it to dev clusters. CIPH-43 → **Completed**. (SRC-SLACK-49, DOC-2044, DOC-2027) |
| **2026-08-23** | Design review DOC-2042 records: chunking mechanism merged and in place, but the buffer-release refactor is **still Active and not verified end-to-end**. Early local testing on a 2.3GB sample shows flat memory across chunks; it has **not** been validated against the full large-file test corpus. |
| **2026-09-22** | WS-05 snapshot: `T031 / CIPH-41` — **Reopened/active**, `[ ]` unchecked. `T033 / CIPH-43` is the only memory item in Done/Evidence ("PDF loader memory leak patched; consumption stable after 10,000 documents"). |

### Technical root cause

Two distinct but related defects — do not conflate them:

1. **The T031 defect (still open).** The merged implementation streams large documents in fixed-size page chunks instead of loading them whole into RAM, but the **buffers allocated for each chunk were not released once the chunk finished processing** — they were left to fall out of scope and something kept them reachable. Peak memory therefore climbed roughly **linearly with file size** instead of staying bounded by the chunk size, defeating the entire purpose of chunking on the largest files. Charlie's fix refactors the stream-chunk handler to **explicitly release each chunk's buffer eagerly, immediately after that chunk is processed**, rather than relying on scope exit.

2. **The T033 defect (closed).** A *separate* loader-side leak: the PDF loader's internal **page-object cache** held references to fully-parsed page objects long after each page's redaction pass had completed (surfacing in `tracemalloc` as the full page-tree retained in `RedactionEngine` after document close). Bob patched the loader to drop the cache entry as soon as a page's redaction pass finishes rather than waiting for document close, and re-profiling confirmed peak memory on a 2GB+ run fell to the chunk-bounded footprint. Bob characterized it as "same family of fix — builds on the chunking buffer-release work."

The T033 patch being verified does **not** close T031; DOC-2044 explicitly states the loader-side leak is "distinct from the T031 buffer-release issue," and that its result "depends on and complements" the still-outstanding T031 fix.

### Who owns the next engineering action

**Charlie** — assignee of CIPH-41 and the engineer performing the per-chunk buffer-release refactor of the stream-chunk handler. The specific outstanding action is to **complete and validate the eager per-chunk buffer release against the full large-file test corpus** (only a 2.3GB local sample has been exercised so far). **Diana** owns the dependent verification step — she asked to be notified when a build is available so she can re-run the stress/QA case that reproduced the climb. The overall WS-05 work state is co-owned by **Charlie / Bob**.

Priority context: because of CMT-2026-08-003, T031 is a MedFirst pilot-blocker prioritized ahead of discretionary performance work and tied to the T011 release gate — which itself now carries a hard no-ship date of 2026-10-15 (CMT-2026-09-002).

### Dataset records cited

- `work-states/WS-05-performance.md` (`path = work-state`, Last Updated 2026-09-22) — authoritative status
- `work-states/comments/2026-08.md` — CMT-2026-08-003
- `work-states/comments/2026-09.md` — CMT-2026-09-002
- `med-synth/tasks/CIPH-41-Large-File-Chunking.md` (SRC-CU-CIPH-41)
- `med-synth/tasks/CIPH-43-Memory-Leak-Profiling.md` (SRC-CU-CIPH-43)
- `med-synth/communication/sources/slack/2026-08-16-large-file-chunking-merge.md` (SRC-SLACK-44)
- `med-synth/communication/sources/slack/2026-08-17-memory-leak-hotspots.md` (SRC-SLACK-48)
- `med-synth/communication/sources/slack/2026-08-18-large-file-chunking-reopen.md` (SRC-SLACK-43)
- `med-synth/communication/sources/slack/2026-08-21-memory-leak-tracemalloc.md` (SRC-SLACK-49)
- `med-synth/documentation/sources/2026-08-23-Large-File-Chunking-Design-Review.md` (SRC-GDOC-42 / DOC-2042)
- `med-synth/documentation/sources/2026-08-23-Memory-Leak-Profiling-Report.md` (SRC-GDOC-44 / DOC-2044)
- `med-synth/documentation/sources/2026-08-27-Memory-Leak-Profiling-Review.md` (SRC-GDOC-27 / DOC-2027)
