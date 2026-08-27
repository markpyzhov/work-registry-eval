# As of **2026-09-22**, which CipherDoc tasks are blocked, and for each is the block upstream/external or internal? State the root cause and the listed task assignee.

<!-- RESPONSE_START -->

I have everything needed. Here is the complete answer.

---

**Blocked CipherDoc tasks as of 2026-09-22 (per the Work State Index, as-of 2026-09-22T12:00:00Z, and the individual Work States, all last updated 2026-09-22)**

Five tasks are Blocked: **T007/CIPH-17, T019/CIPH-29, T024/CIPH-34, T036/CIPH-46, T037/CIPH-47**. Two of the five (T007, T036) are upstream/external blocks; the other three (T019, T024, T037) are internal.

---

**1. T007 / CIPH-17 — Fix coordinate/offset drift in multi-page PDFs (WS-01, Detection and Redaction Engine)**
- **Nature of block: Upstream/external**, plus an added external Legal gate.
- **Root cause:** Redaction masks fail to line up with target text across multi-page PDFs. Debugging traced the drift to a **whitespace-handling defect in the upstream `pdfminer.six` library**, tracked as upstream Issue/PR **#992**, which remains unmerged. Charlie monitored the repo through August and evaluated a local fork in late August, but the team **rejected maintaining a parser fork** due to long-term maintenance risk; as of September 10 no safe local workaround exists. A maintainer DM indicates #992 will land **mid-October at the earliest**, and any pre-normalization workaround would additionally require **written Legal sign-off** on top of the upstream merge (CMT-2026-06-003).
- **Listed assignee:** **Charlie** (Priority: High; opened 2026-06-19 by Bob).

**2. T019 / CIPH-29 — Offline-mode authentication with key rotation for air-gapped installs (WS-04, Regulatory Compliance, Privacy, and Audits)**
- **Nature of block: Internal** (own design/architecture limitation; no third-party dependency).
- **Root cause:** The designed key-rotation flow assumes at least a brief network connection to finish the handshake, so **rotation cannot complete in a strictly air-gapped environment without a centralized authority**. Bob built a local auth mock on 2026-08-04 and ran rotation with networking disabled; on 2026-08-05 it failed to complete, and Alice recorded the block. InfoSec has since approved a **split master-key escrow design (USB token at the clinic + HQ HSM)** and Bob is spiking the implementation, so the air-gapped rotation path now has an approved architecture rather than an open question — but the task **remains blocked until that escrow implementation is built** (CMT-2026-08-001).
- **Listed assignee:** **Diana** (Priority: High; opened 2026-08-01 by Alice).

**3. T024 / CIPH-34 — Authenticated handshake for multi-site Zero-Trust node sync (WS-07, Data Persistence, Encryption, and Secure Storage)**
- **Nature of block: Internal** (own protocol behavior under network conditions; not a third-party or vendor dependency).
- **Root cause:** The authenticated node-replication handshake **times out under high-latency network conditions**. The prototype (2026-08-06) completed reliably on a single LAN segment at nominal round-trip latency, but validation across realistic multi-site latency/jitter failed with timeouts. Diana recorded the block on 2026-09-22. The fix depends on the already-completed encryption work (T021/CIPH-31), but remains unresolved; a high-latency handshake retest plan is the listed next update needed.
- **Listed assignee:** **Bob** (Priority: High; opened 2026-08-04 by Alice).

**4. T036 / CIPH-46 — Fix High-DPI PDF rendering coordinate alignment (WS-06, External Interfaces and Platform Compatibility)**
- **Nature of block: Upstream/external.**
- **Root cause:** Redaction overlay coordinates drift from the actual text region on high-DPI displays — **5–10 pixels on 4K displays at 200% scaling**, with the offset growing as scale factor increases (reproduced at 150% and 200%; does not reproduce at 100%). The scaling-math error was traced on 2026-09-10 to a **defect in the upstream rendering library's scaling math**, with **no safe local fix identified**. It cannot clear the gate until upstream scaling is corrected or an accepted local remediation is chosen. A separate scoping note adds that **12% of the MedFirst pilot corpus fails due to nested Form XObjects**, a failure mode beyond upstream 4K scaling alone (CMT-2026-09-001).
- **Listed assignee:** **Charlie** (Priority: Normal; opened 2026-08-15 by Alice; blocked by Diana 2026-09-10).

**5. T037 / CIPH-47 — Implement async batch API scheduler (WS-05, Performance Benchmarking and System Optimization)**
- **Nature of block: Internal.**
- **Root cause:** A **concurrent I/O race on the shared results manifest**. Because documents vary in size, async workers finish out of order; when multiple workers append to the same results manifest concurrently, writes interleave and can **corrupt the JSON structure**. Concurrency testing on 2026-08-25 confirmed the race is real, not theoretical: workers retry/serialize around the corrupted-write recovery path, **cutting batch throughput by roughly 10%** versus the expected async speedup. The manifest-write race must be resolved — tied to how the completed T026/CIPH-36 multi-threaded worker pool serializes result writing — before the async scheduler can be considered production-ready.
- **Listed assignee:** **Bob** (Priority: Normal; opened 2026-08-18 by Alice; blocked by Diana 2026-08-25).

---

**Summary table**

| Task | Title | Block type | Root cause | Assignee |
|---|---|---|---|---|
| T007 / CIPH-17 | Fix coordinate/offset drift in multi-page PDFs | Upstream/external (+ Legal gate) | Whitespace-handling bug in upstream `pdfminer.six`; PR #992 unmerged, fork rejected | Charlie |
| T019 / CIPH-29 | Offline auth with key rotation (air-gapped) | Internal | Rotation flow needs a network handshake; impossible air-gapped without central authority; escrow design approved but not built | Diana |
| T024 / CIPH-34 | Authenticated handshake for multi-site node sync | Internal | Handshake times out under high-latency networks (worked only at nominal LAN latency) | Bob |
| T036 / CIPH-46 | Fix High-DPI PDF rendering coordinate alignment | Upstream/external | Defect in upstream rendering library's scaling math; 5–10px drift at 4K/200%; no safe local fix | Charlie |
| T037 / CIPH-47 | Implement async batch API scheduler | Internal | Concurrent manifest-write race corrupts JSON and cuts throughput ~10% | Bob |

**Note on a near-miss:** T029/CIPH-39 (Windows OS compatibility) is **not** listed as Blocked — it is **Active**, "held on code-signing" pending an Authenticode certificate. The work state explicitly characterizes that signing gap as a procurement dependency, not an engineering block. Also excluded: T030/CIPH-40 (License Compliance Review) carries a hard Legal P0 gate but is listed as Active/Reopened rather than Blocked.

**Dataset records cited:** `work-states/index.md`; `work-states/WS-01-engine.md`; `work-states/WS-04-policy.md`; `work-states/WS-05-performance.md`; `work-states/WS-06-platforms.md`; `work-states/WS-07-storage.md`; `work-states/comments/2026-08.md` (CMT-2026-08-001); `med-synth/tasks/CIPH-17-Fix-Offset-Mismatch.md`; `med-synth/tasks/CIPH-29-Offline-Mode-Authentication.md`; `med-synth/tasks/CIPH-34-Zero-Trust-Node-Sync.md`; `med-synth/tasks/CIPH-46-High-DPI-PDF-Rendering-Fixes.md`; `med-synth/tasks/CIPH-47-Async-Batch-Processing.md`; `med-synth/communication/sources/slack/2026-08-04-offline-auth-mock-block.md`; `med-synth/documentation/sources/2026-09-04-Async-Batch-Processing-Queue-Review.md`; `med-synth/documentation/sources/2026-09-10-High-DPI-PDF-Rendering-Coordinates-Report.md`; `med-synth/documentation/sources/2026-08-15-Zero-Trust-Node-Sync-Review.md`.
