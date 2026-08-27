# Which MultipartForm cleanup approach is being pursued for otelgin (`#5946` / `#6609`), and what is its current implementation status?

<!-- RESPONSE_START -->

The pursued approach is **automatic cleanup in `otelgin`**: call `c.Request.MultipartForm.RemoveAll()` during the otel middleware’s return/unwind phase. The SIG favored shipping that default behavior first, with no configuration option unless users later demonstrate a need. The reattach-to-original-request and forced-parse alternatives were considered but not selected. [SRC-NOTE-04](https://github.com/open-telemetry/opentelemetry-go/issues/6648#issuecomment-3479584781)

Implementation is **not merged**. PR [#6609 / SRC-PR-01](https://github.com/open-telemetry/opentelemetry-go-contrib/pull/6609) remains open on `fix/gin_multipartform` (95 added lines across 3 files). Conflicts were resolved and the author reported local `otelgin` tests passing; extra upstream/downstream middleware tests were added to document that `RemoveAll` makes temporary files unavailable after the otel middleware returns. Issue [#5946 / SRC-ISSUE-01](https://github.com/open-telemetry/opentelemetry-go-contrib/issues/5946) remains open and was marked a duplicate.
