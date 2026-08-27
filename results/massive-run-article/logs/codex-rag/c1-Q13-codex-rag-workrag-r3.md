# A clinic batch includes a scanned invoice with no usable native text layer, so OCR runs. Mid-job an unhandled worker exception fires before any export is finalized. OCR confidence on the page being processed was 82%. As of the **2026-09-22** rule set, what must happen to outputs and temps, what crash report is written, how the 90% manual-review rule applies (or does not) to this abort, and which related audit/OCR implementation items are still unfinished?

<!-- RESPONSE_START -->

The exception wins: the entire batch aborts fail-closed. No output file or partial export is produced, the output buffer is purged, and all temporary files—including OCR temps—are securely deleted. 【WS-04-policy.md, `406953eb42da656a`; SRC-CU-CIPH-25】

Before shutdown, a separate `audit_log.json` crash report is written containing the triggering filename and stack trace. 【SRC-SLACK-12, `7d969f7c78a9200e`】

At 82%, the page is below the adopted 90% OCR threshold, so on a non-crashing processing path it would be quarantined for manual review with confidence/page/reason metadata and withheld from export pending human approval. Here, it does not preserve a reviewable output: the unhandled worker exception aborts the batch and cleanup removes outputs and temps. Also, the 90% quarantine-path integration remains active rather than fully complete. 【SRC-SLACK-11, `b1a90ff76c3fb04a1`; WS-04-policy.md, `917ecd0b3736fd18`】

Still unfinished as of 2026-09-22:

- **CIPH-18 / T008:** OCR fallback—scanner-pipeline wiring and confidence tuning remain active. 【WS-01-engine.md, `280c5cc6486fd51d`】
- **CIPH-24 / T014:** manual-review quarantine—90% threshold integration with metadata/UI remains active. 【WS-04-policy.md, `917ecd0b3736fd18`】
- **CIPH-26 / T016:** audit-trail logging—CLI-emitted records do not yet match the required schema; this is a release hold. 【WS-04-policy.md, `917ecd0b3736fd18`】
- **CIPH-40 / T030:** license-compliance review remains reopened while an Apache/MIT replacement for an AGPL parser is sought. 【WS-04-policy.md, `917ecd0b3736fd18`】
