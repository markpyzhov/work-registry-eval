# Large-file chunking was merged in mid-August. As of **2026-09-22**, has that completion held? Reconstruct the completion → reopen timeline, the technical root cause, and who owns the next engineering action.

<!-- RESPONSE_START -->

**No — the completion did not hold. As of 2026-09-22, large-file chunking (T031 / CIPH-41) is Reopened/Active, not done.**

## Current status (as of 2026-09-22)

Work State `WS-05: Performance Benchmarking and System Optimization` (Owner: Charlie / Bob, P1, CipherDoc, Last Updated 2026-09-22) is the authority here:

- Task list: `- [ ] T031 (mapped to CIPH-41) — Implement large file stream chunking` — **unchecked**.
- Active Work: **"T031 / CIPH-41: Reopened/active.** Initial chunking landed but Bob found severe memory leaks on files exceeding 2GB during long batch runs (S7). Charlie is refactoring stream buffer release logic."
- Active Work also carries the escalation: **"T031 — MedFirst pilot OOM (CMT-2026-08-003):** Clinic workstation OOM on 4.7GB PDF with 8GB RAM — pilot-blocker prioritized and tied to the T011 release gate."
- ClickUp CIPH-41 "Stream-chunk multi-GB PDF loads without retaining buffers" — **Status: Active (Reopened)**, Assignee **Charlie**, created 2026-08-12.

So the mid-August merge was real, but it was reverted in status terms two days later and has stayed open for roughly five weeks through the 2026-09-22 snapshot.

## Completion → reopen timeline

| Date | Event | Source |
|---|---|---|
| 2026-08-12 | Alice opens CIPH-41 for multi-GB chunking. | SRC-CU-CIPH-41 |
| 2026-08-16 | Charlie merges stream-chunking to mainline: "Merged the stream-chunking implementation into mainline. Calling this done." Bob asks if memory concerns are clean; Charlie: clean "as far as testing showed… We'll see if anything shows up on longer runs." | SRC-SLACK-44, SRC-GDOC-42 |
| 2026-08-17 | Bob reports a slow leak — long-running container hits its memory ceiling after ~4 hours; Diana confirms a steady climb on staging; Evan bumps the limit to 2GB as a stopgap. | SRC-SLACK-48 |
| **2026-08-18** | **Reopen.** Bob: memory still leaking on 2GB+ files despite the chunked-read path being "supposedly done"; notes it is *not* the page buffers themselves but something holding a reference. Diana reproduces in QA — process gets killed on larger inputs. Charlie: "Reopening this until we find it." | SRC-SLACK-43 |
| 2026-08-18 | Bob files CMT-2026-08-003 (correction, WS-05/T031): MedFirst pilot OOM on a 4.7GB PDF with 8GB RAM on a clinic workstation — pilot-blocker, prioritize T031 ahead of nice-to-have perf work, tie explicitly to the T011 release gate. Applied to WS-05/T031 Active Work and Blockers. | CMT-2026-08-003 |
| 2026-08-19 | Fireflies: leak-hotspot work stuck — the usual profiler needs a license server and won't start on the air-gapped lab box. Plan: try stdlib tooling. | SRC-MEET-06 |
| 2026-08-20 | Charlie logs the CIPH-41 "Buffer Release Refactor" activity, status Active (Reopened); confirms release is eager, right after each chunk — "Still working through it, not ready to call it done again yet." | SRC-CU-CIPH-41, SRC-SLACK-44 |
| 2026-08-21 | Charlie switches to stdlib `tracemalloc` (offline-compatible); finds the full page-tree retained in `RedactionEngine` even after document close. | SRC-SLACK-49, SRC-GDOC-27 |
| 2026-08-23 | Bob's loader patch lands (PR #84); Diana's 6-hour soak shows flat memory. Bob: "Same family of fix — builds on the chunking buffer-release work." CIPH-43 → **Completed**. | SRC-SLACK-49, SRC-CU-CIPH-43, SRC-GDOC-44 |
| 2026-08-23 | Design review DOC-2042 records chunking merged, task reopened, buffer-release refactor still Active and "not yet verified end-to-end." | SRC-GDOC-42 |
| 2026-09-22 | WS-05 snapshot: T031 still unchecked / Reopened-active. | WS-05 |

## Technical root cause

There were **two distinct but related leaks**, which is why one closing did not close the other:

1. **The T031 defect (still open).** The stream-chunking implementation processes multi-GB PDFs in fixed-size page chunks instead of loading the whole document into RAM, but **buffers allocated for each chunk were not released once the chunk finished processing** — they were left to fall out of scope rather than being freed explicitly, and something was still holding a reference. Peak memory therefore climbed roughly linearly with file size instead of staying bounded by the chunk size, defeating the purpose of chunking on exactly the largest files (SRC-GDOC-42, SRC-SLACK-43/44). Charlie's fix refactors the stream-chunk handler to **release each chunk's buffer eagerly, immediately after that chunk is processed**. Early local testing on a 2.3GB sample shows flat memory across chunks, but it has **not been validated against the full large-file test corpus** (SRC-GDOC-42).

2. **The T033 / CIPH-43 loader-side leak (closed).** Separately, `tracemalloc` traced retained allocations to the PDF loader's internal **page-object cache**, which held references to fully-parsed page objects long after each page's redaction pass completed — the context manager closed the file handle without releasing the page-tree reference. Bob patched the loader to drop the cache entry as soon as a page's redaction pass finishes rather than waiting for document close. Post-patch profiling showed peak memory on a 2GB+ run dropping to the chunk-bounded footprint; WS-05 Done/Evidence records "PDF loader memory leak patched; consumption stable after 10,000 documents." (SRC-GDOC-44, SRC-SLACK-49, WS-05)

Worth flagging: SRC-GDOC-44 explicitly calls the loader leak "distinct from the T031 buffer-release issue," and its own status note says the result "depends on and complements" the T031 fix. So the green soak-test result from 2026-08-23 is **not** evidence that T031 is closed — and indeed WS-05 still shows T031 open a month later.

A supporting tooling note: the commercial profiler was unusable in the air-gapped lab (network-gated license check), which stalled diagnosis for several days from 2026-08-17 until the 2026-08-21 switch to `tracemalloc`. WS-05 records this as a decision: "Profiling Tools: External cloud profiler superseded by native Python `tracemalloc` for air-gapped operation."

## Who owns the next engineering action

**Charlie** owns it. He is the assignee on CIPH-41 (Active (Reopened)) and is named in WS-05 Active Work as the person "refactoring stream buffer release logic." The specific outstanding action is to **finish and validate the per-chunk eager buffer-release refactor against the full large-file test corpus** — DOC-2042 states the fix "has not yet been validated against the full large-file test corpus," and Charlie himself said on 2026-08-20 he was "not ready to call it done again yet."

Adjacent ownership, for completeness:
- **Diana (QA)** is the verification gate — she reproduced the leak, asked to be told "when there's a build to re-run the stress case against," and ran the 6-hour soak on the loader patch. The closing criterion on CIPH-41 is "Memory buffers are released after each chunk, with no leak on files 2GB and larger."
- **Bob** owned the parallel loader-leak work (CIPH-43), which is Completed, and he is the one who raised both the reopen and the MedFirst pilot-blocker escalation.
- **Evan** owns the T011 release gate that CMT-2026-08-003 ties T031 to; separately, the release board set a hard **no-ship after 2026-10-15** if T005 and T029 are not green (CMT-2026-09-002, WS-03) — note that deadline is bound to T005/T029, not directly to T031, though CMT-2026-08-003 attaches T031 to the same T011 gate.

## Evidence cited

Work State: `work-states/WS-05-performance.md` (Last Updated 2026-09-22). Comments: `CMT-2026-08-003` (Bob, 2026-08-18, WS-05/T031), `CMT-2026-09-002` (Diana, 2026-09-15, WS-03/T011). Sources: `SRC-CU-CIPH-41`, `SRC-CU-CIPH-43`, `SRC-SLACK-44` (2026-08-16 merge thread), `SRC-SLACK-48` (2026-08-17 hotspots), `SRC-SLACK-43` (2026-08-18 reopen), `SRC-MEET-06` (2026-08-19 profiler blocker), `SRC-SLACK-49` (2026-08-21 tracemalloc), `SRC-GDOC-42` (DOC-2042 design review), `SRC-GDOC-44` (DOC-2044 profiling report), `SRC-GDOC-27` (DOC-2027 hotspot identification review).
