# A clinic batch includes a scanned invoice with no usable native text layer, so OCR runs. Mid-job an unhandled worker exception fires before any export is finalized. OCR confidence on the page being processed was 82%. As of the **2026-09-22** rule set, what must happen to outputs and temps, what crash report is written, how the 90% manual-review rule applies (or does not) to this abort, and which related audit/OCR implementation items are still unfinished?

<!-- RESPONSE_START -->

## Answer

**Scenario framing.** The dataset (CipherDoc, `med-synth` corpus) covers exactly this shape of event: a document with no usable native text layer routes through the OCR fallback (T008 / CIPH-18), and an unhandled worker exception during a batch run triggers the fail-closed batch policy (T015 / CIPH-25). The authoritative rule set is `work-states/WS-04-policy.md` (Last Updated **2026-09-22**), with `work-states/WS-01-engine.md` and `work-states/WS-07-storage.md` (both also 2026-09-22) covering the OCR and temp-file sides.

### 1. What must happen to outputs and temps

Per the **Batch Failure Strategy (T015)** decision in WS-04 (2026-09-22):

> "Fail-closed — on any unhandled failure the job aborts with **no output file produced** and temp files are **securely deleted**."

Concretely, from the provenance (SRC-SLACK-12, `2026-06-12-batch-failures.md`; SRC-CU-CIPH-25):

- **The entire job aborts, not just the failing file.** "If any worker node throws an unhandled exception, we abort the entire job and purge the output buffer." No partial exports — the explicit design rationale was "If we can't guarantee 100% of the batch is safe, we should fail-closed."
- **An exception hook in the core engine** catches the fault (including low-level segfaults) and signals the controller to **stop all active streams**.
- **No output file is written at all.** An **atomic rename step at the very end** of the job means the output folder stays empty until the last file is verified — so a mid-job crash "before any export is finalized" leaves nothing exported, including for the files that had already succeeded.
- **Temp files are securely deleted.** For the OCR path specifically, cleanup is handled by in-process `atexit` hooks (WS-07 decision: "Cron-based cleanup superseded by in-process `atexit` hooks for zero-residual footprint," T025 / CIPH-35). SRC-GDOC-19 enumerates the three OCR temp categories a run creates, all of which are in scope: (1) the per-page rasterized image in a process-local temp dir, (2) the **per-page OCR output buffer, written before confidence-threshold filtering is applied**, and (3) the run-level manifest recording which pages fell back to OCR vs native extraction. Diana verified on 2026-08-11 that these hooks remove ephemeral OCR temps on **both the failure and success paths** (SRC-GDOC-40).
- QA sign-off exists for the combined behavior: Diana's 2026-07-16 pass "confirmed no output file gets written on failure and the temp files get securely deleted" (CIPH-25 is **Completed**; WS-04 task list shows `[x] T015`).

Note item (2) above is the load-bearing detail for your 82% page: the raw OCR text for that page exists only as a pre-filter temp buffer, and it is purged by the same cleanup path — it is never promoted to an output or a quarantine artifact, because the abort happens before any export is finalized.

### 2. What crash report is written

A crash report is written to a **separate `audit_log.json`**, emitted **before the shutdown completes**. WS-04: "Crash diagnostics go to a separate `audit_log.json`." Per SRC-SLACK-12, it captures the **stack trace** and the **filename that triggered the fault** — in your case, the scanned invoice. This file is deliberately separate from the (non-existent) output so that the fail-closed purge does not destroy the reason for the failure ("We need to know *why* it failed" — Diana, 2026-06-12).

### 3. How the 90% manual-review rule applies (or does not)

The **OCR Threshold (T014)** decision in WS-04 records: "90% confidence threshold adopted for v1.0.0." Under the manual-review design (SRC-SLACK-11, CIPH-24), a page below 90% — 82% qualifies — would be flagged and routed to the **quarantine folder**, carrying metadata (confidence score, page number, reason flagged) and a UI indicator, and **would not be exported until a human confirms the redaction**. Diana explicitly scoped the threshold to cover OCR quality, not just regex match score: "If the OCR engine gives a low confidence score for a block of text, we should flag it regardless of the regex match."

**But it does not govern this abort.** The two rules do not conflict here, and the 90% rule changes nothing about the outcome:

- The quarantine rule is an **export gate** — it holds a low-confidence page back from export pending human approval. The fail-closed rule has already produced **no export at all** and purged the output buffer, so there is nothing for the quarantine gate to withhold.
- The quarantine artifacts themselves depend on confidence-threshold filtering that is applied *after* the per-page OCR output buffer is written; with the job aborted mid-run and temps securely deleted, no quarantine entry or metadata record survives for that page.
- The dataset records no exception carving low-confidence pages out of the fail-closed purge — the rule is stated unconditionally ("on **any** unhandled failure").

So the correct reading: the 82% reading is below the adopted threshold and *would* have quarantined the page on a run that completed, but for this aborted run the fail-closed rule is the operative one and the manual-review path is moot. The only durable record of the run is the `audit_log.json` crash report. (This last inference — that fail-closed supersedes quarantine rather than the two both applying — follows from the abort producing no output; the dataset does not adjudicate the interaction explicitly.)

### 4. Related audit/OCR implementation items still unfinished

As of the 2026-09-22 work states:

| Item | Where | Status |
|---|---|---|
| **T016 / CIPH-26 — Compliance Audit Trail Logs** | WS-04 (`[ ] T016`) | **Active/reopened, and an open release blocker.** Bob refactored the loader for streaming and added SHA-256 input hashing (2026-08-05), defined the companion JSON audit schema pairing hash + redaction map (2026-08-15), and wired audit-log generation into the CLI batch path (2026-09-10). On 2026-09-18 Diana's verification found **CLI-emitted audit records inconsistent with the defined schema**; the 2026-09-15 pre-release audit flagged this CLI-schema-vs-emitted-record mismatch as a **release hold**. WS-04's "Next Update Needed" is "Audit-log schema alignment…". This is directly relevant to your scenario: the crash report goes to `audit_log.json`, and the audit-record schema conformance around that path is not yet verified. |
| **T014 / CIPH-24 — Manual Review Workflow for Low-Confidence OCR** | WS-04 (`[ ] T014`) | **Active.** Quarantine folder, quarantine metadata (confidence/page/reason), and Charlie's UI indicators are built, and Diana ran an end-to-end pass on 2026-09-18 (detection → quarantine → metadata → UI markers → manual approval). But the **90% threshold logic is still being integrated with metadata injection**, and Diana explicitly declined to lock it: "the 90% threshold tuning itself is still in progress — I want another round of testing before I'd call it locked." |
| **T008 / CIPH-18 — OCR fallback for scanned documents** | WS-01 (`[ ] T008`) | **Active.** Tesseract POC proved the fallback path (2026-06-28); page-serial Tesseract was a latency bottleneck, so Charlie implemented a per-page multiprocessing pool and retuned confidence thresholds. Diana is **still wiring OCR fallback output into the main scanner pipeline**, and confidence tuning continues as of September. WS-01's "Next Update Needed" is "OCR performance status and upstream #992 merge watch." |
| **T025 / CIPH-35 — Ephemeral file cleanup hooks for OCR** | WS-07 (`[x] T025`) | **Finished** — included for completeness because it is the mechanism that satisfies the "temps securely deleted" half of the rule. The 2026-08-07 path trace (SRC-GDOC-19) left "confirming these paths are actually removed on both success and failure" as an open item outside its own scope, but Diana's 2026-08-11 verification (SRC-GDOC-40) closed that, and WS-07 marks the task complete. |

Two adjacent items are **not** part of the OCR/audit picture despite surface keyword overlap: T039 / CIPH-49 (accessibility a11y audit) is unchecked in WS-04 but only because it was **superseded** by the Preview UI overhaul (CIPH-33), and T030 / CIPH-40 (license compliance review, reopened over the AGPL parser discovery, now a hard Legal P0 gate) is a licensing rather than an audit-logging matter.

### Records cited

Work states (authoritative for status): `work-states/WS-04-policy.md`, `work-states/WS-01-engine.md`, `work-states/WS-07-storage.md` — all Last Updated 2026-09-22.
Sources (provenance/detail): SRC-SLACK-12 (`2026-06-12-batch-failures.md`), SRC-CU-CIPH-25 (Batch Fail-Closed, Completed), SRC-SLACK-11 (`2026-06-28-manual-review-threshold.md`), SRC-CU-CIPH-24 (Manual Review Threshold, Active), SRC-CU-CIPH-26 (Audit Trail Logging, Active), SRC-GDOC-11 (Compliance Audit Trail design intent), SRC-CU-CIPH-18 (OCR Fallback, Active), SRC-GDOC-04 (Tesseract POC), SRC-MEET-03 (`2026-07-05-OCR-Progress-Sync.md`), SRC-GDOC-19 (OCR Temp File Path Trace), SRC-GDOC-40 (Ephemeral OCR Temp Cleanup Verification), SRC-SLACK-28 (`2026-08-07-ocr-temp-file-trace.md`).
No work-state comment (`CMT-*`) touches the OCR-threshold, fail-closed, or audit-log items; the seven comments on file address T006, T005, T007, T009, T010, T019, T030, T031, T036, T022, and T024.
