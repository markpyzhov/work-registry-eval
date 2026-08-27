# A clinic batch includes a scanned invoice with no usable native text layer, so OCR runs. Mid-job an unhandled worker exception fires before any export is finalized. OCR confidence on the page being processed was 82%. As of the **2026-09-22** rule set, what must happen to outputs and temps, what crash report is written, how the 90% manual-review rule applies (or does not) to this abort, and which related audit/OCR implementation items are still unfinished?

<!-- RESPONSE_START -->

## Answer

**Scenario framing.** Nothing in the dataset changes the batch-failure or OCR rules after mid-September 2026, so the rule set in force on 2026-09-22 is the fail-closed contract completed under CIPH-25 (implementation 2026-06-15, QA-validated 2026-07-16) plus the OCR temp-cleanup hooks completed under CIPH-35 (confirmed 2026-08-11). The only source actually dated 2026-09-22 concerns the node-sync handshake block (CIPH-34) and is unrelated to this scenario.

### 1. What must happen to outputs

The batch is fail-closed. Per SRC-SLACK-12 and CIPH-25:

- If **any worker node throws an unhandled exception, the entire job is aborted** and the **output buffer is purged**. No partial exports — the decision was explicit that if 100% of the batch cannot be guaranteed safe, nothing ships.
- An **atomic rename step at the very end** means the output folder stays empty until the last file is verified. Because the exception fired before any export was finalized, this run leaves **zero output files on disk** — including for the pages that had already processed successfully.
- QA validated exactly this on 2026-07-16: no output file is produced on failure.

### 2. What must happen to temps

- Temp files must be **securely deleted**. CIPH-35 ("Delete ephemeral OCR temp files after failure/completion", Completed) added cleanup hooks that fire on **both the failure path and the normal completion path**; Diana confirmed secure deletion on 2026-08-11 (SRC-SLACK-29, SRC-GDOC-40).
- For this OCR run specifically, that covers the three artifact categories traced in SRC-GDOC-19: the **per-page rasterized image**, the **per-page OCR output buffer** (written *before* confidence-threshold filtering is applied), and the **run-level manifest** of which pages fell back to OCR vs. native extraction. The unfiltered 82% output buffer for the invoice page is therefore among the temps that must be wiped.
- Additionally, every temp file in the processing queue is AES-256 encrypted with a per-session key held only in volatile memory, so even a surviving temp is unreadable; on reboot the cleanup hook wipes it (SRC-SLACK-21).
- One stated coverage gap: Charlie noted a **hard kill cannot be hooked** — the failure and completion hooks cover only what the OCR branch can reach on its own. An unhandled worker exception is the clean-failure case, so it *is* covered.

### 3. What crash report is written

Before the shutdown, a **crash report is written to a separate `audit_log.json`**, capturing the **stack trace** and the **filename that triggered the fault** (SRC-SLACK-12, Bob, 2026-06-12). This file is written outside the purged output buffer, which is why the abort still leaves diagnostic evidence behind.

### 4. How the 90% manual-review rule applies (or does not)

The rule (SRC-SLACK-11, CIPH-24): anything below **90% confidence gets flagged for manual review**, and confidence explicitly includes **OCR quality**, not just the regex match score — a low OCR confidence flags the block regardless of regex. Sub-threshold documents land in a **quarantine folder** and **are not exported until a human confirms the redaction**, accompanied by metadata (confidence score, page number, reason flagged) and a visual UI indicator on the quarantined page.

At **82%**, this page is below the 90% line and would ordinarily be quarantined and held from export. **But on this abort the rule has nothing to act on**: the fail-closed path purges the output buffer and finalizes no export at all, so the quarantine gate — whose whole function is to withhold a document from export pending human sign-off — is redundant here. Fail-closed is strictly stricter than the 90% rule: quarantine withholds one low-confidence page, the abort withholds the entire batch. Two caveats worth flagging:

- The sources do not contain an explicit rule stating how quarantine and a mid-job abort interact; the above is the consequence of combining the two documented behaviors, not a directly quoted rule.
- The 90% threshold is **not yet locked**. As of Diana's 2026-09-18 end-to-end pass, the threshold tuning "is still in progress" and she wanted another round of testing before calling it settled — so 82% cannot be treated as a stable, final verdict against a finalized threshold.

### 5. Related audit / OCR items still unfinished

| Item | Status | What remains |
|---|---|---|
| **CIPH-26 — Audit Trail Logging** (Diana, High) | **Active — open release blocker** | SHA-256 input hashing, the companion JSON schema (hash + redaction map), and CLI wiring are done (2026-08-05 / 08-15 / 09-10), but Diana's 2026-09-18 verification found **CLI-emitted audit records do not match the defined schema**. Confirmed as a red gate at the 2026-09-15 pre-release audit; Bob has another pass queued. This directly undermines the audit trail as release evidence — the same `audit_log.json` path the crash report relies on. |
| **CIPH-24 — Manual Review Threshold for Low-Confidence OCR** (Diana) | **Active** | Quarantine folder, metadata, and UI indicators exercised end-to-end, but **90% confidence-threshold integration with the quarantine path is still in progress** (2026-09-18). |
| **CIPH-18 — OCR Fallback for Non-Text-Layer Documents** (Charlie) | **Active** | Tesseract POC succeeded; per-page multiprocessing pool and retuned confidence thresholds implemented, but **integration into the scan pipeline is still in progress** — Diana is mid-wiring while parallelization work remains open. |
| **License audit — Tesseract model files** (SRC-GDOC-41, Diana) | **Active (Reopened)**, lower priority | `eng.traineddata` model files came from a community repo and their **training-corpus provenance is unverified** as public-domain/CC0, pending Evan's `tessdata_best` trace. (The parent finding — an AGPL PDF parser swapped in for Ghostscript that turned out to be AGPL too — also remains unresolved; it affects the `rasterizer` module that produces OCR page images.) |
| **Telemetry / crash-reporter audit** (SRC-GDOC-51, Diana) | Partially open | CLI-side telemetry opt-out is verified, but the **third-party Electron crash reporter (Sentry) has not been audited** for whether it respects the opt-out variable or needs its own disable hook for minidump uploads. Relevant here because a crash is exactly the event that would trigger a minidump on a clinic (PHI) batch. |

One resolved-but-worth-noting item: SRC-GDOC-19's open question — whether the three OCR temp path categories are actually removed on both success and failure paths — was explicitly out of scope for that trace, but was subsequently closed by CIPH-35 and Diana's 2026-08-11 verification (SRC-GDOC-40), which states it raises no separate open remanence finding.

### Sources cited

- `med-synth/communication/sources/slack/2026-06-12-batch-failures.md` (SRC-SLACK-12)
- `med-synth/tasks/CIPH-25-Batch-Fail-Closed.md` (SRC-CU-CIPH-25)
- `med-synth/tasks/CIPH-35-Ephemeral-File-Cleanup.md` (SRC-CU-CIPH-35)
- `med-synth/communication/sources/slack/2026-08-09-ocr-temp-cleanup-hooks.md` (SRC-SLACK-29)
- `med-synth/communication/sources/slack/2026-08-07-ocr-temp-file-trace.md` (SRC-SLACK-28)
- `med-synth/documentation/sources/2026-08-20-Ephemeral-File-Cleanup-Review.md` (SRC-GDOC-19)
- `med-synth/documentation/sources/2026-08-20-Ephemeral-File-Cleanup-Audit-Report.md` (SRC-GDOC-40)
- `med-synth/communication/sources/slack/2026-08-05-aes256-pipeline.md` (SRC-SLACK-21)
- `med-synth/documentation/sources/2026-08-07-Local-Encryption-at-Rest-Security-Evaluation.md` (SRC-GDOC-35)
- `med-synth/communication/sources/slack/2026-06-28-manual-review-threshold.md` (SRC-SLACK-11)
- `med-synth/tasks/CIPH-24-Manual-Review-Threshold.md` (SRC-CU-CIPH-24)
- `med-synth/tasks/CIPH-26-Audit-Trail-Logging.md` (SRC-CU-CIPH-26)
- `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (SRC-MEET-10)
- `med-synth/tasks/CIPH-18-OCR-Fallback.md` (SRC-CU-CIPH-18)
- `med-synth/documentation/sources/2026-08-21-License-Compliance-Audit-Report.md` (SRC-GDOC-41)
- `med-synth/documentation/sources/2026-09-06-Telemetry-Opt-Out-Design-and-Compliance-Check.md` (SRC-GDOC-51)
