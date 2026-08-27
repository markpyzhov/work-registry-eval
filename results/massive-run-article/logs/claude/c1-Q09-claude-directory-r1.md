# Beyond Docker and Windows packaging, which compliance and audit items still hold v1.0.0 as of **2026-09-22**? For each, give current status, the concrete defect or risk, and whether engineering search alone can close it.

<!-- RESPONSE_START -->

## Answer

As of the 2026-09-22 as-of timestamp, setting aside T005 (Docker size/CVE) and T029 (Windows code-signing), **two compliance/audit items are actual holds on v1.0.0**, plus one embedded sub-item and several adjacent open compliance items that are not formally release gates.

---

### 1. T016 / CIPH-26 — Compliance audit-trail logging (the audit-log schema gate)

- **Status**: Active / reopened, owner Diana (Bob implementing). Explicitly named a release hold by the 2026-09-15 pre-release audit — one of the three open gate items alongside Docker and Windows signing.
- **Defect**: The audit records the CLI actually emits do not validate against the defined companion JSON schema. Design intent is a SHA-256 hash of each input stream paired with a JSON redaction map for that file. Bob refactored the loader (07-11), added SHA-256 hashing (08-05), defined the companion schema (08-15), and wired generation into the CLI batch path (09-10); Diana's 09-18 verification found the emitted shape inconsistent with the schema.
- **Risk**: The audit trail cannot be used as release evidence. Diana: the gate stays red until schema and records match. Charlie confirmed in the audit call that this is not a packaging problem — it is schema vs. emitted records.
- **Can engineering close it alone?** **Yes.** This is purely internal implementation plus QA re-verification — no legal, vendor, or upstream dependency. Bob has "another pass queued." It is the one gate item on this list fully inside the team's control.
- Evidence: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-26-Audit-Trail-Logging.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-07-08-Compliance-Audit-Trail.md`

### 2. T030 / CIPH-40 — Third-party license compliance review (AGPL)

- **Status**: Active (Reopened), P0. Still listed as an open item on the 2026-09-22 daily brief and ranked #3 in that day's priority order.
- **Defect**: The original audit flagged Ghostscript (AGPLv3, used by the `rasterizer` module for PDF-to-image conversion) as blacklisted. Evan swapped in a replacement PDF parser on 08-11; on 08-12 Diana found the replacement is *also* AGPL-licensed — the swap moved the same license category one layer down. Charlie has been searching for an Apache 2.0 / MIT alternative since 08-15; nothing confirmed.
- **Risk**: Legal memo (CMT-2026-08-002, 2026-08-12): AGPL in the bundle triggers **whole-bundle copyleft exposure** for CipherDoc's distribution model to partner sites. The Q3 audit report carries an explicit warning not to report license compliance as resolved externally.
- **Can engineering close it alone?** **No — explicitly not.** CMT-2026-08-002 escalated this to a **hard Legal gate** and states that engineering library search alone is insufficient to close T030. Finding a viable non-AGPL parser is also flagged under WS-04 "Needs Manual Triage." Even a clean replacement still needs Legal to clear the gate.
- Evidence: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-08.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-40-License-Compliance-Review.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-21-License-Compliance-Audit-Report.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-12-license-agpl-reopen.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md`

### 2b. Sub-item inside T030 — Tesseract `eng.traineddata` provenance (easy to miss)

- **Status**: Separate, lower-priority open item under the same audit; pending Evan's trace of `tessdata_best` provenance.
- **Defect**: Tesseract OCR itself is Apache 2.0, but the `eng.traineddata` model files were sourced from a community repository and their **training-corpus provenance has not been verified as public-domain/CC0**.
- **Risk**: License compliance cannot be certified overall while this is unverified — the same audit report's warning covers it explicitly.
- **Can engineering close it alone?** **Partly, but not fully.** Engineering can trace the provenance chain, but the underlying question is whether the training corpus is licensed acceptably — a legal determination, not a library search. A different parser choice does not resolve it.
- Evidence: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-21-License-Compliance-Audit-Report.md`

---

### Adjacent open compliance items (open, but not carried as v1.0.0 gate items)

- **T019 / CIPH-29 — Offline-mode authentication with key rotation**: **Blocked**. Key rotation cannot complete in a strictly air-gapped environment without a centralized authority; only local mockups exist. InfoSec approved a split master-key escrow design (USB token at clinic + HQ HSM) on 08-05 and Bob is spiking it, so this is now an implementation gap, not an open design question. **Not closable by engineering search** — it needs the escrow to be built plus physical HSM/token provisioning. Still listed as a waiting-on item ("escrow still unimplemented") on the 09-22 brief. (`WS-04-policy.md`, `comments/2026-08.md`, `CIPH-29-Offline-Mode-Authentication.md`)
- **T014 / CIPH-24 — Manual-review quarantine for low-confidence OCR**: **Active**. Quarantine folder, metadata, and UI indicators were exercised end-to-end on 09-18, but the adopted 90% confidence-threshold integration is still in progress. **Yes, engineering can close it** — no external dependency. (`WS-04-policy.md`, `CIPH-24-Manual-Review-Threshold.md`)
- **T007 / CIPH-17 — Offset mismatch, Legal sign-off dependency**: Not a WS-04 item, but it carries a compliance-style gate. Blocked on upstream `pdfminer.six` #992 (maintainer says mid-October at the earliest); the pre-normalization workaround is acceptable **only with written Legal sign-off**, added as an explicit dependency alongside upstream. **Not closable by engineering alone.** (`WS-01-engine.md`, `comments/2026-06.md`)

### Explicitly no longer holding

- **T039 / CIPH-49 — Accessibility (a11y) audit**: **Superseded**, not open. On 08-24 Alice folded the standalone audit into the Redaction Preview UI overhaul (CIPH-33), which natively covers high-contrast and keyboard navigation; accessibility became part of that task's Definition of Done, with no separate audit report. Do not count it as an outstanding audit item. (`WS-04-policy.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-24-a11y-superseded.md`)

---

### Bottom line

Only **T016 (audit-log schema mismatch)** and **T030 (AGPL license compliance, including the tessdata provenance sub-item)** are live compliance/audit holds on v1.0.0 beyond packaging. T016 is fully closable by engineering; T030 is a hard Legal gate that engineering search alone cannot close, by explicit direction. Note the timing pressure: the release board's hard no-ship date of **2026-10-15** (CMT-2026-09-002) is scoped to T005 and T029 only — it does not by its terms cover T016 or T030, yet Diana holds the audit gate red independently and Legal holds T030, so clearing Docker and Windows alone would not open the release.
