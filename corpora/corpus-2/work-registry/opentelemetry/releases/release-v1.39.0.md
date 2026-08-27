**Source ID**: [SRC-REL-01]

# Release: v1.39.0 — Release v1.39.0/v0.61.0/v0.15.0/v0.0.14

**Canonical URL**: https://github.com/open-telemetry/opentelemetry-go/releases/tag/v1.39.0  
**Author**: MrAlias  
**Created**: 2025-12-08T16:32:32Z · **Updated**: 2025-12-08T16:45:46Z  
**Collected**: 2026-07-14T14:35:41Z  
**Tag**: `v1.39.0`  
**Published**: 2025-12-08T16:45:46Z

---

## Overview

### Added

- Greatly reduce the cost of recording metrics in `go.opentelemetry.io/otel/sdk/metric` using hashing for map keys. (#7175)
- Add `WithInstrumentationAttributeSet` option to `go.opentelemetry.io/otel/log`, `go.opentelemetry.io/otel/metric`, and `go.opentelemetry.io/otel/trace` packages. This provides a concurrent-safe and performant alternative to `WithInstrumentationAttributes` by accepting a pre-constructed `attribute.Set`. (#7287)
- Add experimental observability for the Prometheus exporter in `go.opentelemetry.io/otel/exporters/prometheus`. Check the `go.opentelemetry.io/otel/exporters/prometheus/internal/x` package documentation for more information. (#7345)
- Add experimental observability metrics in `go.opentelemetry.io/otel/exporters/otlp/otlplog/otlploggrpc`. (#7353)
- Add temporality selector functions `DeltaTemporalitySelector`, `CumulativeTemporalitySelector`, `LowMemoryTemporalitySelector` to `go.opentelemetry.io/otel/sdk/metric`. (#7434)
- Add experimental observability metrics for simple log processor in `go.opentelemetry.io/otel/sdk/log`. (#7548)
- Add experimental observability metrics in `go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc`. (#7459)
- Add experimental observability metrics in `go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp`. (#7486)
- Add experimental observability metrics for simple span processor in `go.opentelemetry.io/otel/sdk/trace`. (#7374)
- Add experimental observability metrics in `go.opentelemetry.io/otel/exporters/otlp/otlplog/otlploghttp`. (#7512)
- Add experimental observability metrics for manual reader in `go.opentelemetry.io/otel/sdk/metric`. (#7524)
- Add experimental observability metrics for periodic reader in `go.opentelemetry.io/otel/sdk/metric`. (#7571)
- Support `OTEL_EXPORTER_OTLP_LOGS_INSECURE` and `OTEL_EXPORTER_OTLP_INSECURE` environmental variables in `go.opentelemetry.io/otel/exporters/otlp/otlplog/otlploghttp`. (#7608)
- Add `Enabled` method to the `Processor` interface in `go.opentelemetry.io/otel/sdk/log`. All `Processor` implementations now include an `Enabled` method. (#7639)
- The `go.opentelemetry.io/otel/semconv/v1.38.0` package. The package contains semantic conventions from the `v1.38.0` version of the OpenTelemetry Semantic Conventions. See the [migration documentation](./semconv/v1.38.0/MIGRATION.md) for information on how to upgrade from `go.opentelemetry.io/otel/semconv/v1.37.0.`(#7648)

### Changed

- `Distinct` in `go.opentelemetry.io/otel/attribute` is no longer guaranteed to uniquely identify an attribute set. Collisions between `Distinct` values for different Sets are possible with extremely high cardinality (billions of series per instrument), but are highly unlikely. (#7175)
- `WithInstrumentationAttributes` in `go.opentelemetry.io/otel/trace` synchronously de-duplicates the passed attributes instead of delegating it to the returned `TracerOption`. (#7266)
- `WithInstrumentationAttributes` in `go.opentelemetry.io/otel/meter` synchronously de-duplicates the passed attributes instead of delegating it to the returned `MeterOption`. (#7266)
- `WithInstrumentationAttributes` in `go.opentelemetry.io/otel/log` synchronously de-duplicates the passed attributes instead of delegating it to the returned `LoggerOption`. (#7266)
- Rename the `OTEL_GO_X_SELF_OBSERVABILITY` environment variable to `OTEL_GO_X_OBSERVABILITY` in `go.opentelemetry.io/otel/sdk/trace`, `go.opentelemetry.io/otel/sdk/log`, and `go.opentelemetry.io/otel/exporters/stdout/stdouttrace`. (#7302)
- Improve performance of histogram `Record` in `go.opentelemetry.io/otel/sdk/metric` when min and max are disabled using `NoMinMax`. (#7306)
- Improve error handling for dropped data during translation by using `prometheus.NewInvalidMetric` in `go.opentelemetry.io/otel/exporters/prometheus`. ⚠️ **Breaking Change:** Previously, these cases were only logged and scrapes succeeded. Now, when translation would drop data (e.g., invalid label/value), the exporter emits a `NewInvalidMetric`, and Prometheus scrapes **fail with HTTP 500** by default. To preserve the prior behavior (scrapes succeed while errors are logged), configure your Prometheus HTTP handler with: `promhttp.HandlerOpts{ ErrorHandling: promhttp.ContinueOnError }`. (#7363)
- Replace fnv hash with xxhash in `go.opentelemetry.io/otel/attribute` for better performance. (#7371)
- The default `TranslationStrategy` in `go.opentelemetry.io/exporters/prometheus` is changed from `otlptranslator.NoUTF8EscapingWithSuffixes` to `otlptranslator.UnderscoreEscapingWithSuffixes`. (#7421)
- Improve performance of concurrent measurements in `go.opentelemetry.io/otel/sdk/metric`. (#7427)
- Include W3C TraceFlags (bits 0–7) in the OTLP `Span.Flags` field in `go.opentelemetry.io/exporters/otlp/otlptrace/otlptracehttp` and `go.opentelemetry.io/exporters/otlp/otlptrace/otlptracegrpc`. (#7438)
- The `ErrorType` function in `go.opentelemetry.io/otel/semconv/v1.37.0` now handles custom error types.
  If an error implements an `ErrorType() string` method, the return value of that method will be used as the error type. (#7442)

### Fixed

- Fix `WithInstrumentationAttributes` options in `go.opentelemetry.io/otel/trace`, `go.opentelemetry.io/otel/metric`, and `go.opentelemetry.io/otel/log` to properly merge attributes when passed multiple times instead of replacing them. Attributes with duplicate keys will use the last value passed. (#7300)
- The equality of `attribute.Set` when using the `Equal` method is not affected by the user overriding the empty set pointed to by `attribute.EmptySet` in `go.opentelemetry.io/otel/attribute`. (#7357)
- Return partial OTLP export errors to the caller in `go.opentelemetry.io/otel/exporters/otlp/otlplog/otlploggrpc`. (#7372)
- Return partial OTLP export errors to the caller in `go.opentelemetry.io/otel/exporters/otlp/otlplog/otlploghttp`. (#7372)
- Return partial OTLP export errors to the caller in `go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetricgrpc`. (#7372)
- Return partial OTLP export errors to the caller in `go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetrichttp`. (#7372)
- Return partial OTLP export errors to the caller in `go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc`. (#7372)
- Return partial OTLP export errors to the caller in `go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp`. (#7372)
- Fix `AddAttributes`, `SetAttributes`, `SetBody` on `Record` in `go.opentelemetry.io/otel/sdk/log` to not mutate input. (#7403)
- Do not double record measurements of `RecordSet` methods in `go.opentelemetry.io/otel/semconv/v1.37.0`. (#7655)
- Do not double record measurements of `RecordSet` methods in `go.opentelemetry.io/otel/semconv/v1.36.0`. (#7656)

### Removed

- Drop support for [Go 1.23]. (#7274)
- Remove the `FilterProcessor` interface in `go.opentelemetry.io/otel/sdk/log`. The `Enabled` method has been added to the `Processor` interface instead. All `Processor` implementations must now implement the `Enabled` method. Custom processors that do not filter records can implement `Enabled` to return `true`. (#7639)

## What's Changed

* Drop support for Go 1.23 by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7274
* fix(deps): update module go.opentelemetry.io/collector/pdata to v1.40.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7275
* chore(deps): update module github.com/securego/gosec/v2 to v2.22.8 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7276
* fix(deps): update module github.com/golangci/golangci-lint/v2 to v2.4.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7277
* fix(deps): update golang.org/x by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7188
* fix(deps): update module github.com/opentracing-contrib/go-grpc to v0.1.2 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7281
* fix(deps): update googleapis to ef028d9 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7279
* chore(deps): update module github.com/rogpeppe/go-internal to v1.14.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7283
* chore(deps): update module github.com/spf13/pflag to v1.0.9 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7282
* fix(deps): update github.com/opentracing-contrib/go-grpc/test digest to 0261db7 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7278
* Fix missing link in changelog by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7273
* chore(deps): update module github.com/spf13/cobra to v1.10.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7285
* chore(deps): update github/codeql-action action to v3.30.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7284
* chore(deps): update module github.com/spf13/cobra to v1.10.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7286
* Add tracetest example for testing instrumentation by @adity1raut in https://github.com/open-telemetry/opentelemetry-go/pull/7107
* Fix schema urls by @dmathieu in https://github.com/open-telemetry/opentelemetry-go/pull/7288
* chore(deps): update module github.com/spf13/pflag to v1.0.10 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7291
* chore(deps): update benchmark-action/github-action-benchmark action to v1.20.5 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7293
* chore(deps): update module github.com/ghostiam/protogetter to v0.3.16 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7289
* chore(deps): update module github.com/golangci/go-printf-func-name to v0.1.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7290
* chore(deps): update module mvdan.cc/gofumpt to v0.9.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7292
* fix(deps): update module go.opentelemetry.io/proto/otlp to v1.8.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7296
* chore(deps): update actions/stale action to v10 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7299
* chore(deps): update actions/setup-go action to v6 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7298
* fix(deps): update module github.com/prometheus/client_golang to v1.23.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7304
* chore(deps): update codecov/codecov-action action to v5.5.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7303
* Add Observability section to CONTRIBUTING doc by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7272
* chore(deps): update module github.com/bombsimon/wsl/v5 to v5.2.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7309
* chore(deps): update golang.org/x/telemetry digest to 9b996f7 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7308
* chore(deps): update github/codeql-action action to v3.30.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7312
* chore(deps): update github.com/grafana/regexp digest to f7b3be9 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7311
* chore(deps): update module github.com/pjbgf/sha1cd to v0.5.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7317
* chore(deps): update golang.org/x/telemetry digest to af835b0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7313
* fix(deps): update module github.com/prometheus/client_golang to v1.23.2 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7314
* chore(deps): update benchmark-action/github-action-benchmark action to v1.20.7 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7319
* Don't track min and max when disabled by @dashpole in https://github.com/open-telemetry/opentelemetry-go/pull/7306
* fix(deps): update golang.org/x by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7320
* Add benchmark for exponential histogram measurements by @dashpole in https://github.com/open-telemetry/opentelemetry-go/pull/7305
* chore(deps): update golang.org/x by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7324
* chore(deps): update module mvdan.cc/gofumpt to v0.9.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7322
* trace,metric,log: WithInstrumentationAttributes options to merge attributes by @pellared in https://github.com/open-telemetry/opentelemetry-go/pull/7300
* Encapsulate observability in Logs SDK by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7315
* trace,metric,log: add WithInstrumentationAttributeSet option by @pellared in https://github.com/open-telemetry/opentelemetry-go/pull/7287
* chore(deps): update module github.com/spf13/afero to v1.15.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7330
* chore(deps): update module github.com/sagikazarmark/locafero to v0.11.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7329
* chore(deps): update module github.com/lucasb-eyer/go-colorful to v1.3.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7327
* chore(deps): update module github.com/antonboom/errname to v1.1.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7338
* fix(deps): update module go.opentelemetry.io/collector/pdata to v1.41.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7337
* chore(deps): update module github.com/spf13/viper to v1.21.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7334
* chore(deps): update module github.com/spf13/cast to v1.10.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7333
* fix(deps): update googleapis to 9702482 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7335
* chore(deps): update github/codeql-action action to v3.30.2 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7339
* chore(deps): update golang.org/x by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7326
* fix(deps): update module google.golang.org/protobuf to v1.36.9 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7340
* Encapsulate `stdouttrace.Exporter` instrumentation in internal package by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7307
* Do not allocate instrument options if possible in generated semconv packages by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7328
* chore(deps): update module github.com/antonboom/nilnil to v1.1.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7343
* chore(deps): update module golang.org/x/net to v0.44.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7341
* fix(deps): update module golang.org/x/tools to v0.37.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7347
* fix(deps): update module google.golang.org/grpc to v1.75.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7344
* chore(deps): update module go.yaml.in/yaml/v2 to v2.4.3 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7349
* chore(deps): update github/codeql-action action to v3.30.3 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7348
* Rename Self-Observability as just Observability by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7302
* fix(deps): update golang.org/x to df92998 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7350
* trace,metric,log: change WithInstrumentationAttributes to not de-depuplicate the passed attributes in a closure by @axw in https://github.com/open-telemetry/opentelemetry-go/pull/7266
* sdk/metric: add example for metricdatatest package by @sanojsubran in https://github.com/open-telemetry/opentelemetry-go/pull/7323
* chore(deps): update module github.com/antonboom/testifylint to v1.6.4 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7359
* chore(deps): update module github.com/nunnatsa/ginkgolinter to v0.21.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7362
* chore(deps): update module github.com/tetafro/godot to v1.5.2 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7360
* Do not use the user-defined empty set when comparing sets. by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7357
* Track context containing span in `recordingSpan` by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7354
* fix(deps): update module go.opentelemetry.io/auto/sdk to v1.2.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7365
* Encapsulate SDK BatchSpanProcessor observability by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7332
* Encapsulate SDK Tracer observability by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7331
* chore: generate feature flag files from shared by @flc1125 in https://github.com/open-telemetry/opentelemetry-go/pull/7361
* fix(deps): update module github.com/prometheus/otlptranslator to v1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7358
* chore(deps): update module github.com/djarvur/go-err113 to v0.1.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7368
* Fix the typo in the function name `TestNewInstrumentation` by @yumosx in https://github.com/open-telemetry/opentelemetry-go/pull/7369
* Use Set hash in Distinct (2nd attempt) by @dashpole in https://github.com/open-telemetry/opentelemetry-go/pull/7175
* chore(deps): update module github.com/ldez/grignotin to v0.10.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7373
* chore(deps): update module github.com/kulti/thelper to v0.7.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7376
* chore(deps): update otel/weaver docker tag to v0.18.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7377
* fix(deps): update github.com/opentracing-contrib/go-grpc/test digest to a6e64aa by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7375
* feat(prometheus): Add observability for prometheus exporter by @tongoss in https://github.com/open-telemetry/opentelemetry-go/pull/7345
* Return partial OTLP export errors to the caller by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7372
* sdk/log: add TestRecordMethodsInputConcurrentSafe by @pellared in https://github.com/open-telemetry/opentelemetry-go/pull/7378
* chore(deps): update module github.com/sagikazarmark/locafero to v0.12.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7390
* chore(deps): update module github.com/tetafro/godot to v1.5.4 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7391
* fix(deps): update module github.com/golangci/golangci-lint/v2 to v2.5.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7392
* chore: sdk/log/internal/x - generate x package from x component template  by @nikhilmantri0902 in https://github.com/open-telemetry/opentelemetry-go/pull/7389
* chore(deps): update module go.opentelemetry.io/build-tools to v0.28.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7394
* fix(deps): update build-tools to v0.28.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7395
* fix(deps): update googleapis to 9219d12 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7393
* fix(deps): update module go.opentelemetry.io/collector/pdata to v1.42.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7397
* refactor: replace `context.Background()` with `t.Context()`/`b.Context()` in tests by @flc1125 in https://github.com/open-telemetry/opentelemetry-go/pull/7352
* sdk/log: BenchmarkAddAttributes, BenchmarkSetAttributes, BenchmarkSetBody by @pellared in https://github.com/open-telemetry/opentelemetry-go/pull/7387
* Link checker: ignore https localhost uris by @dmathieu in https://github.com/open-telemetry/opentelemetry-go/pull/7399
* chore(deps): update module github.com/ldez/gomoddirectives to v0.7.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7400
* chore(deps): update module dev.gaijin.team/go/golib to v0.7.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7402
* Add experimental `x` package to `otlptracegrpc` by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7401
* chore(deps): update actions/cache action to v4.3.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7409
* [chore]: Clean-up unused obsScopeName const by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7408
* Add benchmark for synchronous gauge measurement by @dashpole in https://github.com/open-telemetry/opentelemetry-go/pull/7407
* Add measure benchmarks with exemplars recorded by @dashpole in https://github.com/open-telemetry/opentelemetry-go/pull/7406
* chore(deps): update github/codeql-action action to v3.30.4 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7414
* chore(deps): update module github.com/quasilyte/go-ruleguard to v0.4.5 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7416
* chore(deps): update module github.com/quasilyte/go-ruleguard/dsl to v0.3.23 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7417
* Optimize the return type of ExportSpans by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7405
* Optimize Observability return types in in Prometheus exporter by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7410
* chore(deps): update module github.com/mattn/go-runewidth to v0.0.17 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7418
* chore(deps): update module github.com/cyphar/filepath-securejoin to v0.5.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7419
* Add concurrent safe tests for metric aggregations by @dashpole in https://github.com/open-telemetry/opentelemetry-go/pull/7379
* chore(deps): update github/codeql-action action to v3.30.5 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7425
* sdk/trace/internal/x: generate x package from x component template #7385 by @ternua8 in https://github.com/open-telemetry/opentelemetry-go/pull/7411
* chore(deps): update module go.augendre.info/fatcontext to v0.9.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7426
* Generate gRPC Client target parsing func by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7424
* chore(deps): update module github.com/mattn/go-runewidth to v0.0.19 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7428
* Prometheus exporter: change default translation strategy by @dashpole in https://github.com/open-telemetry/opentelemetry-go/pull/7421
* Only enforce cardinality limits when the attribute set does not already exist by @dashpole in https://github.com/open-telemetry/opentelemetry-go/pull/7422
* fix(deps): update googleapis to 57b25ae by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7429
* chore(deps): update module github.com/charmbracelet/x/ansi to v0.10.2 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7432
* chore(deps): update golang.org/x/telemetry digest to 8e64475 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7431
* chore(deps): update ossf/scorecard-action action to v2.4.3 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7435
* Allow optimizing locking for built-in exemplar reservoirs  by @dashpole in https://github.com/open-telemetry/opentelemetry-go/pull/7423
* chore(deps): update golang.org/x/telemetry digest to 4eae98a by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7439
* chore(deps): update peter-evans/create-issue-from-file action to v6 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7440
* Add temporality selector functions by @dprotaso in https://github.com/open-telemetry/opentelemetry-go/pull/7434
* fix(deps): update module google.golang.org/protobuf to v1.36.10 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7445
* chore(deps): update github/codeql-action action to v3.30.6 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7446
* Skip link checking for acm.org which blocks the link checker by @dashpole in https://github.com/open-telemetry/opentelemetry-go/pull/7444
* feat: logs SDK observability - otlploggrpc exporter metrics by @yumosx in https://github.com/open-telemetry/opentelemetry-go/pull/7353
* fix(deps): update golang.org/x to 27f1f14 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7448
* fix(deps): update googleapis to 7c0ddcb by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7449
* chore(deps): update module github.com/grpc-ecosystem/grpc-gateway/v2 to v2.27.3 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7450
* Add exemplar reservoir parallel benchmarks by @dashpole in https://github.com/open-telemetry/opentelemetry-go/pull/7441
* chore(deps): update module github.com/ghostiam/protogetter to v0.3.17 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7451
* chore(deps): update actions/stale action to v10.1.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7452
* Support custom error type semantics by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7442
* fix(deps): update build-tools to v0.28.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7455
* chore(deps): update module github.com/go-git/go-git/v5 to v5.16.3 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7456
* chore(deps): update module github.com/bombsimon/wsl/v5 to v5.3.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7457
* sdk/trace: trace id high 64 bit tests by @mahendrabishnoi2 in https://github.com/open-telemetry/opentelemetry-go/pull/7212
* Add the `internal/observ` package to `otlptracegrpc` by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7404
* fix(deps): update googleapis to 65f7160 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7460
* chore(deps): update module go.opentelemetry.io/collector/featuregate to v1.43.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7461
* fix(deps): update module google.golang.org/grpc to v1.76.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7463
* fix(deps): update module go.opentelemetry.io/collector/pdata to v1.43.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7462
* Use sync.Map and atomics to improve sum performance by @dashpole in https://github.com/open-telemetry/opentelemetry-go/pull/7427
* chore(deps): update module github.com/stretchr/objx to v0.5.3 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7464
* chore(deps): update module github.com/prometheus/common to v0.67.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7465
* Document the ordering guarantees provided by the metrics SDK by @dashpole in https://github.com/open-telemetry/opentelemetry-go/pull/7453
* chore(deps): update github/codeql-action action to v3.30.7 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7467
* chore(deps): update google.golang.org/genproto/googleapis/api digest to 49b9836 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7468
* Instrument the `otlptracegrpc` exporter by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7459
* fix(deps): update google.golang.org/genproto/googleapis/rpc digest to 49b9836 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7469
* chore(deps): update module golang.org/x/net to v0.45.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7470
* chore(deps): update github/codeql-action action to v4 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7472
* chore(deps): update module github.com/skeema/knownhosts to v1.3.2 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7471
* fix(deps): update golang.org/x by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7475
* chore(deps): update golang.org/x by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7477
* chore(deps): update module github.com/nunnatsa/ginkgolinter to v0.21.2 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7481
* chore(deps): update module github.com/ldez/exptostd to v0.4.5 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7483
* Add the internal `x` package to `otlptracehttp` by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7476
* Add a version const to otlptracehttp by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7479
* feat: Improve error handling in prometheus exporter by @tongoss in https://github.com/open-telemetry/opentelemetry-go/pull/7363
* Add the `internal/observ` pkg to `otlptracehttp` by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7480
* Move sdk/internal/env to sdk/trace/internal/env by @dmathieu in https://github.com/open-telemetry/opentelemetry-go/pull/7437
* chore(deps): update module github.com/gofrs/flock to v0.13.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7487
* Instrument the `otlptracehttp` exporter by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7486
* chore(deps): update github/codeql-action action to v4.30.8 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7489
* chore(deps): update module github.com/catenacyber/perfsprint to v0.10.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7496
* OTLP trace exporter include W3C trace flags (bits 0–7) in Span.Flags  by @nikhilmantri0902 in https://github.com/open-telemetry/opentelemetry-go/pull/7438
* Fix typos and linguistic errors in documentation / hacktoberfest by @survivant in https://github.com/open-telemetry/opentelemetry-go/pull/7494
* chore(deps): update module github.com/kunwardeep/paralleltest to v1.0.15 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7501
* RELEASING - Remove demo-accounting service from dependency list by @Kielek in https://github.com/open-telemetry/opentelemetry-go/pull/7503
* Added the `internal/observ` package to otlploghttp by @yumosx in https://github.com/open-telemetry/opentelemetry-go/pull/7484
* fix(deps): update googleapis to 4626949 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7506
* chore(deps): update module github.com/godoc-lint/godoc-lint to v0.10.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7508
* fix(observ): correct rejected items  and update comment style by @yumosx in https://github.com/open-telemetry/opentelemetry-go/pull/7502
* chore(deps): update module github.com/go-critic/go-critic to v0.14.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7509
* Prometheus exporter tests: iterate through all scopes rather than looking only at the first by @tongoss in https://github.com/open-telemetry/opentelemetry-go/pull/7510
* chore: sdk/internal/x - generate x package from shared template by @nikhilmantri0902 in https://github.com/open-telemetry/opentelemetry-go/pull/7495
* sdk/log: Fix AddAttributes, SetAttributes, SetBody on Record to not mutate input by @pellared in https://github.com/open-telemetry/opentelemetry-go/pull/7403
* chore(deps): update github/codeql-action action to v4.30.9 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7515
* feat: sdk/trace: span processed metric for simple span processor by @mahendrabishnoi2 in https://github.com/open-telemetry/opentelemetry-go/pull/7374
* Simulate failures for histogram creation paths without risking a nil-interface panic by @tongoss in https://github.com/open-telemetry/opentelemetry-go/pull/7518
* fix(deps): update golang.org/x by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7482
* fix(deps): update googleapis to 88f65dc by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7521
* chore(deps): update module go.opentelemetry.io/collector/featuregate to v1.44.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7522
* fix(deps): update module go.opentelemetry.io/collector/pdata to v1.44.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7523
* chore(deps): update module github.com/abirdcfly/dupword to v0.1.7 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7525
* Instrument the `otlploghttp` exporter by @yumosx in https://github.com/open-telemetry/opentelemetry-go/pull/7512
* chore(deps): update module mvdan.cc/gofumpt to v0.9.2 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7527
* Move scorpionknifes to emeritus by @dmathieu in https://github.com/open-telemetry/opentelemetry-go/pull/7526
* chore(deps): update module github.com/prometheus/procfs to v0.18.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7530
* fix(deps): update googleapis to 3a174f9 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7529
* chore(deps): update golang.org/x/telemetry digest to 5be28d7 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7528
* fix(deps): update golang.org/x to a4bb9ff by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7533
* Added the `internal/observ` package to log by @yumosx in https://github.com/open-telemetry/opentelemetry-go/pull/7532
* chore(deps): update module github.com/charithe/durationcheck to v0.0.11 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7534
* chore(deps): update github artifact actions (major) by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7537
* chore(deps): update github/codeql-action action to v4.31.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7536
* chore(deps): update module github.com/prometheus/procfs to v0.19.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7539
* chore(deps): update module github.com/ashanbrown/makezero/v2 to v2.1.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7538
* chore(deps): update module github.com/ashanbrown/forbidigo/v2 to v2.3.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7540
* chore(deps): update module github.com/prometheus/procfs to v0.19.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7542
* chore(deps): update module github.com/clipperhouse/uax29/v2 to v2.3.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7543
* chore(deps): update mvdan.cc/unparam digest to 5beb8c8 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7544
* chore(deps): update module github.com/karamaru-alpha/copyloopvar to v1.2.2 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7545
* chore(deps): update golang.org/x/telemetry digest to d7a2859 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7546
* chore(deps): update module github.com/prometheus/common to v0.67.2 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7547
* chore(deps): update module github.com/stbenjam/no-sprintf-host-port to v0.3.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7551
* fix(deps): update googleapis to ab9386a by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7553
* chore(deps): update lycheeverse/lychee-action action to v2.7.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7552
* Add disclaimer to span.SetAttributes by @dashpole in https://github.com/open-telemetry/opentelemetry-go/pull/7550
* chore(deps): update module github.com/go-critic/go-critic to v0.14.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7557
* chore(deps): update github/codeql-action action to v4.31.2 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7556
* chore(deps): update module github.com/prometheus/procfs to v0.19.2 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7558
* fix(deps): update module github.com/golangci/golangci-lint/v2 to v2.6.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7554
* chore(deps): update module github.com/go-critic/go-critic to v0.14.2 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7559
* chore: handle Float64Histogram in log/observe errMeter by @dmathieu in https://github.com/open-telemetry/opentelemetry-go/pull/7555
* chore(deps): update module github.com/charmbracelet/x/term to v0.2.2 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7560
* fix(deps): update build-tools to v0.29.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7561
* chore(deps): update module github.com/cyphar/filepath-securejoin to v0.5.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7563
* chore(deps): update module github.com/cyphar/filepath-securejoin to v0.6.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7564
* fix(deps): update googleapis to f26f940 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7569
* fix(deps): update module go.opentelemetry.io/proto/otlp to v1.9.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7570
* Instrument manual reader from sdk/metric by @tongoss in https://github.com/open-telemetry/opentelemetry-go/pull/7524
* docs: remove demo repository update after release by @pellared in https://github.com/open-telemetry/opentelemetry-go/pull/7566
* docs: sign artifacts before releasing by @pellared in https://github.com/open-telemetry/opentelemetry-go/pull/7567
* fix(deps): update module go.opentelemetry.io/collector/pdata to v1.45.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7575
* chore(deps): update golang.org/x/telemetry digest to ab4e49a by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7578
* fix(deps): update module github.com/golangci/golangci-lint/v2 to v2.6.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7579
* trace: add fuzz tests for TraceIDFromHex and SpanIDFromHex by @harshit-jindal02 in https://github.com/open-telemetry/opentelemetry-go/pull/7577
* chore(deps): update otel/weaver docker tag to v0.19.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7580
* feat: instrument periodic reader from sdk/metric by @tongoss in https://github.com/open-telemetry/opentelemetry-go/pull/7571
* chore(deps): update module github.com/mirrexone/unqueryvet to v1.3.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7583
* chore(deps): update golang.org/x/telemetry digest to cbe4531 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7582
* sdk/log: update ExampleProcessor_eventName to use otel.event.name attribute by @pellared in https://github.com/open-telemetry/opentelemetry-go/pull/7568
* chore(deps): update golang.org/x/telemetry digest to 5cc343d by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7584
* chore(deps): update module github.com/maratori/testableexamples to v1.0.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7585
* chore(deps): update module github.com/maratori/testpackage to v1.1.2 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7586
* chore(deps): update module github.com/catenacyber/perfsprint to v0.10.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7588
* fix(deps): update golang.org/x by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7590
* fix(deps): update googleapis to 83f4791 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7594
* chore(deps): update golang.org/x by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7599
* fix(deps): update googleapis to 95abcf5 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7598
* chore(deps): update golang.org/x/telemetry digest to 03ef243 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7600
* fix(deps): update module golang.org/x/tools to v0.39.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7601
* chore: exporters/prometheus/internal/x - Generate x package from x component template by @petern48 in https://github.com/open-telemetry/opentelemetry-go/pull/7491
* fix(deps): update golang.org/x to e25ba8c by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7602
* chore(deps): update github/codeql-action action to v4.31.3 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7603
* chore(deps): update module github.com/mgechev/revive to v1.13.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7605
* fix(deps): update module github.com/golangci/golangci-lint/v2 to v2.6.2 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7604
* chore(deps): update module go.opentelemetry.io/collector/featuregate to v1.46.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7610
* chore(deps): update actions/checkout action to v5.0.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7609
* fix(deps): update module google.golang.org/grpc to v1.77.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7612
* chore(deps): update module github.com/prometheus/common to v0.67.3 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7613
* fix(deps): update module go.opentelemetry.io/collector/pdata to v1.46.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7611
* Upgrade macos tests to latest by @dmathieu in https://github.com/open-telemetry/opentelemetry-go/pull/7597
* chore(deps): update github/codeql-action action to v4.31.4 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7615
* Replace fnv with xxhash by @pree-dew in https://github.com/open-telemetry/opentelemetry-go/pull/7497
* chore(deps): update actions/setup-go action to v6.1.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7623
* chore(deps): update module go.uber.org/zap to v1.27.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7620
* chore(deps): update module github.com/cyphar/filepath-securejoin to v0.6.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7618
* chore(deps): update module golang.org/x/crypto to v0.45.0 [security] by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7622
* chore(deps): update actions/checkout action to v6 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7624
* otlploghttp: support OTEL_EXPORTER_OTLP_LOGS_INSECURE and OTEL_EXPORTER_OTLP_INSECURE env vars by @fd in https://github.com/open-telemetry/opentelemetry-go/pull/7608
* chore(deps): update module dev.gaijin.team/go/golib to v0.8.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7627
* chore(deps): update module github.com/prometheus/common to v0.67.4 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7626
* chore(deps): update golang.org/x/telemetry digest to e487659 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7619
* chore(deps): update module github.com/go-git/go-git/v5 to v5.16.4 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7629
* chore(deps): update github/codeql-action action to v4.31.5 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7631
* chore(deps): update module github.com/tomarrell/wrapcheck/v2 to v2.12.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7632
* chore(deps): update golang.org/x/telemetry digest to 55bbf37 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7633
* fix(deps): update googleapis to 79d6a2a by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7634
* fix(deps): update golang.org/x to 87e1e73 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7636
* chore(deps): update module github.com/hashicorp/go-version to v1.8.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7641
* chore(deps): update golang.org/x/telemetry digest to abf20d0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7643
* chore(deps): update github/codeql-action action to v4.31.6 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7644
* fix(deps): update module go.opentelemetry.io/collector/pdata to v1.47.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7646
* chore(deps): update module github.com/godoc-lint/godoc-lint to v0.10.2 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7650
* chore(deps): update actions/stale action to v10.1.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7653
* fix(deps): update googleapis to ff82c1b by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7652
* chore(deps): update actions/checkout action to v6.0.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7651
* chore(deps): update golang.org/x/telemetry digest to 8fff8a5 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7654
* fix(deps): update module github.com/golangci/golangci-lint/v2 to v2.7.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7661
* Generate semconv/v1.38.0 by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7648
* chore(deps): update module github.com/spf13/cobra to v1.10.2 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7668
* Instrument the `SimpleLogProcessor` from sdk/log by @yumosx in https://github.com/open-telemetry/opentelemetry-go/pull/7548
* chore(deps): update module github.com/ldez/gomoddirectives to v0.8.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7669
* fix(deps): update module github.com/golangci/golangci-lint/v2 to v2.7.1 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7671
* Fix package documentation name and return err in `semconv/v1.37.0` by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7655
* Fix package name documentation and missing copyright in `semconv/v1.33.0` by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7658
* Fix package name documentation and missing copyright in `semconv/v1.34.0` by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7657
* Fix whitespace in `semconv/v1.37.0` by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7660
* Fix package documentation name and return error in `semconv/v1.36.0` by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7656
* Fix whitespace in `semconv/v1.34.0` by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7664
* Fix package name documentation and missing copyright in `semconv/v1.32.0` by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7659
* Fix whitespace in `semconv/v1.36.0` by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7663
* Fix whitespace in `semconv/v1.32.0` by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7666
* Fix whitespace in `semconv/v1.33.0` by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7665
* Regenerate `ErrorType` documentation in `semconv/v1.37.0` by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7667
* chore(deps): update github/codeql-action action to v4.31.7 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7675
* chore(deps): update module github.com/go-git/go-billy/v5 to v5.7.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7679
* Fix flaky `TestClientInstrumentation` by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7677
* Check context prior to delaying retry in OTLP exporters by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7678
* fix(deps): update module github.com/golangci/golangci-lint/v2 to v2.7.2 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7680
* chore(deps): update github.com/securego/gosec/v2 digest to 41f28e2 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7682
* chore(deps): update module golang.org/x/sync to v0.19.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7683
* fix(deps): update module golang.org/x/sys to v0.39.0 by @renovate[bot] in https://github.com/open-telemetry/opentelemetry-go/pull/7684
* sdk/log: move Enabled method from FilterProcessor to Processor by @pellared in https://github.com/open-telemetry/opentelemetry-go/pull/7639
* Release v1.39.0 by @MrAlias in https://github.com/open-telemetry/opentelemetry-go/pull/7676

## New Contributors
* @adity1raut made their first contribution in https://github.com/open-telemetry/opentelemetry-go/pull/7107
* @axw made their first contribution in https://github.com/open-telemetry/opentelemetry-go/pull/7266
* @sanojsubran made their first contribution in https://github.com/open-telemetry/opentelemetry-go/pull/7323
* @nikhilmantri0902 made their first contribution in https://github.com/open-telemetry/opentelemetry-go/pull/7389
* @ternua8 made their first contribution in https://github.com/open-telemetry/opentelemetry-go/pull/7411
* @dprotaso made their first contribution in https://github.com/open-telemetry/opentelemetry-go/pull/7434
* @survivant made their first contribution in https://github.com/open-telemetry/opentelemetry-go/pull/7494
* @harshit-jindal02 made their first contribution in https://github.com/open-telemetry/opentelemetry-go/pull/7577
* @petern48 made their first contribution in https://github.com/open-telemetry/opentelemetry-go/pull/7491
* @fd made their first contribution in https://github.com/open-telemetry/opentelemetry-go/pull/7608

**Full Changelog**: https://github.com/open-telemetry/opentelemetry-go/compare/v1.38.0...v1.39.0

