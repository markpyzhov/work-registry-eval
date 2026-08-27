# Large-file chunking was merged in mid-August. As of **2026-09-22**, has that completion held? Reconstruct the completion → reopen timeline, the technical root cause, and who owns the next engineering action.

<!-- RESPONSE_START -->

## Answer

**No — the completion did not hold.** Large-file chunking was declared done on 2026-08-16 and reopened two days later. As of 2026-09-22 it is still open: ClickUp task **CIPH-41** ("Stream-chunk multi-GB PDF loads without retaining buffers") carries status **Active (Reopened)**, assigned to **Charlie**. No source in the dataset records it being re-closed after the reopen.

### Completion → reopen timeline

| Date | Event |
|---|---|
| 2026-08-12 | Alice opens CIPH-41: large-file chunking needed for multi-GB documents (SRC-CU-CIPH-41). |
| 2026-08-14 | Charlie starts stream-based chunked reads; adds an overlap window so entities spanning a chunk boundary get caught on both sides (SRC-SLACK-42). Design note DOC-2025 records the "Stream-and-Split" layer — 100-page blocks → temp sub-documents → worker pool → re-merge — and flags a *pending* 10,000-page stress test to check whether the re-merge step reintroduces OOM (SRC-GDOC-25). |
| **2026-08-16** | Charlie merges stream chunking to mainline: "Merged the stream-chunking implementation into mainline. Calling this done." Bob asks whether the memory concerns are fully clean; Charlie: "As far as testing showed, clean. We'll see if anything shows up on longer runs." (SRC-SLACK-44, confirmed in SRC-GDOC-42.) |
| **2026-08-18** | **Reopened.** Bob: on long-running batches with files over 2GB memory is still leaking despite the chunked-read path being "supposedly done"; it is not the page buffers themselves — "something else is holding a reference." Diana reproduces in QA: memory climbs steadily and the process is eventually killed on larger inputs. Charlie takes the investigation (SRC-SLACK-43). |
| 2026-08-20 | Charlie posts root cause and starts the buffer-release refactor; explicitly declines to re-close: "Still working through it, not ready to call it done again yet." Diana asks for a build to re-run the stress case against (SRC-SLACK-44). Task activity log records "Buffer Release Refactor — Active (Reopened)" (SRC-CU-CIPH-41). |
| 2026-08-21→23 | Parallel leak hunt (CIPH-43, Bob): usual commercial profiler unusable in the offline lab (network-gated license check), so Charlie switches to stdlib `tracemalloc`; it shows the full page-tree retained in `RedactionEngine` after document close. Bob patches the loader's page-object cache; Diana's 6-hour soak test shows flat memory; PR #84 merged; Evan rolls it to dev clusters. **CIPH-43 is Completed** — but it is a distinct, loader-side leak (SRC-SLACK-49, SRC-GDOC-44, SRC-GDOC-27, SRC-CU-CIPH-43). |
| 2026-08-23 | Design review DOC-2042 final status: chunking mechanism merged and in place; buffer-release refactor **still Active and not yet verified end-to-end**. Early local testing on a 2.3GB sample shows flat memory, but the fix has **not** been validated against the full large-file test corpus (SRC-GDOC-42). |
| 2026-08-24 → 2026-09-22 | No source records any further change to CIPH-41. Latest state stands at Active (Reopened). |

### Technical root cause

Two related but distinct memory retentions, both surfaced by the 2GB+ chunked runs:

1. **The reopen cause (CIPH-41, still open).** Buffers allocated per chunk were not explicitly released once a worker moved past the chunk — the code relied on them falling out of scope. Peak memory therefore climbed roughly linearly with file size instead of staying bounded by chunk size, which defeated the entire purpose of chunking on the largest files and produced OOM kills on long batches. Charlie's fix refactors the stream-chunk handler to release each chunk's buffer *eagerly*, right after that chunk is processed ("that's the whole point, don't let it accumulate"), rather than at end-of-file. (SRC-GDOC-42, SRC-SLACK-44, SRC-CU-CIPH-41)

2. **A separate loader-side leak (CIPH-43, closed).** `tracemalloc` traced retained allocations to the PDF loader's internal page-object cache, which held references to fully-parsed page objects long after each page's redaction pass finished, waiting for document close. Bob patched the loader to drop the cache entry as soon as a page's redaction pass completes; post-patch profiling showed peak memory on a 2GB+ run dropping to the chunk-bounded footprint. (SRC-GDOC-44, SRC-GDOC-27, SRC-SLACK-49)

Note the relationship: DOC-2044 states the loader-side fix "depends on and complements" the chunking/buffer-release work — so CIPH-43's completion does *not* close CIPH-41.

### Who owns the next engineering action

**Charlie** owns the next engineering action — he is the assignee of CIPH-41 and the author of the in-progress per-chunk buffer-release refactor. The outstanding work is to finish that refactor and validate it against the **full large-file test corpus** (only a 2.3GB local sample has been checked so far). Acceptance criteria still unmet: "Memory buffers are released after each chunk, with no leak on files 2GB and larger."

Two verification dependencies sit alongside it:
- **Diana (QA)** is waiting on a build to re-run the stress case / large-file corpus against — she asked for one on 2026-08-20 and no source shows it delivered.
- The **10,000-page re-merge stress test** flagged pending in DOC-2025 (does the RAM-using final re-merge step reintroduce the OOM crash?) has no recorded result anywhere in the dataset.

### Caveat on evidence coverage

The dataset contains no source dated between 2026-08-24 and 2026-09-22 that touches CIPH-41. The nearest September evidence — the 2026-09-15 pre-release audit (SRC-MEET-10) — reviews release gates (Docker slim/CVE, Windows signing, upstream high-DPI, audit-log schema mismatch) and does **not** mention large-file chunking at all. So the "still reopened as of 2026-09-22" conclusion rests on the absence of any closing event after 2026-08-23 rather than on a positive September status record.

### Sources cited

- `med-synth/tasks/CIPH-41-Large-File-Chunking.md` (SRC-CU-CIPH-41)
- `med-synth/tasks/CIPH-43-Memory-Leak-Profiling.md` (SRC-CU-CIPH-43)
- `med-synth/communication/sources/slack/2026-08-14-large-file-chunking.md` (SRC-SLACK-42)
- `med-synth/communication/sources/slack/2026-08-16-large-file-chunking-merge.md` (SRC-SLACK-44)
- `med-synth/communication/sources/slack/2026-08-18-large-file-chunking-reopen.md` (SRC-SLACK-43)
- `med-synth/communication/sources/slack/2026-08-21-memory-leak-tracemalloc.md` (SRC-SLACK-49)
- `med-synth/documentation/sources/2026-08-14-Large-File-Chunking-Review.md` (SRC-GDOC-25 / DOC-2025)
- `med-synth/documentation/sources/2026-08-23-Large-File-Chunking-Design-Review.md` (SRC-GDOC-42 / DOC-2042)
- `med-synth/documentation/sources/2026-08-23-Memory-Leak-Profiling-Report.md` (SRC-GDOC-44 / DOC-2044)
- `med-synth/documentation/sources/2026-08-27-Memory-Leak-Profiling-Review.md` (SRC-GDOC-27 / DOC-2027)
- `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (SRC-MEET-10) — negative evidence
