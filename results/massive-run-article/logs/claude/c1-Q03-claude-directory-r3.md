# Large-file chunking was merged in mid-August. As of **2026-09-22**, has that completion held? Reconstruct the completion → reopen timeline, the technical root cause, and who owns the next engineering action.

<!-- RESPONSE_START -->

## Answer: No — the completion did not hold, and as of 2026-09-22 T031/CIPH-41 is still open

The mid-August merge was declared done, reversed two days later, and has never been re-closed. The authoritative Work State for 2026-09-22 still carries it as unfinished.

### Current status as of 2026-09-22

- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/index.md` — as-of `2026-09-22T12:00:00Z`; lists **T031 (large-file memory leak)** under "Active / Reopened."
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-05-performance.md` — T031 checkbox unchecked; Active Work: *"Reopened/active. Initial chunking landed but Bob found severe memory leaks on files exceeding 2GB during long batch runs. Charlie is refactoring stream buffer release logic."* "Next Update Needed: T031 stream buffer refactor."
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-41-Large-File-Chunking.md` — **Status: Active (Reopened)**, **Assignee: Charlie**.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md` — under blockers: *"T031 — MedFirst pilot OOM still release-coupled."*

### Completion → reopen timeline

| Date | Event | File |
|---|---|---|
| 2026-08-12 | CIPH-41 opened by Alice for multi-GB PDF chunking | `med-synth/tasks/CIPH-41-Large-File-Chunking.md` |
| 2026-08-14 | Charlie starts stream-based chunked reads; adds an overlap window for entities spanning chunk boundaries | `med-synth/communication/sources/slack/2026-08-14-large-file-chunking.md` (SRC-SLACK-42) |
| 2026-08-14 | Design note DOC-2025 documents the "Stream-and-Split" layer (100-page blocks → sub-documents → re-merge); flags a **pending 10,000-page stress test** on the re-merge step and a known trade-off that cross-page regex matches break | `med-synth/documentation/sources/2026-08-14-Large-File-Chunking-Review.md` (SRC-GDOC-25) |
| **2026-08-16 09:19** | **Charlie merges stream chunking to mainline: "Calling this done."** Bob asks if memory concerns are fully clean; Charlie: *"As far as testing showed, clean. We'll see if anything shows up on longer runs."* | `med-synth/communication/sources/slack/2026-08-16-large-file-chunking-merge.md` (SRC-SLACK-44) |
| **2026-08-18 10:30** | **Bob reopens** — files over 2GB still leak on long-running batches. Bob: *"something else is holding a reference."* Diana reproduces in QA; process gets OOM-killed on larger inputs | `med-synth/communication/sources/slack/2026-08-18-large-file-chunking-reopen.md` (SRC-SLACK-43) |
| 2026-08-18 | Bob files CMT-2026-08-003: MedFirst pilot hit OOM on a **4.7GB PDF with 8GB RAM** on a clinic workstation → escalated to **pilot-blocker, explicitly tied to the T011 release gate** | `work-states/comments/2026-08.md` |
| 2026-08-19 | Leak profiling stalls: the licensed profiler can't reach its license server on the air-gapped lab box; team pivots to stdlib tooling | `med-synth/communication/sources/fireflies/2026-08-19-Memory-Leak-Profiling-Blocker.md` (SRC-MEET-06) |
| 2026-08-20 | Charlie posts root cause and logs a ClickUp "Buffer Release Refactor" activity; confirms release will be **eager, per chunk** — *"Still working through it, not ready to call it done again yet."* Diana asks for a build to re-run the stress case | SRC-SLACK-44; `med-synth/tasks/CIPH-41-Large-File-Chunking.md` |
| 2026-08-21→23 | Adjacent CIPH-43 work: `tracemalloc` finds `RedactionEngine` retaining the full page-tree after document close; Bob's PR #84 merged, 6-hour soak flat. Bob: *"Same family of fix — builds on the chunking buffer-release work."* | `med-synth/communication/sources/slack/2026-08-21-memory-leak-tracemalloc.md` (SRC-SLACK-49); `med-synth/documentation/sources/2026-08-23-Memory-Leak-Profiling-Report.md`; `2026-08-27-Memory-Leak-Profiling-Review.md` |
| 2026-08-23 | Design review DOC-2042: fix shows flat memory on a 2.3GB local sample, but **not yet validated against the full large-file test corpus** | `med-synth/documentation/sources/2026-08-23-Large-File-Chunking-Design-Review.md` (SRC-GDOC-42) |
| 2026-09-02 / 09-15 / 09-22 | T031 carried forward in every brief as an open MedFirst pilot-blocker on the release-critical path | `briefs/2026-09-02-…`, `2026-09-15-…`, `2026-09-22-daily-brief.md` |

### Technical root cause

The chunking *mechanism* was correct and remains merged; the defect was in lifetime management of the per-chunk buffers.

- Buffers allocated for each chunk were **not explicitly released once a worker moved past them** — they stayed reachable because something still held a reference, so garbage collection never reclaimed them (SRC-SLACK-44, 2026-08-20; SRC-SLACK-43).
- Consequence: **peak memory climbed roughly linearly with file size instead of staying bounded by chunk size**, defeating the entire point of chunking on the largest files (SRC-GDOC-42).
- The specific retained reference identified via `tracemalloc` was the full page-tree held in `RedactionEngine` after the document object was closed — the context manager closed the file handle but never dropped the page-tree reference (SRC-SLACK-49). That loader-side leak was patched under CIPH-43 (PR #84) and verified; the 2026-08-23 profiling report is explicit that it is **distinct from, and dependent on, the T031 buffer-release issue**, so CIPH-43 closing does not close CIPH-41.
- The in-progress fix is a refactor of the stream-chunk handler to **release each chunk's buffer eagerly, immediately after processing**, rather than relying on scope exit (SRC-SLACK-44; SRC-GDOC-42; CIPH-41 activity history).

Two secondary risks from the original design note remain unretired in the evidence: the re-merge step itself consumes RAM and the 10,000-page stress test was never recorded as run, and chunking breaks regex matches spanning a page boundary (context-awareness traded for memory stability) — SRC-GDOC-25.

### Ownership of the next engineering action

- **Charlie (Engine)** owns it. He is the CIPH-41 assignee, logged the 2026-08-20 Buffer Release Refactor activity, and is named in WS-05 Active Work as the person refactoring stream buffer release. WS-05's "Next Update Needed" is the **T031 stream buffer refactor**, and its acceptance bar is CIPH-41's criterion: buffers released after each chunk with **no leak on files 2GB and larger**.
- **Diana (QA)** holds the verification step — she asked to be told when a build exists to re-run the stress case (SRC-SLACK-44, 2026-08-20) and the fix is still unvalidated against the full large-file corpus (SRC-GDOC-42).
- **Bob** is the reporter/escalation owner (SRC-SLACK-43, CMT-2026-08-003); closure must additionally prove buffer release **on clinic hardware** — the 4.7GB-on-8GB MedFirst scenario — because T031 is coupled to the T011 release gate (`briefs/2026-09-02-daily-brief.md`, `briefs/2026-09-22-daily-brief.md`).

**Bottom line:** the 2026-08-16 "done" was premature and was retracted on 2026-08-18. Five weeks later the chunking implementation is still merged and in place, but the per-chunk buffer-release fix that makes it actually work on 2GB+ files is unfinished and unverified, and it remains a release-coupled pilot-blocker owned by Charlie.
