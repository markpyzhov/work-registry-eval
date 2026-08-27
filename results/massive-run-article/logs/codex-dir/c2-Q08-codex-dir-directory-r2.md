# What is the status of `opentelemetry-go-contrib` issue `#7254` (otelhttp error recording under the new semantic conventions)?

<!-- RESPONSE_START -->

`opentelemetry-go-contrib#7254` is **closed as completed** (closed 2026-01-13), with milestone **v1.40.0**. The Corpus 2 work registry marks its task complete, but explicitly says **no release evidence establishes delivery**. [Issue record](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/issues/opentelemetry-go-contrib-7254.md:9) [Work state](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md:53)

The underlying defect was that `otelhttp`’s `ErrorType` always produced an attribute, preventing the intended `span.RecordError(err)` path. The discussed resolution for a terminating error was to set `error.type` and an error span status, rather than record an exception event. [Issue record](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/issues/opentelemetry-go-contrib-7254.md:19) [Resolution discussion](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/issues/opentelemetry-go-contrib-7254.md:247)

Historically it was considered a possible `otelhttp` stabilization blocker because it depended on interpreting evolving semantic-convention wording; Robert was assigned to clarify the approach. [SIG note](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3479655348.md:56) The issue was moved from v1.39.0 to v1.40.0, cross-referenced to PR #8386 on 2026-01-12, and closed the next day; the supplied corpus does not establish whether or when the change shipped in a release. [Timeline](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/issues/opentelemetry-go-contrib-7254.md:314)
