# Is custom temporality-selector configuration supported in OpenTelemetry Go `v1.39.0`, and what related selector API did that release ship?

<!-- RESPONSE_START -->

No. The Go SIG explicitly declined custom temporality-selector configuration snippets, preferring the full OpenTelemetry configuration-file format. [SRC-NOTE-03]

OpenTelemetry Go `v1.39.0` did ship three selector functions in `go.opentelemetry.io/otel/sdk/metric`:

- `DeltaTemporalitySelector`
- `CumulativeTemporalitySelector`
- `LowMemoryTemporalitySelector`

[SRC-REL-01]
