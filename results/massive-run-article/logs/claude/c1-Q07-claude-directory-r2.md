# As of **2026-09-22**, which CipherDoc tasks are blocked, and for each is the block upstream/external or internal? State the root cause and the listed task assignee.

<!-- RESPONSE_START -->

## Blocked CipherDoc tasks as of 2026-09-22

Authoritative source: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/index.md` (as-of 2026-09-22T12:00:00Z) — five tasks are Blocked, and exactly five ClickUp task records carry `Status: Blocked`.

### 1. T007 / CIPH-17 — Fix Coordinate/Offset Drift in Multi-Page PDFs
- **Assignee (listed):** Charlie
- **Block type:** **Upstream / external** (with an internal Legal gate on the only workaround path)
- **Root cause:** Offset/coordinate drift traces to whitespace handling inside the upstream `pdfminer.six` parser. The fix depends on upstream Issue/PR **#992**, still unmerged as of the 2026-09-10 check. Charlie evaluated forking `pdfminer.six` in late August; the team rejected it as unsustainable maintenance risk, so no local workaround was adopted. Maintainer DM puts earliest realistic merge at **mid-October**, and any pre-normalization workaround additionally requires **written Legal sign-off**.
- **Files:** `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-01-engine.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-17-Fix-Offset-Mismatch.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-06-26-blocked-on-upstream.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-06.md` (CMT-2026-06-003)

### 2. T019 / CIPH-29 — Offline auth with key rotation for air-gapped installs
- **Assignee (listed):** Diana (Bob is spiking the escrow implementation)
- **Block type:** **Internal** — own design/implementation gap, driven by an external deployment constraint (strictly air-gapped sites), not by a third party
- **Root cause:** The designed key-rotation flow assumes at least a brief network connection to finish the handshake; testing against Bob's local auth mock with networking disabled (2026-08-05) showed rotation cannot complete. Rotation is impossible in a strictly air-gapped environment without a centralized authority. InfoSec has since approved a split master-key escrow architecture (USB token at clinic + HQ HSM), but the task **remains blocked until that is built**.
- **Files:** `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-29-Offline-Mode-Authentication.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-04-offline-auth-mock-block.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-08.md` (CMT-2026-08-001)

### 3. T024 / CIPH-34 — Authenticated handshake for multi-site node sync
- **Assignee (listed):** Bob (block logged by Diana on 2026-09-22)
- **Block type:** **Internal** — own protocol design plus an internal cross-workstream dependency on the encryption path
- **Root cause:** Nominal-latency handshake validation passed, but the high-latency simulation walked through in the 2026-09-22 deep-dive never completes — the prototype exchange assumes fast round trips and times out on slow links. The Singapore field trial fails at **180ms RTT with the 5s prototype timeout** and asks for a **30s** budget; the team explicitly **declined a timeout bump** as papering over the problem, pending stabilization of the AES-256 encryption path on the wire.
- **Files:** `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-07-storage.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-34-Zero-Trust-Node-Sync.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-22-Handshake-Protocol-Deep-Dive.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md` (CMT-2026-09-004)

### 4. T036 / CIPH-46 — Correct high-DPI PDF coordinate scaling
- **Assignee (listed):** Charlie (block logged by Diana on 2026-09-10)
- **Block type:** **Upstream / external**, with an internal scope extension that upstream may not cover
- **Root cause:** A known bug in the upstream rendering library **`pdf-lib-core`** — it mishandles XObject coordinates when a parent transform is applied. Redaction coordinates drift 5–10 px on 4K displays at 200% scaling. The bug sits deep in the library's C++ core so it cannot be patched locally; Charlie filed an upstream issue with no maintainer response. Separately, offline QA found **12% of the MedFirst pilot corpus** fails due to nested Form XObjects — a scope beyond the 4K scaling bug that may need an engine-side workaround even after an upstream fix. PDF flattening was floated as a workaround but risks file-size blowup and text-layer loss.
- **Files:** `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-06-platforms.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-46-High-DPI-PDF-Rendering-Fixes.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-09-10-high-dpi-upstream-block.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md` (CMT-2026-09-001)

### 5. T037 / CIPH-47 — Async job scheduler for concurrent batch API work
- **Assignee (listed):** Bob (block logged by Diana on 2026-08-25)
- **Block type:** **Internal** — a defect in the team's own code, dependent on the internal multi-threading workstream
- **Root cause:** A concurrent manifest-write / I/O race. The scheduler shell alone was fine; once the new async workers share I/O with the existing multi-threaded batch pool (T026 / CIPH-36), the race appears — roughly **10% throughput regression** versus the sync baseline, and it can corrupt the manifest JSON under load. Alice held all further async work until the interaction with the multi-thread pool is resolved.
- **Files:** `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-05-performance.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-47-Async-Batch-Processing.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-25-async-batch-io-race.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-09-04-Async-Batch-Processing-Queue-Review.md`

### Summary
| Task | Title | Assignee | Block type | Root cause |
|---|---|---|---|---|
| T007 / CIPH-17 | Multi-page PDF offset drift | Charlie | Upstream/external (+ internal Legal gate) | Unmerged `pdfminer.six` PR #992 whitespace fix; fork rejected |
| T019 / CIPH-29 | Offline auth key rotation | Diana | Internal | Rotation design requires a network handshake; escrow approved but unbuilt |
| T024 / CIPH-34 | Node-sync handshake | Bob | Internal | Handshake times out on high-latency links; timeout bump declined pending encryption path |
| T036 / CIPH-46 | High-DPI coordinate scaling | Charlie | Upstream/external (+ internal Form XObject scope) | `pdf-lib-core` XObject transform bug; no local patch possible |
| T037 / CIPH-47 | Async batch scheduler | Bob | Internal | Concurrent I/O/manifest-write race with the multi-thread pool; ~10% throughput loss |

**Not counted as blocked** (worth flagging because they read like blocks): **T029 / CIPH-39 (Windows compatibility, Diana/Evan area)** is **Active**, held on procuring an Authenticode code-signing certificate — WS-06 states explicitly this is a procurement dependency, not an engineering block; and **T030 / CIPH-40 (License compliance)** is **Reopened/active** behind a hard P0 Legal AGPL whole-bundle gate, not marked Blocked (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-06-platforms.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md`).
