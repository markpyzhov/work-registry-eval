# As of **2026-09-22**, which CipherDoc tasks are blocked, and for each is the block upstream/external or internal? State the root cause and the listed task assignee.

<!-- RESPONSE_START -->

As of 2026-09-22, five CipherDoc tasks are marked **Blocked**:

- **CIPH-17 — Fix Coordinate/Offset Drift in Multi-Page PDFs** — **Upstream/external**. `pdfminer.six` whitespace handling is defective; upstream PR #992 remains unmerged, and the team rejected maintaining a local fork. Assignee: **Charlie**. *(Source: SRC-CU-CIPH-17)*

- **CIPH-46 — Correct high-DPI PDF coordinate scaling** — **Upstream/external**. A rendering-library scaling/coordinate bug has no local fix available. Assignee: **Charlie**. *(Source: SRC-CU-CIPH-46)*

- **CIPH-47 — Async job scheduler for concurrent batch API work** — **Internal**. CipherDoc’s concurrent results-manifest writes race and corrupt/serialize I/O, causing about a 10% throughput regression. Assignee: **Bob**. *(Source: SRC-CU-CIPH-47)*

- **CIPH-34 — Authenticated handshake for multi-site node sync** — **Internal**. The handshake times out on high-latency links; AES-256-path overhead and the current exchange design push it beyond the timeout window. Assignee: **Bob**. *(Sources: SRC-CU-CIPH-34; SRC-MEET-11)*

- **CIPH-29 — Offline auth with key rotation for air-gapped installs** — **Internal**. The designed key-rotation flow requires a network connection to complete its handshake, so it cannot work in an air-gapped deployment. Assignee: **Diana**. *(Sources: SRC-CU-CIPH-29; SRC-SLACK-17)*
