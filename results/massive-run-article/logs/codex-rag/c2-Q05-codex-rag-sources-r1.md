# Is custom temporality-selector configuration supported in OpenTelemetry Go `v1.39.0`, and what related selector API did that release ship?

<!-- RESPONSE_START -->

No—custom temporality-selector configuration snippets were not supported; the SIG recommended using the full OpenTelemetry configuration-file format instead. [SRC-NOTE-03]

OpenTelemetry Go `v1.39.0` did ship predefined selector functions in `go.opentelemetry.io/otel/sdk/metric`:

- `DeltaTemporalitySelector`
- `CumulativeTemporalitySelector`
- `LowMemoryTemporalitySelector`

[SRC-REL-01]
