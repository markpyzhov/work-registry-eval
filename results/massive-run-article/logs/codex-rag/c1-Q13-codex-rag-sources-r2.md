# A clinic batch includes a scanned invoice with no usable native text layer, so OCR runs. Mid-job an unhandled worker exception fires before any export is finalized. OCR confidence on the page being processed was 82%. As of the **2026-09-22** rule set, what must happen to outputs and temps, what crash report is written, how the 90% manual-review rule applies (or does not) to this abort, and which related audit/OCR implementation items are still unfinished?

<!-- RESPONSE_START -->

The batch must fail closed: abort the entire job, stop active streams, purge the output buffer, and produce no partial/final exports—the output folder remains empty because publication occurs only after final verification. All OCR temps must be securely deleted on the failure path. (`SRC-SLACK-12`; `SRC-CU-CIPH-35`)

Before shutdown, write a separate `audit_log.json` crash report containing the stack trace and the filename that triggered the worker fault. (`SRC-SLACK-12`)

The 82% OCR confidence is below the proposed 90% threshold. In a non-crash processing outcome, it is intended to send the page/document to quarantine for human confirmation, with confidence, page, and reason metadata, and prevent export. But this is an abort, so fail-closed cancellation—not manual review—governs the result; there is no export to hold for approval. Also, as of the date given, the 90% threshold’s full quarantine-path integration/tuning remains active, so it is not yet a locked rule. (`SRC-SLACK-11`; `SRC-CU-CIPH-24`)

Still unfinished related work:

- **CIPH-18 OCR fallback:** scan-pipeline integration of per-page multiprocessing and confidence-threshold tuning remains active. (`SRC-CU-CIPH-18`)
- **CIPH-24 manual review:** end-to-end pieces were exercised, but full 90% threshold integration remains active. (`SRC-CU-CIPH-24`)
- **CIPH-26 audit trail:** CLI-emitted audit records still fail to match the defined JSON schema, leaving the audit gate/release blocker open. (`SRC-CU-CIPH-26`; `SRC-MEET-10`)

OCR temp cleanup itself is completed and verified for both failure and normal completion paths. (`SRC-GDOC-40`)
