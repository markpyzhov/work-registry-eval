# As of **2026-09-22**, which CipherDoc tasks are blocked, and for each is the block upstream/external or internal? State the root cause and the listed task assignee.

<!-- RESPONSE_START -->

As of 2026-09-22, five CipherDoc tasks are marked blocked:

| Task | Block type | Root cause | Assignee |
|---|---|---|---|
| T007 / CIPH-17 — Fix Coordinate/Offset Drift | Upstream/external | `pdfminer.six` whitespace-handling fix depends on unmerged upstream PR #992; maintaining a local fork was rejected. | Charlie |
| T019 / CIPH-29 — Offline auth/key rotation | Internal | Key rotation cannot work in the air-gapped design without centralized authority; the approved escrow architecture still needs implementation. | Diana |
| T024 / CIPH-34 — Zero-trust node sync | Internal | The handshake times out on high-latency links; the timeout workaround was deferred pending encryption-path stabilization. | Bob |
| T036 / CIPH-46 — High-DPI PDF coordinate scaling | Upstream/external | An upstream rendering-library scaling-math defect causes 5–10 px coordinate drift at 200%/4K scaling. | Charlie |
| T037 / CIPH-47 — Async batch processing | Internal | A concurrent manifest-write I/O race reduces throughput by ~10% and can corrupt JSON under load. | Bob |

Evidence: `WS-01` / `SRC-CU-CIPH-17`; `WS-04` / `SRC-CU-CIPH-29`; `WS-07` / `SRC-CU-CIPH-34`; `WS-06` / `SRC-CU-CIPH-46`; `WS-05` / `SRC-CU-CIPH-47`.
