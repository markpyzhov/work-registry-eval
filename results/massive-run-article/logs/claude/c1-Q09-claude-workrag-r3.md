# Beyond Docker and Windows packaging, which compliance and audit items still hold v1.0.0 as of **2026-09-22**? For each, give current status, the concrete defect or risk, and whether engineering search alone can close it.

<!-- RESPONSE_START -->

## Answer

As of the 2026-09-22 work-state snapshot, setting aside T005 (Docker size/CVE) and T029 (Windows code-signing), **two compliance/audit items are explicitly holding v1.0.0**, with two further open WS-04 items that are in scope for v1.0.0 but not named as release gates.

### 1. T016 / CIPH-26 — Compliance Audit Trail Logging (the audit gate)

- **Current status:** Active/reopened, P0 area (WS-04), assignee Diana, task priority High. Explicitly an **open release blocker**. Diana's position at the 2026-09-15 pre-release audit: the audit-log gate stays red until schema and records match.
- **Concrete defect:** The audit records **emitted by the CLI do not validate against the defined companion JSON schema**. The design requires each processed file to produce a SHA-256 hash of the input stream plus a companion JSON document recording the redaction map applied. Bob refactored the loader for streaming (2026-07-11), added SHA-256 hashing (2026-08-05), defined the audit schema (2026-08-15), and wired generation into the CLI batch path (2026-09-10) — but Diana's 2026-09-18 verification pass found the emitted shape inconsistent with the schema. Bob has another pass queued.
- **Risk:** The mismatch undercuts the audit trail as release evidence — the artifact intended to prove redaction provenance cannot be validated, so the compliance evidence pack is not defensible.
- **Can engineering close it alone?** **Yes.** This is purely an internal schema-vs-emitter alignment problem, with no external or legal dependency. Diana explicitly framed it at the pre-release audit as "not a packaging issue — it's schema versus emitted records." Once the CLI output validates cleanly, the gate clears.

### 2. T030 / CIPH-40 — Third-Party License Compliance Review (the legal gate)

- **Current status:** Active (Reopened), escalated to **P0** on 2026-08-12. Assignee Diana; Charlie doing the library search. Listed under WS-04 "Needs Manual Triage": finding a viable non-AGPL PDF parsing library.
- **Concrete defect:** The 2026-08-09 dependency-tree inventory flagged the PDF-parsing dependency's license. The team swapped in a replacement parser on 2026-08-11, then reopened the task on 2026-08-12 when **the replacement parser itself turned out to be AGPL-licensed**. Acceptance criteria require no restrictive copyleft in the shipped dependency set and an adopted Apache/MIT alternative; neither is satisfied. The retrospective license inventory report explicitly states it **does not certify overall license compliance** — the parser-license question remains open.
- **Risk:** Diana's legal memo (CMT-2026-08-002, 2026-08-12): **AGPL in the bundle triggers whole-bundle copyleft exposure for the distribution model** — i.e., shipping would expose the entire product bundle to copyleft obligations.
- **Can engineering search alone close it?** **No — explicitly not.** CMT-2026-08-002 directs that this be treated as a **hard Legal gate**, stating "engineering search alone is insufficient to close T030." Finding an Apache/MIT parser is necessary but not sufficient; written Legal clearance is required. (A related precedent: on T007, the pdfminer.six pre-normalization workaround was likewise made contingent on written Legal sign-off.)

### Also open in WS-04, but not designated release-gate holds in the record

- **T014 / CIPH-24 — Manual Review Workflow for Low-Confidence OCR.** Active, assignee Diana. The quarantine folder, quarantine metadata (confidence, page, reason) and Charlie's UI indicators are built, and a 2026-09-18 end-to-end pass (detection → quarantine → metadata → UI markers → manual approval) held together — but the **90% confidence-threshold integration/tuning is still in progress**; Diana wants another round of testing before calling it locked. The 90% threshold is a decision adopted **for v1.0.0**, so the item is in-scope for the release. Risk: an untuned threshold means low-confidence redactions may escape quarantine and be exported without human confirmation. **Closable by engineering alone** (threshold tuning plus test rounds).
- **T019 / CIPH-29 — Offline Mode Authentication.** **Blocked.** Key rotation is impossible in a strictly air-gapped environment without a centralized authority; local rotation mockups exist only. InfoSec approved a split master-key escrow design (USB token at clinic + HQ HSM) per CMT-2026-08-001, and Bob is spiking implementation, but it **remains Blocked until built**. Not engineering-search-closable in the T030 sense — it needs implementation of an approved architecture, and the architecture question itself already required an InfoSec decision.

### Items that are *not* holding the release (to avoid false positives)

- **T010 / CIPH-20 (security audit and vulnerability scans)** — Completed. The medium-severity CORS `*` origin finding was patched to configured `ALLOWED_ORIGINS`, re-verified 2026-07-15, with the RedByte pen-test attestation letter (2026-07-11) in the evidence pack.
- **T013, T015, T017, T020, T032, T038** — all Completed (export/internal-review policy matrix; fail-closed batch with atomic rename and secure temp deletion; overlapping-policy conflict resolution; HIPAA dictionary; auditable redaction-profile JSON export; telemetry opt-out verified via offline network trace).
- **T039 / CIPH-49 (accessibility a11y audit)** — **Superseded**, folded into the Preview UI overhaul (CIPH-33), which natively covers high-contrast and keyboard navigation. Not a blocker.
- **T009 / CIPH-19 (REST auth)** — Deferred to v1.1; v1.0.0 assumes a trusted local network, reconfirmed 2026-08-20. Note the separate contractual constraint (CMT-2026-07-001): MedFirst's enterprise renewal requires REST authentication no later than 2026-03-31 — a roadmap obligation, not a v1.0.0 gate.

### Bottom line

Of the compliance and audit items, **T016 (audit-log schema mismatch) and T030 (AGPL license exposure) are the two holding v1.0.0**. They differ in a way that matters for planning: T016 is fully within engineering's control and closes when the CLI-emitted records validate against the schema; **T030 cannot be closed by engineering search alone** — even a clean Apache/MIT parser leaves a hard Legal gate to clear. Both stack on top of the T005/T029 security-gate hold, against a release-board hard no-ship date of **2026-10-15** (CMT-2026-09-002) if T005 and T029 are not green.

**Dataset records cited:** `work-states/WS-04-policy.md`; `work-states/WS-03-ops.md`; `work-states/index.md`; `work-states/comments/2026-08.md` (CMT-2026-08-001, CMT-2026-08-002); `work-states/comments/2026-09.md` (CMT-2026-09-002); `work-states/comments/2026-07.md` (CMT-2026-07-001, CMT-2026-07-002); `med-synth/tasks/CIPH-26-Audit-Trail-Logging.md`; `med-synth/tasks/CIPH-40-License-Compliance-Review.md`; `med-synth/tasks/CIPH-24-Manual-Review-Threshold.md`; `med-synth/tasks/CIPH-21-Release-v1-Gates.md`; `med-synth/tasks/CIPH-20-Security-Audit.md`; `med-synth/documentation/sources/2026-07-08-Compliance-Audit-Trail.md`; `med-synth/documentation/sources/2026-08-21-License-Compliance-Review-Review.md`; `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md`; `med-synth/communication/sources/slack/2026-06-28-manual-review-threshold.md`; `med-synth/communication/sources/slack/2026-06-28-defer-auth.md`.
