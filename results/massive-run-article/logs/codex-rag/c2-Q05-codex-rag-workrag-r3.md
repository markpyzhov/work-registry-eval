# Is custom temporality-selector configuration supported in OpenTelemetry Go `v1.39.0`, and what related selector API did that release ship?

<!-- RESPONSE_START -->

No. OpenTelemetry Go v1.39.0 did **not** support custom temporality-selector parsing/configuration; that approach was rejected in favor of the full OpenTelemetry configuration-file format. [WS-02 Metrics Performance, record `a4e6f21fa31a6b3d`]

It did ship selector functions in `go.opentelemetry.io/otel/sdk/metric`:

- `DeltaTemporalitySelector`
- `CumulativeTemporalitySelector`
- `LowMemoryTemporalitySelector`

These were released via #7434. [Release v1.39.0, `SRC-REL-01`, record `ed28cf4950c6c6d3`]
