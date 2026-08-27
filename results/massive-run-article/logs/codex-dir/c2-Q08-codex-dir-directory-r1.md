# What is the status of `opentelemetry-go-contrib` issue `#7254` (otelhttp error recording under the new semantic conventions)?

<!-- RESPONSE_START -->

`opentelemetry-go-contrib#7254` is **closed as completed** (closed 2026-01-13) and was moved to the `v1.40.0` milestone. The work-state treats the otelhttp error-recording task as complete, but **no available release record establishes that the fix shipped**. [WS-05 Contrib](work-states/WS-05-contrib.md), [issue record](opentelemetry/issues/opentelemetry-go-contrib-7254.md)

The issue concerned whether `otelhttp` should record terminating errors as exception events via `span.RecordError`, versus setting `error.type` and span error status under the new semantic conventions. The discussion ultimately aligned the proposed handling of terminating errors with setting `error.type` and error status rather than calling `RecordError`; semantic-convention clarification/stabilization was part of the surrounding concern. [issue record](opentelemetry/issues/opentelemetry-go-contrib-7254.md)

Historically, it was considered a possible otelhttp stabilization blocker, with Robert assigned to clarify the semconv interpretation, but the work state records it as resolved and closed. [meeting note](opentelemetry/meeting-notes/entry-3479655348.md)
