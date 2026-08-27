# A clinic batch includes a scanned invoice with no usable native text layer, so OCR runs. Mid-job an unhandled worker exception fires before any export is finalized. OCR confidence on the page being processed was 82%. As of the **2026-09-22** rule set, what must happen to outputs and temps, what crash report is written, how the 90% manual-review rule applies (or does not) to this abort, and which related audit/OCR implementation items are still unfinished?

<!-- RESPONSE_START -->

## Answer

**Scenario:** clinic batch, scanned invoice with no usable native text layer → OCR fallback runs → unhandled worker exception fires mid-job, before any export is finalized. Page OCR confidence = 82%. Rule set as of **2026-09-22**.

---

### 1. What must happen to outputs

Fail-closed, with **no partial export**. Per the Batch Failure Strategy decision (T015) recorded in `work-states/WS-04-policy.md` (Last Updated 2026-09-22): on any unhandled failure the job aborts with **no output file produced**.

The mechanics behind it (`SRC-SLACK-12`, Slack #cipherdoc, 2026-06-12):
- If any worker node throws an unhandled exception, the **entire job is aborted** and the **output buffer is purged** — the already-successful files in the batch are not kept.
- An exception hook in the core engine catches low-level faults and signals the controller to **stop all active streams**.
- An **atomic rename step at the very end** means the output folder stays empty until the last file is verified — so a mid-job crash leaves nothing behind to release.

QA-validated: Diana's 2026-07-16 pass confirmed no output file is written on failure (`SRC-CU-CIPH-25`, CIPH-25 Completed 2026-06-15, QA-signed 2026-07-16).

### 2. What must happen to temps

Temp files must be **securely deleted** (T015 decision, WS-04). For the OCR path specifically this is covered by dedicated cleanup hooks:

- Cleanup hooks fire on **both the failure path and the normal completion path** (`SRC-SLACK-29`, 2026-08-09/08-11; CIPH-35, Status Completed).
- The hooks were built from a full inventory of OCR temp-write sites (`SRC-GDOC-19` / `SRC-SLACK-28`), covering three categories a single OCR run creates: (1) a **per-page rasterized image** in a process-local temp dir, (2) a **per-page OCR output buffer**, written *before* confidence-threshold filtering is applied, and (3) a **run-level manifest** of which pages fell back to OCR vs. native extraction.
- Diana confirmed secure deletion on 2026-08-11 across both failure and completion paths; no leftovers (`SRC-GDOC-40`, CIPH-35 activity 2026-08-11).

Caveat recorded in the evidence: a **hard kill** cannot be hooked. Charlie's stated coverage is "everything the OCR branch can reach on its own" between the failure hook and the completion hook (`SRC-SLACK-29`). An unhandled *exception* — this scenario — is on the failure path and is covered.

### 3. What crash report is written

A **crash report written to a separate `audit_log.json`, before shutdown**, capturing the **stack trace** and the **filename that triggered the fault** (`SRC-SLACK-12`; carried into the T015 decision in WS-04: "Crash diagnostics go to a separate `audit_log.json`"). It is written to a *separate* file precisely so diagnostics survive the purge of the output buffer.

Note this crash-diagnostics `audit_log.json` is distinct from — and should not be confused with — the compliance audit-trail records under T016/CIPH-26 (SHA-256 input hash + companion redaction-map JSON), which are still failing schema verification (see §5).

### 4. How the 90% manual-review rule applies to this abort

The adopted rule (T014 decision, WS-04): **90% confidence threshold adopted for v1.0.0**; anything below it is flagged for manual review, and "confidence" explicitly factors in **OCR quality**, not just regex match score — a low OCR confidence score for a block of text flags it regardless of regex match (`SRC-SLACK-11`, 2026-06-28). Mechanically, sub-threshold docs land in a **quarantine folder** and "won't be exported until a human confirms the redaction," accompanied by quarantine metadata (confidence score, page number, reason flagged) and UI indicators (`SRC-SLACK-11`, 2026-08-06 / 08-20 / 09-05).

At 82%, this page is **below the 90% threshold**, so on a normal run it would be quarantined rather than exported.

**But it does not apply to this abort in any operative way.** The two rules never collide, because the quarantine rule governs *whether a surviving output may be released*, and after a fail-closed abort there is no surviving output to hold:
- The abort produces **no output file at all** and purges the output buffer — quarantine-vs-export is moot when nothing was exported.
- The per-page OCR output buffer for this page is written **before** confidence-threshold filtering is applied (`SRC-GDOC-19`), so at crash time the 82% result exists only as a temp artifact — and temps are securely deleted on the failure path.
- Fail-closed is the stricter outcome anyway: quarantine withholds one document pending human confirmation; fail-closed withholds the entire batch unconditionally.

Two limits worth stating plainly. First, the dataset **does not contain an explicit precedence rule** stating "abort supersedes quarantine" — the above is the consistent reading of the two rules as written, not a quoted directive. Second, the 90% rule is **not settled as of 2026-09-22**: Diana's 2026-09-18 end-to-end pass found the pipeline holds together but the "90% threshold tuning itself is still in progress — I want another round of testing before I'd call it locked" (`SRC-SLACK-11`).

### 5. Related audit/OCR implementation items still unfinished

As of the 2026-09-22 work states, unchecked in the task lists:

| Item | Status |
|---|---|
| **T016 / CIPH-26 — Compliance Audit Trail Logs** | **Active/reopened; open release blocker.** Bob refactored the loader for SHA-256 hashing (2026-08-05), defined the companion JSON audit schema (2026-08-15), and wired audit-log generation into the CLI path (2026-09-10). Diana's 2026-09-18 verification found **CLI-emitted audit records inconsistent with the defined schema**. The **September 15 pre-release audit flagged CLI schema vs. emitted-record mismatch as a release hold** (WS-04 Active Work; `SRC-CU-CIPH-26`). |
| **T014 / CIPH-24 — Manual Review Workflow for Low-Confidence OCR** | **Active.** Quarantine folder, metadata (confidence/page/reason), and UI indicators are built and were exercised end-to-end, but **90% confidence-threshold logic is still being integrated with metadata injection for visual indicators**, and threshold tuning is not locked (WS-04 Active Work; `SRC-CU-CIPH-24`; `SRC-SLACK-11`). |
| **T008 / CIPH-18 — OCR Fallback for scanned documents** (WS-01) | **Active.** Charlie integrated per-page multiprocessing for page-level parallelism; **Diana is still wiring OCR results into the main scanner pipeline**, and **confidence tuning continues as of September**. WS-01's "Next Update Needed" names **OCR performance status** (WS-01 Active Work; `SRC-CU-CIPH-18`). |
| **T039 / CIPH-49 — Accessibility (a11y) Audit** | Unchecked but **Superseded** — absorbed by the Preview UI overhaul (CIPH-33), which natively addresses high-contrast and keyboard-navigation requirements (WS-04 Decisions; `SRC-SLACK-67`). Listed for completeness; not open work. |

For contrast, the items this scenario depends on are **done**: T015/CIPH-25 fail-closed (Completed, QA-validated 2026-07-16) and CIPH-35 ephemeral OCR temp cleanup (Completed, secure deletion confirmed 2026-08-11).

---

**Records cited:** `work-states/WS-04-policy.md` (path = work-state, Last Updated 2026-09-22) · `work-states/WS-01-engine.md` (path = work-state, Last Updated 2026-09-22) · `SRC-SLACK-12` (2026-06-12-batch-failures.md) · `SRC-SLACK-11` (2026-06-28-manual-review-threshold.md) · `SRC-SLACK-28` (2026-08-07-ocr-temp-file-trace.md) · `SRC-SLACK-29` (2026-08-09-ocr-temp-cleanup-hooks.md) · `SRC-CU-CIPH-25` · `SRC-CU-CIPH-24` · `SRC-CU-CIPH-26` · `SRC-CU-CIPH-18` · `SRC-CU-CIPH-35` · `SRC-GDOC-19` · `SRC-GDOC-40` · `SRC-GDOC-11`. No comment record (path = comments) bears on fail-closed, OCR temps, or the confidence threshold.
