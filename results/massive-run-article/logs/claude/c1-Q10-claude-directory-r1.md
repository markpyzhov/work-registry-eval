# Write a concise cross-workstream management briefing as of **2026-09-22** covering at least three workstreams: at least two completed milestones that still hold, at least three items of work that were completed then reopened, at least two durable blockers, and the top risks that should escalate before ship. Do not present reopened work as done.

<!-- RESPONSE_START -->

I have all the authoritative work states, comments, and provenance sources. Here is the briefing.

---

# CipherDoc — Cross-Workstream Management Briefing
**As of 2026-09-22** (Work State Index as-of timestamp `2026-09-22T12:00:00Z`)
Source of record: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/` (all seven work states last updated 2026-09-22)

## Portfolio snapshot

| WS | Area | Priority | Status | Headline |
|---|---|---|---|---|
| WS-01 | Detection & redaction engine | P0 | in_progress | T007 blocked upstream since June; OCR (T008) still active |
| WS-02 | REST API & Batch CLI | P1 | in_progress | Cleanest stream — no active work, no open blockers; T009 deferred |
| WS-03 | Packaging, release gating, security | P0 | in_progress | Hard **2026-10-15 no-ship** deadline; two gates still red |
| WS-04 | Compliance, privacy, audits | P0 | in_progress | P0 Legal AGPL gate + audit-log schema mismatch |
| WS-05 | Performance & memory | P1 | in_progress | Large-file chunking reopened; async scheduler blocked |
| WS-06 | Platforms & interfaces | P2 | in_progress | Windows held on cert procurement; High-DPI blocked upstream |
| WS-07 | Storage, encryption, node sync | P1 | in_progress | Node-sync handshake blocked; quota reopened |

*(`/c1/work-states/index.md`)*

---

## 1. Completed milestones that still hold

These are closed with evidence and are not in dispute. Safe to treat as banked.

- **T010 / CIPH-20 — Security audit and vulnerability scans (WS-03).** Medium-severity CORS `*` origin issue found in the 2026-07-06 scan was patched by restricting to configured `ALLOWED_ORIGINS`; re-scans on 2026-07-15 confirmed the patch holds. Backed by an external **RedByte pen-test attestation letter dated 2026-07-11**, now part of the release evidence pack. *(`work-states/WS-03-ops.md`; `CMT-2026-07-002` in `work-states/comments/2026-07.md`)*
- **T021 / CIPH-31 — AES-256 local encryption at rest (WS-07).** Redaction outputs encrypted with a machine-local AES-256 key; zero-leakage confirmed in a cold-start audit. *(`work-states/WS-07-storage.md`)*
- **T028 / CIPH-38 — Bare-metal performance benchmarks (WS-05).** Confirmed **500 pages/minute** on standard enterprise hardware. *(`work-states/WS-05-performance.md`)*
- **T027 / CIPH-37 — Air-gapped mode testing (WS-06).** 1,000 files processed end-to-end in a networking-disabled VM. *(`work-states/WS-06-platforms.md`)*
- **T020 / CIPH-30 — HIPAA PII pattern update (WS-04)** and **T032 / CIPH-42 — auditable redaction-profile schema export (WS-04)**, both merged and verified. *(`work-states/WS-04-policy.md`)*
- **T012 / CIPH-22 — CLI/API configuration parity (WS-02).** Worth noting because it is a *repaired* claim that now holds: an initial parity belief was disproved on 2026-07-09 when the CLI was found to ignore `custom_regex` flags; PR #52 fixed engine initialization and 2026-07-11 tests confirmed unified config loading. *(`work-states/WS-02-api.md`)*

**One caveat on a "done" item:** T006 / CIPH-16 (YAML policy loader) is complete, but MedFirst's three legacy JSON pilot policies must auto-migrate before production cutover. Evan owns the JSON→YAML converter, and that migration is an open **release dependency tied to the T011 gate** — the loader being merged does not clear it. *(`work-states/WS-01-engine.md`; `CMT-2026-06-001`)*

---

## 2. Work completed, then reopened — NOT done

Five items were declared complete and have since been reopened. All remain open as of 2026-09-22 and must not be counted toward release readiness.

1. **T005 / CIPH-15 — Docker packaging (WS-03).** Initially completed at ~800MB. **Reopened 2026-06-25** when Diana found OCR-dependency bundling had pushed the image to **2.1GB**. Evan applied multi-stage builds, swapped Ubuntu 22.04 → Alpine (with `gcompat` for glibc/musl), and stripped unused packages; as of **2026-08-12 the image still exceeds the ~450MB GA target and CVE verification is still failing**. Note the dual gate: an interim RC may ship at **800MB once CVE-clean**, GA target remains **~450MB** — do not conflate them. *(`work-states/WS-03-ops.md`; `med-synth/communication/sources/slack/2026-06-25-docker-size.md`; `CMT-2026-06-002`)*
2. **T030 / CIPH-40 — License compliance review (WS-04).** **Reopened 2026-08-12**: the PDF parser swapped in to clear an *earlier* audit finding turned out to be **AGPL-licensed**. Charlie is searching for an Apache/MIT alternative. Escalated to **P0** — this is now a hard Legal gate, not an engineering task. *(`work-states/WS-04-policy.md`; `med-synth/communication/sources/slack/2026-08-12-license-agpl-reopen.md`; `CMT-2026-08-002`)*
3. **T031 / CIPH-41 — Large-file stream chunking (WS-05).** Initial chunking landed, then **reopened 2026-08-18** when Bob found memory still leaking on files over 2GB during long batch runs — not the page buffers, something is holding references. Diana reproduced it in QA (process eventually killed). Charlie is refactoring stream-buffer release logic. Compounded by the **MedFirst pilot OOM on a 4.7GB PDF with 8GB RAM**, making this a pilot blocker explicitly tied to the T011 release gate. *(`work-states/WS-05-performance.md`; `med-synth/communication/sources/slack/2026-08-18-large-file-chunking-reopen.md`; `CMT-2026-08-003`)*
4. **T022 / CIPH-32 — Storage quota management (WS-07).** Diana verified and **called it done on 2026-08-06** (engine halts writes at the 500MB floor). **Reopened 2026-09-15** — production-like batches trip the hard halt before doing useful work. Bob refactored to a 10% buffer tolerance and Evan re-tested cleanly on 2026-09-18, but Ops capacity planning then **retargeted the production baseline from 500MB to 2GB free disk**, so the halt thresholds must be re-pointed and re-verified in clinic VMs. Still open. *(`work-states/WS-07-storage.md`; `med-synth/communication/sources/slack/2026-08-06-storage-quota-halt.md`; `CMT-2026-09-003`)*
5. **T016 / CIPH-26 — Compliance audit-trail logging (WS-04).** Loader refactor, SHA-256 hashing, schema definition, and CLI wiring all landed (through 2026-09-10), but the **2026-09-18 verification found CLI-emitted audit records inconsistent with the defined schema**. Diana is holding the audit gate red. Flagged at the 2026-09-15 pre-release audit as a release hold. *(`work-states/WS-04-policy.md`; `med-synth/tasks/CIPH-26-Audit-Trail-Logging.md`; `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md`)*

Also formally **superseded, not delivered**: T039 / CIPH-49 accessibility audit was folded into the CIPH-33 Preview UI overhaul, which natively covers high-contrast and keyboard navigation. *(`work-states/WS-04-policy.md`)*

---

## 3. Durable blockers (long-running, not self-clearing)

- **T007 / CIPH-17 — Multi-page PDF offset mismatch (WS-01). Blocked since June.** Depends on upstream `pdfminer.six` issue/PR **#992**; the maintainer's DM puts earliest realistic merge at **mid-October**. The team evaluated and **rejected** maintaining a parser fork, and as of 2026-09-10 the PR is still unmerged with no safe local workaround. A pre-normalization workaround requires **written Legal sign-off** on top of the upstream merge — a double gate outside engineering's control. *(`work-states/WS-01-engine.md`; `CMT-2026-06-003`)*
- **T019 / CIPH-29 — Offline mode authentication (WS-04). Blocked.** Key rotation is impossible in a strictly air-gapped environment without a central authority. InfoSec approved a split master-key escrow design (USB token at clinic + HQ HSM) on 2026-08-05 and Bob is spiking it — the architecture question is closed, but the item **stays blocked until it is actually built**. Escrow remains unimplemented as of today. *(`work-states/WS-04-policy.md`; `CMT-2026-08-001`)*
- **T024 / CIPH-34 — Zero-trust node sync handshake (WS-07). Blocked.** Nominal-latency validation passed, but the handshake never completes on high-latency links. At today's deep dive the team **explicitly declined a timeout bump** ("bumping timeouts just hides it") and left the work blocked pending encryption-path stabilization. *(`work-states/WS-07-storage.md`; `med-synth/communication/sources/fireflies/2026-09-22-Handshake-Protocol-Deep-Dive.md`)*
- **T036 / CIPH-46 — High-DPI PDF rendering (WS-06). Blocked upstream.** Redaction coordinates drift 5–10 pixels on 4K displays at 200% scaling, rooted in the upstream rendering library's scaling math. Scope has since widened: offline QA found **12% of the MedFirst pilot corpus fails due to nested Form XObjects**, which an upstream scaling fix alone may not cover. *(`work-states/WS-06-platforms.md`; `CMT-2026-09-001`)*
- **T037 / CIPH-47 — Async batch scheduler (WS-05). Blocked.** A concurrent manifest-write race cuts throughput ~10% and **can corrupt JSON under load**. *(`work-states/WS-05-performance.md`)*
- **T029 / CIPH-39 — Windows compatibility (WS-06). Held, not engineering-blocked.** Path/backslash handling is fixed; the hold is that Windows Defender SmartScreen flags unsigned binaries until an **Authenticode certificate is procured**. This is a procurement and budget dependency — engineering cannot burn it down. *(`work-states/WS-06-platforms.md`)*

---

## 4. Top risks to escalate before ship

**R1 — The 2026-10-15 no-ship deadline is 23 days out and both gating items are red.** The release board set a **hard** (explicitly not advisory) no-ship after 2026-10-15 if **T005** (Docker size/CVE) and **T029** (Windows signing) are not green. T005 has been reopened since June with the CVE scan still failing as of 2026-08-12; T029 waits on a certificate that has **no confirmed budget or procurement timeline**. Escalate procurement immediately — it is the item least likely to move on engineering effort alone. *(`work-states/WS-03-ops.md`; `CMT-2026-09-002`; `med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md`)*

**R2 — The AGPL exposure is a P0 legal risk that engineering cannot close.** Legal's memo states AGPL in the bundle triggers **whole-bundle copyleft exposure for our distribution model**. A library search alone is insufficient to close T030. Needs a Legal-owned decision path and a named date, not a parallel engineering search. *(`CMT-2026-08-002`; `work-states/WS-04-policy.md`)*

**R3 — Compliance evidence is not yet trustworthy.** The audit trail is the release evidence for a HIPAA-adjacent product, and its CLI-emitted records still fail schema validation (T016). Diana's position is unambiguous: the gate stays red until schema and records match. Shipping with a broken audit trail is a compliance risk, not just a QA defect. *(`med-synth/tasks/CIPH-26-Audit-Trail-Logging.md`; `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md`)*

**R4 — Two unresolved contradictions require management triage, not engineering iteration.**
- *Node sync (T024):* the Singapore field trial demands a **30s timeout budget** at 180ms RTT, while today's deep dive **refused any timeout bump** pending encryption-path work. These directives conflict; someone must decide whether the 30s budget can be tested without violating the encryption-path caution, or whether the handshake exchange count needs redesign. *(`CMT-2026-09-004` vs. `med-synth/communication/sources/fireflies/2026-09-22-Handshake-Protocol-Deep-Dive.md`)*
- *High-DPI (T036):* decide local engine-side workaround vs. upstream-only for the nested Form XObject subset. Waiting on upstream leaves 12% of the pilot corpus failing. *(`CMT-2026-09-001`)*

**R5 — MedFirst pilot exposure is concentrated and compounding.** The pilot is simultaneously exposed to the T031 OOM on large PDFs, the 12% High-DPI Form XObject failures, the unmigrated legacy JSON policies under T006, and the T019 air-gapped auth gap. Any one of these can stall the pilot; together they are the single largest customer-facing risk. *(`CMT-2026-08-003`, `CMT-2026-09-001`, `CMT-2026-06-001`, `CMT-2026-08-001`)*

**R6 — Upstream timing collides with the ship date.** T007's earliest realistic upstream merge is **mid-October**, effectively coincident with the 2026-10-15 no-ship date, and the only alternative path requires written Legal sign-off. Plan for T007 not landing in v1.0.0. *(`CMT-2026-06-003`)*

**R7 — A contract commitment sits outside the v1.0 plan and its recorded date needs confirmation.** JWT auth (T009) is deferred to v1.1, but MedFirst's IT renewal is recorded as requiring REST authentication "no later than **2026-03-31**" — a date that has already elapsed relative to today. Either the commitment is already in breach or the recorded date is wrong; confirm with Bob/Alice before the release board meets. *(`CMT-2026-07-001`; `work-states/WS-02-api.md`)*

---

## Recommended escalation order

1. **Windows Authenticode certificate procurement** (R1) — longest lead time, entirely non-engineering, and one of two hard gates.
2. **Legal decision path on AGPL / T030** (R2) — P0, and no amount of engineering search closes it.
3. **Docker slim + CVE burn-down against the RC-vs-GA dual gate** (R1) — confirm whether the 800MB CVE-clean RC threshold is an acceptable ship posture, which may materially de-risk the deadline.
4. **T016 audit schema alignment** (R3) — engineering-tractable, and it unblocks the compliance evidence pack.
5. **Adjudicate the T024 and T036 contradictions** (R4) — both are stalled on a decision, not on effort.

**Bottom line:** WS-02 is effectively clean and several security, encryption, benchmark, and air-gapped milestones are genuinely banked. But the two P0 streams that gate release (WS-03, WS-04) each carry a reopened item plus a dependency outside engineering's control, and five previously-"done" items are back open. The 2026-10-15 date is not currently defensible without a decision on the RC size threshold and immediate movement on certificate procurement and the Legal AGPL gate.
