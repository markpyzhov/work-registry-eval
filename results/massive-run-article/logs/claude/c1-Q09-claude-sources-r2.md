# Beyond Docker and Windows packaging, which compliance and audit items still hold v1.0.0 as of **2026-09-22**? For each, give current status, the concrete defect or risk, and whether engineering search alone can close it.

<!-- RESPONSE_START -->

## Compliance and audit items still holding v1.0.0 as of 2026-09-22 (beyond Docker T005 and Windows packaging/signing T029)

Four items in the assigned dataset are still open. None of them shows a status change after the dates noted below, so as of 2026-09-22 each stands as described.

---

### 1. Audit-trail logging — CIPH-26 / T016 (Diana, High)

**Current status:** Active. Still an explicit release blocker. Last event: 2026-09-18, Diana "Audit Verify (Mismatch)".

**Concrete defect:** The audit system computes a SHA-256 hash per input stream plus a companion JSON redaction map, and Bob wired audit-log generation into the CLI batch path on 2026-09-10. Verification found that the audit records the CLI actually emits do not validate against the defined companion JSON schema. At the 2026-09-15 pre-release audit Diana was explicit that this is not a packaging problem — it is "schema versus emitted records" — and that the mismatch "undercuts the audit trail as release evidence." She is holding the audit gate red until schema and records match; Bob has another pass queued.

**Can engineering close it alone?** Yes. This is entirely internal: reconcile the emitter with the defined schema (or the schema with the emitter) and re-run Diana's validation. No third party, procurement, or upstream dependency is involved.

---

### 2. Third-party license compliance audit — CIPH-40 / DOC-2041, DOC-2024 (Diana, High)

**Current status:** Active (Reopened) since 2026-08-12. Last substantive update 2026-08-15 (search still unconcluded); report written up 2026-08-21.

**Concrete defect:** The original audit flagged Ghostscript (AGPLv3, used by the `rasterizer` module for PDF-to-image conversion) as blacklisted because its viral copyleft terms apply to any binary distributed to partner sites. Evan swapped in a replacement parser on 2026-08-11 and marked it done; on 2026-08-12 Diana reopened the task after checking the replacement's license file directly — the replacement is *also* AGPL-licensed. The swap moved the same license category problem one layer down. Client agreements rule out shipping copyleft in the core engine, so the shipped dependency set is currently non-compliant.

**Can engineering search alone close it?** Not demonstrated — and this is precisely where searching has already stalled. Charlie has been searching for an Apache 2.0 / MIT alternative since 2026-08-15; he found "a couple" of candidates but "neither one covers everything the old library did," and he declined to force a bad fit. Closing it needs either a candidate that actually meets the rasterization feature requirements (search may never produce one), or a scope/rework decision — Charlie explicitly could not estimate the rework cost of another swap without comparing candidates. The audit report carries a standing warning: do not report license compliance as resolved externally.

---

### 3. OCR training-data provenance (`eng.traineddata` / `tessdata_best`) — secondary item under the same license audit

**Current status:** Open, separate and lower-priority, pending Evan's provenance trace. Unchanged as of the 2026-08-21 report.

**Concrete risk:** Tesseract OCR itself is Apache 2.0, but the `eng.traineddata` model files were pulled from a community repository and their training-corpus provenance has not been verified as public-domain/CC0. Until traced, the shipped model files have unknown licensing on their training data.

**Can engineering search alone close it?** No. Codebase search cannot establish provenance — this requires tracing the `tessdata_best` upstream sourcing and training corpus outside the repo, and a licensing judgement on what is found. It is an external investigation, not an engineering lookup.

---

### 4. Telemetry opt-out — Sentry crash-reporter path unaudited — DOC-2051 (Diana, last updated 2026-09-06)

**Current status:** Partially closed. The CLI-side opt-out is verified Completed (network trace on 2026-08-24 confirmed zero outbound telemetry with the flag set; CIPH-48 is Completed). The crash-reporter path is not.

**Concrete risk:** The third-party Electron crash reporter (Sentry) has never been audited for whether it independently respects the opt-out environment variable or requires its own separate disable hook for minidump uploads. The document states flatly that full privacy compliance for air-gapped/opt-out users cannot be claimed until that path is audited separately. Related design context: a pending-queue leak was already found and patched during design (the `TelemetryLogger` kept writing event payloads to a local SQLite queue while opted out, so re-enabling telemetry would have flushed a backlog the user believed was never recorded) — evidence that the opt-out surface has had non-obvious gaps.

**Can engineering search alone close it?** Partly, but not by search alone. It needs an actual behavioural audit of the Sentry integration — instrumenting/tracing the minidump upload path with the opt-out set — plus, if it does not honour the variable, wiring a dedicated disable hook. That is empirical verification and possibly vendor-documentation work, not a code search.

---

### Adjacent hardening item worth flagging (not a formal gate)

**Argon2id passphrase-derived key hardening** — recorded at the AES-256 at-rest crypto sign-off (DOC-2035, 2026-08-07) as a **pre-v1.0 hardening item tracked separately**, explicitly *not* a sign-off condition. On machines without a hardware TPM the volume key is still derived from a user passphrase via PBKDF2-HMAC-SHA256 at 100k iterations; Diana flagged that moving to Argon2id would meaningfully raise the cost of offline brute-force against weak passphrases on non-TPM hardware. No later status appears in the dataset. This is closable by engineering alone (a KDF implementation change), but the sources do not show it blocking the release gate.

### Two "certification" caveats that limit what can be claimed at release

- The **air-gapped/offline batch sign-off** (DOC-2047, CIPH-37, Completed 2026-08-10) is explicitly **preliminary only and not a compliance certification** — it does not cover side-channel analysis, physical security, or any regulatory attestation, and it carries a known 45-second remote licence-check hang.
- The **HIPAA pattern verification report** (DOC-2034, 2026-08-08) confirms only the merge and a regression check against the financial-PII baseline. It is explicitly **not a HIPAA compliance certification** and does not assess coverage completeness against every HIPAA identifier category in production data.

These are not open gates, but they mean no HIPAA or air-gap compliance claim is currently supported by the evidence pack.

---

### Not counted here

For completeness: the other items open at the 2026-09-15 pre-release audit are engineering/upstream, not compliance-audit — the high-DPI coordinate scaling bug (T036, Blocked on upstream rendering-library scaling math, DOC-2049) and the pdfminer.six offset-mismatch fix (blocked on unmerged upstream PR #992, with the team declining to fork). REST API authentication is Deferred to v1.1 by decision, reconfirmed 2026-08-20, on a trusted-local-network assumption — not a blocker.

**Sources cited:** SRC-CU-CIPH-26 (`med-synth/tasks/CIPH-26-Audit-Trail-Logging.md`); SRC-MEET-10 (`med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md`); SRC-GDOC-11 (`med-synth/documentation/sources/2026-07-08-Compliance-Audit-Trail.md`); SRC-CU-CIPH-40 (`med-synth/tasks/CIPH-40-License-Compliance-Review.md`); SRC-GDOC-41 (`med-synth/documentation/sources/2026-08-21-License-Compliance-Audit-Report.md`); SRC-GDOC-24 (`med-synth/documentation/sources/2026-08-21-License-Compliance-Review-Review.md`); SRC-SLACK-40 (`.../slack/2026-08-12-license-agpl-reopen.md`); SRC-SLACK-41 (`.../slack/2026-08-11-license-parser-swap.md`); SRC-SLACK-39 (`.../slack/2026-08-09-license-audit.md`); SRC-MEET-08 (`.../fireflies/2026-08-15-Windows-License-Sync.md`); SRC-GDOC-51 (`med-synth/documentation/sources/2026-09-06-Telemetry-Opt-Out-Design-and-Compliance-Check.md`); SRC-CU-CIPH-48 (`med-synth/tasks/CIPH-48-Telemetry-Opt-Out.md`); SRC-SLACK-64 (`.../slack/2026-08-24-telemetry-opt-out-verify.md`); SRC-GDOC-35 (`med-synth/documentation/sources/2026-08-07-Local-Encryption-at-Rest-Security-Evaluation.md`); SRC-GDOC-47 (`med-synth/documentation/sources/2026-08-10-Air-Gapped-Mode-Offline-Signoff.md`); SRC-GDOC-34 (`med-synth/documentation/sources/2026-08-08-PII-Pattern-HIPAA-Verification-Report.md`); SRC-CU-CIPH-21 (`med-synth/tasks/CIPH-21-Release-v1-Gates.md`); SRC-GDOC-39 (`med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md`); SRC-GDOC-49 (`med-synth/documentation/sources/2026-09-10-High-DPI-PDF-Rendering-Coordinates-Report.md`); SRC-SLACK-07 (`.../slack/2026-06-26-blocked-on-upstream.md`); SRC-SLACK-08 (`.../slack/2026-06-28-defer-auth.md`).
