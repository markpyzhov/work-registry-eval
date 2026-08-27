# What is the status of `opentelemetry-go-contrib` issue `#7254` (otelhttp error recording under the new semantic conventions)?

<!-- RESPONSE_START -->

`#7254` is **closed as completed** (closed 2026-01-13), after being moved to the `v1.40.0` milestone. The work-state marks the otelhttp error-recording task done, but **does not establish that it shipped in any release**.  

The issue concerned whether otelhttp should record errors as span events (`RecordError`) versus relying on error attributes/status under the newer semantic conventions.  
Citations: `WS-05: Contrib Modules` / `T002`; `SRC-ISSUE-02`; `SRC-MILE-04`; `SRC-NOTE-06`.
