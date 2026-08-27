# What is the status of `opentelemetry-go-contrib` issue `#7254` (otelhttp error recording under the new semantic conventions)?

<!-- RESPONSE_START -->

`opentelemetry-go-contrib#7254` is **closed as completed**. It was closed by pellared on **2026-01-13**, assigned to milestone **v1.40.0** (which is itself closed). The issue had been linked to contrib PR **#8386** immediately before closure. [SRC-ISSUE-02; SRC-MILE-04]

The underlying bug was that `otelhttp`’s new-semconv path could not record an error because its `ErrorType` behavior conflicted with the `RecordError` guard. The discussion aligned toward following the semantic conventions: for terminating errors, set `error.type` and span error status rather than unconditionally emitting an exception event; `RecordError` remains relevant for non-terminating/retry scenarios. [SRC-ISSUE-02]
