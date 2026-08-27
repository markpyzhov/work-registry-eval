# As of **2026-09-22**, which CipherDoc tasks are blocked, and for each is the block upstream/external or internal? State the root cause and the listed task assignee.

<!-- RESPONSE_START -->

As of 2026-09-22, CipherDoc has five tasks in **Blocked** status:

| Task | Assignee | Block type | Root cause |
|---|---|---|---|
| CIPH-17 — Fix Coordinate/Offset Drift in Multi-Page PDFs | Charlie | Upstream/external | `pdfminer.six` whitespace-handling issue; upstream PR #992 remains unmerged and the team rejected maintaining a local fork. *(SRC-CU-CIPH-17)* |
| CIPH-29 — Offline auth with key rotation for air-gapped installs | Diana | Internal | The designed key-rotation flow requires a network connection to complete its handshake, so it cannot work in a fully air-gapped deployment. *(SRC-CU-CIPH-29; SRC-SLACK-17)* |
| CIPH-34 — Authenticated handshake for multi-site node sync | Bob | Internal | The handshake times out under high-latency conditions; no workable fix or timeout-bump workaround was accepted, and resolution remains tied to the encryption/handshake design path. *(SRC-CU-CIPH-34; SRC-MEET-11)* |
| CIPH-46 — Correct high-DPI PDF coordinate scaling | Charlie | Upstream/external | A scaling-math defect was traced to the upstream rendering library (`pdf-lib-core`); there is no local fix available. *(SRC-CU-CIPH-46; SRC-SLACK-58)* |
| CIPH-47 — Async job scheduler for concurrent batch API work | Bob | Internal | Concurrent writes to the shared results manifest create an I/O race, corrupting/retrying writes and causing roughly a 10% throughput regression. *(SRC-CU-CIPH-47; SRC-GDOC-50)* |
