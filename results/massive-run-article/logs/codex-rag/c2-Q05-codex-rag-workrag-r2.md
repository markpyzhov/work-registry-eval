# Is custom temporality-selector configuration supported in OpenTelemetry Go `v1.39.0`, and what related selector API did that release ship?

<!-- RESPONSE_START -->

No. Custom temporality-selector parsing/configuration was rejected for the Go SDK; users were directed to the full OpenTelemetry configuration-file format instead. (`SRC-NOTE-03`)

OpenTelemetry Go `v1.39.0` did ship selector functions in `go.opentelemetry.io/otel/sdk/metric`: `DeltaTemporalitySelector`, `CumulativeTemporalitySelector`, and `LowMemoryTemporalitySelector` (PR #7434). (`SRC-REL-01`)
