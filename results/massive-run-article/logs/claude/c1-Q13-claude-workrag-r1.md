# A clinic batch includes a scanned invoice with no usable native text layer, so OCR runs. Mid-job an unhandled worker exception fires before any export is finalized. OCR confidence on the page being processed was 82%. As of the **2026-09-22** rule set, what must happen to outputs and temps, what crash report is written, how the 90% manual-review rule applies (or does not) to this abort, and which related audit/OCR implementation items are still unfinished?

<!-- RESPONSE_START -->

## Answer

**Scenario framing.** The invoice has no usable native text layer, so the OCR fallback path (T008 / CIPH-18) engages. A mid-job unhandled worker exception then fires before any export is finalized. As of the 2026-09-22 rule set, this is governed by the **Batch Failure Strategy (T015 / CIPH-25) — fail-closed**, which is recorded as a settled decision and a completed task.

### 1. What must happen to outputs

**No output file is produced at all — for the entire job, not just the failing page.**

- On any unhandled failure, the job **aborts entirely** and the output buffer is **purged**. The decision was explicitly framed as: if 100% of the batch cannot be guaranteed safe, fail closed — **no partial exports**, and successful files from earlier in the batch are *not* kept.
- The mechanism enforcing this is an **atomic rename step at the very end** of the run: the output folder stays empty until the last file is verified. Because the crash occurred **before any export was finalized**, the atomic rename never happens, so the clinic batch's output directory remains empty.
- An **exception hook in the core engine** catches the fault (including low-level segfaults) and signals the controller to **stop all active streams**.
- The AES-256 at-rest sign-off depends on exactly this behavior: an unencrypted partial output left on disk after a crash would have undermined the encryption guarantee, and the pipeline refuses to write plaintext rather than degrade.

*Sources: `SRC-SLACK-12` (Slack: Batch Failure Strategy, 2026-06-12), `SRC-CU-CIPH-25`, `WS-04-policy` Decisions, `SRC-GDOC-35`.*

### 2. What must happen to temps

**Temp files are securely deleted.**

- The fail-closed contract requires temp files to be **securely deleted** on failure. Diana's QA pass on 2026-07-16 confirmed both halves: no output file written on failure, and secure temp deletion.
- Specifically for the OCR path, CIPH-35 (T025) added **cleanup hooks covering both the failure path and the normal completion path**, built from a traced inventory of OCR temp sites. That task is **Completed**; Diana confirmed secure deletion on 2026-08-11 against both failure and completion paths.
- The three OCR temp artifact categories that must be cleared for this run are: (1) the **per-page rasterized image** (one per page, in a process-local temp dir), (2) the **per-page OCR output buffer** — written *before* confidence-threshold filtering is applied, so the 82% raw output is in this buffer and must be removed — and (3) the **run-level manifest** listing which pages fell back to OCR versus native extraction.
- One documented gap: a **hard kill cannot be hooked**. Charlie's stated coverage is "everything the OCR branch can reach on its own" via the failure hook plus the completion hook. An unhandled worker *exception* — the case here — is reachable by the failure hook, so cleanup applies; an outright process kill is outside that guarantee.

*Sources: `SRC-CU-CIPH-35`, `SRC-SLACK-29` (2026-08-09 OCR temp cleanup hooks), `SRC-GDOC-19` (OCR Temp File Path Trace), `SRC-GDOC-40` (Ephemeral OCR Temp Cleanup verification), `SRC-SLACK-12`.*

### 3. What crash report is written

**A crash report is written to a separate `audit_log.json`, before shutdown.**

- It is written to a **separate** file — deliberately not into the (purged) output path — and is written **before the shutdown completes**.
- Contents captured: the **stack trace** and the **filename that triggered the fault** (here, the scanned invoice).
- Rationale, per Diana: the team needs to know *why* it failed, since nothing else survives the abort.

*Sources: `SRC-SLACK-12`, `WS-04-policy` Decisions ("Crash diagnostics go to a separate `audit_log.json`").*

### 4. How the 90% manual-review rule applies (or does not)

**It does not apply to this abort. The 82% confidence never results in a quarantined page here.**

- The rule itself: a **90% confidence threshold** was adopted for v1.0.0 (T014 / CIPH-24). Anything below it is flagged for manual review, and "confidence" deliberately includes **OCR quality**, not only regex match score — a low OCR confidence score for a block of text flags the page regardless of the regex match. So 82% is unambiguously below threshold and *would* normally flag.
- The normal consequence would be routing to the **quarantine folder**, where the document is **held and not exported until a human confirms the redaction**, accompanied by quarantine metadata (**confidence score, page number, and reason flagged**) and visual UI indicators for reviewers.
- **Why it is moot here:** quarantine is a gate on *export*. Fail-closed already guarantees **zero output for the whole job**, so there is nothing to withhold — the stricter rule subsumes the weaker one. Manual review holds a document back from being exported; the abort means no document was exported in the first place, and the entire batch is discarded. There is no quarantined artifact to review, and no partial output to approve.
- **Two further reasons the quarantine path cannot be relied on for this run:**
  1. The confidence-threshold filter is applied **after** the per-page OCR output buffer is written. The crash fired mid-job, so the 82% page's buffer exists as a temp artifact but the filtering/quarantine decision on it is not a finalized product — and that buffer is a cleanup target under the fail-closed deletion, not a preserved review item.
  2. The 90% threshold logic is **not yet fully integrated** (see below), so it is not a settled, dependable behavior even absent the crash.
- Note also that **`audit_log.json` is exempt from the purge** — it is the one artifact that survives the abort by design. The 82% figure is *not* documented as being carried into that crash report; the recorded contents are the stack trace and the triggering filename.

*Sources: `SRC-SLACK-11` (Manual Review Threshold Design), `SRC-CU-CIPH-24`, `WS-04-policy` Decisions and Active Work, `SRC-GDOC-19`.*

### 5. Related audit/OCR implementation items still unfinished

Four items remain open as of the 2026-09-22 work state:

| Item | Status | Detail |
|---|---|---|
| **T016 / CIPH-26 — Audit Trail Logging** | **Active / reopened — open release blocker** | Highest-severity item and directly adjacent to the crash report. Bob refactored the loader for streaming, added SHA-256 hashing of input streams, defined the companion JSON audit schema (hash + redaction map), and on 2026-09-10 wired audit-log generation into the CLI path. But Diana's 2026-09-18 verification found the **CLI-emitted audit records inconsistent with the defined schema**. The 2026-09-15 pre-release audit flagged this as a **release hold**; Diana is keeping the audit-log gate red until schema and records match, since the mismatch "undercuts the audit trail as release evidence." Bob has another pass queued. Assignee: Diana; Priority: High. |
| **T014 / CIPH-24 — Manual Review Threshold for Low-Confidence OCR** | **Active** | Quarantine folder, quarantine metadata, and Charlie's UI indicators are built, and Diana ran a full end-to-end pass on 2026-09-18 (detection → quarantine → metadata → UI markers → manual approval). The pipeline holds together, but **90% threshold tuning is still in progress** — Diana wants another round of testing before calling it locked, and the acceptance criterion "90% confidence-threshold logic fully integrated with the quarantine path" is still open. Assignee: Diana. |
| **T008 / CIPH-18 — OCR Fallback for Non-Text-Layer Documents** | **Active** | The Tesseract POC succeeded; profiling identified the page-serial loop as a latency bottleneck, and Charlie implemented a **per-page multiprocessing pool** and retuned confidence thresholds. Diana is **still wiring OCR fallback output into the main scanner pipeline**, and **confidence tuning continues as of September**. Acceptance criterion for clean integration of multiprocessing and threshold tuning with the scan pipeline is not met. Assignee: Charlie. WS-01's "Next Update Needed" still lists OCR performance status. |
| **T025 / CIPH-35 — Ephemeral OCR temp cleanup** | **Completed** (listed for completeness) | Not unfinished. Cleanup hooks verified on both failure and completion paths, secure deletion confirmed 2026-08-11. The 2026-08-20 report explicitly states it **does not raise a separate open remanence finding**. The only residual caveat is the acknowledged inability to hook a hard process kill. |

By contrast, **T015 / CIPH-25 (fail-closed) is Completed** and QA-validated — the rules in sections 1–3 above are settled and enforceable today. What is *not* settled is the audit-record schema that the surviving `audit_log.json` diagnostics would ultimately need to conform to, and the threshold logic that would have governed the 82% page had the job survived.

### Summary

The batch aborts wholesale: no output file for any file in the clinic batch, the output buffer is purged, the atomic rename never fires so the output folder stays empty, and all OCR temps (rasterized page images, pre-filter OCR output buffers, run manifest) are securely deleted. A crash report capturing the stack trace and the triggering filename is written to a separate `audit_log.json` before shutdown. The 82% confidence would ordinarily breach the 90% threshold and quarantine the page for manual review, but that rule is moot here — fail-closed already produces zero output, so there is nothing to hold back, and no reviewable artifact survives. Still unfinished: the audit-trail CLI/schema mismatch (T016, an active release blocker), the 90% threshold integration itself (T014), and the OCR fallback pipeline wiring and confidence tuning (T008).
