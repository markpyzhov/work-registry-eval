# Is custom temporality-selector configuration supported in OpenTelemetry Go `v1.39.0`, and what related selector API did that release ship?

<!-- RESPONSE_START -->

No. The SIG rejected custom, string-based temporality-selector parsing/configuration in the SDK; users were directed to use the full OpenTelemetry configuration-file format instead. The earlier “Exposed Temporality Selector Function” proposal was subsequently characterized as API pollution and slated for closure. [WS-02 metrics performance](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-02-metrics-performance.md:37), [decision note](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3390010099.md:29)

However, OpenTelemetry Go `v1.39.0` did ship related predefined selector APIs in `go.opentelemetry.io/otel/sdk/metric`, via PR `#7434`: `DeltaTemporalitySelector`, `CumulativeTemporalitySelector`, and `LowMemoryTemporalitySelector`. [v1.39.0 release](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/releases/release-v1.39.0.md:22)
