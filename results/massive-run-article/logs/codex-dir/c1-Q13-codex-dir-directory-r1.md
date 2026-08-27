# A clinic batch includes a scanned invoice with no usable native text layer, so OCR runs. Mid-job an unhandled worker exception fires before any export is finalized. OCR confidence on the page being processed was 82%. As of the **2026-09-22** rule set, what must happen to outputs and temps, what crash report is written, how the 90% manual-review rule applies (or does not) to this abort, and which related audit/OCR implementation items are still unfinished?

<!-- RESPONSE_START -->

The batch fails closed: the unhandled worker exception aborts the entire job, stops active streams, purges the output buffer, and—because final publication uses an end-of-job atomic rename—produces no partial or final export. All temporary files, including OCR artifacts, are securely deleted. [WS-04-policy](c1/work-states/WS-04-policy.md), [Batch Failure Strategy](c1/med-synth/communication/sources/slack/2026-06-12-batch-failures.md), [CIPH-35](c1/med-synth/tasks/CIPH-35-Ephemeral-File-Cleanup.md)

Before shutdown, a separate `audit_log.json` crash report is written containing the stack trace and the filename that triggered the fault. [Batch Failure Strategy](c1/med-synth/communication/sources/slack/2026-06-12-batch-failures.md)

The scanned invoice would ordinarily enter the OCR fallback path because it has no usable native text layer. Its 82% confidence is below the adopted 90% threshold, so in a non-crash completion path it belongs in manual-review quarantine, with confidence/page/reason metadata, and is withheld from export until human approval. But the exception abort is not a low-confidence disposition: it overrides that path, so the job is aborted rather than exported or merely quarantined. Moreover, the 90% threshold’s end-to-end integration remains active/not fully complete. [WS-01-engine](c1/work-states/WS-01-engine.md), [WS-04-policy](c1/work-states/WS-04-policy.md), [CIPH-24](c1/med-synth/tasks/CIPH-24-Manual-Review-Threshold.md)

Unfinished related work as of 2026-09-22:

- OCR fallback (CIPH-18/T008) remains active: per-page multiprocessing exists, but scanner-pipeline wiring and confidence tuning are still in progress. [WS-01-engine](c1/work-states/WS-01-engine.md), [CIPH-18](c1/med-synth/tasks/CIPH-18-OCR-Fallback.md)
- Manual-review workflow (CIPH-24/T014) remains active: quarantine/UI/metadata have been exercised, but the 90% integration is unfinished. [WS-04-policy](c1/work-states/WS-04-policy.md), [CIPH-24](c1/med-synth/tasks/CIPH-24-Manual-Review-Threshold.md)
- Audit trail logging (CIPH-26/T016) remains an open release blocker: SHA-256 input hashes, redaction-map JSON, and CLI wiring were implemented, but CLI-emitted audit records do not match/validate against the defined schema. This is distinct from the fail-closed crash diagnostic file. [WS-04-policy](c1/work-states/WS-04-policy.md), [CIPH-26](c1/med-synth/tasks/CIPH-26-Audit-Trail-Logging.md), [Pre-Release Audit](c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md)
