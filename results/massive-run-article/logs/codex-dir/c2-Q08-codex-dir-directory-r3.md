# What is the status of `opentelemetry-go-contrib` issue `#7254` (otelhttp error recording under the new semantic conventions)?

<!-- RESPONSE_START -->

`opentelemetry-go-contrib#7254` is **closed as completed**: the work registry marks its mapped task (`T002`) complete, and the issue was closed by `pellared` on **2026-01-13**. It was moved from the `v1.39.0` milestone to `v1.40.0` on 2025-12-04. [WS-05-contrib.md](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md) · [opentelemetry-go-contrib-7254.md](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/issues/opentelemetry-go-contrib-7254.md)

The issue concerned whether `otelhttp` should create exception events via `span.RecordError` for terminating errors under the new semantic conventions. The recorded direction was to set `error.type` and span error status for terminating errors rather than call `RecordError`; the topic had been a potential `otelhttp` stabilization blocker because it required semantic-convention/spec interpretation. [opentelemetry-go-contrib-7254.md](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/issues/opentelemetry-go-contrib-7254.md) · [entry-3479655348.md](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3479655348.md)

However, **delivery in a release is not established by the corpus**: there is no release source after `v1.39.0` that demonstrates which release contains the resolution. [WS-05-contrib.md](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md)
