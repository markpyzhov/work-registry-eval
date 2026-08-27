# As of **2026-09-22**, which CipherDoc tasks are blocked, and for each is the block upstream/external or internal? State the root cause and the listed task assignee.

<!-- RESPONSE_START -->

## Blocked CipherDoc tasks as of 2026-09-22

Five tasks carry **Blocked** status in the authoritative work states (as-of timestamp 2026-09-22T12:00:00Z).

### 1. T007 / CIPH-17 — Fix Coordinate/Offset Drift in Multi-Page PDFs
- **Block type:** **Upstream / external** (with a second external gate: Legal)
- **Root cause:** Whitespace-handling defect inside `pdfminer.six`; the fix lives in upstream issue/PR **#992**, which is still unmerged as of Sept 10. Charlie monitored the repo through August and evaluated a local fork in late August, but the team rejected maintaining a parser fork due to long-term maintenance risk, so no local workaround exists. A maintainer DM puts #992 at **mid-October earliest**, and any pre-normalization workaround additionally requires **written Legal sign-off**.
- **Listed assignee:** **Charlie**
- Files: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-01-engine.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-17-Fix-Offset-Mismatch.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-06-26-blocked-on-upstream.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-06.md` (CMT-2026-06-003)

### 2. T019 / CIPH-29 — Offline Mode Authentication (air-gapped key rotation)
- **Block type:** **Internal** (architecture/environment constraint, no external dependency)
- **Root cause:** Key rotation cannot complete in a strictly air-gapped environment because there is no centralized authority reachable; local rotation mockups exist but rotation itself is impossible offline. InfoSec has **approved** a split master-key escrow design (USB token + HQ HSM) and Bob is spiking the implementation — the task stays blocked purely until that escrow is actually built.
- **Listed assignee:** **Diana** (task opened and moved to Blocked by Alice; Bob is running the escrow spike)
- Files: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-29-Offline-Mode-Authentication.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-08.md` (CMT-2026-08-001)

### 3. T024 / CIPH-34 — Zero-Trust Node Sync authenticated handshake
- **Block type:** **Internal** (own protocol design; the failure is environmental network latency, not a third-party dependency)
- **Root cause:** Nominal-latency handshake validation passed, but the **high-latency simulation run on September 22 times out** — the handshake never completes over slow links. The team explicitly **declined a timeout-bump workaround** pending stabilization of the encryption path. Field data from the Singapore trial shows failure at **180ms RTT against the 5s prototype timeout**, with a requested **30s** timeout budget; whether 30s suffices without redesigning the handshake exchange count is flagged for manual triage.
- **Listed assignee:** **Bob** (blocked-status transition logged by Diana on 2026-09-22)
- Files: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-07-storage.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-34-Zero-Trust-Node-Sync.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-22-Handshake-Protocol-Deep-Dive.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md` (CMT-2026-09-004)

### 4. T036 / CIPH-46 — High-DPI PDF Rendering coordinate alignment
- **Block type:** **Upstream / external**, with an internal-scope tail
- **Root cause:** Scaling-math bug in the upstream rendering library **`pdf-lib-core`** — it mishandles coordinates for XObjects when a parent transform is applied; redaction coordinates drift **5–10 pixels on 4K displays at 200% scaling**. The defect is deep in the library's C++ core, not patchable locally; Charlie filed an upstream issue and maintainers have not responded. The internal tail: offline QA found **12% of the MedFirst pilot corpus** fails on nested Form XObjects, a scope beyond the upstream 4K scaling issue alone, so an engine-side workaround may be needed regardless. A PDF-flattening workaround was considered and set aside (file-size blowup, possible text-layer loss).
- **Listed assignee:** **Charlie** (blocked-status transition logged by Diana on 2026-09-10)
- Files: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-06-platforms.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-46-High-DPI-PDF-Rendering-Fixes.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-09-10-high-dpi-upstream-block.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md` (CMT-2026-09-001)

### 5. T037 / CIPH-47 — Async Batch API Scheduler
- **Block type:** **Internal** (defect in CipherDoc's own code)
- **Root cause:** Concurrent **manifest-write race** in the async worker path — it cuts throughput roughly **10%** and can **corrupt the manifest JSON under load**. The fix is coupled to the multi-threading work.
- **Listed assignee:** **Bob** (blocked-status transition logged by Diana on 2026-08-25)
- Files: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-05-performance.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-47-Async-Batch-Processing.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-25-async-batch-io-race.md`

## Summary

| Task | Title | Upstream/external vs internal | Root cause | Assignee |
|---|---|---|---|---|
| T007 / CIPH-17 | Multi-page offset drift | **External** (upstream + Legal) | `pdfminer.six` PR #992 unmerged; fork rejected; workaround needs Legal sign-off | Charlie |
| T019 / CIPH-29 | Offline mode auth | **Internal** | Key rotation impossible air-gapped without central authority; approved escrow not yet built | Diana |
| T024 / CIPH-34 | Zero-trust node sync | **Internal** | Handshake times out on high-latency links (180ms RTT vs 5s timeout); timeout bump declined | Bob |
| T036 / CIPH-46 | High-DPI rendering | **External** (+ internal Form XObject tail) | `pdf-lib-core` scaling-math bug in C++ core; 5–10px drift at 4K/200% | Charlie |
| T037 / CIPH-47 | Async batch scheduler | **Internal** | Concurrent manifest-write race: ~10% throughput loss, JSON corruption under load | Bob |

**Split:** 2 externally blocked (T007, T036), 3 internally blocked (T019, T024, T037).

## Two adjacent items that are *not* counted as Blocked

- **T029 / CIPH-39 (Windows Compatibility)** — status is **Active**, held on Authenticode code-signing (Defender SmartScreen flags unsigned binaries). WS-06 states explicitly that the signing gap is a **procurement dependency, not an engineering block**, so it is not carried as Blocked even though it gates the T011 release.
- **T030 / CIPH-40 (License Compliance)** — status is **Reopened/active**, not Blocked, but it sits behind a hard **P0 Legal gate**: an AGPL parser in the bundle triggers whole-bundle copyleft, and Legal's memo says an engineering library search alone cannot close it. Charlie is searching for an Apache/MIT alternative.

(`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/index.md` and `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md` both corroborate this blocked set: T007, T019, T024, T036, T037.)
