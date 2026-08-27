# Several streams remain blocked while others are only reopened. As of **2026-09-22**, what work can still advance in parallel, what cannot progress until an external dependency moves, and what release-checklist work is gated on packaging and Windows signing?

<!-- RESPONSE_START -->

## As of 2026-09-22 — CipherDoc (index as-of `2026-09-22T12:00:00Z`)

Source of truth: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/index.md` and the seven WS files, which already incorporate their Sources and Comments.

---

### 1. Work that can still advance in parallel (active / reopened, nothing external holding it)

These are all "reopened or active" rather than blocked — each has a named owner and a next step that the team controls, so they can run concurrently:

| Item | Stream | What is moving | Evidence |
|---|---|---|---|
| **T005 / CIPH-15 — Docker packaging** (reopened 2026-06-25) | WS-03 | Evan on multi-stage build + Alpine base, unused OCR/runtime packages stripped; as of 2026-08-12 still over the ~450MB target with CVE verification outstanding. Two thresholds tracked separately: interim RC may ship at **800MB once CVE-clean**, GA target stays **~450MB** | `work-states/WS-03-ops.md`; `med-synth/tasks/CIPH-15-Docker-Packaging.md`; `work-states/comments/2026-06.md` (CMT-2026-06-002); `med-synth/communication/sources/slack/2026-06-25-docker-size.md` |
| **T008 / CIPH-18 — OCR fallback** | WS-01 | Charlie integrated multiprocessing page-level parallelism; Diana wiring OCR results into the main scanner pipeline; confidence tuning continues into September | `work-states/WS-01-engine.md`; `med-synth/tasks/CIPH-18-OCR-Fallback.md` |
| **T006 / CIPH-16 — legacy JSON→YAML migration** | WS-01 | Task itself is done (YAML loader merged), but Evan owns an auto-migration converter for MedFirst's three legacy JSON pilot policies — a release dependency tied to the T011 gate | `work-states/WS-01-engine.md`; `work-states/comments/2026-06.md` (CMT-2026-06-001) |
| **T014 / CIPH-24 — manual-review quarantine** | WS-04 | 90% confidence threshold logic being integrated with metadata injection for visual indicators | `work-states/WS-04-policy.md`; `med-synth/communication/sources/slack/2026-06-28-manual-review-threshold.md` |
| **T016 / CIPH-26 — audit-trail logging** (active/reopened) | WS-04 | Bob refactored the loader for SHA-256 hashing and has another pass queued; Diana verifying emitted records against the defined schema. It is a release hold, but the fix is purely internal (Charlie confirms it is "schema versus emitted records", not packaging) | `work-states/WS-04-policy.md`; `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` |
| **T022 / CIPH-32 — storage quota** (reopened) | WS-07 | Bob refactoring the halt loop for a 10% buffer, retargeted to the corrected **2GB** production free-disk baseline (not 500MB), then re-verify in clinic VMs | `work-states/WS-07-storage.md`; `work-states/comments/2026-09.md` (CMT-2026-09-003) |
| **T031 / CIPH-41 — large-file chunking** (reopened) | WS-05 | Charlie refactoring stream-buffer release logic after Bob found leaks above 2GB; prioritized as a MedFirst pilot-blocker (OOM on a 4.7GB PDF / 8GB RAM workstation) and tied explicitly to the T011 gate | `work-states/WS-05-performance.md`; `work-states/comments/2026-08.md` (CMT-2026-08-003) |
| **T029 / CIPH-39 — Windows compatibility (engineering half)** | WS-06 | Path/backslash handling already fixed; engineering work continues. Only the signing gap is external — WS-06 states explicitly it is "a procurement dependency, not an engineering block" | `work-states/WS-06-platforms.md`; `med-synth/communication/sources/slack/2026-08-12-windows-build-artifact.md` |
| **T030 / CIPH-40 — non-AGPL parser search (engineering half)** | WS-04 | Charlie can keep searching for an Apache/MIT-licensed alternative — but see §2: the search cannot *close* the task | `work-states/WS-04-policy.md`; `med-synth/communication/sources/slack/2026-08-12-license-agpl-reopen.md` |

---

### 2. Work that cannot progress until an external dependency moves

**Genuinely external (outside the team's control):**

- **T007 / CIPH-17 — multi-page offset mismatch.** Blocked on upstream `pdfminer.six` PR/Issue **#992**, still unmerged as of 2026-09-10. Maintainer DM puts earliest realistic merge at **mid-October**. The team evaluated and *rejected* maintaining a local parser fork, and no safe local workaround exists. A second, compounding gate: any pre-normalization workaround requires **written Legal sign-off** in addition to the upstream merge. `work-states/WS-01-engine.md`; `work-states/comments/2026-06.md` (CMT-2026-06-003); `med-synth/communication/sources/slack/2026-06-26-blocked-on-upstream.md`
- **T036 / CIPH-46 — High-DPI PDF rendering.** Coordinates drift 5–10 px on 4K displays at 200% scaling. The bug is deep in the `pdf-lib-core` C++ core; Charlie states it cannot be patched locally, and the upstream issue he filed has had **no maintainer response**. Scope is wider than the upstream bug: 12% of the MedFirst pilot corpus fails on **nested Form XObjects**, so even the upstream scaling fix may not cover it. Open decision: ship with a documented known limitation, flatten PDFs first (costs file size and text layers), or swap rendering libraries entirely. `work-states/WS-06-platforms.md`; `med-synth/communication/sources/slack/2026-09-10-high-dpi-upstream-block.md`; `work-states/comments/2026-09.md` (CMT-2026-09-001)
- **T030 / CIPH-40 — license compliance.** Reopened 2026-08-12 after AGPL was found in a candidate replacement PDF parser. Legal memo escalated it to **P0 hard Legal gate**: AGPL in the bundle triggers whole-bundle copyleft exposure for the distribution model, and **engineering library search alone cannot close T030**. `work-states/WS-04-policy.md`; `work-states/comments/2026-08.md` (CMT-2026-08-002)
- **T029 / CIPH-39 — Windows code-signing.** Windows Defender/SmartScreen flag unsigned binaries; Evan: "this isn't something we can work around on the engineering side, we need the certificate." Waiting on **Authenticode certificate procurement** (budget + timeline still in Needs Manual Triage); Alice is chasing the certificate process. `work-states/WS-06-platforms.md`; `med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md`

**Blocked, but on an internal dependency rather than an outside party** (worth separating — no external party has to move, yet they still cannot advance today):

- **T024 / CIPH-34 — zero-trust node sync.** Nominal-latency handshake validation passed, but the 2026-09-22 high-latency simulation never completes. The team **declined a timeout-bump workaround** ("bumping timeouts just hides it") pending encryption-path stabilization; the path depends on the AES-256 crypto workstream. Unreconciled tension: the Singapore field trial fails at 180ms RTT with the 5s prototype timeout and asks for a **30s** budget, which the meeting caution resists. `work-states/WS-07-storage.md`; `med-synth/communication/sources/fireflies/2026-09-22-Handshake-Protocol-Deep-Dive.md`; `work-states/comments/2026-09.md` (CMT-2026-09-004)
- **T019 / CIPH-29 — offline mode authentication.** Key rotation is impossible in a strictly air-gapped environment without a centralized authority. InfoSec has **approved** a split master-key escrow (USB token at clinic + HQ HSM) and Bob is spiking it — so the architecture is settled, but it remains **Blocked until built**. `work-states/WS-04-policy.md`; `work-states/comments/2026-08.md` (CMT-2026-08-001)
- **T037 / CIPH-47 — async batch scheduler.** Concurrent manifest-write / I/O race between async workers and the existing multi-thread batch pool cuts throughput ~10% and can corrupt JSON under load. Alice: "a 10% hit is not shippable"; Bob is holding further async work until the pool interaction is understood; Diana captured repro steps for re-run. `work-states/WS-05-performance.md`; `med-synth/communication/sources/slack/2026-08-25-async-batch-io-race.md`; `med-synth/documentation/sources/2026-09-04-Async-Batch-Processing-Queue-Review.md`

---

### 3. Release-checklist work gated on packaging and Windows signing

**T011 / CIPH-21 (Release v1.0 Gates, owner Evan) is the gated item.** It is Active under a security-gate hold and **cannot close until T005 (Docker size/CVE) and T029 (Windows code-signing) are both green**. `work-states/WS-03-ops.md`; `med-synth/tasks/CIPH-21-Release-v1-Gates.md`

- **Everything else on the original checklist is already met.** The 2026-07-12 draft checklist depended on T001–T006 and T010; six of seven were complete (T001 core engine, T002 financial regex, T003 batch CLI, T004 REST API, T006 policy config, T010 security audit), with **T005 the only unmet dependency** at that point. `med-synth/documentation/sources/2026-07-12-Release-Checklist.md`
- **T029 was added later.** A subsequent prerequisite audit found the checklist still incomplete with T005 *and* T029 open — and noted release notes were **drafted in parallel while gates stayed open**. Diana placed the security-gate hold covering both. `med-synth/tasks/CIPH-21-Release-v1-Gates.md`
- **Third hold on the same board (not packaging/signing):** the 2026-09-15 pre-release audit keeps the **audit-log schema vs emitted-record mismatch (T016)** red as a release blocker alongside Docker and Windows signing. Diana: she cannot clear the audit gate until schema and records match. `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md`
- **Hard deadline:** the release board set a **no-ship after 2026-10-15** if T005 and T029 are not green — recorded as a hard deadline, not advisory. `work-states/comments/2026-09.md` (CMT-2026-09-002)
- **Other items explicitly tied to the T011 gate:** the T006 legacy JSON→YAML migration (CMT-2026-06-001) and T031 large-file chunking / MedFirst OOM (CMT-2026-08-003).
- **Watch item on T005's gate definition:** because of the dual thresholds, "packaging green" is ambiguous unless RC (800MB, CVE-clean) and GA (~450MB) are kept distinct on the checklist — CMT-2026-06-002 explicitly warns against conflating them.

**Standing priority order** for 2026-09-22: (1) WS-03 T005 + T029 before 2026-10-15, (2) WS-07 T024 high-latency handshake, (3) WS-04 T030 Legal gate. `briefs/2026-09-22-daily-brief.md`

---

### Also on the board (neither advancing nor externally blocked)

- **T009 / CIPH-19 — JWT REST auth: Deferred** to v1.1; not a v1.0.0 blocker since launch targets local single-machine use. Contract caveat: MedFirst IT renewal requires REST authentication no later than **2026-03-31**. `work-states/WS-02-api.md`; `work-states/comments/2026-07.md` (CMT-2026-07-001)
- **T039 / CIPH-49 — a11y audit: Superseded** by the CIPH-33 Preview UI overhaul, which natively covers high-contrast and keyboard navigation. `work-states/WS-04-policy.md`; `med-synth/communication/sources/slack/2026-08-24-a11y-superseded.md`
- **Open triage questions** (no owner-resolvable next step yet): whether a 30s timeout budget fixes the Singapore 180ms RTT failures without redesigning the handshake exchange count; whether the nested Form XObject subset needs an engine-side workaround if upstream's scaling fix doesn't cover it; and the budget/procurement timeline for the Authenticode certificate. `work-states/WS-06-platforms.md`; `work-states/WS-07-storage.md`
