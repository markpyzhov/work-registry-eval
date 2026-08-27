# Write a concise cross-workstream management briefing as of **2026-09-22** covering at least three workstreams: at least two completed milestones that still hold, at least three items of work that were completed then reopened, at least two durable blockers, and the top risks that should escalate before ship. Do not present reopened work as done.

<!-- RESPONSE_START -->

## CipherDoc — Cross-Workstream Management Briefing
**As of 2026-09-22** (Work State as-of timestamp 2026-09-22T12:00:00Z). All seven workstreams (WS-01 … WS-07) are `in_progress`; none is closed.

---

### 1. Completed milestones that still hold

| Item | Workstream | Evidence |
|---|---|---|
| **T010 / CIPH-20 — Security audit & vulnerability scans** | WS-03 (Ops, P0) | Medium-severity CORS `*` origin finding patched to configured `ALLOWED_ORIGINS`; re-scans on 2026-07-15 confirmed the patch holds. RedByte external pen-test attestation letter (2026-07-11) sits in the release evidence pack. `(WS-03 S4, S5, S6; CMT-2026-07-002)` |
| **T012 / CIPH-22 — CLI ↔ REST API configuration parity** | WS-02 (P1) | An earlier parity *claim* was disproved on 2026-07-09 (CLI ignored `custom_regex`); PR #52 fixed engine initialisation and 2026-07-11 tests confirmed unified config loading. Verified — this one survived its own correction. `(WS-02 S7, S9)` |
| **T021 / CIPH-31 — AES-256 local encryption at rest** | WS-07 (P1) | Zero-leakage confirmed in cold-start audit. `(WS-07 S2)` |
| **T028 / CIPH-38 — Bare-metal performance benchmarks** | WS-05 (P1) | 500 pages/minute on standard enterprise hardware; T026 worker pool scales linearly to 16 cores. `(WS-05 S2, S5)` |
| **T023 / CIPH-33 — Redaction preview UI overlay**; **T027 / CIPH-37 — air-gapped mode test**; **T035 / CIPH-45 — Electron GUI wrapper** | WS-06 (P2) | Preview renders bounding-box overlays; 1,000 files processed in a networking-disabled VM; Electron package test passes over the IPC bridge (progress-bar smoothness is a tracked non-blocking UX follow-up). `(WS-06 S4, S6, S11, S12)` |
| **T020 / CIPH-30 HIPAA PII patterns, T015 fail-closed batch, T032 auditable profile export, T038 telemetry opt-out** | WS-04 (P0) | Merged/verified; T038 confirmed by offline network trace. `(WS-04 S14, S3/S8, S18, S20)` |

---

### 2. Work completed then reopened — **not done**

These carry a prior "Completed" signal in the record. Treat none of them as closed.

1. **T005 / CIPH-15 — Docker packaging (WS-03, P0). Active (Reopened).** Initially completed at ~800MB, then superseded and reopened 2026-06-25 when OCR bundling ballooned the image to 2.1GB. Multi-stage builds and an Alpine base landed, but as of 2026-08-12 the image still exceeds the ~450MB GA target and **CVE verification is failing**. CISO review set dual gates: interim RC at 800MB once CVE-clean, GA at ~450MB. `(WS-03 S1, S2; CMT-2026-06-002)`
2. **T030 / CIPH-40 — License compliance review (WS-04, P0). Active (Reopened).** Ghostscript (AGPLv3) was swapped for an alternative PDF parser and marked Completed — follow-up review found the **replacement is also AGPL**, reintroducing the same copyleft category one layer down. Reopened 2026-08-12; Charlie is still searching for an Apache-2.0/MIT rasterization-capable parser, with **no confirmed replacement**. A separate lower-priority item remains open on unverified `eng.traineddata` training-corpus provenance. `(SRC-GDOC-41; WS-04 S15, S16)`
3. **T031 / CIPH-41 — Large-file stream chunking (WS-05, P1). Active (Reopened).** Chunking merged to mainline 2026-08-16; post-merge testing at ≥2GB surfaced a per-chunk buffer leak with peak memory climbing linearly with file size. Charlie's buffer-release refactor shows flat memory on a 2.3GB sample but is **not yet validated against the full large-file corpus**. `(SRC-GDOC-42; WS-05 S6, S7)`
4. **T016 / CIPH-26 — Compliance audit trail logs (WS-04, P0). Active (Reopened).** SHA-256 hashing loader refactor done, but emitted records still do not match the defined schema. Diana is holding the audit gate red. `(WS-04 S5, S9; SRC-MEET-10)`
5. **T022 / CIPH-32 — Storage quota management (WS-07, P1). Reopened/Active.** Monitor halts processing too aggressively near ~500MB free; Bob is refactoring for a 10% buffer tolerance. Ops has since reset the **production baseline to 2GB free disk**, not 500MB. `(WS-07 S4; CMT-2026-09-003)`

Also not done, despite adjacent completed work: **T029 / CIPH-39 (Windows)** — path handling fixed, but release is held on code-signing; **T039 a11y audit** is **Superseded** (folded into the completed T023 preview overlay on 2026-08-24), not delivered.

---

### 3. Durable blockers (persisting, with external dependencies)

- **T007 / CIPH-17 — multi-page offset mismatch (WS-01, P0).** Blocked on upstream `pdfminer.six` #992. Repo monitored through August; a local parser fork was evaluated and **rejected**. Unmerged as of 2026-09-10, maintainer indicates **mid-October at the earliest**, and any pre-normalization workaround needs **written Legal sign-off** on top of the upstream merge. `(WS-01 S6, S7; CMT-2026-06-003)`
- **T019 / CIPH-29 — offline mode authentication (WS-04, P0).** Key rotation is impossible in a strictly air-gapped environment without a central authority. InfoSec approved a split master-key escrow (USB token at clinic + HQ HSM) and Bob is spiking it — **architecture approved, implementation not built; still Blocked**. `(WS-04 S12; CMT-2026-08-001)`
- **T036 / CIPH-46 — High-DPI coordinate alignment (WS-06).** Blocked on upstream rendering-library scaling math; coordinates drift 5–10px on 4K at 200% scaling, no safe local fix identified. Offline QA found **12% of the MedFirst pilot corpus fails on nested Form XObjects — beyond what the upstream 4K fix would cover**. `(SRC-GDOC-49; WS-06 S14; CMT-2026-09-001)`
- **T024 / CIPH-34 — zero-trust node sync handshake (WS-07).** Nominal-latency validation passed; the **2026-09-22 high-latency simulation times out** and the handshake never completes. Singapore field trial fails at 180ms RTT against the 5s prototype timeout; a 30s budget is proposed, but the team declined a timeout-bump workaround pending encryption-path stabilization. Open question whether 30s suffices without redesigning the exchange count. `(WS-07 S6, S7; CMT-2026-09-004)`
- **T037 / CIPH-47 — async batch scheduler (WS-05).** Blocked on a concurrent manifest-write race that corrupts JSON under load and **cuts throughput ~10%** versus the expected async speedup. `(WS-05 S11, S12)`
- **T029 / CIPH-39 — Windows code-signing (WS-06 → WS-03).** SmartScreen flags unsigned binaries; this is a **procurement dependency, not an engineering block** — budget and timeline for the Authenticode certificate are still in manual triage. `(WS-06 S9)`

---

### 4. Top risks to escalate before ship

1. **Hard no-ship date, two unmet gates.** The release board set a **hard no-ship after 2026-10-15** if T005 (Docker size/CVE) and T029 (Windows signing) are not green. Neither is green today; T005 has been reopened since June and T029's blocker is an unfunded certificate purchase. This is the single highest-severity item. `(CMT-2026-09-002; WS-03 S9, S10)`
2. **Audit-log gate is red — release evidence is incomplete.** The 2026-09-15 pre-release audit kept T016 open on CLI schema vs emitted-record mismatch; Diana will not clear the audit gate until they match. This undercuts the compliance evidence pack for a P0 privacy product. `(SRC-MEET-10)`
3. **Legal AGPL exposure is a P0 gate engineering cannot close.** Legal's memo holds that AGPL in the bundle triggers **whole-bundle copyleft for our distribution model**. Escalated to P0 as a hard Legal gate — a library search alone is insufficient, and no compliant parser has been confirmed. Escalate to Legal + product for a distribution-model decision, not just to engineering. `(CMT-2026-08-002; SRC-GDOC-41)`
4. **Pilot-blocking OOM tied to the release gate.** MedFirst hit OOM on a 4.7GB PDF with 8GB RAM on a clinic workstation; T031 was prioritized ahead of nice-to-have perf work and tied explicitly to the T011 gate — and the fix is still unverified end-to-end. `(CMT-2026-08-003; SRC-GDOC-42)`
5. **Two upstream dependencies sit outside the team's control and outside the ship window.** pdfminer.six #992 is mid-October at best against a 2026-10-15 no-ship, and the High-DPI rendering defect has no accepted local remediation — with 12% of the pilot corpus failing for a reason upstream won't fix anyway. Decide now between accepting the defect, funding a workaround with Legal sign-off, or descoping. `(WS-01 S6/S7; WS-06 S14, CMT-2026-09-001)`
6. **Deferred REST auth has a contractual clock.** T009 (JWT) is deferred to v1.1 on the basis that v1.0.0 targets local single-machine use — but **MedFirst IT renewal requires REST authentication no later than 2026-03-31**. Fine for ship, must not be forgotten in v1.1 planning. `(WS-02 S5; CMT-2026-07-001)`

---

**Records used:** `work-states/index.md`; `work-states/WS-01-engine.md`, `WS-02-api.md`, `WS-03-ops.md`, `WS-04-policy.md`, `WS-05-performance.md`, `WS-06-platforms.md`, `WS-07-storage.md`; `work-states/comments/2026-08.md`; sources SRC-GDOC-05, SRC-GDOC-41, SRC-GDOC-42, SRC-GDOC-48, SRC-GDOC-49, SRC-GDOC-50, SRC-MEET-10, SRC-CU-CIPH-34, SRC-CU-CIPH-47; comments CMT-2026-06-002/003, CMT-2026-07-001/002, CMT-2026-08-001/002/003, CMT-2026-09-001/002/003/004.
