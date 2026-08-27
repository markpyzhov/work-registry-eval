# Is custom temporality-selector configuration supported in OpenTelemetry Go `v1.39.0`, and what related selector API did that release ship?

<!-- RESPONSE_START -->

No. Custom temporality-selector parsing/configuration in the SDK was rejected in favor of the full OpenTelemetry configuration-file format.

Instead, OpenTelemetry Go `v1.39.0` shipped these selector functions in `go.opentelemetry.io/otel/sdk/metric`:

- `DeltaTemporalitySelector`
- `CumulativeTemporalitySelector`
- `LowMemoryTemporalitySelector`

Citations: `work-states/WS-02-metrics-performance.md` (T004; `SRC-NOTE-03`, `SRC-NOTE-04`, `SRC-REL-01`); `opentelemetry/releases/release-v1.39.0.md` (`SRC-REL-01`, PR #7434).
