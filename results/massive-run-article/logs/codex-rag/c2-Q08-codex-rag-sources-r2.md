# What is the status of `opentelemetry-go-contrib` issue `#7254` (otelhttp error recording under the new semantic conventions)?

<!-- RESPONSE_START -->

`opentelemetry-go-contrib#7254` is **closed as completed**. It was closed by `pellared` on **2026-01-13**, assigned to **v1.40.0** (whose milestone is also closed), and cross-references PR **#8386** immediately before closure. [SRC-ISSUE-02] [SRC-MILE-04]

The reported bug was that `otelhttp`’s new-semantic-convention path did not reliably call `span.RecordError(err)`, because the condition conflicted with how `ErrorType` behaved. The eventual direction in discussion was to follow the semantic-convention guidance: do **not** use `RecordError` for terminating errors; reserve it for non-terminating/intermediate errors such as retry attempts. [SRC-ISSUE-02]
