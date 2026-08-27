# As of **2026-09-22**, which CipherDoc tasks are blocked, and for each is the block upstream/external or internal? State the root cause and the listed task assignee.

<!-- RESPONSE_START -->

I have complete evidence for all five blocked tasks.

## CipherDoc blocked tasks as of 2026-09-22

The Work State Index (`work-states/index.md`, as-of 2026-09-22T12:00:00Z) lists exactly five blocked tasks: **T007, T019, T024, T036, T037**. Two are upstream/external blocks; three are internal.

---

### 1. T007 / CIPH-17 — Fix coordinate/offset drift in multi-page PDFs
**Block type: UPSTREAM/EXTERNAL** (plus an added external Legal gate)
**Listed assignee: Charlie** (ClickUp CIPH-17)

**Root cause:** Redaction masks drift from the target text across multi-page PDFs because of a whitespace-normalization defect (non-breaking spaces injected into extracted text) inside the upstream `pdfminer.six` parser. The fix lives in upstream issue/PR **#992**, which remains unmerged. The team evaluated maintaining a local `pdfminer.six` fork in late August and rejected it as long-term maintenance risk; as of 2026-09-10 no safe local workaround exists. A maintainer DM (CMT-2026-06-003) puts the earliest realistic merge at mid-October, and adds a second external gate: any pre-normalization workaround requires **written Legal sign-off** in addition to the upstream merge.

Records: `SRC-CU-CIPH-17`, `SRC-SLACK-07`, `SRC-SLACK-05`, `WS-01-engine.md`, `CMT-2026-06-003`

---

### 2. T019 / CIPH-29 — Offline auth with key rotation for air-gapped installs
**Block type: INTERNAL** (own design/implementation gap; no external party gating it)
**Listed assignee: Diana** (ClickUp CIPH-29)

**Root cause:** The designed key-rotation flow assumes at least a brief network connection to complete the handshake, so rotation cannot complete in a strictly air-gapped environment without a centralized authority. Bob's local auth mock (2026-08-04/05) ran the rotation with networking disabled and it failed to complete. InfoSec has since approved a split master-key escrow architecture (USB token at the clinic + HQ HSM) with Bob spiking the implementation (CMT-2026-08-001) — so the architecture is settled, but the task **remains blocked until that escrow implementation is built**.

Records: `SRC-CU-CIPH-29`, `SRC-SLACK-17`, `SRC-SLACK-16`, `SRC-GDOC-13`, `WS-04-policy.md`, `CMT-2026-08-001`

---

### 3. T024 / CIPH-34 — Authenticated handshake for multi-site zero-trust node sync
**Block type: INTERNAL** (own handshake/encryption-path design; the trigger is environmental network latency, not a third party)
**Listed assignee: Bob** (ClickUp CIPH-34)

**Root cause:** The prototype handshake assumes fast round trips. Nominal-latency validation passed, but high-latency simulation on 2026-09-22 times out — the handshake never completes on slow links. The team explicitly **declined a timeout-bump workaround** (Evan: bumping timeouts only hides it), leaving the fix dependent on the encryption/crypto path stabilizing. Field data (CMT-2026-09-004): the Singapore field trial fails at 180 ms RTT against the current 5 s prototype timeout; a **30 s timeout budget** is needed on high-latency links, and the nominal-latency pass must not be treated as sufficient for field sign-off.

Records: `SRC-CU-CIPH-34`, `SRC-MEET-11`, `SRC-SLACK-27`, `WS-07-storage.md`, `CMT-2026-09-004`

---

### 4. T036 / CIPH-46 — Fix High-DPI PDF rendering coordinate alignment
**Block type: UPSTREAM/EXTERNAL** (with a partly internal residual scope)
**Listed assignee: Charlie** (ClickUp CIPH-46)

**Root cause:** Redaction coordinates drift 5–10 pixels on 4K displays at 200% scaling. The scaling-math error was traced to a defect in the upstream rendering library **`pdf-lib-core`**, in how it handles XObject coordinates when a parent transform is applied — deep in the library's C++ core, so not locally patchable. Charlie opened an upstream issue; maintainers have not responded. No safe local fix identified; PDF flattening was floated but rejected as it inflates file size and can lose text layers.

Important qualifier (CMT-2026-09-001): offline QA on the MedFirst pilot corpus found **12% of documents fail alignment due to nested Form XObjects — beyond 4K scaling alone**, so the upstream fix alone may not close this and an engine-side workaround may still be needed. That residual portion is internal.

Records: `SRC-CU-CIPH-46`, `SRC-SLACK-58`, `SRC-GDOC-49`, `SRC-GDOC-30`, `WS-06-platforms.md`, `CMT-2026-09-001`

---

### 5. T037 / CIPH-47 — Async batch API job scheduler
**Block type: INTERNAL** (defect in CipherDoc's own concurrency code)
**Listed assignee: Bob** (ClickUp CIPH-47)

**Root cause:** A concurrent I/O race in the team's own async worker pool. Because documents vary in size, workers finish out of order and multiple workers append to the same shared results manifest concurrently, interleaving writes and corrupting the JSON structure. Confirmed by concurrency testing on 2026-08-25: workers retry/serialize around the corrupted-write recovery path, **cutting batch throughput by roughly 10%** versus the expected async speedup. Resolution depends on how the (already-completed) T026 multi-threaded worker pool's result-writing is serialized.

Records: `SRC-CU-CIPH-47`, `SRC-SLACK-61`, `SRC-GDOC-50`, `WS-05-performance.md`

---

### Summary table

| Task | Title | Upstream/External vs Internal | Root cause | Listed assignee |
|---|---|---|---|---|
| T007 / CIPH-17 | Multi-page PDF offset drift | **Upstream/External** | Whitespace-handling bug in `pdfminer.six`; PR #992 unmerged, fork rejected; Legal sign-off also gates any workaround | Charlie |
| T019 / CIPH-29 | Offline auth + key rotation | **Internal** | Rotation flow requires network handshake; impossible air-gapped without central authority; approved escrow design not yet built | Diana |
| T024 / CIPH-34 | Zero-trust node sync handshake | **Internal** | Handshake times out on high-latency links (fails at 180 ms RTT vs 5 s timeout); no timeout-bump workaround; depends on encryption path | Bob |
| T036 / CIPH-46 | High-DPI coordinate alignment | **Upstream/External** | `pdf-lib-core` scaling/XObject transform bug, unpatchable locally; plus a 12% nested-Form-XObject subset that may need an internal fix | Charlie |
| T037 / CIPH-47 | Async batch scheduler | **Internal** | Concurrent manifest-write race corrupts JSON and costs ~10% throughput | Bob |

**Split:** 2 upstream/external (T007, T036 — both assigned to Charlie, both dependent on unresponsive third-party maintainers), 3 internal (T019, T024, T037).

One caveat worth flagging: the Work State's per-task "Owner" fields differ from the ClickUp assignee in some cases (for example WS-06 is owned by Diana/Evan while CIPH-46's assignee is Charlie, and WS-04 is owned by Alice/Diana while CIPH-29's assignee is Diana). The assignees above are the ones listed on the ClickUp task records, as asked.
