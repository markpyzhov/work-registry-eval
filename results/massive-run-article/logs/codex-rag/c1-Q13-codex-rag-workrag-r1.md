# A clinic batch includes a scanned invoice with no usable native text layer, so OCR runs. Mid-job an unhandled worker exception fires before any export is finalized. OCR confidence on the page being processed was 82%. As of the **2026-09-22** rule set, what must happen to outputs and temps, what crash report is written, how the 90% manual-review rule applies (or does not) to this abort, and which related audit/OCR implementation items are still unfinished?

<!-- RESPONSE_START -->

The batch must fail closed: abort the entire job, stop active streams, purge the output buffer, produce no output/export file, and securely delete all temporary files. The output folder remains empty because final publication occurs only after final verification. 【SRC-SLACK-12, 7d969f7c78a9200e】【WS-04-policy, 406953eb42da656a】

Before shutdown, write a separate `audit_log.json` crash report containing the stack trace and the filename that triggered the fault. 【SRC-SLACK-12, 7d969f7c78a9200e】

The 82% OCR confidence is below the 90% review threshold. In a normally completed processing path, that page would be quarantined for manual review and withheld from export pending human confirmation. Here, though, the unhandled worker exception controls: the job aborts and its outputs/temps are purged, so it does not proceed as a reviewable quarantine/export workflow. This is an inference from the two governing rules. 【SRC-SLACK-11, b1a90ff76c3fb32a】【SRC-SLACK-12, 7d969f7c78a9200e】

Still unfinished as of 2026-09-22:

- **T014 / CIPH-24:** manual-review workflow—the 90% threshold’s integration/tuning with quarantine remains active.
- **T016 / CIPH-26:** audit-trail logging—CLI-emitted records still fail the defined JSON schema, a release blocker.
- **T008 / CIPH-18:** OCR fallback—scan-pipeline wiring and confidence tuning remain active, despite page-level multiprocessing being integrated.

【WS-04-policy, 917ecd0b3736fd18】【WS-04-policy, 99fa4c3e7450f6a7】【WS-01-engine, 280c5cc6486fd51d】
