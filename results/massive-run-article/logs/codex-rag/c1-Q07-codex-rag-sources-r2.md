# As of **2026-09-22**, which CipherDoc tasks are blocked, and for each is the block upstream/external or internal? State the root cause and the listed task assignee.

<!-- RESPONSE_START -->

As of 2026-09-22, these CipherDoc tasks are blocked:

| Task | Block type | Root cause | Assignee |
|---|---|---|---|
| CIPH-17 — Fix Coordinate/Offset Drift in Multi-Page PDFs | Upstream/external | `pdfminer.six` whitespace-handling issue / PR #992 is still unmerged; the team rejected maintaining a local fork. (`SRC-CU-CIPH-17`) | Charlie |
| CIPH-29 — Offline auth with key rotation for air-gapped installs | Internal | The designed key-rotation flow requires a network handshake, so it cannot complete in an air-gapped deployment; design change or requirement decision is needed. (`SRC-CU-CIPH-29`, `SRC-SLACK-17`) | Diana |
| CIPH-34 — Authenticated handshake for multi-site node sync | Internal | Under high latency, the handshake times out; AES-256 output-path overhead contributes, and the product’s encryption/handshake path needs resolution. (`SRC-CU-CIPH-34`, `SRC-MEET-11`) | Bob |
| CIPH-46 — Correct high-DPI PDF coordinate scaling | Upstream/external | A bug in the upstream rendering library’s scaling math has no safe local fix. (`SRC-CU-CIPH-46`, `SRC-GDOC-49`) | Charlie |
| CIPH-47 — Async job scheduler for concurrent batch API work | Internal | Concurrent I/O writes race, causing about a 10% throughput regression; the internal multi-threading/result-write design must be resolved. (`SRC-CU-CIPH-47`) | Bob |
