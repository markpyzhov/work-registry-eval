# Beyond Docker and Windows packaging, which compliance and audit items still hold v1.0.0 as of **2026-09-22**? For each, give current status, the concrete defect or risk, and whether engineering search alone can close it.

<!-- RESPONSE_START -->

## Compliance and audit items still holding CipherDoc v1.0.0 (as of 2026-09-22, excluding Docker/T005 and Windows packaging/T029)

Work-state as-of timestamp: 2026-09-22T12:00:00Z (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/index.md`).

### 1. T016 / CIPH-26 — Compliance Audit Trail Logs — **the third named release gate**

- **Status**: Open, **Active/Reopened**; explicitly held "red" by QA. Named alongside Docker and Windows signing as an open blocker in the 2026-09-15 pre-release audit.
- **Defect**: The audit records the CLI actually emits do **not validate against the defined companion JSON schema**. The design pairs a SHA-256 hash of each input stream with a JSON redaction map; Bob refactored the loader (2026-07-11), added SHA-256 hashing (2026-08-05), defined the schema (2026-08-15), and wired generation into the CLI batch path (2026-09-10), but Diana's 2026-09-18 verification found the emitted shape inconsistent with the schema. Charlie confirmed in the audit meeting that this is schema-vs-emitted-records, **not** a packaging problem.
- **Risk**: An audit trail that fails its own schema is unusable as release evidence — Diana: it "undercuts the audit trail as release evidence." Gate stays red until records and schema match.
- **Can engineering close it alone?** **Yes.** Purely an implementation/verification loop — Bob has another pass queued, then Diana re-verifies. No legal or external sign-off involved.
- Evidence: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-26-Audit-Trail-Logging.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-07-08-Compliance-Audit-Trail.md`

### 2. T030 / CIPH-40 — License Compliance Review — **P0 Legal gate**

- **Status**: Open, **Active (Reopened)** since 2026-08-12; escalated to P0. Still listed as an open P0 Legal gate in the 2026-09-22 brief.
- **Defect**: The original audit flagged Ghostscript (AGPLv3, used by the `rasterizer` module for PDF-to-image conversion) as blacklisted. The team swapped in a replacement PDF parser and marked it complete — but the **replacement is itself AGPL-licensed**, reintroducing the same license category one layer down. Charlie has been searching for an Apache 2.0/MIT alternative since 2026-08-15; **no suitable replacement confirmed**.
- **Risk**: Legal memo (2026-08-12) holds that AGPL in the bundle triggers **whole-bundle copyleft exposure** for CipherDoc's distribution model to partner sites. The audit report carries an explicit warning not to report license compliance as resolved externally.
- **Can engineering close it alone?** **No — explicitly not.** CMT-2026-08-002 states engineering library search alone is insufficient; this is a hard Legal gate. Finding a clean parser is necessary but not sufficient — Legal must clear the bundle. This item is also flagged under "Needs Manual Triage."
- Evidence: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-08.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-40-License-Compliance-Review.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-21-License-Compliance-Audit-Report.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-12-license-agpl-reopen.md`

### 3. Tesseract `eng.traineddata` provenance — secondary open license item

- **Status**: Open, lower priority, pending Evan's trace of `tessdata_best` provenance. Tracked in the license audit report rather than as its own work-state task.
- **Defect**: Tesseract OCR itself is Apache 2.0, but the `eng.traineddata` model files were pulled from a community repository and their **training-corpus provenance has not been verified as public-domain/CC0**.
- **Risk**: Unverified provenance on shipped model data; the audit report's warning couples it with the parser issue as a reason not to declare license compliance resolved externally.
- **Can engineering close it alone?** **No.** It requires a provenance trace back to the upstream corpus and a licensing determination on what that trace turns up — a code/dependency search cannot establish corpus origin.
- Evidence: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-21-License-Compliance-Audit-Report.md`

### 4. T019 / CIPH-29 — Offline Mode Authentication (air-gapped) — **Blocked**

- **Status**: **Blocked**, open, High priority. Listed as a waiting-on item in the 2026-09-22 brief ("Escrow still unimplemented").
- **Defect**: Key rotation cannot complete in a strictly air-gapped environment without a centralized authority; local rotation mockups exist but testing against the auth mock showed rotation depends on network access. InfoSec approved a split master-key escrow design (USB token at clinic + HQ HSM) on 2026-08-05 and Bob began a spike, but it remains **unbuilt**.
- **Risk**: Air-gapped clinic deployments would ship without a working offline auth/key-rotation path — a privacy/security control gap for the exact deployment model CipherDoc targets.
- **Can engineering close it alone?** **Yes, at this point.** The design question is settled (InfoSec already approved the escrow architecture); what remains is implementation. It was an open architectural question before 2026-08-05, but is now engineering execution only.
- Evidence: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-08.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-29-Offline-Mode-Authentication.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-04-offline-auth-mock-block.md`

### 5. T014 / CIPH-24 — Manual Review Workflow for Low-Confidence OCR

- **Status**: Open, **Active**. The 90% confidence threshold was adopted for v1.0.0, so the policy decision is made; the code is not finished.
- **Defect**: Quarantine folder, quarantine metadata (confidence, page, reason), and Charlie's visual UI indicators were exercised end-to-end on 2026-09-18, but **90% threshold logic is still being integrated** with the metadata/quarantine path.
- **Risk**: Without the threshold wired in, low-confidence OCR pages can pass through unquarantined — redactions on scanned documents ship without the mandated human-review backstop.
- **Can engineering close it alone?** **Yes.** Integration work plus QA; no external gate.
- Evidence: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-24-Manual-Review-Threshold.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-06-28-manual-review-threshold.md`

### Adjacent item with a Legal dependency (not a WS-04 compliance task)

- **T007 / CIPH-17 — multi-page offset mismatch**: Blocked on upstream `pdfminer.six` #992 (maintainer says mid-October earliest). The pre-normalization workaround is acceptable **only with written Legal sign-off**, so Legal is an explicit dependency alongside upstream. Engineering cannot unilaterally ship the workaround; a local fork was evaluated and rejected. Evidence: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-01-engine.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-06.md`.

### Compliance/audit items that are NOT holding the release

- **T010 / CIPH-20 Security audit** — closed. The medium-severity CORS `*` origin finding in the 2026-07-06 scan report is a **dated pre-patch snapshot**; it was patched to configured `ALLOWED_ORIGINS` and re-scans on 2026-07-15 confirmed the fix. A RedByte external pen-test attestation letter (2026-07-11) supplements the evidence pack.
- **T015 fail-closed batch**, **T013 export policy**, **T017 policy conflict resolution**, **T020 HIPAA PII patterns**, **T032 auditable profile-export schema**, **T038 telemetry opt-out** — all complete and evidenced in WS-04.
- **T035 ephemeral OCR temp cleanup** — verified 2026-08-11; the audit report raises no separate open remanence finding.
- **T039 / CIPH-49 a11y audit** — **superseded**, not open work; folded into the CIPH-33 Preview UI overhaul, which natively covers high-contrast and keyboard navigation.

### Bottom line

Three items would still be open even if Docker and Windows signing cleared tomorrow and are the ones a compliance reviewer should track: **T016 audit-log schema mismatch** (the only compliance item explicitly named in the release-gate list, and closable by engineering), **T030 AGPL license exposure** (P0, and explicitly *not* closable by engineering search alone), and the **Tesseract training-data provenance** sub-item (also not closable by search). **T019** and **T014** are open WS-04 compliance work that engineering can finish on its own but are not named in the T011 gate list. Against the hard **2026-10-15 no-ship deadline**, note that the deadline as recorded (CMT-2026-09-002) is tied specifically to T005 and T029 — the audit-log and license gates are held separately by QA and Legal.
