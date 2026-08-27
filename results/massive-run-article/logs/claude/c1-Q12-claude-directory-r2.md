# Several streams remain blocked while others are only reopened. As of **2026-09-22**, what work can still advance in parallel, what cannot progress until an external dependency moves, and what release-checklist work is gated on packaging and Windows signing?

<!-- RESPONSE_START -->

## As of 2026-09-22 — CipherDoc (v1.0.0)

Work State index as-of timestamp: `2026-09-22T12:00:00Z` (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/index.md`).

---

## 1. Work that can still advance in parallel

These are engineering-owned and have no external gate on the work itself (several still cannot *close*, but they can *progress*):

| Item | Stream | What can move now |
|---|---|---|
| **T005 / CIPH-15 — Docker packaging** | WS-03 | Reopened/active. Evan is on multi-stage builds + Alpine base, unused OCR/runtime packages stripped. Two thresholds tracked separately: interim RC may ship at **800MB once CVE-clean**, GA target remains **~450MB**. As of the 2026-08-12 verification, size still exceeds target and CVE verification is outstanding. |
| **T029 / CIPH-39 — Windows compatibility** | WS-06 | Engineering work continues. Path/backslash handling is already fixed and a Windows build artifact exists. Only the *signing* leg is externally gated (see §2). |
| **T016 / CIPH-26 — Audit trail logging** | WS-04 | Active/reopened. Bob refactored the loader for SHA-256 hashing and has another pass queued on the CLI emitter; Diana verifies emitted records against the defined schema. Purely internal — Charlie explicitly confirmed at the 09-15 audit that this "isn't a packaging issue." |
| **T008 / CIPH-18 — OCR fallback** | WS-01 | Active. Charlie integrated multiprocessing page-level parallelism; Diana is wiring OCR results into the main scanner pipeline; confidence tuning continues into September. |
| **T014 / CIPH-24 — Manual review / quarantine** | WS-04 | Active. 90% confidence threshold logic being integrated with metadata injection for visual indicators. |
| **T022 / CIPH-32 — Storage quota** | WS-07 | Reopened/active. Bob's 10% buffer-tolerance refactor continues, retargeted from 500MB to the **2GB production baseline** per Ops capacity planning, then re-verify in clinic VMs. |
| **T031 / CIPH-41 — Large-file chunking** | WS-05 | Reopened/active. Charlie is refactoring stream-buffer release logic after Bob found leaks on >2GB files. Prioritized as a MedFirst pilot-blocker (OOM on a 4.7GB PDF with 8GB RAM). |
| **T006 / CIPH-16 — Legacy JSON→YAML migration** | WS-01 | Evan owns the converter for MedFirst's three legacy JSON pilot policies; a release dependency, but the build work itself is unblocked. |
| **T030 / CIPH-40 — Non-AGPL parser search** | WS-04 | The *search* can proceed (Charlie hunting an Apache/MIT-licensed alternative), but closure is Legal-gated — see §2. |

Also unblocked-but-parked: **T009 / CIPH-19 (JWT REST auth)** is a *deferral*, not a block — moved to v1.1 because v1.0.0 targets local single-machine usage; MedFirst IT renewal nonetheless requires REST auth no later than 2026-03-31. **T039 / CIPH-49 (a11y audit)** is superseded, folded into the CIPH-33 Preview UI overhaul.

---

## 2. Work that cannot progress until an external dependency moves

**Truly external (outside the team's control):**

- **T007 / CIPH-17 — Multi-page offset mismatch (WS-01).** Blocked on upstream `pdfminer.six` #992. Maintainer DM puts earliest realistic merge at **mid-October**. Charlie evaluated a local fork in late August; the team rejected maintaining a parser fork. As of Sept 10 the PR is still unmerged and no safe local workaround exists. A second gate stacks on top: any pre-normalization workaround needs **written Legal sign-off** in addition to the upstream merge.
- **T036 / CIPH-46 — High-DPI PDF rendering (WS-06).** Blocked in the `pdf-lib-core` C++ core's XObject coordinate math under parent transforms; Charlie states it cannot be patched locally and upstream maintainers have not responded to his issue. Coordinates drift 5–10px on 4K at 200% scaling. Scope is wider than the upstream bug: Diana's offline QA found **12% of the MedFirst pilot corpus** fails on nested Form XObjects. Open decision: ship with the limitation as a documented known issue, flatten PDFs (file-size/text-layer cost), or swap rendering libraries.
- **T029 signing leg (WS-06).** A **procurement** dependency, not an engineering one — Windows Defender/SmartScreen flags unsigned binaries; Evan: "this isn't something we can work around on the engineering side, we need the certificate." Alice is chasing the certificate process; budget and procurement timeline are open triage items.
- **T030 / CIPH-40 — License compliance (WS-04).** Escalated to **P0** on the Legal memo that AGPL in the bundle triggers whole-bundle copyleft exposure for the distribution model. Explicitly a **hard Legal gate — engineering library search alone cannot close it.**

**Blocked, but on internal resolution rather than an outside party** (worth separating, since they are on the blocker list but no third party needs to move):

- **T024 / CIPH-34 — Zero-trust node sync (WS-07).** Nominal-latency handshake validation passed, but the Sept 22 high-latency simulation times out. The deep-dive **declined a timeout-bump workaround pending encryption-path stabilization**, while the Singapore field trial (fails at 180ms RTT on the 5s prototype timeout) calls for a **30s** budget. That tension is flagged for manual triage: whether 30s resolves it without redesigning the handshake exchange count.
- **T037 / CIPH-47 — Async batch scheduler (WS-05).** Blocked on a concurrent manifest-write race where async workers share I/O with the existing multi-thread batch pool — ~10% throughput loss and possible JSON corruption. Alice halted further async work; Bob is holding; Diana captured repro steps for a candidate fix.
- **T019 / CIPH-29 — Offline mode authentication (WS-04).** Key rotation is impossible in a strictly air-gapped environment without a central authority. InfoSec **approved** a split master-key escrow (USB token at clinic + HQ HSM) and Bob is spiking it — the architecture is settled; it remains blocked only until built.

---

## 3. Release-checklist work gated on packaging and Windows signing

**T011 / CIPH-21 (Release v1.0 Gates, WS-03, owner Evan) is the gated item, and it is under a security-gate hold placed by Diana.**

- **Dependencies already satisfied:** T001–T006 and T010 are met (Core engine, financial regex, Batch CLI, REST API, Docker packaging *dependency slot*, policy config, security audit). The July 12 draft checklist recorded six of seven met with T005 the only unmet one at the time.
- **Still unmet — the two gates named in the acceptance criteria:** **T005** (Docker image size/CVE) and **T029** (Windows code-signing). CIPH-21's criteria state explicitly that the task remains Active pending both.
- **Hard deadline:** the release board set a **no-ship after 2026-10-15** if T005 and T029 are not green — recorded as a hard deadline, not advisory.
- **A third hold surfaced at the Sept 15 pre-release audit:** the **audit-log schema vs emitted-records mismatch (T016)**. Diana keeps that gate red until CLI-emitted records match the defined schema, because the mismatch undercuts the audit trail as release evidence. Alice's close: "Docker slim-down, Windows signing, and we keep the audit mismatch visible as a release blocker. No one closes those today." Upstream high-DPI (T036) was also listed as staying on the board.
- **Work proceeding in parallel despite the open gates:** release notes were drafted while gates stayed open (noted in CIPH-21). Evidence-pack assembly is otherwise complete on the security side — T010 closed with the CORS `*`-origin finding patched to configured `ALLOWED_ORIGINS`, re-scans confirmed on July 15, supplemented by the RedByte pen-test attestation letter dated 2026-07-11.
- **Two additional items explicitly tied to the T011 gate:** the MedFirst legacy JSON→YAML policy migration (T006) and the T031 large-file OOM pilot-blocker.

**Near-term actions named in the record:** secure the Authenticode certificate and finish Alpine/CVE Docker verification; decide whether the 30s handshake timeout budget can be tested without violating the encryption-path caution.

---

### Evidence

Work States (authoritative for status): `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/index.md`, `WS-01-engine.md`, `WS-02-api.md`, `WS-03-ops.md`, `WS-04-policy.md`, `WS-05-performance.md`, `WS-06-platforms.md`, `WS-07-storage.md` (all in `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/`).

Brief: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md`

Comments: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-06.md` (CMT-2026-06-001/002/003), `.../2026-08.md` (CMT-2026-08-001/002/003), `.../2026-09.md` (CMT-2026-09-001/002/003/004).

Sources: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-07-12-Release-Checklist.md` (SRC-GDOC-05); `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md`, `CIPH-15-Docker-Packaging.md`, `CIPH-39-Windows-Compatibility.md` (in `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/`); `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (SRC-MEET-10), `.../2026-09-22-Handshake-Protocol-Deep-Dive.md` (SRC-MEET-11); `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md` (SRC-SLACK-37), `.../2026-09-10-high-dpi-upstream-block.md` (SRC-SLACK-58), `.../2026-08-25-async-batch-io-race.md` (SRC-SLACK-61).
