# As of **2026-09-22**, which CipherDoc tasks are blocked, and for each is the block upstream/external or internal? State the root cause and the listed task assignee.

<!-- RESPONSE_START -->

As of 2026-09-22, the CipherDoc tasks marked **Blocked** are:

| Task | Block type | Root cause | Assignee |
|---|---|---|---|
| **CIPH-17** — Fix Coordinate/Offset Drift | Upstream/external | `pdfminer.six` whitespace-handling fix is awaiting upstream Issue/PR #992; the team rejected maintaining a local fork. | Charlie |
| **CIPH-29** — Offline auth with key rotation | Internal | Key rotation cannot complete in a strictly air-gapped environment without centralized authority; the approved escrow architecture still needs implementation. | Diana |
| **CIPH-34** — Authenticated handshake for multi-site sync | Internal | The handshake times out under high-latency links (5s prototype vs. 30s needed); workaround deferred pending encryption-path stabilization. | Bob |
| **CIPH-46** — Correct high-DPI PDF coordinate scaling | Upstream/external | An upstream rendering-library scaling-math bug causes 5–10 px coordinate drift at 200% / 4K; no local fix is available. | Charlie |
| **CIPH-47** — Async job scheduler | Internal | A concurrent manifest-write/I/O race cuts throughput by ~10% and can corrupt JSON under load. | Bob |

Evidence: WS-01 / `SRC-CU-CIPH-17`; WS-04 / `SRC-CU-CIPH-29`; WS-07 / `SRC-CU-CIPH-34`; WS-06 / `SRC-CU-CIPH-46`; WS-05 / `SRC-CU-CIPH-47`.

I excluded CIPH-40 and CIPH-21: they have open gates/dependencies but their task records are **Active (Reopened)** and **Active**, respectively, not Blocked.
