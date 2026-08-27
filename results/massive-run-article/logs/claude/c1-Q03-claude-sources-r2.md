# Large-file chunking was merged in mid-August. As of **2026-09-22**, has that completion held? Reconstruct the completion → reopen timeline, the technical root cause, and who owns the next engineering action.

<!-- RESPONSE_START -->

## Answer

**No — the completion did not hold.** Large-file chunking was merged and declared done on 2026-08-16, but was reopened two days later and, on the evidence available, is still open as of 2026-09-22. The task **CIPH-41 / T031 "Stream-chunk multi-GB PDF loads without retaining buffers"** carries status **Active (Reopened)**, assigned to **Charlie**, with its last recorded activity on 2026-08-20 and no subsequent closure event in any source.

### Completion → reopen timeline

| Date | Event | Source |
|---|---|---|
| 2026-08-12 | Alice opens CIPH-41 (T031) for large-file chunking on multi-GB documents | SRC-CU-CIPH-41 |
| 2026-08-14 | Charlie starts stream-based chunked reads; design note documents the "Stream-and-Split" layer (100-page blocks → temp sub-documents → worker pool → post-merge). Failure mode being solved: whole document tree loaded into RAM, causing `OOMKilled` on >2GB files in 4GB Docker containers. An overlap window is added for entities spanning chunk boundaries | SRC-SLACK-42, SRC-GDOC-25 |
| 2026-08-16 09:19 | Charlie merges stream-chunking to mainline: "Calling this done." Bob asks whether the memory concerns are fully clean; Charlie answers "As far as testing showed, clean. We'll see if anything shows up on longer runs." | SRC-SLACK-44, SRC-GDOC-42 |
| 2026-08-17 | Independent memory signal: Bob sees the long-running container hit its memory limit after ~4 hours; Diana confirms a steady RSS climb on staging; Evan raises the limit to 2GB as a stopgap | SRC-SLACK-48 |
| 2026-08-18 10:30 | **Reopen.** Bob reopens large-file chunking: on long-running batches with files over 2GB, memory still leaks despite the chunked-read path being "done." Bob notes it is not the page buffers themselves — something else holds a reference. Diana reproduces in QA; the process eventually gets killed on larger inputs. Charlie: "Reopening this until we find it." | SRC-SLACK-43 |
| 2026-08-19 | Investigation stalls: the usual commercial profiler needs a license server and won't start on the air-gapped lab box; team agrees to try stdlib tooling | SRC-MEET-06, SRC-GDOC-27 |
| 2026-08-20 09:01 | Charlie states the root cause and starts the buffer-release refactor. **This is the last recorded activity on CIPH-41.** | SRC-SLACK-44, SRC-CU-CIPH-41 |
| 2026-08-21 | Profiling switches to stdlib `tracemalloc`; it shows the full page-tree retained in `RedactionEngine` even after the document object is closed | SRC-SLACK-49, SRC-GDOC-27 |
| 2026-08-23 | **Separate task closes.** Bob's loader-side patch (PR #84) lands, releasing the page-tree reference in the context manager; Diana's 6-hour soak test shows flat memory; Evan rolls it to dev clusters. **CIPH-43 (T-loader profiling) → Completed.** | SRC-SLACK-49, SRC-GDOC-44, SRC-CU-CIPH-43 |
| 2026-08-23 | Design review records CIPH-41 itself as still open: early local testing on a 2.3GB sample shows flat memory, "but the fix has not yet been validated against the full large-file test corpus" | SRC-GDOC-42 |
| 2026-08-23 → 2026-09-22 | No further source records any activity, verification, or closure on CIPH-41 | — |

### Technical root cause

Two distinct but related memory faults, and it is important not to conflate them:

1. **The T031/CIPH-41 defect (still open).** Buffers allocated for each chunk were not explicitly released once the chunk finished processing — the code relied on them falling out of scope, but a worker kept a reference alive after moving past the chunk. Peak memory therefore climbed roughly *linearly with file size* instead of staying bounded by the chunk size, defeating the entire purpose of chunking on the largest files. Charlie's fix is a refactor of the stream-chunk handler to release each chunk's buffer **eagerly, immediately after that chunk is processed**, rather than waiting for the whole file to finish.

2. **The CIPH-43 loader-side leak (closed 2026-08-23).** Tracemalloc traced retained allocations to the PDF loader's internal page-object cache, which held references to fully-parsed page objects long after that page's redaction pass completed. Bob patched the loader to drop the cache entry at end-of-page rather than at document close. This was verified — post-patch peak memory on a 2GB+ run matched the chunk-bounded footprint, and a 6-hour soak test was flat.

The profiling report is explicit that these are separate: the loader-side leak is "distinct from the T031 buffer-release issue," and its result "depends on and complements the T031 chunking/buffer-release fix." So CIPH-43 being Completed does **not** close CIPH-41 — this is the trap in reading the record.

### Who owns the next engineering action

**Charlie** owns it. He is the assignee of CIPH-41 (T031) and the owner of the design review DOC-2042. The outstanding action is to finish and validate the per-chunk buffer-release refactor against the **full large-file test corpus** — early local testing on a 2.3GB sample looked flat, but end-to-end verification has not happened. Charlie's own words on 2026-08-20: "Still working through it, not ready to call it done again yet."

Two supporting/dependent items sit behind him:
- **Diana (QA)** is waiting on a build to re-run the stress case against ("Let me know when there's a build to re-run the stress case against," 2026-08-20). No source shows that build being delivered or that re-run occurring.
- A **10,000-page stress test** remains pending from the original design note (DOC-2025) to verify that the final re-merge step — which itself uses RAM — does not reintroduce the OOM crash. No source records this test being run.

### Acceptance criteria still unmet

Of CIPH-41's two acceptance criteria, the first is satisfied (large PDFs are processed via stream chunking rather than whole-file loads, merged 2026-08-16). The second — "Memory buffers are released after each chunk, with no leak on files 2GB and larger" — is not yet verified.

### Caveat

The dataset contains no source dated between 2026-08-23 and 2026-09-22 that touches CIPH-41. The "still open as of 2026-09-22" conclusion therefore rests on the absence of any closure event in a record that does extend into late September elsewhere (the 2026-09-15 pre-release audit and a 2026-09-22 activity entry on the unrelated CIPH-34 both exist), rather than on a positive September-dated statement about chunking. Notably, the 2026-09-15 pre-release gate review lists Docker slim-down/CVE, Windows signing, upstream high-DPI, and the audit-log schema mismatch as open blockers, and does not mention large-file chunking at all — so chunking is not being tracked as a release gate either way.

### Sources cited

- `med-synth/tasks/CIPH-41-Large-File-Chunking.md` (SRC-CU-CIPH-41)
- `med-synth/tasks/CIPH-43-Memory-Leak-Profiling.md` (SRC-CU-CIPH-43)
- `med-synth/communication/sources/slack/2026-08-14-large-file-chunking.md` (SRC-SLACK-42)
- `med-synth/communication/sources/slack/2026-08-16-large-file-chunking-merge.md` (SRC-SLACK-44)
- `med-synth/communication/sources/slack/2026-08-17-memory-leak-hotspots.md` (SRC-SLACK-48)
- `med-synth/communication/sources/slack/2026-08-18-large-file-chunking-reopen.md` (SRC-SLACK-43)
- `med-synth/communication/sources/slack/2026-08-21-memory-leak-tracemalloc.md` (SRC-SLACK-49)
- `med-synth/communication/sources/fireflies/2026-08-19-Memory-Leak-Profiling-Blocker.md` (SRC-MEET-06)
- `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (SRC-MEET-10)
- `med-synth/documentation/sources/2026-08-14-Large-File-Chunking-Review.md` (SRC-GDOC-25, DOC-2025)
- `med-synth/documentation/sources/2026-08-23-Large-File-Chunking-Design-Review.md` (SRC-GDOC-42, DOC-2042)
- `med-synth/documentation/sources/2026-08-23-Memory-Leak-Profiling-Report.md` (SRC-GDOC-44, DOC-2044)
- `med-synth/documentation/sources/2026-08-27-Memory-Leak-Profiling-Review.md` (SRC-GDOC-27, DOC-2027)
