# Is custom temporality-selector configuration supported in OpenTelemetry Go `v1.39.0`, and what related selector API did that release ship?

<!-- RESPONSE_START -->

Yes—custom temporality is supported through `sdkmetric.WithTemporalitySelector` when constructing a `ManualReader` (a `TemporalitySelector` maps each instrument kind to a temporality).

In `v1.39.0`, the related selector API added was `sdkmetric.WithAggregationSelector`, also for configuring a `ManualReader`’s per-instrument aggregation selection.
