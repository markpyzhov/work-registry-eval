# As of **2026-09-22**, which CipherDoc tasks are blocked, and for each is the block upstream/external or internal? State the root cause and the listed task assignee.

<!-- RESPONSE_START -->

As of 2026-09-22, **five** tasks are explicitly `Blocked` (not nine):

| Task | Dependency | Root cause | Assignee |
|---|---|---|---|
| T007 / CIPH-17 | Upstream/external | `pdfminer.six` whitespace fix/PR #992 remains unmerged; local fork rejected; Legal also gates any workaround. | Charlie |
| T019 / CIPH-29 | Internal | Air-gapped key rotation requires a replacement for central authority; approved split-escrow architecture is not yet built. | Diana (Bob spiking escrow) |
| T024 / CIPH-34 | Internal | Handshake times out on high-latency links; timeout bump deferred pending encryption-path stabilization. | Bob |
| T036 / CIPH-46 | Upstream/external | Upstream rendering-library scaling-math bug causes 5–10px high-DPI coordinate drift; nested Form XObjects add scope. | Charlie |
| T037 / CIPH-47 | Internal | Concurrent manifest-write/I/O race can corrupt JSON and costs ~10% throughput; depends on multi-threading work. | Bob |

Citations: [WS-01-engine](c1/work-states/WS-01-engine.md), [CIPH-17](c1/med-synth/tasks/CIPH-17-Fix-Offset-Mismatch.md), [WS-04-policy](c1/work-states/WS-04-policy.md), [CIPH-29](c1/med-synth/tasks/CIPH-29-Offline-Mode-Authentication.md), [WS-07-storage](c1/work-states/WS-07-storage.md), [CIPH-34](c1/med-synth/tasks/CIPH-34-Zero-Trust-Node-Sync.md), [WS-06-platforms](c1/work-states/WS-06-platforms.md), [CIPH-46](c1/med-synth/tasks/CIPH-46-High-DPI-PDF-Rendering-Fixes.md), [WS-05-performance](c1/work-states/WS-05-performance.md), [CIPH-47](c1/med-synth/tasks/CIPH-47-Async-Batch-Processing.md).
