# What is the status of `opentelemetry-go-contrib` issue `#7254` (otelhttp error recording under the new semantic conventions)?

<!-- RESPONSE_START -->

Issue **#7254 is closed as completed** (closed 2026-01-13) and was tracked under milestone **v1.40.0**. The authoritative work state marks the otelhttp error-recording task complete, but **does not establish a release containing the resolution**.

The issue concerned inconsistent behavior under the new conventions: `error.type` was set while `span.RecordError(err)` was not reached. Discussion centered on whether terminating errors should be represented as events or attributes, pending semantic-convention clarification.  
Records: `WS-05: Contrib Modules` (`T002`), `SRC-ISSUE-02`.
