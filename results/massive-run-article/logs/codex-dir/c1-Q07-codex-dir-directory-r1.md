# As of **2026-09-22**, which CipherDoc tasks are blocked, and for each is the block upstream/external or internal? State the root cause and the listed task assignee.

<!-- RESPONSE_START -->

As of 2026-09-22, the authoritative registry lists five blocked CipherDoc tasks. [Work State Index](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/index.md)

| Task | Block type | Root cause | Listed assignee |
|---|---|---|---|
| T007 / CIPH-17 — Fix Coordinate/Offset Drift | Upstream/external | `pdfminer.six` Issue/PR #992 (whitespace handling) remains unmerged; the team rejected a local parser fork, and any workaround also needs Legal sign-off. | Charlie ([task](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-17-Fix-Offset-Mismatch.md), [state](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-01-engine.md)) |
| T019 / CIPH-29 — Offline Mode Authentication | Internal | Key rotation cannot work in a strictly air-gapped environment without centralized authority; the approved split-key escrow architecture still needs implementation. | Diana ([task](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-29-Offline-Mode-Authentication.md), [state](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md)) |
| T024 / CIPH-34 — Zero-Trust Node Sync | Internal | The authenticated handshake times out on high-latency links; the team deferred a timeout increase pending stabilization of the encryption path. | Bob ([task](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-34-Zero-Trust-Node-Sync.md), [state](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-07-storage.md)) |
| T036 / CIPH-46 — High-DPI PDF Rendering | Upstream/external | An upstream rendering-library scaling-math bug causes 5–10px coordinate drift at 4K/200% scaling; no local fix is available. | Charlie ([task](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-46-High-DPI-PDF-Rendering-Fixes.md), [state](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-06-platforms.md)) |
| T037 / CIPH-47 — Async Batch Processing | Internal | A concurrent manifest-write/I/O race reduces throughput by about 10% and may corrupt JSON under load. | Bob ([task](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-47-Async-Batch-Processing.md), [state](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-05-performance.md)) |
