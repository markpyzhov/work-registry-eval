# A clinic batch includes a scanned invoice with no usable native text layer, so OCR runs. Mid-job an unhandled worker exception fires before any export is finalized. OCR confidence on the page being processed was 82%. As of the **2026-09-22** rule set, what must happen to outputs and temps, what crash report is written, how the 90% manual-review rule applies (or does not) to this abort, and which related audit/OCR implementation items are still unfinished?

<!-- RESPONSE_START -->

## Answer (rule set as of 2026-09-22)

The authoritative Work State is `WS-04: Regulatory Compliance, Privacy, and Audits` (Last Updated 2026-09-22; index as-of `2026-09-22T12:00:00Z`), with the OCR temp-file half governed by `WS-07: Data Persistence, Encryption, and Secure Storage`.

### 1. Outputs — fail-closed, whole job aborts
- **Batch Failure Strategy (T015 / CIPH-25)**: on *any* unhandled failure the job aborts with **no output file produced**. This is job-wide, not per-file: an unhandled exception in any worker aborts the entire job and purges the output buffer — no partial exports, even for files that already succeeded.
- Mechanism: an **atomic rename at the very end** — the output folder stays empty until the last file is verified — so an abort mid-job leaves nothing behind. A low-level exception hook in the core engine also signals the controller to stop all active streams.
- Status: **Completed**. Bob implemented 2026-06-15; Diana QA-validated on 2026-07-16 that no output file is produced on failure. This behavior is a hard dependency of the AES-256 at-rest sign-off (an unencrypted partial output after a crash would void the encryption guarantee).
- Caveat on stale evidence: the 2026-06-15 daily brief says "corrupted files quarantine to `.failed` instead of crashing the batch." That does **not** describe the current rule — the authoritative WS-04 state and CIPH-25 both specify whole-job abort with zero output.

### 2. Temps — securely deleted on the failure path
- Batch level: temp files are **securely deleted** on failure (QA-validated 2026-07-16 alongside the no-output check).
- OCR level (T025 / CIPH-35, **Completed**): in-process cleanup hooks fire on **both the failure path and the completion path**, purging ephemeral OCR temps from `/tmp/cipherdoc-*` immediately after processing. Diana confirmed secure deletion on 2026-08-11 across both paths. The design supersedes cron-based cleanup in favor of in-process `atexit` hooks for a zero-residual footprint.
- Known coverage limit: Charlie noted the hooks **cannot cover a hard kill** of the process — they cover "everything the OCR branch can reach on its own." An unhandled worker exception is exactly such a reachable failure path, so this scenario **is** covered; a SIGKILL would not be.

### 3. Crash report
A crash report is written to a **separate `audit_log.json`** before shutdown, capturing the **stack trace** and the **filename that triggered the fault**. It is deliberately separate from the (nonexistent) output artifacts — diagnostics survive, redacted content does not.

### 4. The 90% manual-review rule — adopted, but it does not govern this abort
- The rule: **90% confidence threshold adopted for v1.0.0**; anything below is flagged for manual review, factoring in *both* regex match score and OCR block confidence. Sub-threshold documents land in a quarantine folder and **are not exported until a human confirms the redaction**, with metadata (confidence score, page number, flag reason) and UI indicators for reviewers.
- At **82%**, the page is below threshold and would normally quarantine. But quarantine is a **gate on export**, and fail-closed has already removed the thing it gates: the job aborted before any export was finalized, no output file exists, and temps were purged. There is nothing to hold for review and nothing unsafe released — the fail-closed abort is the stricter, controlling outcome. What is preserved is the crash record in `audit_log.json`, not a quarantined page.
- Additionally, the rule is **not yet fully operative**: T014 / CIPH-24 remains **Active**. The 2026-09-18 end-to-end pass (detection → quarantine → metadata → UI markers → manual approval) held together, but Diana explicitly says the 90% threshold tuning "is still in progress — I want another round of testing before I'd call it locked."

### 5. Related audit/OCR items still unfinished as of 2026-09-22
- **T016 / CIPH-26 — Compliance Audit Trail Logging (Active/reopened, release blocker).** SHA-256 input hashing, the companion JSON schema (hash + redaction map), and CLI wiring are all built, but Diana's 2026-09-18 verification found **CLI-emitted audit records do not validate against the defined schema**. The 2026-09-15 pre-release audit kept this as a red release gate ("Until those match, I can't clear the audit gate"). Practical implication: compliance audit records emitted around an abort like this may not be schema-valid evidence.
- **T014 / CIPH-24 — Manual Review Threshold (Active).** 90% threshold logic still being integrated with the quarantine path and metadata injection for visual indicators.
- **T008 / CIPH-18 — OCR Fallback (Active).** Charlie added per-page multiprocessing and retuned confidence thresholds; Diana is still wiring OCR results into the main scanner pipeline, and **confidence tuning continues as of September**. The 82% figure therefore comes from a pipeline still under integration and a threshold not yet locked.
- **Adjacent, engine-side:** T007 / CIPH-17 (multi-page offset mismatch) remains **Blocked** on upstream `pdfminer.six` #992 (earliest mid-October) with a Legal sign-off gate on any pre-normalization workaround.
- **Adjacent, crash-reporting privacy:** the third-party Electron crash reporter (Sentry) has **not** been audited for whether it independently respects the telemetry opt-out or needs its own disable hook for minidump uploads — full privacy compliance for air-gapped/opt-out users can't be claimed until that path is audited.

### Files supporting these claims (absolute paths)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md` — authoritative fail-closed rule, 90% threshold decision, T014/T016 active status
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-07-storage.md` — OCR temp cleanup (T025), `atexit` supersession
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-01-engine.md` — T008 OCR active, T007 blocked
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/index.md` — as-of timestamp, active/blocked list
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-06-12-batch-failures.md` — abort + purge, atomic rename, `audit_log.json` crash report
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-25-Batch-Fail-Closed.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-35-Ephemeral-File-Cleanup.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-09-ocr-temp-cleanup-hooks.md` — both paths covered; hard-kill limit
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-07-ocr-temp-file-trace.md` — temp-site inventory origin
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-20-Ephemeral-File-Cleanup-Audit-Report.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-24-Manual-Review-Threshold.md` and `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-06-28-manual-review-threshold.md` — 90% rule, quarantine-blocks-export, still tuning
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-26-Audit-Trail-Logging.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-07-08-Compliance-Audit-Trail.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` — schema/record mismatch hold
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-18-OCR-Fallback.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-07-05-OCR-Progress-Sync.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-06-28-OCR-Pipeline-Design.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-07-Local-Encryption-at-Rest-Security-Evaluation.md` — encryption sign-off depends on fail-closed deletion
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-09-06-Telemetry-Opt-Out-Design-and-Compliance-Check.md` — unaudited Sentry crash-reporter path
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-06-15-daily-brief.md` — the superseded `.failed` quarantine wording
