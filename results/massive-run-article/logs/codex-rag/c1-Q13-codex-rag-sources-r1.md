# A clinic batch includes a scanned invoice with no usable native text layer, so OCR runs. Mid-job an unhandled worker exception fires before any export is finalized. OCR confidence on the page being processed was 82%. As of the **2026-09-22** rule set, what must happen to outputs and temps, what crash report is written, how the 90% manual-review rule applies (or does not) to this abort, and which related audit/OCR implementation items are still unfinished?

<!-- RESPONSE_START -->

The worker exception causes a **fail-closed abort**: stop active streams, abort the entire batch, purge the output buffer, and leave **no finalized or partial exports**. OCR temporary artifacts must be securely deleted on the failure path. [SRC-SLACK-12; SRC-CU-CIPH-35]

Before shutdown, write a separate `audit_log.json` crash report containing:

- The exception stack trace
- The filename that triggered the fault

[SRC-SLACK-12]

The 82% OCR result is below the intended 90% manual-review threshold, so in a non-crashing run it would be quarantined and withheld from export pending human confirmation. But this is an abort, not a completed low-confidence workflow: the job-level fail-closed rule takes precedence, so there is no output to quarantine or manually approve. Also, as of 2026-09-22, the 90% threshold’s full quarantine-path integration was still in progress. [SRC-SLACK-11; SRC-CU-CIPH-24; SRC-SLACK-12]

Still unfinished related work:

- **CIPH-18 — OCR fallback:** scan-pipeline integration of per-page multiprocessing and confidence-threshold tuning remains active. [SRC-CU-CIPH-18]
- **CIPH-24 — low-confidence manual review:** full 90% threshold integration with quarantine remains active. [SRC-CU-CIPH-24]
- **CIPH-26 — audit trail logging:** CLI-emitted audit records still fail to match the defined companion JSON schema, an open release blocker. [SRC-CU-CIPH-26]

The temp-cleanup work itself is completed and verified for both failure and completion paths. [SRC-CU-CIPH-35]
