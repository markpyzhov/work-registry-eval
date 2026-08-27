# A clinic batch includes a scanned invoice with no usable native text layer, so OCR runs. Mid-job an unhandled worker exception fires before any export is finalized. OCR confidence on the page being processed was 82%. As of the **2026-09-22** rule set, what must happen to outputs and temps, what crash report is written, how the 90% manual-review rule applies (or does not) to this abort, and which related audit/OCR implementation items are still unfinished?

<!-- RESPONSE_START -->

## Answer

**Scenario:** clinic batch → scanned invoice with no usable native text layer → OCR fallback path (SRC-CU-CIPH-18 / SRC-GDOC-04, T008/WS-01) → unhandled worker exception mid-job, before any export is finalized, on a page whose OCR confidence was 82%.

### 1. What must happen to outputs

Fail-closed, whole-job abort — no partial export:

- Any worker node throwing an unhandled exception aborts the **entire job** and purges the output buffer. The rule was set explicitly against keeping the successful files: "If we can't guarantee 100% of the batch is safe, we should fail-closed. No partial exports." (SRC-SLACK-12, 2026-06-12)
- An exception hook in the core engine catches low-level faults (including segfaults) and signals the controller to stop all active streams (SRC-SLACK-12).
- Because finalization uses an **atomic rename at the very end**, the output folder stays empty until the last file is verified — so a crash before export finalization leaves zero output files on disk (SRC-SLACK-12).
- QA validated this: no output file is produced on failure (SRC-SLACK-12 2026-07-16; SRC-CU-CIPH-25, Completed 2026-06-15, QA-validated 2026-07-16).
- This fail-closed deletion behavior for interrupted runs is also the precondition the AES-256 at-rest sign-off was withheld on — an unencrypted partial output left on disk after a crash would have undermined the encryption guarantee (SRC-GDOC-35).

### 2. What must happen to temps

All ephemeral OCR temporary files must be securely deleted; they must not survive a failed page or a successful completion:

- The failure-path cleanup hook fires and removes the OCR temps, using the site inventory from the temp-path trace (SRC-SLACK-29, 2026-08-09; SRC-CU-CIPH-35, Completed).
- The three temp categories a single OCR fallback run creates, all of which the hooks target (SRC-GDOC-19): (1) per-page rasterized image, one per page, in a process-local temp directory; (2) per-page OCR output buffer, written **before** confidence-threshold filtering is applied; (3) a run-level manifest recording which pages fell back to OCR vs. native text extraction.
- Diana verified on 2026-08-11 that temps are gone after both the failure and the normal completion path, with no leftovers; secure deletion confirmed (SRC-GDOC-40, SRC-SLACK-29, SRC-CU-CIPH-35).
- **Known limit:** a hard process kill cannot be hooked. The failure hook plus the completion hook cover "everything the OCR branch can reach on its own" (SRC-SLACK-29). An unhandled exception is a clean failure path, so it is covered.

### 3. Crash report

Before shutdown, a crash report is written to a **separate `audit_log.json`**, capturing the **stack trace** and the **filename that triggered the fault** (SRC-SLACK-12, 2026-06-12). Diana's original requirement was that logs must record *why* it failed; this log is separate from the purged output so the failure is diagnosable even though nothing was exported.

### 4. How the 90% manual-review rule applies to this abort

**It does not gate this abort — the 82% page never reaches quarantine, because the job is dead first.**

- The rule (SRC-SLACK-11, SRC-CU-CIPH-24): a 90% confidence threshold; anything below is flagged for manual review. Confidence is defined as **both** regex match score and OCR quality — a low OCR confidence score for a block of text flags it regardless of the regex match. Sub-90% documents land in a quarantine folder and are **not exported until a human confirms the redaction**, accompanied by metadata (confidence score, page number, reason flagged) and visual UI indicators for quarantined pages.
- 82% is below 90%, so under normal processing this page would have been quarantined for manual review rather than exported.
- But quarantine is a **hold-before-export** control, and the fail-closed rule operates earlier and more broadly: the unhandled exception aborts the whole job and purges the output buffer, and nothing was exported anyway (atomic rename never ran). The 90% rule adds nothing to the disposition here — there is no surviving output to quarantine, and the OCR output buffer for that page (which is written *before* confidence filtering is applied, per SRC-GDOC-19) is itself a temp that the failure-path cleanup hook securely deletes.
- Practical consequence: on re-run, the 82% page must still be quarantined for manual review under the 90% rule — the abort defers that decision, it does not satisfy or waive it.

### 5. Related audit/OCR implementation items still unfinished

| Item | Status | Detail |
|---|---|---|
| **CIPH-26 — Audit Trail Logging** (T016) | **Active — open release blocker** | SHA-256 input-stream hash + companion JSON redaction-map schema, wired into the CLI batch path. CLI integration landed 2026-09-10, but Diana's 2026-09-18 verification found **CLI-emitted audit records inconsistent with the defined schema**. Diana is keeping the audit-log gate red until schema and records match (SRC-CU-CIPH-26, SRC-MEET-10 2026-09-15). This directly affects the crash report's evidentiary value, since the crash report is written into `audit_log.json`. |
| **CIPH-24 — Manual Review Threshold for Low-Confidence OCR** (WS-04) | **Active** | Quarantine folder, metadata, and UI indicators are built and were exercised end-to-end on 2026-09-18, but the **90% confidence-threshold integration/tuning is still in progress** — Diana wants another round of testing before calling it locked (SRC-CU-CIPH-24, SRC-SLACK-11). So the very rule that would govern the 82% page is not yet settled. |
| **CIPH-18 — OCR Fallback for Non-Text-Layer Documents** (T008/WS-01) | **Active** | Per-page multiprocessing pool and retuned confidence thresholds are implemented; Diana has begun wiring OCR fallback output into the scan pipeline, but **integration/parallelization remains Active** (SRC-CU-CIPH-18, SRC-GDOC-04). |
| **Tesseract `eng.traineddata` provenance** | **Open, lower priority** | Tesseract itself is Apache 2.0, but the model files came from a community repository and their training-corpus provenance is unverified as public-domain/CC0; pending Evan's `tessdata_best` trace (SRC-GDOC-41). |
| **License compliance — rasterizer PDF parser** | **Active (Reopened)** | The Ghostscript (AGPLv3) swap reintroduced an AGPL library one layer down; Charlie is still searching for an Apache 2.0/MIT alternative for the rasterization path used by OCR (SRC-GDOC-41). |

Related-but-closed for contrast: CIPH-25 (Batch Fail-Closed) and CIPH-35 (Ephemeral OCR Temp Cleanup) are both **Completed and QA-verified**, which is why the abort/purge/temp-deletion behavior above is reliable.

**Note on the "2026-09-22 rule set":** nothing in the dataset dated 2026-09-22 changes any of the above. The only 2026-09-22 records are the node-sync handshake timeout block (SRC-MEET-11, SRC-SLACK-27, SRC-CU-CIPH-34), which is unrelated to OCR, fail-closed abort, or the manual-review threshold. The governing rules as of that date are therefore the fail-closed rules from 2026-06-12/2026-07-16 and the threshold work as it stood on 2026-09-18.

### Sources cited
- `med-synth/communication/sources/slack/2026-06-12-batch-failures.md` (SRC-SLACK-12)
- `med-synth/tasks/CIPH-25-Batch-Fail-Closed.md` (SRC-CU-CIPH-25)
- `med-synth/communication/sources/slack/2026-06-28-manual-review-threshold.md` (SRC-SLACK-11)
- `med-synth/tasks/CIPH-24-Manual-Review-Threshold.md` (SRC-CU-CIPH-24)
- `med-synth/documentation/sources/2026-08-20-Ephemeral-File-Cleanup-Review.md` (SRC-GDOC-19)
- `med-synth/documentation/sources/2026-08-20-Ephemeral-File-Cleanup-Audit-Report.md` (SRC-GDOC-40)
- `med-synth/communication/sources/slack/2026-08-09-ocr-temp-cleanup-hooks.md` (SRC-SLACK-29)
- `med-synth/communication/sources/slack/2026-08-07-ocr-temp-file-trace.md` (SRC-SLACK-28)
- `med-synth/tasks/CIPH-35-Ephemeral-File-Cleanup.md` (SRC-CU-CIPH-35)
- `med-synth/tasks/CIPH-26-Audit-Trail-Logging.md` (SRC-CU-CIPH-26)
- `med-synth/documentation/sources/2026-07-08-Compliance-Audit-Trail.md` (SRC-GDOC-11)
- `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (SRC-MEET-10)
- `med-synth/tasks/CIPH-18-OCR-Fallback.md` (SRC-CU-CIPH-18)
- `med-synth/documentation/sources/2026-06-28-OCR-Pipeline-Design.md` (SRC-GDOC-04)
- `med-synth/documentation/sources/2026-08-07-Local-Encryption-at-Rest-Security-Evaluation.md` (SRC-GDOC-35)
- `med-synth/documentation/sources/2026-08-21-License-Compliance-Audit-Report.md` (SRC-GDOC-41)
- `med-synth/communication/sources/fireflies/2026-09-22-Handshake-Protocol-Deep-Dive.md` (SRC-MEET-11) — checked, not applicable
