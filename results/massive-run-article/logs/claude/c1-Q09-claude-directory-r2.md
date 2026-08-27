# Beyond Docker and Windows packaging, which compliance and audit items still hold v1.0.0 as of **2026-09-22**? For each, give current status, the concrete defect or risk, and whether engineering search alone can close it.

<!-- RESPONSE_START -->

## Answer — compliance and audit items still holding v1.0.0 as of 2026-09-22 (excluding T005 Docker and T029 Windows signing)

Authoritative state: `work-states/WS-04-policy.md` and `work-states/WS-03-ops.md` (both Last Updated 2026-09-22), plus `work-states/index.md` (as-of 2026-09-22T12:00:00Z).

---

### 1. T016 / CIPH-26 — Compliance audit-trail logging  **(explicit release blocker)**

- **Status**: Active / reopened. The 2026-09-15 pre-release audit lists it as an open release hold alongside Docker and Windows signing; Diana: the audit-log gate stays red until schema and records match.
- **Defect**: Audit records emitted by the CLI batch path do not validate against the defined companion JSON schema (SHA-256 input hash + redaction map). Bob wired CLI generation on 2026-09-10; Diana's 2026-09-18 verification found the emitted shape inconsistent with the schema. This is a schema-vs-emitted-records problem, not a packaging one.
- **Risk**: The audit trail cannot be used as release evidence — the compliance artifact that ties each redaction back to a specific input is unverifiable.
- **Can engineering close it alone?** **Yes.** It is an internal serialization/schema-alignment fix (Bob has another pass queued) plus Diana's QA re-verification. No legal or third-party dependency.
- Evidence: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-26-Audit-Trail-Logging.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-07-08-Compliance-Audit-Trail.md`

### 2. T030 / CIPH-40 — Third-party license compliance review  **(P0 Legal gate)**

- **Status**: Active (Reopened) since 2026-08-12; still open in the 2026-09-22 brief as "P0 Legal AGPL/whole-bundle gate still open."
- **Defect**: The original audit flagged Ghostscript (AGPLv3) in the `rasterizer` module. The replacement PDF parser swapped in on 2026-08-11 turned out to be AGPL-licensed as well — the swap moved the same license category one layer down. Charlie's search for an Apache 2.0 / MIT alternative had not concluded as of the latest record.
- **Risk**: Legal memo (2026-08-12) states AGPL in the bundle triggers **whole-bundle copyleft exposure** for CipherDoc's distribution model to partner sites. The license inventory report carries an explicit warning not to report license compliance as resolved externally.
- **Can engineering search alone close it?** **No — explicitly not.** `CMT-2026-08-002` escalates it to P0 and states engineering search alone is insufficient; WS-04 records it as a hard Legal gate. A permissive parser must be found *and* Legal must clear the bundle.
- Evidence: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-08.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-40-License-Compliance-Review.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-21-License-Compliance-Audit-Report.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-21-License-Compliance-Review-Review.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-12-license-agpl-reopen.md`

### 3. OCR training-data provenance (secondary open item under the same license audit)

- **Status**: Open, lower priority, pending Evan's trace of `tessdata_best` provenance.
- **Defect**: Tesseract OCR itself is Apache 2.0, but the `eng.traineddata` model files were sourced from a community repository and their training-corpus provenance has not been verified as public-domain/CC0.
- **Risk**: Unverified provenance on shipped model data; the audit report explicitly says license compliance must not be reported as resolved while this is open.
- **Can engineering close it alone?** **Only partly.** The trace itself is an engineering task, but if upstream provenance cannot be established, the accept/reject call is a licensing judgment, not a search result.
- Evidence: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-21-License-Compliance-Audit-Report.md`

### 4. T019 / CIPH-29 — Offline-mode authentication for air-gapped installs

- **Status**: **Blocked** (WS-04 and the 2026-09-22 brief: "Escrow still unimplemented").
- **Defect**: The designed key-rotation flow assumes at least a brief network handshake; testing against the local auth mock (2026-08-04/05) showed rotation cannot complete with the network down. InfoSec approved a split master-key escrow (USB token at clinic + HQ HSM) on 2026-08-05, but it has not been built.
- **Risk**: Air-gapped clinic deployments ship without a working credential-rotation control — a privacy/security control gap in exactly the deployment mode CipherDoc targets.
- **Can engineering close it alone?** **Yes for the build, but it was never a search problem** — the architecture already required InfoSec approval (obtained) and depends on hardware provisioning (USB token + HQ HSM). Bob is spiking the implementation.
- Evidence: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-08.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-29-Offline-Mode-Authentication.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-04-offline-auth-mock-block.md`

### 5. T014 / CIPH-24 — Manual-review threshold / quarantine for low-confidence OCR

- **Status**: Active. Index lists it among active items ("T014 OCR quarantine").
- **Defect**: The 90% confidence threshold was adopted for v1.0.0, and the end-to-end pass on 2026-09-18 (detection → quarantine → metadata → UI markers → manual approval) held together, but threshold tuning is **not locked** — Diana wants another round of testing before calling it done.
- **Risk**: The privacy safety valve that prevents low-confidence redactions from being exported without human confirmation is not yet calibrated; mis-tuned thresholds either leak under-redacted documents or flood reviewers.
- **Can engineering close it alone?** **Yes** — tuning plus QA sign-off; no external gate.
- Evidence: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-24-Manual-Review-Threshold.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-06-28-manual-review-threshold.md`

### 6. Adjacent legal gate worth flagging: T007 / CIPH-17 (offset mismatch)

Not a compliance deliverable itself, but it carries a **written Legal sign-off requirement**: per `CMT-2026-06-003`, any pre-normalization workaround needs Legal approval in addition to the upstream `pdfminer.six` #992 merge (maintainer ETA mid-October, still unmerged as of 2026-09-10). So a second Legal dependency sits on the release path beyond T030. Evidence: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-01-engine.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-06.md`.

---

## What is *not* holding the release (compliance/audit side)

- **T010 / CIPH-20 security audit** — complete; CORS `*` finding patched to `ALLOWED_ORIGINS`, re-scans 2026-07-15 confirmed, plus RedByte external pen-test attestation letter (2026-07-11) in the evidence pack.
- **T013** research-export vs internal-review policy matrix, **T015** batch fail-closed (QA-validated 2026-07-16), **T017** policy conflict resolution, **T020** HIPAA PII pattern update, **T032** auditable redaction-profile schema export, **T038** telemetry opt-out (verified by offline network trace) — all Completed.
- **T039 / CIPH-49 accessibility audit** — **Superseded** on 2026-08-24, folded into the Preview UI overhaul (CIPH-33). It does not hold the release.

## Framing note on the deadline

The hard **2026-10-15 no-ship deadline** (`CMT-2026-09-002`) is tied specifically to T005 and T029 going green. The compliance items above are *separate* holds — but the 2026-09-15 pre-release audit stacks the audit-log mismatch on the same release-blocker board, and Alice's close was that no one clears any of them. Of the set, only **T030 (license) cannot be closed by engineering search alone**; the rest are engineering/QA execution with existing approvals.
