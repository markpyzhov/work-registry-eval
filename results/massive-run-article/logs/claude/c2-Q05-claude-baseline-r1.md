# Is custom temporality-selector configuration supported in OpenTelemetry Go `v1.39.0`, and what related selector API did that release ship?

<!-- RESPONSE_START -->

**Short answer:** Yes — custom temporality selection is supported, but it is not a v1.39.0 feature. It has been part of the stable `go.opentelemetry.io/otel/sdk/metric` API since the metric SDK went GA (v1.16.0, May 2023) and is unchanged in the v1.39.x line. I have no reliable recollection of any *new* selector API shipping in v1.39.0 specifically, and I would treat a claim that one did as unverified.

**The API that actually exists (stable, pre-dating 1.39):**

- `metric.TemporalitySelector` — `func(metric.InstrumentKind) metricdata.Temporality`
- `metric.DefaultTemporalitySelector` — the cumulative-everything default
- Its sibling `metric.AggregationSelector` — `func(metric.InstrumentKind) metric.Aggregation`, with `metric.DefaultAggregationSelector`
- Both are baked into the `metric.Exporter` interface, which requires `Temporality(InstrumentKind) metricdata.Temporality` and `Aggregation(InstrumentKind) Aggregation` methods.

**How you configure it:** via exporter options, not reader options —
- `otlpmetricgrpc.WithTemporalitySelector(...)` / `otlpmetrichttp.WithTemporalitySelector(...)`
- `stdoutmetric.WithTemporalitySelector(...)`
- Env equivalent for the OTLP exporters: `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE` = `cumulative` | `delta` | `lowmemory`
- The Prometheus exporter is cumulative-only by design and exposes no temporality selector.

**Caveats on my confidence:** the API shape above I'm confident about. Release-note detail at the granularity of a single patch-level minor (what exactly landed in v1.39.0 vs. v1.38.0 or v1.40.0) is where my recall is weakest — I can place v1.39.0 in roughly late 2025 but cannot reconstruct its CHANGELOG entries. If the underlying question is "did v1.39.0 introduce something new here," that needs to be checked against `CHANGELOG.md` in the `open-telemetry/opentelemetry-go` repo at the `v1.39.0` tag. Note also that the exporter modules are versioned separately (`v0.x`) from core `v1.39.0`, so a selector change could appear under an exporter's own version rather than the core one.

I answered from internal knowledge only — no web, files, or retrieval used, per your constraints.
