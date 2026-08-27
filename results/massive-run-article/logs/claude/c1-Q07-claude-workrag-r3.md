# As of **2026-09-22**, which CipherDoc tasks are blocked, and for each is the block upstream/external or internal? State the root cause and the listed task assignee.

<!-- RESPONSE_START -->

## Blocked CipherDoc tasks as of 2026-09-22

The authoritative Work State Index (as-of 2026-09-22T12:00:00Z) lists exactly five tasks in **Blocked** status: **T007, T019, T024, T036, T037**.

---

### 1. T007 / CIPH-17 — Fix coordinate/offset drift in multi-page PDFs (WS-01)
- **Block type:** **Upstream / external** (third-party open-source dependency)
- **Root cause:** Redaction masks drift out of alignment with target text across multi-page PDFs. Debugging traced the drift to a **whitespace-handling defect in the upstream `pdfminer.six` library**, tracked as upstream **Issue/PR #992**, which remains unmerged. Charlie monitored the repo through August and evaluated maintaining a local fork in late August, but the team rejected owning a parser fork due to long-term maintenance risk. As of September 10 the PR is still unmerged and no safe local workaround exists. A commented gate adds that the maintainer indicated #992 lands mid-October at the earliest, and that any pre-normalization workaround would additionally require **written Legal sign-off** (CMT-2026-06-003).
- **Listed assignee:** **Charlie** (Priority: High)

### 2. T019 / CIPH-29 — Offline-mode authentication with key rotation for air-gapped installs (WS-04)
- **Block type:** **Internal** (own design/architecture problem; no external party is gating it)
- **Root cause:** The key-rotation flow assumes network reachability. Testing against a local auth mock (2026-08-05) showed **key rotation cannot complete without network access in an air-gapped setting**, which is precisely the target deployment. No resolution has been found. The design doc notes rotation behavior for a workstation offline for an extended period was never validated.
- **Listed assignee:** **Diana** (Priority: High)

### 3. T024 / CIPH-34 — Zero-Trust authenticated handshake for multi-site node sync (WS-07)
- **Block type:** **Internal** (own protocol implementation; network conditions are the trigger, not a third party)
- **Root cause:** The node-replication handshake completed reliably on a single LAN segment at nominal latency, but **validation under high-latency networks failed with timeouts**. Blocked on 2026-09-22 by Diana; the fix depends on the (already completed) encryption work but remains unresolved. Next step on record is a high-latency retest plan.
- **Listed assignee:** **Bob** (Priority: High)

### 4. T036 / CIPH-46 — Fix High-DPI PDF rendering coordinate alignment (WS-06)
- **Block type:** **Upstream / external** (third-party rendering library)
- **Root cause:** Redaction coordinates drift **5–10 pixels on 4K displays at 200% scaling** (reproduces at 150% and 200%, not at 100%). The scaling-math error was traced to a **defect in the upstream rendering library's scaling math**; no safe local fix has been identified. Blocked 2026-09-10. A commented scope note adds a second, partly internal dimension: offline QA found **12% of the MedFirst pilot corpus fails due to nested Form XObjects**, which is beyond upstream 4K scaling alone (CMT-2026-09-001).
- **Listed assignee:** **Charlie** (Priority: Normal)

### 5. T037 / CIPH-47 — Async Batch API scheduler (WS-05)
- **Block type:** **Internal** (own concurrency defect)
- **Root cause:** A **concurrent manifest-write race** in the async worker pool. Because documents finish out of order, multiple workers appending to the shared results manifest interleave writes and **can corrupt the JSON**; recovery/serialization around corrupted writes **cuts throughput by roughly 10%** versus the sync baseline. Confirmed under load on 2026-08-25; the interaction is with the existing multi-threaded batch pool (T026). Alice held further async rollout until resolved.
- **Listed assignee:** **Bob** (Priority: Normal)

---

### Summary

| Task | ClickUp | Block type | Root cause | Assignee |
|---|---|---|---|---|
| T007 | CIPH-17 | Upstream/external | Unmerged `pdfminer.six` PR #992 (whitespace handling); fork rejected | Charlie |
| T019 | CIPH-29 | Internal | Key rotation cannot complete without network in air-gapped setting | Diana |
| T024 | CIPH-34 | Internal | Handshake timeouts under high-latency multi-site networks | Bob |
| T036 | CIPH-46 | Upstream/external | Upstream rendering-library scaling math (5–10px drift at 4K/200%) | Charlie |
| T037 | CIPH-47 | Internal | Concurrent manifest-write race; JSON corruption, ~10% throughput loss | Bob |

**Split:** two blocks are upstream/external (T007, T036 — both third-party library defects with no accepted local remediation), three are internal (T019, T024, T037 — CipherDoc's own design and concurrency defects).

### Items that are *not* blocked, despite looking adjacent
- **T029 / CIPH-39 (Windows compatibility)** is **Active**, not Blocked. Path handling is fixed; the release is held on an **Authenticode code-signing certificate** — the work state explicitly classifies this as a **procurement dependency, not an engineering block**.
- **T009 / CIPH-19 (REST API auth)** is **Deferred** to v1.1, not blocked (though the MedFirst contract CMT-2026-07-001 requires REST auth by 2026-03-31 for IT renewal).
- **T005, T008, T011, T014, T016, T022, T030, T031** are Active/Reopened, and **T039** is Superseded.

### Sources cited
Work states: `work-states/index.md` (as-of 2026-09-22T12:00:00Z), `WS-01-engine.md`, `WS-04-policy.md`, `WS-05-performance.md`, `WS-06-platforms.md`, `WS-07-storage.md`. Provenance: `SRC-CU-CIPH-17`, `SRC-CU-CIPH-29`, `SRC-CU-CIPH-34`, `SRC-CU-CIPH-46`, `SRC-CU-CIPH-47`, `SRC-SLACK-61`, `SRC-GDOC-13`, `SRC-GDOC-18`, `SRC-GDOC-30`, `SRC-GDOC-49`, `SRC-GDOC-50`; comments CMT-2026-06-003, CMT-2026-09-001.
