# Beyond Docker and Windows packaging, which compliance and audit items still hold v1.0.0 as of **2026-09-22**? For each, give current status, the concrete defect or risk, and whether engineering search alone can close it.

<!-- RESPONSE_START -->

## Compliance and audit items still holding v1.0.0 as of 2026-09-22

Beyond T005 (Docker image size/CVE) and T029 (Windows code-signing), **two** compliance/audit items are release-holding, and both sit in **WS-04 (Regulatory Compliance, Privacy, and Audits — P0, owners Alice/Diana)**.

---

### 1. T016 / CIPH-26 — Compliance Audit Trail Logs

**Current status:** Active (reopened). Named an explicit release hold at the 2026-09-15 pre-release audit, and carried in WS-03/T011 as one of the three open blockers on the v1.0.0 release gate alongside Docker and Windows signing.

**Concrete defect:** The audit-log design (DOC-2011, SRC-GDOC-11) requires each processed file to emit a SHA-256 hash of the input stream paired with a companion JSON document recording the redaction map applied. Bob refactored the loader (2026-07-11), added SHA-256 input hashing (2026-08-05), defined the companion JSON schema (2026-08-15), and wired audit-log generation into the CLI batch path (2026-09-10). On **2026-09-18 Diana's verification pass found the CLI-emitted audit records do not validate against the defined schema** — the shape coming out of the CLI is inconsistent with what the schema expects. Charlie confirmed in the 09-15 audit that this is not a packaging problem but specifically schema-versus-emitted-records. Diana's position: the mismatch "undercuts the audit trail as release evidence," and she is holding the audit gate red until schema and records match.

**Risk:** Without validating records, there is no defensible audit trail to present as release evidence for a PII/PHI redaction product.

**Can engineering search alone close it?** **Yes — this is purely an engineering fix.** No external party, legal opinion, or procurement is in the loop. Bob already has another alignment pass queued; once emitted records validate against the companion JSON schema, Diana's verification clears the gate. It is bounded to the CLI emission path and the schema definition.

---

### 2. T030 / CIPH-40 — License Compliance Review (third-party licenses before release)

**Current status:** Active (Reopened), escalated to **P0**. Assignee Diana; Charlie running the library search. Listed in WS-04 "Needs Manual Triage" as the outstanding item.

**Concrete defect:** The 2026-08-09 dependency inventory (DOC-2041) flagged **Ghostscript (AGPLv3)**, used by the `rasterizer` module for PDF-to-image conversion, as blacklisted for its viral copyleft terms on binaries distributed to partner sites. The team swapped in a replacement PDF parser on 2026-08-11 and briefly marked it Completed — then reopened the task on **2026-08-12** when the replacement parser turned out to be **AGPL-licensed itself**. The swap fixed the specific Ghostscript dependency but reintroduced the same license category one layer down. As of the 2026-08-21 retrospective, no suitable Apache-2.0 or MIT alternative meeting the rasterization requirements had been confirmed.

**Risk:** Per Diana's Legal memo (CMT-2026-08-002, 2026-08-12), **AGPL in the bundle triggers whole-bundle copyleft exposure for CipherDoc's distribution model** — i.e. shipping would expose the entire product bundle, not just the offending module. Acceptance criteria require that no restrictive copyleft licenses remain in the shipped dependency set.

**Can engineering search alone close it?** **No — explicitly not.** CMT-2026-08-002 records this as a **hard Legal gate**: "engineering search alone is insufficient to close T030." Finding a permissively licensed parser is necessary but not sufficient; Legal must clear the bundle's copyleft exposure. This is the key asymmetry between the two items.

**Secondary open item under the same audit (lower priority, not currently a release hold):** Tesseract OCR is itself Apache-2.0, but the `eng.traineddata` model files were sourced from a community repository and their **training-corpus provenance has not been verified as public-domain/CC0**. Tracked pending Evan's trace of the `tessdata_best` provenance. This is a provenance/documentation trace rather than a code change, so engineering search alone also cannot definitively close it — it depends on what upstream provenance records exist.

---

### Related WS-04 items that are open but are *not* named as v1.0.0 holds

- **T014 / CIPH-24 (Manual Review Workflow for Low-Confidence OCR)** — Active. Quarantine folder, metadata (confidence/page/reason), and Charlie's visual UI indicators were exercised end-to-end on 2026-09-18, but the 90% confidence-threshold integration with metadata injection is still in progress. The 90% threshold is the adopted v1.0.0 decision. Not flagged as a release hold in the pre-release audit.
- **T019 / CIPH-29 (Offline Mode Authentication)** — Blocked. InfoSec approved a split master-key escrow design (USB token at clinic + HQ HSM) per CMT-2026-08-001; Bob is spiking implementation. Key rotation remains impossible in a strictly air-gapped environment without a centralized authority. The architecture is settled — it is blocked on being built, not on an open question.
- **T039 / CIPH-49 (Accessibility a11y Audit)** — **Superseded**, not a hold. Folded into the Preview UI overhaul (CIPH-33), which natively covers high-contrast and keyboard navigation.
- **Completed and not blocking:** T013 (export vs internal review policies), T015 (batch fail-closed, QA-validated 2026-07-16), T017 (overlapping policy conflicts), T020 (HIPAA PII patterns), T032 (auditable redaction-profile schema export), T038 (telemetry opt-out, verified by offline network trace). T010 (security audit/vulnerability scans, WS-03) is also Completed — the medium-severity CORS `*` origin finding was patched to configured `ALLOWED_ORIGINS` and re-scans on 2026-07-15 confirmed the patch, with a RedByte pen-test attestation letter (2026-07-11) in the evidence pack.

---

### Timing context

The release board set a **hard no-ship after 2026-10-15** if T005 and T029 are not green (CMT-2026-09-002, Diana, 2026-09-15 — explicitly "hard deadline, not advisory"). Note the deadline language names only T005 and T029; T016 and T030 are tracked as holds through the audit gate and the Legal P0 gate respectively rather than through that deadline clause. Of the two compliance items, **T030 carries the longer tail** — its Legal dependency means it cannot be resolved on engineering velocity alone, whereas T016 is a bounded schema-alignment fix already in flight.

**Sources used:** `work-states/WS-04-policy.md`, `work-states/WS-03-ops.md`, `work-states/index.md`, `work-states/comments/2026-08.md` (CMT-2026-08-002, CMT-2026-08-001), `work-states/comments/2026-09.md` (CMT-2026-09-002), `med-synth/tasks/CIPH-26-Audit-Trail-Logging.md`, `med-synth/tasks/CIPH-40-License-Compliance-Review.md`, `med-synth/tasks/CIPH-24-Manual-Review-Threshold.md`, `med-synth/tasks/CIPH-21-Release-v1-Gates.md`, `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (SRC-MEET-10), `med-synth/documentation/sources/2026-08-21-License-Compliance-Audit-Report.md` (DOC-2041), `med-synth/documentation/sources/2026-08-21-License-Compliance-Review-Review.md` (DOC-2024), `med-synth/documentation/sources/2026-07-08-Compliance-Audit-Trail.md` (DOC-2011).
