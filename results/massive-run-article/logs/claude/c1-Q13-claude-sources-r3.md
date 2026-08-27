# A clinic batch includes a scanned invoice with no usable native text layer, so OCR runs. Mid-job an unhandled worker exception fires before any export is finalized. OCR confidence on the page being processed was 82%. As of the **2026-09-22** rule set, what must happen to outputs and temps, what crash report is written, how the 90% manual-review rule applies (or does not) to this abort, and which related audit/OCR implementation items are still unfinished?

<!-- RESPONSE_START -->

## Answer

**Scenario:** clinic batch, scanned invoice with no usable native text layer → OCR fallback path (CIPH-18 / T008, WS-01); unhandled worker exception mid-job, before any export is finalized; page OCR confidence 82%.

### 1. Outputs — fail-closed, nothing is released

Per the batch fail-closed rule (CIPH-25 / T015, WS-04), which is **Completed and QA-validated**:

- If **any worker node throws an unhandled exception, the entire job is aborted and the output buffer is purged**. There are **no partial exports** — the explicit decision was "if we can't guarantee 100% of the batch is safe, we fail-closed."
- The engine has an exception hook in the core engine that catches low-level faults (including segfaults) and signals the controller to **stop all active streams**.
- An **atomic rename step at the very end** means the output folder stays empty until the last file is verified. Because the crash fired before any export was finalized, **no output file exists for any file in the batch** — including the successfully processed ones, and including the clinic invoice.
- Diana's QA pass (2026-07-16) confirmed no output file gets written on failure. This behavior is also the precondition the AES-256 at-rest encryption sign-off was withheld on — an unencrypted partial output left on disk after a crash would have voided the encryption guarantee.

### 2. Temps — securely deleted on the failure path

- The batch fail-closed QA pass confirmed temp files are **securely deleted** on failure.
- Specifically for OCR (CIPH-35, **Completed**): cleanup hooks were added covering **both the failure path and the normal completion path**, built from the full OCR temp-site inventory, and Diana verified on 2026-08-11 that ephemeral OCR temps are gone after both paths, with no leftovers.
- The OCR temp artifacts targeted (SRC-GDOC-19) are three categories per run: (1) per-page rasterized images in a process-local temp dir, (2) per-page OCR output buffers written *before* confidence-threshold filtering is applied, (3) a run-level manifest of which pages fell back to OCR vs. native extraction. For the invoice, that includes an unfiltered 82%-confidence OCR buffer — which the cleanup hook is required to purge.
- **Stated caveat:** a hard kill of the process cannot be hooked. Coverage is guaranteed only for what the OCR branch can reach on its own via the failure and completion hooks. An unhandled worker exception is a clean failure path, so it is covered.

### 3. Crash report

- A crash report is written to a **separate `audit_log.json`** *before* the shutdown completes. It captures the **stack trace** and the **filename that triggered the fault**. This is deliberately separate from the purged output buffer so the "why did it fail" evidence survives the fail-closed purge.

### 4. The 90% manual-review rule — does not save this page from the abort

- The rule (CIPH-24 / WS-04): anything below **90% confidence** is flagged for manual review; confidence factors in **both regex match score and OCR quality**, so a low OCR score flags the block regardless of the regex match. Sub-threshold docs land in a **quarantine folder** and **are not exported until a human confirms the redaction**, accompanied by quarantine metadata (confidence score, page number, reason flagged) and visual UI indicators.
- At **82%**, this page is squarely below the threshold, so on a normal run it would be quarantined and held for manual review rather than exported.
- **On this abort, that path is moot.** The 90% rule governs *whether an output may be exported*; fail-closed governs *whether the job produces output at all*. Since the exception aborts the whole job and purges the buffer before finalization, there is no output to quarantine and nothing reaches a reviewer — the manual-review gate never comes into play. (The sources do not describe any special interaction between quarantine and a mid-job abort; the fail-closed contract is the controlling rule, and it is the more restrictive of the two.)
- Also important: the 90% rule is **not locked** as of the current rule set. On 2026-09-18 Diana ran the end-to-end pass (detection → quarantine → metadata → UI markers → manual approval) and reported the pipeline holds together but **"the 90% threshold tuning itself is still in progress"** — she wants another round of testing before calling it locked. So the number is provisional, not a settled gate.

### 5. Related audit / OCR items still unfinished

| Item | Status | What's outstanding |
|---|---|---|
| **CIPH-26 — Audit Trail Logging** (T016, Diana, High) | **Active — open release blocker** | SHA-256 input hashing, companion JSON schema (hash + redaction map), and CLI wiring (2026-09-10) are all in, but Diana's 2026-09-18 verification found **CLI-emitted audit records do not match the defined schema**. Bob has another pass queued. Diana is keeping the audit-log gate **red** until schema and records match (2026-09-15 pre-release review). This directly undercuts `audit_log.json`-based crash evidence as release evidence. |
| **CIPH-24 — Manual Review Threshold for Low-Confidence OCR** (Diana) | **Active** | 90% confidence-threshold logic is **not yet fully integrated** with the quarantine path; threshold tuning still in progress as of 2026-09-18. Quarantine folder, metadata, and UI indicators exercised end-to-end but not signed off. |
| **CIPH-18 — OCR Fallback for Non-Text-Layer Documents** (Charlie) | **Active** | Per-page multiprocessing pool and retuned confidence thresholds are built, but **clean integration with the scan pipeline is still in progress**; parallelization work remains open. Diana has only *begun* wiring OCR fallback output into the scan pipeline. |
| **License audit — Tesseract `eng.traineddata` provenance** | **Open (lower priority)** | Tesseract itself is Apache 2.0, but the model files came from a community repo and their training-corpus provenance is unverified as public-domain/CC0. Pending Evan's `tessdata_best` trace. |
| **License audit — rasterizer PDF parser** (CIPH-40) | **Active (Reopened)** | Relevant to the OCR path since rasterization feeds OCR. Ghostscript (AGPLv3) was swapped out, but the replacement parser turned out to be AGPL too; Charlie is still searching for an Apache-2.0/MIT alternative, unresolved as of 2026-08-15. |

**Closed, for contrast:** CIPH-25 (batch fail-closed) and CIPH-35 (ephemeral OCR temp cleanup) are both **Completed and verified** — the abort/purge/secure-delete behavior described above is settled. The open item flagged in the OCR temp path trace ("confirm these paths are actually removed on success and failure") was subsequently closed by CIPH-35's 2026-08-11 verification.

### Net effect for this clinic batch

The invoice's OCR run is discarded entirely: no redacted output for it or for any other file in the batch, all OCR temps (raster images, the pre-filter 82% OCR buffer, the run manifest) securely deleted, and a crash report with stack trace and triggering filename written to `audit_log.json` before shutdown. The 82% page never reaches quarantine or a human reviewer, because the job never produces output to review. The batch must be rerun from scratch. Caveat on evidence quality: the audit-log path itself (CIPH-26) is a currently-failing release blocker, so the crash record's schema conformance cannot be relied on as clean release evidence.

### Sources cited

- `med-synth/communication/sources/slack/2026-06-12-batch-failures.md` (SRC-SLACK-12) — abort/purge, exception hook, atomic rename, `audit_log.json` crash report, QA sign-off
- `med-synth/tasks/CIPH-25-Batch-Fail-Closed.md` (SRC-CU-CIPH-25) — fail-closed Completed + QA-validated
- `med-synth/tasks/CIPH-35-Ephemeral-File-Cleanup.md` (SRC-CU-CIPH-35) — temp cleanup Completed
- `med-synth/communication/sources/slack/2026-08-09-ocr-temp-cleanup-hooks.md` (SRC-SLACK-29) — failure/completion hooks, hard-kill caveat
- `med-synth/communication/sources/slack/2026-08-07-ocr-temp-file-trace.md` (SRC-SLACK-28) — temp-site inventory
- `med-synth/documentation/sources/2026-08-20-Ephemeral-File-Cleanup-Review.md` (SRC-GDOC-19) — three temp categories
- `med-synth/documentation/sources/2026-08-20-Ephemeral-File-Cleanup-Audit-Report.md` (SRC-GDOC-40) — 2026-08-11 secure-deletion confirmation
- `med-synth/communication/sources/slack/2026-06-28-manual-review-threshold.md` (SRC-SLACK-11) — 90% rule, quarantine, threshold still in progress
- `med-synth/tasks/CIPH-24-Manual-Review-Threshold.md` (SRC-CU-CIPH-24) — Active status
- `med-synth/tasks/CIPH-26-Audit-Trail-Logging.md` (SRC-CU-CIPH-26) — audit schema mismatch, release blocker
- `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (SRC-MEET-10) — audit gate red
- `med-synth/tasks/CIPH-18-OCR-Fallback.md` (SRC-CU-CIPH-18) — OCR fallback Active
- `med-synth/documentation/sources/2026-08-07-Local-Encryption-at-Rest-Security-Evaluation.md` (SRC-GDOC-35) — encryption sign-off dependency on fail-closed
- `med-synth/documentation/sources/2026-08-21-License-Compliance-Audit-Report.md` (SRC-GDOC-41) — traineddata provenance, parser license reopen
