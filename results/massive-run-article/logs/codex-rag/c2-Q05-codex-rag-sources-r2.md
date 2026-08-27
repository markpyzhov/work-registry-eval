# Is custom temporality-selector configuration supported in OpenTelemetry Go `v1.39.0`, and what related selector API did that release ship?

<!-- RESPONSE_START -->

No. The Go SIG explicitly decided against SDK support for custom temporality-selector configuration snippets, directing users to the full OpenTelemetry configuration-file format instead. [SRC-NOTE-03]

However, `v1.39.0` did ship predefined selector functions in `go.opentelemetry.io/otel/sdk/metric`: `DeltaTemporalitySelector`, `CumulativeTemporalitySelector`, and `LowMemoryTemporalitySelector`. [SRC-REL-01]
