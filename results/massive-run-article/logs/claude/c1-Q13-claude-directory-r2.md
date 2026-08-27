# A clinic batch includes a scanned invoice with no usable native text layer, so OCR runs. Mid-job an unhandled worker exception fires before any export is finalized. OCR confidence on the page being processed was 82%. As of the **2026-09-22** rule set, what must happen to outputs and temps, what crash report is written, how the 90% manual-review rule applies (or does not) to this abort, and which related audit/OCR implementation items are still unfinished?

<!-- RESPONSE_START -->

I have everything needed. Here is the complete answer.

---

## Scenario, as of the 2026-09-22 rule set

A scanned clinic invoice with no usable native text layer routes through the OCR fallback (T008 / CIPH-18), an unhandled worker exception fires mid-job before any export is finalized, and OCR confidence on the in-flight page is 82%.

### 1. What must happen to outputs

**Fail-closed: the entire job aborts and no output file is produced.** This is the governing rule for T015 / CIPH-25, recorded as an active decision in the authoritative Work State:

> "Fail-closed — on any unhandled failure the job aborts with **no output file produced** and temp files are **securely deleted**."
> — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md` (Decisions, T015)

Mechanics and scope from the source thread:
- Any worker node throwing an unhandled exception aborts the **whole** job and purges the output buffer — no partial exports, even for files that already succeeded ("If we can't guarantee 100% of the batch is safe, we should fail-closed. No partial exports.").
- An exception hook in the core engine catches low-level faults (including segfaults) and signals the controller to stop all active streams.
- An **atomic rename** at the very end is what guarantees this: the output folder stays empty until the last file is verified, so a crash before finalization leaves nothing behind.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-06-12-batch-failures.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-25-Batch-Fail-Closed.md`

Because the crash fires **before any export is finalized**, the atomic-rename step never runs — so nothing from this clinic batch is released, including the successfully processed files.

This behavior is **done and QA-validated**: Bob completed the implementation 2026-06-15; Diana's 2026-07-16 QA pass confirmed no output file on failure and secure temp deletion, signing off ahead of the encryption (T021) and offline-mode (T027) work that depends on it (`WS-04-policy.md` Done/Evidence; `CIPH-25-Batch-Fail-Closed.md`).

### 2. What must happen to temps

**Temp files are securely deleted on the failure path.** Two layers apply:

- **Batch-level (T015 / CIPH-25):** secure temp deletion is part of the fail-closed contract and was QA-validated on 2026-07-16.
- **OCR-specific (T025 / CIPH-35 — Completed):** ephemeral OCR temp cleanup hooks fire on **both** the failure path and the normal completion path; temp files are purged from `/tmp/cipherdoc-*` immediately after processing. Diana confirmed secure deletion on 2026-08-11 against the QA scenario that had previously left orphaned files.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-07-storage.md` (T025, Done/Evidence), `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-35-Ephemeral-File-Cleanup.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-09-ocr-temp-cleanup-hooks.md`

**Known coverage limit:** the hooks cannot cover a **hard kill** of the process. Charlie: cleanup can't be hooked on an outright kill, but between the failure hook and the completion hook "we cover everything the OCR branch can reach on its own." An unhandled exception is a clean failure path, so it *is* covered here — this caveat only bites on SIGKILL-class terminations (`2026-08-09-ocr-temp-cleanup-hooks.md`).

### 3. The crash report that is written

**Crash diagnostics go to a separate `audit_log.json`, written before shutdown**, capturing the **stack trace** and the **filename that triggered the fault** (here, the scanned invoice).

- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md` (T015 decision: "Crash diagnostics go to a separate `audit_log.json`.")
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-06-12-batch-failures.md` (Bob, 2026-06-12 13:16 — written before the shutdown, captures stack trace + triggering filename)

Note this crash report is deliberately **separate** from the exported output path — it is the only artifact that survives the abort.

### 4. How the 90% manual-review rule applies (it does not, on this abort)

**It does not fire for this crash.** The 82% score is below the adopted 90% threshold, so in a normal run that page would be flagged and routed to the quarantine folder — but quarantine is a *pre-export hold* mechanism, and fail-closed preempts it:

- The 90% confidence threshold was adopted for v1.0.0; confidence is defined to include OCR quality, not just regex match score — a low OCR score flags the block "regardless of the regex match" (`WS-04-policy.md` OCR Threshold decision; `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-06-28-manual-review-threshold.md`).
- Quarantine's purpose is that sub-threshold docs "land there and **won't be exported** until a human confirms the redaction" (Diana, 2026-08-06). Fail-closed already guarantees **zero** export for the entire job, so the quarantine hold has nothing left to withhold.
- The two rules are not in tension and do not need reconciling: quarantine gates *what gets exported*; fail-closed gates *whether the job exports at all*. On an unhandled worker exception, the job-level abort is absolute and applies to every file in the batch regardless of individual confidence scores.
- Practically: the batch must be re-run after the exception is fixed. On that re-run the 82% page would be quarantined with its metadata (confidence score, page number, flag reason) and require human confirmation before release.

**One important caveat:** the quarantine path itself is **not finished** (see below), so relying on it as an operative safety net today is premature — the 90% threshold integration is still in progress.

### 5. Related audit/OCR implementation items still unfinished

Four open items, per the authoritative Work States as of the 2026-09-22 as-of timestamp (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/index.md`, as-of `2026-09-22T12:00:00Z`):

| Item | State | What remains |
|---|---|---|
| **T016 / CIPH-26 — Compliance Audit Trail Logging** | **Active / reopened — open release blocker** | SHA-256 input hashing and the companion JSON schema (hash + redaction map) are built, and Bob wired audit-log generation into the CLI batch path on 2026-09-10. But Diana's 2026-09-18 verification found **CLI-emitted audit records do not match the defined schema**. Diana holds the audit gate **red** until they match; Bob has another pass queued. |
| **T014 / CIPH-24 — Manual Review Threshold for Low-Confidence OCR** | **Active** | Quarantine folder, metadata (confidence, page, reason) and Charlie's UI visual indicators are built, and Diana's 2026-09-18 end-to-end pass (detection → quarantine → metadata → UI markers → manual approval) held together. But the **90% threshold tuning itself is still in progress** — Diana wants another round of testing before calling it locked. Threshold logic is still being integrated with metadata injection for visual indicators. |
| **T008 / CIPH-18 — OCR Fallback for Non-Text-Layer Documents** | **Active** | The very path this scenario exercises. Tesseract POC succeeded; Charlie replaced the page-serial latency bottleneck with a per-page multiprocessing pool and retuned confidence thresholds. Diana is still **wiring OCR results into the main scanner pipeline**; confidence tuning continues as of September. |
| **T039 / CIPH-49 — Accessibility a11y Audit** | **Superseded** (not a live item) | Folded into the Preview UI overhaul (CIPH-33), which natively covers high-contrast and keyboard navigation. Listed for completeness since the quarantine UI indicators touch the same surface. |

**Net compliance exposure:** the abort behavior itself (T015) is complete and QA-validated, and OCR temp cleanup (T025) is complete — so outputs and temps are handled correctly. The weak link is **evidence**: T016's audit records still fail schema validation, which is exactly the artifact you would rely on to prove after the fact that this clinic batch aborted cleanly and released nothing. The audit-log mismatch is one of the open holds keeping the v1 release gate (T011) closed against the hard **2026-10-15** no-ship deadline, alongside Docker size/CVE (T005) and Windows signing (T029).

**Supporting files:** `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-26-Audit-Trail-Logging.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-24-Manual-Review-Threshold.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-18-OCR-Fallback.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-01-engine.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-07-08-Compliance-Audit-Trail.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-06-28-OCR-Pipeline-Design.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-07-05-OCR-Progress-Sync.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md`
