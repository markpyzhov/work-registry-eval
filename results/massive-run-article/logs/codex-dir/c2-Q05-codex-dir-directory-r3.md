# Is custom temporality-selector configuration supported in OpenTelemetry Go `v1.39.0`, and what related selector API did that release ship?

<!-- RESPONSE_START -->

No. OpenTelemetry Go rejected custom, string-based temporality-selector parsing/configuration in the SDK; users were directed to the full OpenTelemetry configuration-file format instead. [WS-02](</Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-02-metrics-performance.md:28>) [SIG note](</Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3390010099.md:29>)

Separately, `v1.39.0` shipped built-in selector functions in `go.opentelemetry.io/otel/sdk/metric` via PR `#7434`: `DeltaTemporalitySelector`, `CumulativeTemporalitySelector`, and `LowMemoryTemporalitySelector`. [Release v1.39.0](</Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/releases/release-v1.39.0.md:22>)
