# As of **2026-09-22**, which CipherDoc tasks are blocked, and for each is the block upstream/external or internal? State the root cause and the listed task assignee.

<!-- RESPONSE_START -->

C1 Q07 (as of 2026-09-22; <250w)

| Task | Dependency type | Root cause | Assignee |
|---|---|---|---|
| T011 / CIPH-21 | Mixed: internal + external procurement | Release hold: Docker size/CVE (T005) and Authenticode signing (T029) unresolved; no-ship after 10/15. | Evan |
| T024 / CIPH-34 | Internal | Handshake times out on high-latency links; team rejected timeout bump pending encryption-path/design stabilization. | Bob |
| T036 / CIPH-46 | External/upstream (plus internal scope) | Rendering-library scaling math; nested Form XObjects also fail 12% of MedFirst corpus. | Charlie |
| T031 / CIPH-41 | Internal | >2GB PDFs leak buffers; MedFirst 4.7GB file OOMs an 8GB workstation. | Charlie |
| T019 / CIPH-29 | Internal | Air-gapped rotation needs centralized authority; approved split-key escrow is not built. | Diana (Bob is spiking implementation) |
| T007 / CIPH-17 | External/upstream + Legal | `pdfminer.six` #992 remains unmerged; local fork rejected and workaround requires Legal approval. | Charlie |

The brief also explicitly reports **T037 / CIPH-47** blocked internally: concurrent manifest-write/I/O race cuts throughput ~10% and can corrupt JSON; assignee **Bob**.

Citations: [brief blocker scope](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md:19); [T011](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md:31); [T024](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-07-storage.md:36); [T036](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-06-platforms.md:39); [T031/T037](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-05-performance.md:33); [T019](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md:54); [T007](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-01-engine.md:38).
