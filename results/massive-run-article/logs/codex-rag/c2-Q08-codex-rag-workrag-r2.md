# What is the status of `opentelemetry-go-contrib` issue `#7254` (otelhttp error recording under the new semantic conventions)?

<!-- RESPONSE_START -->

Issue **#7254 is closed as completed** (closed **2026-01-13**) and was assigned to milestone **v1.40.0**. The work resolved the otelhttp error-recording behavior under the new semantic conventions. [SRC-ISSUE-02; WS-05]

The issue concerned an inconsistency where `otelhttp` recorded an exception only when `ErrorType` was invalid, despite `ErrorType` always producing an attribute. The discussion settled on treating terminating errors through `error.type` and error status rather than automatically emitting `span.RecordError`; `RecordError` remains relevant for non-terminating/retry scenarios. [SRC-ISSUE-02]

It had been considered a possible otelhttp stabilization blocker, with Robert assigned to clarify the interpretation and proposed resolution. The dataset does **not** establish a release containing the fix. [SRC-NOTE-06; WS-05]
