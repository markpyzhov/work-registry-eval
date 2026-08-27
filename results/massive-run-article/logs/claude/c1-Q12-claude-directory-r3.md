# Several streams remain blocked while others are only reopened. As of **2026-09-22**, what work can still advance in parallel, what cannot progress until an external dependency moves, and what release-checklist work is gated on packaging and Windows signing?

<!-- RESPONSE_START -->

## Answer — CipherDoc status as of 2026-09-22

All seven work states carry **Last Updated: 2026-09-22**, and the Work State Index as-of timestamp is **2026-09-22T12:00:00Z**, so the picture below is current, not inferred.

---

### 1. Work that can still advance in parallel

These are the **active / reopened** items — engineering-owned, with no external party in the critical path. They can all run concurrently:

| Item | Stream | What can move |
|---|---|---|
| **T005 / CIPH-15 — Docker packaging** | WS-03 | Reopened 2026-06-25 after OCR bundling pushed the image from ~800MB to 2.1GB. Evan has multi-stage builds and an Alpine base in; as of the 2026-08-12 verification the image still exceeds the ~450MB target and CVE verification is still failing. Two thresholds must be tracked separately: interim RC may ship at **800MB once CVE-clean**, GA target stays **~450MB** (`CMT-2026-06-002`). |
| **T029 / CIPH-39 — Windows compatibility** | WS-06 | Backslash path handling is fixed and a Windows build artifact exists. WS-06 is explicit that the signing gap is *a procurement dependency, not an engineering block* — so Windows engineering work continues in parallel. |
| **T008 / CIPH-18 — OCR fallback** | WS-01 | Active. Charlie integrated multiprocessing for page-level parallelism; Diana is wiring OCR results into the main scanner pipeline; confidence tuning continues through September. |
| **T006 / CIPH-16 — legacy JSON→YAML migration** | WS-01 | Evan owns the converter for MedFirst's three legacy JSON pilot policies. It is a release dependency tied to T006 and the T011 gate (`CMT-2026-06-001`), but nothing external blocks it. |
| **T014 / CIPH-24 — manual review quarantine** | WS-04 | Active: 90% confidence-threshold logic being integrated with metadata injection for visual indicators. |
| **T016 / CIPH-26 — audit trail logging** | WS-04 | Active/reopened. SHA-256 hashing and CLI wiring landed (2026-09-10); Diana's 2026-09-18 verify found emitted records inconsistent with the defined schema. Bob has "another pass queued" (`SRC-MEET-10`). Charlie confirmed in the audit this is *not* a packaging issue — schema vs emitted records — so it proceeds independently of T005/T029. |
| **T022 / CIPH-32 — storage quota** | WS-07 | Reopened/active. Bob is refactoring the halt loop for 10% buffer tolerance, now retargeted to a **2GB** production baseline rather than 500MB (`CMT-2026-09-003`), pending re-verification in clinic VMs. |
| **T031 / CIPH-41 — large-file stream chunking** | WS-05 | Reopened/active. Charlie is refactoring stream buffer release after each chunk; files >2GB still leak. Prioritized as a MedFirst pilot-blocker after OOM on a 4.7GB PDF with 8GB RAM, and explicitly tied to the T011 gate (`CMT-2026-08-003`). |
| **T030 / CIPH-40 — non-AGPL parser search** | WS-04 | The *engineering half* can advance: Charlie is searching for an Apache- or MIT-licensed alternative. Closure cannot (see below). |

---

### 2. Work that cannot progress until an external dependency moves

**Genuinely external (outside the team's control):**

- **T007 / CIPH-17 — multi-page offset mismatch (WS-01).** Blocked on upstream `pdfminer.six` **#992**. The maintainer DM puts earliest realistic merge at **mid-October** (`CMT-2026-06-003`). A local fork was evaluated in late August and rejected; as of 2026-09-10 the PR is still unmerged and no safe local workaround exists. A second external gate applies: any pre-normalization workaround needs **written Legal sign-off** in addition to the upstream merge.
- **T036 / CIPH-46 — High-DPI PDF rendering (WS-06).** Blocked on the `pdf-lib-core` rendering library's coordinate handling for XObjects under a parent transform — Charlie: the bug is deep in their C++ core and cannot be patched locally. An upstream issue is open and maintainers have **not responded**. Coordinates drift 5–10 px on 4K at 200% scaling. Scope has since widened: **12% of the MedFirst pilot corpus** fails due to nested Form XObjects, beyond 4K scaling alone (`CMT-2026-09-001`). Open decision: ship with a documented known issue vs. swap rendering libraries; flattening was floated but risks file-size blowup and text-layer loss.
- **T030 / CIPH-40 — license compliance (WS-04).** Reopened 2026-08-12 when the swapped-in PDF parser turned out to be AGPL. Legal's memo escalated this to **P0**: AGPL in the bundle triggers whole-bundle copyleft for the current distribution model, and it is a **hard Legal gate — engineering library search alone cannot close it** (`CMT-2026-08-002`).
- **T029's signing certificate (WS-06).** Not engineering-solvable: Evan — the cert is the actual blocker and cannot be worked around on the engineering side. Alice is chasing the procurement process. Budget and procurement timeline are flagged for manual triage.

**Blocked, but on internal cross-stream dependencies rather than third parties:**

- **T024 / CIPH-34 — zero-trust node sync (WS-07).** Nominal-latency handshake validation passed, but the 2026-09-22 high-latency simulation never completes. The deep-dive explicitly **declined a timeout bump** ("bumping timeouts just hides it") and left the work blocked **pending the encryption/AES-256 wire-path workstream**. Diana is holding the high-latency repro for re-check when crypto or the handshake design moves. Unresolved tension for triage: the Singapore field trial fails at 180ms RTT with the 5s prototype timeout and asks for a **30s timeout budget** (`CMT-2026-09-004`) — which the meeting's caution does not currently permit testing.
- **T037 / CIPH-47 — async batch scheduler (WS-05).** Blocked on a concurrent manifest-write / I/O race where async workers share I/O with the existing multi-thread batch pool: ~10% throughput loss vs. sync baseline and JSON corruption under load. Alice: "a 10% hit is not shippable"; Bob is holding further async work until the pool interaction is understood.
- **T019 / CIPH-29 — offline mode authentication (WS-04).** Blocked: key rotation cannot complete in a strictly air-gapped environment without a centralized authority. InfoSec has **approved** a split master-key escrow (USB token at clinic + HQ HSM) and Bob is spiking it, so the architecture is settled — but it remains blocked **until built** (`CMT-2026-08-001`).

**Not blocked — off the board:**
- **T009 / CIPH-19** (REST JWT auth) — deferred to v1.1; v1.0.0 targets local single-machine use. Caveat: MedFirst's IT renewal contractually requires REST auth no later than **2026-03-31** (`CMT-2026-07-001`).
- **T039 / CIPH-49** (a11y audit) — superseded, folded into the CIPH-33 Preview UI overhaul, which natively covers high-contrast and keyboard navigation.

---

### 3. Release-checklist work gated on packaging and Windows signing

**T011 / CIPH-21 (Release v1.0 Gates, WS-03, owner Evan) is the gated item, and it is under a security-gate hold placed by Diana.**

- The 2026-07-12 checklist draft (DOC-2005) depends on **T001–T006 and T010**. Six of seven were met at draft time; **T005 was the sole unmet dependency**, reopened on Diana's 2026-06-25 size/CVE review.
- CIPH-21's acceptance criteria now name **two** unmet gates: **T005 (Docker image size/CVE)** and **T029 (Windows code-signing)**. WS-03 states flatly that T011 cannot close until both are green. Release notes were drafted in parallel while the gates stayed open.
- **Hard deadline:** the release board set a **no-ship after 2026-10-15** if T005 and T029 are not green — recorded as "hard, not advisory" (`CMT-2026-09-002`). This is the top priority item in the 2026-09-22 brief.
- The **2026-09-15 pre-release audit** stacked a third hold on top of the two packaging/signing gates: **audit-log schema alignment (T016)**, which Diana is keeping red until CLI-emitted records match the defined schema. Upstream high-DPI (T036) also remains on the board. Evan: "Release isn't opening with any of those unresolved"; Alice: "No one closes those today."
- Two further items are explicitly coupled to the T011 gate even though they sit in other streams: the **legacy JSON→YAML migration** under T006 (`CMT-2026-06-001`) and **large-file chunking T031** after the MedFirst OOM (`CMT-2026-08-003`).
- Already banked as release evidence: **T010 security audit complete** — the medium-severity CORS `*` finding was patched to configured `ALLOWED_ORIGINS` and confirmed by 2026-07-15 re-scans, plus the **RedByte pen-test attestation letter dated 2026-07-11** in the evidence pack (`CMT-2026-07-002`).
- Concrete follow-ups named for the release path: secure the **Authenticode certificate** and finish **Alpine/CVE Docker verification**.

**Net:** three of the release holds are progressable in-house right now (Docker slim/CVE, Windows engineering, audit-log schema), one is pure procurement (the signing cert), and the release cannot close on any of them past 2026-10-15.

---

### Files supporting the above (absolute paths)

Work states and index:
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/index.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-01-engine.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-02-api.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-05-performance.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-06-platforms.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-07-storage.md`

Comments (`CMT-*`):
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-06.md` (CMT-2026-06-001/-002/-003)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-07.md` (CMT-2026-07-001/-002)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-08.md` (CMT-2026-08-001/-002/-003)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md` (CMT-2026-09-001/-002/-003/-004)

Brief:
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md`

Sources (`SRC-*`):
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-07-12-Release-Checklist.md` (SRC-GDOC-05)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md` (SRC-CU-CIPH-21)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-15-Docker-Packaging.md` (SRC-CU-CIPH-15)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-39-Windows-Compatibility.md` (SRC-CU-CIPH-39)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-26-Audit-Trail-Logging.md` (SRC-CU-CIPH-26)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-41-Large-File-Chunking.md` (SRC-CU-CIPH-41)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (SRC-MEET-10)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-22-Handshake-Protocol-Deep-Dive.md` (SRC-MEET-11)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md` (SRC-SLACK-37)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-09-10-high-dpi-upstream-block.md` (SRC-SLACK-58)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-25-async-batch-io-race.md` (SRC-SLACK-61)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-04-offline-auth-mock-block.md` (SRC-SLACK-17)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-12-license-agpl-reopen.md` (SRC-SLACK-40)
