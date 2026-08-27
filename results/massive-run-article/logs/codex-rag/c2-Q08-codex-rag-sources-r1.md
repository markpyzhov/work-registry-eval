# What is the status of `opentelemetry-go-contrib` issue `#7254` (otelhttp error recording under the new semantic conventions)?

<!-- RESPONSE_START -->

Issue [#7254](https://github.com/open-telemetry/opentelemetry-go-contrib/issues/7254) is **closed (completed)**. It was closed by `pellared` on **2026-01-13** and assigned to milestone **v1.40.0**. [SRC-ISSUE-02](https://github.com/open-telemetry/opentelemetry-go-contrib/issues/7254)

The issue concerned conflicting `otelhttp` logic: `RecordError` was effectively not reached under the new semantic conventions because `ErrorType` was always present. The resolved direction discussed was to treat terminating errors by setting `error.type` and span status, rather than recording an exception event; `RecordError` remained relevant for non-terminating/retry cases. [SRC-ISSUE-02](https://github.com/open-telemetry/opentelemetry-go-contrib/issues/7254)

The timeline cross-references PR `#8386` on 2026-01-12, immediately before closure; the retrieved record does not explicitly state the PR’s merge status or its exact changes. [SRC-ISSUE-02](https://github.com/open-telemetry/opentelemetry-go-contrib/issues/7254)
