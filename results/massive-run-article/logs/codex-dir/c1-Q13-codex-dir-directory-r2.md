# A clinic batch includes a scanned invoice with no usable native text layer, so OCR runs. Mid-job an unhandled worker exception fires before any export is finalized. OCR confidence on the page being processed was 82%. As of the **2026-09-22** rule set, what must happen to outputs and temps, what crash report is written, how the 90% manual-review rule applies (or does not) to this abort, and which related audit/OCR implementation items are still unfinished?

<!-- RESPONSE_START -->

For a scanned invoice, OCR fallback is intended but still active; scan-pipeline wiring and confidence tuning remain unfinished. [WS-01](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-01-engine.md:31)

At 82% confidence, the v1.0 policy is manual-review quarantine (<90%), with metadata/UI indicators; threshold integration remains active. [WS-04](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md:48)

An unhandled worker error before export overrides that path: fail-closed abort, no output (including no partial export), secure deletion of temps, and crash diagnostics written separately to `audit_log.json`; QA validated this. [WS-04](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md:61)

Caveat: the normal audit trail is unfinished/release-blocking because CLI-emitted records fail schema validation. [CIPH-26](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-26-Audit-Trail-Logging.md:12)
