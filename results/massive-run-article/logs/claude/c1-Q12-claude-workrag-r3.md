# Several streams remain blocked while others are only reopened. As of **2026-09-22**, what work can still advance in parallel, what cannot progress until an external dependency moves, and what release-checklist work is gated on packaging and Windows signing?

<!-- RESPONSE_START -->

## Answer

**Scope note.** Everything below is CipherDoc, read against the seven Work States as of their `Last Updated: 2026-09-22` (index as-of timestamp `2026-09-22T12:00:00Z`).

---

### 1. Work that can still advance in parallel

These are the active/reopened items where the team owns the next step and nothing external has to move first:

- **T005 / CIPH-15 — Docker packaging (WS-03, Evan).** Reopened/active. The image ballooned to 2.1GB after OCR dependencies were bundled; Evan implemented multi-stage builds and swapped to Alpine, but as of August 12 the image still exceeds the ~450MB target and CVE verification is failing. Two thresholds are tracked separately: interim RC at 800MB once CVE-clean, GA at ~450MB (CMT-2026-06-002). `(WS-03 S1, S2; CMT-2026-06-002)`
- **T008 / CIPH-18 — OCR fallback (WS-01, Charlie/Diana).** Active. Multiprocessing for page-level parallelism is integrated; Diana is wiring OCR results into the main scanner pipeline, and confidence tuning continues into September. `(WS-01 S8, S9)`
- **T014 / CIPH-24 — OCR quarantine workflow (WS-04).** Active. The 90% confidence threshold logic is being integrated with metadata injection for visual indicators. `(WS-04 S7)`
- **T016 / CIPH-26 — Audit trail logging (WS-04, Bob/Diana).** Active/reopened. Bob refactored the loader for SHA-256 hashing; Diana is verifying that emitted records match the defined schema. Bob has "another pass queued." Note this is a release hold in its own right (see §3). `(WS-04 S5, S9; SRC-MEET-10)`
- **T022 / CIPH-32 — Storage quota buffer (WS-07, Bob).** Reopened/active. The monitor halts too aggressively at ~500MB free; Bob is refactoring the loop for a 10% buffer tolerance. Ops capacity planning has since reset the production baseline to **2GB** free disk, not 500MB (CMT-2026-09-003). `(WS-07 S4; CMT-2026-09-003)`
- **T029 / CIPH-39 — Windows compatibility engineering (WS-06, Evan).** Active. Backslash path handling is fixed and a Windows build artifact was produced by 2026-08-12. Packaging itself is no longer the blocker — **engineering work continues in parallel**; only the release gate is held. `(WS-06 S7, S8, S9; SRC-GDOC-39)`
- **T031 / CIPH-41 — Large-file memory leak (WS-05, Charlie).** Reopened/active. Initial chunking landed, but Bob found severe memory leaks on files over 2GB during long batch runs; Charlie is refactoring stream buffer release logic. Prioritized as a MedFirst pilot blocker (clinic workstation OOM on a 4.7GB PDF with 8GB RAM). `(WS-05 S6, S7; CMT-2026-08-003)`
- **T030 / CIPH-40 — License compliance search (WS-04, Charlie).** Reopened/active engineering-wise — Charlie is searching for an Apache- or MIT-licensed parser after the August 12 AGPL discovery. **Caveat:** the search can advance, but it cannot *close* the task — see §2.
- **T006 / CIPH-16 — legacy JSON→YAML migration (WS-01, Evan).** Active dependency work: the MedFirst pilot requires auto-migration of three legacy JSON policies before production cutover. `(CMT-2026-06-001)`

**WS-02 (REST API and Batch CLI)** has *no* active work at all — Active Work is explicitly `*None.*`. T003, T004 and T012 are done; T009 is deferred.

---

### 2. Work that cannot progress until an external dependency moves

**Genuinely external — the team cannot unblock these themselves:**

- **T007 / CIPH-17 — Multi-page PDF offset mismatch (WS-01).** Blocked on upstream `pdfminer.six` Issue/PR #992. Charlie monitored the repo through August and evaluated a local fork in late August, but **the team rejected maintaining a parser fork**. As of September 10 the PR remains unmerged and no safe local workaround exists. The only tracked next action is "upstream #992 merge watch." `(WS-01 S6, S7)`
- **T036 / CIPH-46 — High-DPI PDF rendering (WS-06).** Blocked by upstream rendering-library scaling math; redaction coordinates drift 5–10 pixels on 4K displays at 200% scaling. It was still listed as an open upstream block at the September 15 pre-release audit. Additionally, offline QA found **12% of the MedFirst pilot corpus fails due to nested Form XObjects — beyond upstream 4K scaling alone** — so an engine-side workaround may be needed even after upstream fixes (flagged for manual triage). `(WS-06 S14; CMT-2026-09-001)`
- **T029 signing gate (WS-06 / WS-03).** Procurement, not engineering. No Authenticode code-signing certificate has been procured or configured in the Windows build pipeline; the produced artifact is unsigned, triggering SmartScreen warnings and Defender flagging. Site IT policies commonly block unsigned/SmartScreen-flagged binaries outright. "Budget and procurement timeline for Windows Authenticode code-signing certificate" is an open manual-triage item. `(WS-06 S9; SRC-GDOC-39)`
- **T030 / CIPH-40 — License compliance (WS-04).** A hard **Legal** gate. The Legal memo states AGPL in the bundle triggers whole-bundle copyleft, and **engineering library search alone cannot close T030**. Finding a viable non-AGPL PDF parsing library is flagged for manual triage. `(CMT-2026-08-002; WS-04 S16)`

**Blocked, but on internal design/architecture rather than a third party** (worth separating — these are stalled without an external actor):

- **T024 / CIPH-34 — Zero-Trust node sync (WS-07).** Blocked. Nominal-latency handshake validation passed, but the September 22 high-latency simulation times out — the handshake never completes on slow links. The team explicitly **declined a timeout-bump workaround**: "Bumping timeouts just hides it." It depends on the AES-256 encryption path stabilizing, since per-packet crypto overhead pushes the exchange past the timeout window. Diana is leaving the high-latency repro in place to re-check when encryption or the handshake design changes. The Singapore field trial fails at 180ms RTT with the current 5s prototype timeout; a **30s timeout budget** is required on high-latency links, and a nominal-latency pass must not be treated as sufficient for field sign-off. `(WS-07 S6, S7; CMT-2026-09-004)`
- **T019 / CIPH-29 — Offline mode authentication (WS-04).** Blocked. Local key-rotation mockups exist, but rotation is impossible in a strictly air-gapped environment without a centralized authority. InfoSec approved a split master-key escrow (USB token + HQ HSM) and Bob is spiking the implementation, but it **remains blocked until built**. How rotation behaves for a workstation offline for an extended period is unvalidated pending a local auth mock. `(WS-04 S12; CMT-2026-08-001; SRC-GDOC-13)`
- **T037 / CIPH-47 — Async batch processing (WS-05).** Blocked. A concurrent manifest-write race reduces throughput ~10% and can corrupt JSON under load. `(WS-05 S11, S12)`

**Deferred / superseded (not blocked, just out of scope):**
- **T009 / CIPH-19 — REST API JWT auth** is deferred to v1.1; v1.0.0 targets local single-machine usage. Bob is capturing v1.1 requirements while deferred. One contractual exception: MedFirst IT's enterprise renewal requires REST authentication **no later than 2026-03-31**. `(WS-02 S5; CMT-2026-07-001)`
- **T039 / CIPH-49 — a11y audit** was superseded by the Preview UI overhaul (CIPH-33), which natively covers high-contrast and keyboard navigation. `(WS-04 S22)`

---

### 3. Release-checklist work gated on packaging and Windows signing

The release gate is **T011 / CIPH-21** (WS-03, owner Evan), currently **active under a security-gate hold**.

- **T011 cannot close until T005 (Docker size/CVE) and T029 (Windows code-signing certificate) are both green.** `(WS-03 S9, S10)`
- The **September 15 pre-release audit** listed three open blockers on the board: Docker slim/CVE work, Windows signing, and audit-log schema alignment — plus the upstream high-DPI block. Alice: security-gate work stays open; no one closes those. Evan: "Release isn't opening with any of those unresolved." `(SRC-MEET-10)`
- **Audit-log gate (T016)** is a distinct hold stacked on top of packaging and signing: Diana will keep it red until the CLI schema and the emitted records match, because the mismatch undercuts the audit trail as release evidence. Charlie confirmed in that meeting this is *not* a packaging issue — it's schema versus emitted records. `(SRC-MEET-10; WS-04 S5, S9)`
- **Hard deadline:** the release board set a **no-ship after 2026-10-15** if T005 and T029 are not green. `(CMT-2026-09-002)`
- **On the signing side specifically:** procuring a code-signing certificate and wiring signing into the release build step is described as the *only* remaining item before T029 clears the Windows compatibility gate — "and, by extension, the T011 release checklist, which is holding on this exact signing gap alongside the T005 image slim-down." Audit status: active; signing certificate procurement is the sole open blocker. `(SRC-GDOC-39)`
- **Next update needed on WS-03:** Docker multi-stage build progress, final CVE scan results, and release gate clearance. On WS-06: code-signing certificate status and upstream High-DPI fix timeline.

---

### Summary

Roughly two-thirds of the board is still parallelizable — Docker slimming, OCR fallback and quarantine, audit-log schema alignment, quota buffering, Windows engineering, the large-file memory leak, and the license search all have owners and next steps. What is genuinely stalled on outsiders is narrow but high-leverage: an unmerged upstream `pdfminer.six` PR, upstream high-DPI scaling math, a Legal AGPL ruling, and an unprocured Authenticode certificate. Two more items (node-sync handshake, offline auth) are blocked on internal architecture the team has deliberately chosen not to paper over with workarounds. The release checklist is the convergence point: T011 is held on T005 and T029, with the audit-log mismatch as a third independent hold, against a 2026-10-15 no-ship date.

**Dataset records cited:** `work-states/index.md`; `work-states/WS-01-engine.md`, `WS-02-api.md`, `WS-03-ops.md`, `WS-04-policy.md`, `WS-05-performance.md`, `WS-06-platforms.md`, `WS-07-storage.md`; `work-states/comments/2026-07.md`, `2026-09.md`; sources `SRC-MEET-10` (2026-09-15 Pre-Release Audit), `SRC-MEET-11` (2026-09-22 Handshake Protocol Deep Dive), `SRC-SLACK-27` (Node Sync Handshake Validation), `SRC-GDOC-39` (2026-09-02 Windows Compatibility Audit Report), `SRC-GDOC-13` (Offline-Mode Authentication Review), `SRC-CU-CIPH-19` (REST API Auth).
