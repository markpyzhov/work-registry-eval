# As of **2026-09-22**, which CipherDoc tasks are blocked, and for each is the block upstream/external or internal? State the root cause and the listed task assignee.

<!-- RESPONSE_START -->

As of 2026-09-22 (work-state index as-of timestamp `2026-09-22T12:00:00Z`), **five CipherDoc tasks are Blocked**. This is consistent across the authoritative work states and the ClickUp task records (only CIPH-17, -29, -34, -46, -47 carry `Status: Blocked`).

---

### 1. T007 / CIPH-17 — Fix Coordinate/Offset Drift in Multi-Page PDFs
- **Block type: Upstream/external** (plus an external Legal gate)
- **Root cause:** Coordinate/offset drift traced to whitespace handling inside the upstream `pdfminer.six` library; the fix lives in upstream Issue/PR #992, which remains unmerged. A local fork was evaluated in late August and rejected over long-term maintenance risk, so no safe local workaround exists. Maintainer DM puts the earliest realistic merge at mid-October, and any pre-normalization workaround additionally requires written Legal sign-off — Legal is an explicit second dependency alongside upstream.
- **Listed assignee:** Charlie
- **Evidence:** `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-01-engine.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-17-Fix-Offset-Mismatch.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-06.md` (`CMT-2026-06-003`), `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-06-26-blocked-on-upstream.md`

### 2. T019 / CIPH-29 — Offline Mode Authentication (air-gapped key rotation)
- **Block type: Internal** (own unimplemented work + environmental constraint; no third-party dependency)
- **Root cause:** Key rotation cannot complete in a strictly air-gapped environment without a centralized authority — local rotation mockups exist but rotation requires network access. InfoSec has since approved a split master-key escrow architecture (USB token at clinic + HQ HSM), so the design question is settled; the task stays Blocked purely until that escrow is actually built.
- **Listed assignee:** Diana (note: `CMT-2026-08-001` records Bob spiking the escrow implementation, but the ClickUp-listed assignee on CIPH-29 is Diana)
- **Evidence:** `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-29-Offline-Mode-Authentication.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-08.md` (`CMT-2026-08-001`)

### 3. T024 / CIPH-34 — Authenticated Handshake for Multi-Site Node Sync
- **Block type: Internal** (own protocol/encryption-path design; surfaced by external field conditions, not an external dependency)
- **Root cause:** Nominal-latency handshake validation passed, but high-latency simulation on 2026-09-22 times out — the handshake never completes on slow links. The team declined a simple timeout-bump workaround pending stabilization of the encryption path, and resolution is coupled to the encryption work. The Singapore field trial adds concrete data: failures at 180ms RTT against the 5s prototype timeout, with a requested 30s timeout budget on high-latency links. Open triage: whether 30s resolves it, or whether the handshake exchange count needs redesign.
- **Listed assignee:** Bob
- **Evidence:** `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-07-storage.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-34-Zero-Trust-Node-Sync.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md` (`CMT-2026-09-004`), `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-22-Handshake-Protocol-Deep-Dive.md`

### 4. T036 / CIPH-46 — High-DPI PDF Rendering Coordinate Scaling
- **Block type: Upstream/external — but with an internal component**
- **Root cause:** The scaling-math error is a bug in the upstream rendering library; redaction coordinates drift 5–10 pixels on 4K displays at 200% scaling, with no local fix available. Internal wrinkle: offline QA on the MedFirst pilot corpus found 12% of documents fail coordinate alignment due to **nested Form XObjects**, a separate cause the upstream scaling fix may not cover — that subset may need an engine-side (internal) workaround.
- **Listed assignee:** Charlie
- **Evidence:** `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-06-platforms.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-46-High-DPI-PDF-Rendering-Fixes.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md` (`CMT-2026-09-001`), `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-09-10-high-dpi-upstream-block.md`

### 5. T037 / CIPH-47 — Async Batch API Scheduler
- **Block type: Internal** (defect in own code, plus an internal cross-task dependency)
- **Root cause:** A concurrent manifest-write race condition — async workers landed, but the race cuts throughput by roughly 10% and can corrupt the manifest JSON under load. Resolution depends on the multi-threading work (T026 / CIPH-36).
- **Listed assignee:** Bob
- **Evidence:** `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-05-performance.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-47-Async-Batch-Processing.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-25-async-batch-io-race.md`

---

### Summary table

| Task | Title | Upstream/external vs internal | Root cause | Listed assignee |
|---|---|---|---|---|
| T007 / CIPH-17 | Multi-page PDF offset drift | **Upstream/external** (+ Legal gate) | Unmerged `pdfminer.six` PR #992 (whitespace handling); local fork rejected | Charlie |
| T019 / CIPH-29 | Offline/air-gapped auth | **Internal** | Key rotation impossible air-gapped without central authority; approved escrow not yet built | Diana |
| T024 / CIPH-34 | Zero-trust node sync handshake | **Internal** | Handshake times out on high-latency links (180ms RTT vs 5s timeout); timeout bump declined pending encryption-path stabilization | Bob |
| T036 / CIPH-46 | High-DPI coordinate scaling | **Upstream/external** (+ internal Form XObject subset) | Upstream rendering-library scaling-math bug; 5–10px drift at 4K/200% | Charlie |
| T037 / CIPH-47 | Async batch scheduler | **Internal** | Concurrent manifest-write race: ~10% throughput loss, JSON corruption under load; depends on T026 | Bob |

**Split:** 2 upstream/external (T007, T036 — both third-party library bugs affecting PDF coordinates), 3 internal (T019, T024, T037).

**Two adjacent items worth flagging** (not Blocked, but held): **T029 / CIPH-39 (Windows Compatibility)** is Active, held on procuring an Authenticode code-signing certificate — the work state explicitly calls this "a procurement dependency, not an engineering block." **T030 / CIPH-40 (License Compliance)** is Active (Reopened) under a hard P0 Legal gate on AGPL whole-bundle copyleft. Both gate the T011 release against the hard 2026-10-15 no-ship deadline.
