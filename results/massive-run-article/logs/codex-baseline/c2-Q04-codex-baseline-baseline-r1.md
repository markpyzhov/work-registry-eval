# What is the status of the otelgin MultipartForm temporary-file cleanup work tracked by `opentelemetry-go-contrib` issue `#5946` and pull request `#6609`?

<!-- RESPONSE_START -->

As of 2026-02-27, the cleanup work is complete: PR [#6609](https://github.com/open-telemetry/opentelemetry-go-contrib/pull/6609) was merged to address issue [#5946](https://github.com/open-telemetry/opentelemetry-go-contrib/issues/5946), which is closed.

The otelgin middleware now cleans up request `MultipartForm` temporary files after the Gin handler finishes, preventing disk-backed multipart uploads from being left behind.
