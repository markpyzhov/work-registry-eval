# Large-file chunking was merged in mid-August. As of **2026-09-22**, has that completion held? Reconstruct the completion → reopen timeline, the technical root cause, and who owns the next engineering action.

<!-- RESPONSE_START -->

I have everything needed.

## Short answer

**No — the completion did not hold.** As of the 2026-09-22 as-of timestamp, large-file chunking (**T031 / CIPH-41**) is **Active (Reopened)**, not done. **Charlie** owns the next engineering action: the per-chunk buffer-release refactor, which is still unverified against the full large-file test corpus.

---

## 1. Completion → reopen timeline

| Date | Event | Evidence |
|---|---|---|
| 2026-08-12 | Alice opens CIPH-41 ("Stream-chunk multi-GB PDF loads without retaining buffers") | `/c1/med-synth/tasks/CIPH-41-Large-File-Chunking.md` |
| 2026-08-14 | Charlie starts stream-based chunked reads; adds an overlap window between chunks so entities spanning a boundary aren't missed | `/c1/med-synth/communication/sources/slack/2026-08-14-large-file-chunking.md` |
| 2026-08-14 | Design note records the "Stream-and-Split" layer (100-page blocks → temp sub-docs → worker pool → re-merge) and flags a *pending* 10,000-page stress test on the re-merge step | `/c1/med-synth/documentation/sources/2026-08-14-Large-File-Chunking-Review.md` |
| **2026-08-16 09:19** | **Charlie merges stream chunking to mainline and "calls this done."** Asked by Bob whether the memory concerns were fully clean, Charlie hedges: clean "as far as testing showed… we'll see if anything shows up on longer runs" | `/c1/med-synth/communication/sources/slack/2026-08-16-large-file-chunking-merge.md` |
| 2026-08-17 | Independent leak signal: Bob sees a long-running container hit its memory limit after ~4h; Diana confirms a steady RSS climb on staging; Evan raises the container limit to 2GB as a stopgap | `/c1/med-synth/communication/sources/slack/2026-08-17-memory-leak-hotspots.md` |
| **2026-08-18 10:30** | **Bob reopens.** On long-running batches with files over 2GB, memory still leaks despite the chunked-read path. He notes it is *not* the page buffers themselves — "something else is holding a reference." Diana reproduces in QA (process eventually killed). Charlie: "Reopening this until we find it." | `/c1/med-synth/communication/sources/slack/2026-08-18-large-file-chunking-reopen.md` |
| 2026-08-18 | Bob files CMT-2026-08-003 (correction): MedFirst pilot hit **OOM on a 4.7GB PDF with 8GB RAM** on a clinic workstation → **pilot-blocker**, prioritized ahead of nice-to-have perf work and tied explicitly to the **T011 release gate** | `/c1/work-states/comments/2026-08.md` |
| 2026-08-19 | Daily brief records T031 reopened with MedFirst OOM context | `/c1/briefs/2026-08-19-daily-brief.md` |
| **2026-08-20** | Charlie posts root cause and starts the fix: chunk buffers were not explicitly released once a worker moved past them. Fix releases **eagerly, right after each chunk** — explicitly *not* ready to call done again. Diana asks for a build to re-run the stress case | `/c1/med-synth/communication/sources/slack/2026-08-16-large-file-chunking-merge.md` (thread ran to 2026-08-20); CIPH-41 activity history |
| 2026-08-23 | Post-merge design review: peak memory climbed roughly **linearly with file size** instead of staying bounded by chunk size. Early local test on a 2.3GB sample shows flat memory, but **not validated against the full large-file test corpus** | `/c1/med-synth/documentation/sources/2026-08-23-Large-File-Chunking-Design-Review.md` |
| 2026-09-02 / 09-15 / 09-22 | T031 continuously carried as an open, release-coupled blocker; the 2026-09-22 brief lists "T031 — MedFirst pilot OOM still release-coupled" under Blockers | `/c1/briefs/2026-09-02-daily-brief.md`, `/c1/briefs/2026-09-15-daily-brief.md`, `/c1/briefs/2026-09-22-daily-brief.md` |
| **As of 2026-09-22** | Authoritative state: `T031` unchecked; "**Reopened/active**"; index lists T031 under Active/Reopened as "large-file memory leak" | `/c1/work-states/WS-05-performance.md`, `/c1/work-states/index.md` |

Note the completion claim survived only **two days** (merged 08-16, reopened 08-18) — and there is no record anywhere in the package of it being closed again in the ~5 weeks since.

## 2. Technical root cause

The chunking *mechanism* was correct and remains merged; the defect was in lifetime management of the per-chunk buffers.

- **Stated root cause (Charlie, 2026-08-20):** chunk buffers were **not explicitly released** once a worker moved past them — the code relied on them falling out of scope rather than releasing them deterministically. Something upstream retained a live reference, so the allocations stayed reachable and were never freed.
- **Symptom shape:** peak memory grew **roughly linearly with file size** instead of staying bounded by chunk size, which "defeated the point of chunking for the largest files" (2026-08-23 design review). Manifested as steady RSS climb over long batch runs and eventual OOM-kill on 2GB+ inputs.
- **Corroborating profiling evidence:** with the licensed profiler unusable on the air-gapped lab box, the team switched to stdlib `tracemalloc`. Tracing a chunked large-file run pointed at the **PDF loader's page-buffer handling** — buffers staying reachable across chunk boundaries (`/c1/med-synth/documentation/sources/2026-08-27-Memory-Leak-Profiling-Review.md`). The specific retention found was the full **page-tree held in `RedactionEngine` even after the document object was closed** (`/c1/med-synth/communication/sources/slack/2026-08-21-memory-leak-tracemalloc.md`).
- **The fix in flight:** refactor the stream-chunk handler to explicitly release each chunk's buffer immediately after that chunk is processed. A 2.3GB local sample shows flat memory across chunks — but this has **not** been validated end-to-end against the full large-file corpus.

**Important distinction — two related but separate items:**
- **T033 / CIPH-43** (Memory Leak Profiling, assignee **Bob**) is **Completed**: Bob's PR #84 added explicit cleanup so the context manager releases the page-tree reference rather than just closing the file handle; Diana's 6-hour soak showed flat memory. Bob described it as "same family of fix — builds on the chunking buffer-release work."
- **T031 / CIPH-41** (Large-File Chunking, assignee **Charlie**) is **still open**. The completed loader-leak patch did **not** close the chunking task. Anyone reading only CIPH-43 or the 2026-08-23 soak-test result could wrongly conclude the large-file leak is resolved.

## 3. Who owns the next engineering action

- **Owner of the next engineering action: Charlie** — assignee of record on CIPH-41, and the person doing the stream **buffer-release refactor** (per-chunk eager release). CIPH-41's own activity history ends at Charlie's 2026-08-20 "Buffer Release Refactor" entry with status Active (Reopened); WS-05 states "Charlie is refactoring stream buffer release logic," and the "Next Update Needed" field names "T031 stream buffer refactor."
- **Verification gate: Diana (QA)** — she has an open standing ask for a build to re-run the 2GB+ stress case, and the 2026-08-23 review confirms the fix is not yet validated against the full large-file test corpus.
- **Escalation / prioritization: Bob** raised the pilot-blocker correction; **Alice (PM)** carries the T011 release-gate coupling. WS-05 area ownership is listed as **Charlie / Bob**.
- **Acceptance criteria still unmet:** "Memory buffers are released after each chunk, with no leak on files 2GB and larger."

## Caveats worth flagging

1. The 2026-08-14 design note lists an *unresolved* secondary risk that no later record closes: the **post-processing re-merge step also uses RAM**, and the planned 10,000-page stress test to confirm it doesn't re-introduce OOM is still marked *Pending*. Nothing in the package reports that test being run.
2. The same note records an accepted trade-off that is separate from the leak: chunking **breaks regex matches that span a page/chunk boundary** ("trading context-awareness for memory stability"), only partly mitigated by Charlie's overlap window.
3. The last substantive engineering activity on T031 in this package is **2026-08-23**. Every September reference (briefs 09-02, 09-15, 09-22) restates it as an open, release-coupled blocker without new technical progress — so the item has been carried roughly a month without a recorded status change.

### Files cited
- `/c1/work-states/WS-05-performance.md` (authoritative as-of state)
- `/c1/work-states/index.md`
- `/c1/work-states/comments/2026-08.md` (CMT-2026-08-003)
- `/c1/med-synth/tasks/CIPH-41-Large-File-Chunking.md`
- `/c1/med-synth/tasks/CIPH-43-Memory-Leak-Profiling.md`
- `/c1/med-synth/communication/sources/slack/2026-08-14-large-file-chunking.md`
- `/c1/med-synth/communication/sources/slack/2026-08-16-large-file-chunking-merge.md`
- `/c1/med-synth/communication/sources/slack/2026-08-17-memory-leak-hotspots.md`
- `/c1/med-synth/communication/sources/slack/2026-08-18-large-file-chunking-reopen.md`
- `/c1/med-synth/communication/sources/slack/2026-08-21-memory-leak-tracemalloc.md`
- `/c1/med-synth/communication/sources/fireflies/2026-08-19-Memory-Leak-Profiling-Blocker.md`
- `/c1/med-synth/documentation/sources/2026-08-14-Large-File-Chunking-Review.md`
- `/c1/med-synth/documentation/sources/2026-08-23-Large-File-Chunking-Design-Review.md`
- `/c1/med-synth/documentation/sources/2026-08-27-Memory-Leak-Profiling-Review.md`
- `/c1/briefs/2026-08-19-daily-brief.md`, `/c1/briefs/2026-09-02-daily-brief.md`, `/c1/briefs/2026-09-15-daily-brief.md`, `/c1/briefs/2026-09-22-daily-brief.md`
