# A clinic batch includes a scanned invoice with no usable native text layer, so OCR runs. Mid-job an unhandled worker exception fires before any export is finalized. OCR confidence on the page being processed was 82%. As of the **2026-09-22** rule set, what must happen to outputs and temps, what crash report is written, how the 90% manual-review rule applies (or does not) to this abort, and which related audit/OCR implementation items are still unfinished?

<!-- RESPONSE_START -->

The batch must fail closed: abort the entire job, stop active streams, purge its output buffer, produce no output file (no partial exports), and securely delete all temporary files. The final-output folder stays empty until end-of-job verification. `SRC-SLACK-12`, `SRC-CU-CIPH-25`

Before shutdown, write a separate `audit_log.json` crash report containing the stack trace and the filename that triggered the fault. `SRC-SLACK-12`

The 82% OCR confidence is below the 90% rule. In a non-aborted run, it would send that page to manual-review quarantine—with confidence, page, and reason metadata—and withhold it from export until human approval. Here, however, the unhandled exception aborts the full batch; it does not yield a quarantined/exportable partial result. The 90% integration itself remains in progress. `SRC-SLACK-11`, `SRC-CU-CIPH-24`

Still unfinished as of 2026-09-22:

- **CIPH-18 / T008:** OCR fallback integration—per-page multiprocessing and confidence-threshold tuning are not yet fully integrated with the scan pipeline.
- **CIPH-24 / T014:** low-confidence OCR manual-review workflow—the 90% threshold integration/tuning remains active.
- **CIPH-26 / T016:** compliance audit trail—the CLI-emitted records still fail to match the defined JSON schema, an open release blocker. `SRC-CU-CIPH-18`, `SRC-CU-CIPH-24`, `SRC-CU-CIPH-26`, `WS-04-policy`
