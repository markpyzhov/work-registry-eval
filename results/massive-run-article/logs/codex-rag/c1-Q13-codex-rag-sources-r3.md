# A clinic batch includes a scanned invoice with no usable native text layer, so OCR runs. Mid-job an unhandled worker exception fires before any export is finalized. OCR confidence on the page being processed was 82%. As of the **2026-09-22** rule set, what must happen to outputs and temps, what crash report is written, how the 90% manual-review rule applies (or does not) to this abort, and which related audit/OCR implementation items are still unfinished?

<!-- RESPONSE_START -->

The job must fail closed: abort the entire batch, stop active streams, purge its output buffer, and produce no partial exports—the output folder remains empty because finalization is atomic. OCR temporary artifacts must be securely deleted on the failure path. [SRC-SLACK-12; SRC-CU-CIPH-25; SRC-GDOC-40]

Before shutdown, write a separate `audit_log.json` containing the exception stack trace and the filename that triggered the fault. [SRC-SLACK-12]

The 82% OCR confidence is below the intended 90% manual-review threshold. In a completed flow, that page would be quarantined and withheld from export pending human approval. Here, however, the unhandled worker exception aborts the whole job first: there is no surviving page/output to route for review. Moreover, the 90% threshold’s end-to-end integration and tuning were still Active as of September 18. [SRC-SLACK-11; SRC-CU-CIPH-24]

Still unfinished or unresolved related work as of the rule date:

- **CIPH-18 OCR fallback:** production integration of per-page multiprocessing and confidence-threshold tuning with the scan pipeline remains Active. [SRC-CU-CIPH-18]
- **CIPH-24 manual review:** 90% threshold integration/tuning with quarantine remains Active. [SRC-CU-CIPH-24]
- **Audit-log release gate:** CLI-generated audit records still do not match the defined schema. [SRC-MEET-10]
- **Crash-report privacy audit:** Sentry’s independent handling of telemetry opt-out/minidump uploads has not been audited. [SRC-GDOC-51]
- **OCR dependency audit:** the rasterizer still needs a suitable permissively licensed replacement, and Tesseract `eng.traineddata` provenance remains unverified. [SRC-GDOC-41]
