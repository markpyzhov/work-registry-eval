# As of **2026-09-22**, which CipherDoc tasks are blocked, and for each is the block upstream/external or internal? State the root cause and the listed task assignee.

<!-- RESPONSE_START -->

As of **2026-09-22**, five CipherDoc (CIPH) tasks carry **Status: Blocked** in the source records. Two are blocked externally (upstream libraries), three are blocked internally (own design/implementation defects).

---

## Upstream / external blocks

**CIPH-17 — Fix Coordinate/Offset Drift in Multi-Page PDFs**
- **Assignee (listed):** Charlie · Priority: High · Created 2026-06-19
- **Root cause:** Coordinate/offset drift traced to a whitespace-handling defect in the upstream `pdfminer.six` parser. The fix lives in upstream issue/PR **#992**, which remains unmerged with no maintainer movement. Maintaining a local fork was evaluated on 2026-08-20 and **rejected** as long-term maintenance risk, so no local workaround was adopted; last re-check 2026-09-10 confirmed #992 still unmerged.
- **Block type:** Upstream/external (third-party library, waiting on maintainers).

**CIPH-46 — Correct high-DPI PDF coordinate scaling**
- **Assignee (listed):** Charlie · Priority: Normal · Created 2026-08-15; blocked 2026-09-10 by Diana
- **Root cause:** Redaction masks misalign on high-DPI displays (reproduces at 150% and 200% scale, not at 100%). Charlie's scaling/rotation fix works for simple documents but breaks on nested Form XObjects; the defect is a known bug in the upstream rendering library **`pdf-lib-core`** in how it handles XObject coordinates under a parent transform. It sits in that library's C++ core — not locally patchable. An issue was opened upstream with no response. Flattening PDFs was floated as a workaround and rejected (file-size blowup, potential loss of text layers).
- **Block type:** Upstream/external. Still listed as an open upstream block in the 2026-09-15 pre-release audit.

---

## Internal blocks

**CIPH-34 — Authenticated handshake for multi-site node sync**
- **Assignee (listed):** Bob · Priority: High · Created 2026-08-04; blocked 2026-09-22 by Diana
- **Root cause:** The authenticated node-replication handshake passes at nominal LAN latency but **times out and never completes over a simulated high-latency link**, degrading as the link slows. Bob attributes it to the internally added AES-256 output-path pipeline adding per-packet overhead, pushing the exchange past the timeout window; the prototype assumed fast round trips. The team explicitly refused a timeout bump as a workaround ("bumping timeouts just hides it") and left it blocked pending movement on the encryption path.
- **Block type:** Internal (own handshake design + own encryption pipeline). Note the high-latency network is the test condition, not an external dependency.

**CIPH-47 — Async job scheduler for concurrent batch API work**
- **Assignee (listed):** Bob · Priority: Normal · Created 2026-08-18; blocked 2026-08-25 by Diana
- **Root cause:** A **concurrent I/O race** in the team's own code: async workers finish out of order and append concurrently to the same shared results manifest, interleaving writes and corrupting the JSON. Workers then retry/serialize around the corrupted-write recovery path, cutting batch throughput by roughly **10%** versus the sync baseline instead of delivering the expected async speedup. The race surfaces when the new async workers share I/O with the existing internal multi-threaded worker pool (T026). Alice halted the work: "A 10% hit is not shippable."
- **Block type:** Internal (own concurrency/manifest-serialization defect).

**CIPH-29 — Offline auth with key rotation for air-gapped installs**
- **Assignee (listed):** Diana · Priority: High · Created 2026-08-01; blocked 2026-08-05 by Alice
- **Root cause:** Testing against Bob's local auth mock (network disabled, simulating a real air-gapped site) showed **key rotation cannot complete without network access** — the designed rotation flow assumes at least a brief connection to finish the handshake. No resolution has been found; the team parked it pending a decision on whether to redesign the flow or relax the offline requirement.
- **Block type:** Internal (own design assumption fails the product's own air-gapped requirement). No third party is being waited on.

---

## Summary table

| Task | Title | Assignee | Block type | Root cause |
|---|---|---|---|---|
| CIPH-17 | Coordinate/offset drift, multi-page PDFs | Charlie | **Upstream/external** | `pdfminer.six` whitespace bug; PR #992 unmerged; fork rejected |
| CIPH-46 | High-DPI PDF coordinate scaling | Charlie | **Upstream/external** | `pdf-lib-core` XObject-transform bug in its C++ core; upstream unresponsive |
| CIPH-34 | Authenticated handshake, multi-site node sync | Bob | **Internal** | Handshake times out under high latency; AES-256 per-packet overhead exceeds timeout budget |
| CIPH-47 | Async job scheduler, batch API | Bob | **Internal** | Concurrent I/O race on shared results manifest; ~10% throughput regression |
| CIPH-29 | Offline auth with key rotation (air-gapped) | Diana | **Internal** | Rotation flow requires a network connection it cannot have offline |

**Split: 2 external (both Charlie, both PDF-library defects), 3 internal (Bob ×2, Diana ×1).**

Two related items are commonly confused with these but are **not** in Blocked status and so are excluded: **CIPH-39** (Windows code-signing certificate missing — status *Active*, and its blocker is a procurement gap, externally-sourced but internally owned) and **CIPH-21** (Release v1.0 Gates — status *Active*, holding on the Docker slim-down/CVE and Windows signing gates).

**Sources cited:** SRC-CU-CIPH-17, SRC-CU-CIPH-29, SRC-CU-CIPH-34, SRC-CU-CIPH-46, SRC-CU-CIPH-47 (ClickUp task records); SRC-GDOC-49 (DOC-2049, High-DPI upstream block), SRC-GDOC-50 (DOC-2050, async batch queue review), SRC-GDOC-13 (DOC-2013, offline key-rotation design), SRC-GDOC-18/SRC-GDOC-38 (handshake prototype notes); SRC-SLACK-07 (upstream PDF library), SRC-SLACK-58 (high-DPI upstream block), SRC-SLACK-61 (async batch I/O race), SRC-SLACK-27 (handshake validation), SRC-SLACK-17 (offline auth mock/rotation block); SRC-MEET-11 (2026-09-22 handshake deep dive), SRC-MEET-10 (2026-09-15 pre-release audit).
