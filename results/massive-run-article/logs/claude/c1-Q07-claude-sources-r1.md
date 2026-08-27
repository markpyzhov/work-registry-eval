# As of **2026-09-22**, which CipherDoc tasks are blocked, and for each is the block upstream/external or internal? State the root cause and the listed task assignee.

<!-- RESPONSE_START -->

## Blocked CipherDoc tasks as of 2026-09-22

Five CipherDoc (CIPH) tasks carry status **Blocked**. Two are blocked by **upstream/external** dependencies; three are **internal** engineering blocks.

### Upstream / external blocks (2)

**CIPH-17 — Fix Coordinate/Offset Drift in Multi-Page PDFs**
- **Assignee:** Charlie (Priority: High, created 2026-06-19)
- **Block type:** Upstream/external
- **Root cause:** Redaction masks do not line up with target text across multi-page PDFs. Debugging traced the drift to a whitespace-handling defect in the third-party `pdfminer.six` parser (non-breaking spaces appearing in extracted text; on dense pages roughly half the spans misalign). The fix sits in upstream issue/PR **#992**, which remains unmerged with no maintainer movement as of the 2026-09-10 check. Maintaining a local fork of the parser was explicitly evaluated and rejected as too much long-term maintenance risk, so the team chose to stay blocked pending upstream merge with no local workaround adopted. Alice flagged this as a real risk to the v1.0 timeline; Charlie's position was that eating the delay beats owning a parser fork.
- *Sources:* SRC-CU-CIPH-17; SRC-SLACK-07 (#cipherdoc, 2026-06-26 → 2026-09-10); SRC-SLACK-05 (2026-06-23)

**CIPH-46 — Correct high-DPI PDF coordinate scaling**
- **Assignee:** Charlie (Priority: Normal, created 2026-08-15; blocked 2026-09-10 by Diana)
- **Block type:** Upstream/external
- **Root cause:** Coordinate misalignment on high-DPI displays (reproduces at 150% and 200% scale, not at 100%; offset grows with scale factor). Charlie's scaling-math and page-rotation fixes handled simple cases, but break on documents with nested Form XObjects. The remaining defect is a known bug in the upstream rendering library (`pdf-lib-core`) in how it handles XObject coordinates when a parent transform is applied — it is deep in the library's C++ core and cannot be patched locally. Charlie opened an upstream issue; maintainers have not responded. A PDF-flattening workaround was floated and rejected (file-size blowup, possible loss of text layers). Team decision on 2026-09-10 was to leave it blocked and document it as a known issue affecting a small subset of complex documents, pending a decision on whether to ship with the limitation or swap rendering libraries.
- *Sources:* SRC-CU-CIPH-46; SRC-GDOC-49 (DOC-2049, 2026-09-10); SRC-SLACK-58 (2026-09-10); SRC-GDOC-30 (DOC-2030); SRC-SLACK-56/57

### Internal blocks (3)

**CIPH-34 — Authenticated handshake for multi-site node sync**
- **Assignee:** Bob (Priority: High, created 2026-08-04; blocked 2026-09-22 by Diana)
- **Block type:** Internal (own encryption workstream / handshake design)
- **Root cause:** The zero-trust node-replication handshake passed nominal-latency validation on a single LAN segment (2026-08-08, no failures), but on a simulated high-latency link it **times out and never completes the exchange**, degrading further as the link slows. Diagnosis: the internally-added AES-256 output-path pipeline adds per-packet overhead that pushes the exchange past the timeout window on slow links. In the 2026-09-22 handshake deep-dive, the team explicitly rejected bumping timeouts as a workaround ("bumping timeouts just hides it") and left the work blocked, dependent on the internal encryption path settling before retest. Diana kept the high-latency repro in place for re-checking.
- *Sources:* SRC-CU-CIPH-34; SRC-MEET-11 (Fireflies, 2026-09-22); SRC-SLACK-27 (2026-08-08 → 2026-09-22); SRC-GDOC-18/38

**CIPH-47 — Async job scheduler for concurrent batch API work**
- **Assignee:** Bob (Priority: Normal, created 2026-08-18; blocked 2026-08-25 by Diana)
- **Block type:** Internal (own multi-threaded worker pool)
- **Root cause:** A concurrent I/O race between the new async workers and the existing internal multi-threaded batch worker pool. Because documents vary in size, workers finish out of order and interleave appends to the same shared results manifest, corrupting the JSON structure; workers then retry/serialize around the corrupted-write recovery path, cutting batch throughput by roughly **10%** versus the sync baseline instead of delivering the expected async speedup. Alice halted the work on 2026-08-25 ("a 10% hit is not shippable"); resolution depends on how the worker pool's result-writing gets serialized.
- *Sources:* SRC-CU-CIPH-47; SRC-GDOC-50 (DOC-2050); SRC-SLACK-61 (2026-08-25); SRC-SLACK-59

**CIPH-29 — Offline auth with key rotation for air-gapped installs**
- **Assignee:** Diana (Priority: High, created 2026-08-01; blocked 2026-08-05 by Alice)
- **Block type:** Internal (own design assumption)
- **Root cause:** The key-rotation flow Diana designed assumes at least a brief network connection to finish the handshake, which contradicts the air-gapped requirement. Bob's local auth mock, run with the network disabled, confirmed rotation **cannot complete offline**. No resolution has been found for rotating a key with no network at all. Alice left it blocked pending a regroup on whether the design changes or the offline requirement is relaxed.
- *Sources:* SRC-CU-CIPH-29; SRC-SLACK-17 (2026-08-04 → 2026-08-05); SRC-SLACK-16 (2026-08-02); SRC-GDOC-13 (DOC-2013)

### Summary table

| Task | Title | Assignee | Block type | Root cause |
|---|---|---|---|---|
| CIPH-17 | Coordinate/offset drift, multi-page PDFs | Charlie | Upstream/external | `pdfminer.six` whitespace handling; PR #992 unmerged; fork rejected |
| CIPH-46 | High-DPI PDF coordinate scaling | Charlie | Upstream/external | `pdf-lib-core` XObject coordinate bug under parent transform; unpatchable locally |
| CIPH-34 | Authenticated handshake, multi-site node sync | Bob | Internal | AES-256 per-packet overhead pushes handshake past timeout on high-latency links |
| CIPH-47 | Async job scheduler, batch API | Bob | Internal | Concurrent I/O race with multi-thread pool corrupts shared manifest; ~10% throughput loss |
| CIPH-29 | Offline auth with key rotation | Diana | Internal | Rotation design requires brief network connectivity; impossible air-gapped |

**Note on adjacent items (not counted as Blocked):** CIPH-39 (Windows Defender/SmartScreen blocking the unsigned build, missing code-signing certificate — an external dependency) and CIPH-21 (Release v1.0 Gates, held on the Docker CVE and Windows signing gates) both carry status **Active**, not Blocked, and are assigned to Evan. CIPH-38 was briefly blocked on bare-metal environment provisioning but is now Completed.
