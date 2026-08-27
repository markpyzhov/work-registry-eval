# Beyond Docker and Windows packaging, which compliance and audit items still hold v1.0.0 as of **2026-09-22**? For each, give current status, the concrete defect or risk, and whether engineering search alone can close it.

<!-- RESPONSE_START -->

## Answer

Beyond the Docker image (T005/CIPH-15) and Windows code-signing (T029) gates, **two compliance/audit items still hold CipherDoc v1.0.0** as of 2026-09-22 — both in WS-04 (Regulatory Compliance, Privacy, and Audits, P0, owners Alice/Diana), and both explicitly named as release holds.

### 1. T016 / CIPH-26 — Compliance Audit Trail Logs

**Current status:** Active / reopened, unchecked in the WS-04 task list; ClickUp CIPH-26 is Active (assignee Diana, Priority High). Diana has held the audit-log gate "red."

**Concrete defect:** The audit records the CLI actually emits do not validate against the defined companion JSON audit schema. The design requires, per processed file, a SHA-256 hash of the input stream paired with a JSON document recording the redaction map applied. Bob refactored the loader (2026-07-11), added SHA-256 input hashing (2026-08-05), defined the companion schema (2026-08-15), and wired audit-log generation into the CLI batch path (2026-09-10) — but Diana's 2026-09-18 verification pass found the emitted records inconsistent with the schema. The 2026-09-15 pre-release audit recorded the same: "the CLI path and the log records aren't matching the schema we defined," which "undercuts the audit trail as release evidence." Bob has another pass queued.

**Risk:** Without schema-conformant records, the audit trail cannot serve as release evidence — the compliance artifact exists but is not verifiable, so QA cannot clear the gate.

**Can engineering work alone close it?** Yes. This is purely an internal schema-versus-emitter alignment problem — Charlie explicitly confirmed in the pre-release audit that it is "not a packaging issue — it's schema versus emitted records." There is no external or legal dependency: Bob's queued pass plus Diana's re-verification is the whole closure path.

### 2. T030 / CIPH-40 — License Compliance Review

**Current status:** Active (Reopened), unchecked in WS-04; ClickUp CIPH-40 ("Audit third-party licenses before release," assignee Diana, Priority High) reopened 2026-08-12. Escalated to **P0**. WS-04 lists "finding a viable non-AGPL PDF parsing library" under Needs Manual Triage, and names license-search status as one of the two things needing the next update.

**Concrete defect:** The 2026-08-09 dependency inventory flagged **Ghostscript (AGPLv3)**, used by the `rasterizer` module for PDF-to-image conversion, as blacklisted for its viral copyleft terms on binaries distributed to partner sites. The team swapped in a replacement PDF parser on 2026-08-11 and briefly marked it Completed — but on 2026-08-12 the replacement turned out to be AGPL-licensed itself, reintroducing the same license category one layer down. Charlie is searching for an Apache 2.0 or MIT-licensed alternative that meets the rasterization requirement; as of the 2026-08-21 report no suitable replacement had been confirmed, and the retrospective explicitly states it "does not certify overall license compliance."

**Risk:** Per Diana's Legal memo (CMT-2026-08-002, 2026-08-12), **AGPL in the bundle triggers whole-bundle copyleft exposure for CipherDoc's distribution model** — client agreements rule out shipping copyleft code in the core engine. This is a distribution/legal-exposure risk, not just a dependency-hygiene issue.

**Can engineering search alone close it?** **No.** CMT-2026-08-002 is explicit: treat it as a **hard Legal gate — engineering search alone is insufficient to close T030**. Finding a permissively-licensed parser is necessary but not sufficient; Legal must clear the whole-bundle copyleft question.

**Secondary open item under the same audit:** Tesseract OCR itself is Apache 2.0, but the `eng.traineddata` model files were sourced from a community repository and their training-corpus provenance has not been verified as public-domain/CC0. Tracked as a separate, lower-priority open item pending Evan's trace of `tessdata_best` provenance — and it is a provenance-verification task, not something a library search resolves.

### Related open WS-04 items that are *not* recorded as release-gate holds

- **T014 / CIPH-24 (Manual Review Workflow for Low-Confidence OCR)** — Active. Quarantine folder, metadata (confidence/page/reason), and Charlie's visual UI indicators were exercised end-to-end on 2026-09-18, but the 90% confidence-threshold integration with metadata injection is still in progress. The 90% threshold is the adopted v1.0.0 decision; the dataset does not list this as a release-gate blocker.
- **T019 / CIPH-29 (Offline Mode Authentication)** — Blocked. Key rotation is impossible in a strictly air-gapped environment without a centralized authority; InfoSec approved a split master-key escrow design (USB token at clinic + HQ HSM) per CMT-2026-08-001 and Bob is spiking it, but it remains blocked until built. Not listed among the release gates.
- **T039 / CIPH-49 (a11y audit)** — Superseded by the Preview UI overhaul (CIPH-33); no longer a live item.
- Note for contrast: REST API auth (T009/CIPH-19) was explicitly **deferred to v1.1** and re-confirmed out of v1.0.0 scope on 2026-08-20.

### Sources used

`work-states/WS-04-policy.md`; `work-states/WS-03-ops.md`; `work-states/index.md`; `work-states/comments/2026-08.md` (CMT-2026-08-001, CMT-2026-08-002); `med-synth/tasks/CIPH-26-Audit-Trail-Logging.md`; `med-synth/tasks/CIPH-40-License-Compliance-Review.md`; `med-synth/tasks/CIPH-24-Manual-Review-Threshold.md`; `med-synth/tasks/CIPH-21-Release-v1-Gates.md`; `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (SRC-MEET-10); `med-synth/communication/sources/slack/2026-08-12-license-agpl-reopen.md` (SRC-SLACK-40); `med-synth/communication/sources/slack/2026-08-09-license-audit.md` (SRC-SLACK-39); `med-synth/documentation/sources/2026-08-21-License-Compliance-Audit-Report.md` (SRC-GDOC-41); `med-synth/documentation/sources/2026-08-21-License-Compliance-Review-Review.md` (SRC-GDOC-24); `med-synth/documentation/sources/2026-07-08-Compliance-Audit-Trail.md` (SRC-GDOC-11).
