# Is custom temporality-selector configuration supported in OpenTelemetry Go `v1.39.0`, and what related selector API did that release ship?

<!-- RESPONSE_START -->

No. OpenTelemetry Go `v1.39.0` did not support custom/string-based temporality-selector parsing or configuration; SIG preferred the full OpenTelemetry configuration-file format instead. The earlier exposed-selector proposal was considered API pollution. [WS-02 metrics work state](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-02-metrics-performance.md:37)

The release did ship predefined selector functions in `go.opentelemetry.io/otel/sdk/metric` (PR #7434): `DeltaTemporalitySelector`, `CumulativeTemporalitySelector`, and `LowMemoryTemporalitySelector`. [v1.39.0 release](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/releases/release-v1.39.0.md:22)
