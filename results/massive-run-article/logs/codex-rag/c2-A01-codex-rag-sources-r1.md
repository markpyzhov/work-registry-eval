# Which MultipartForm cleanup approach is being pursued for otelgin (`#5946` / `#6609`), and what is its current implementation status?

<!-- RESPONSE_START -->

The pursued fix is explicit cleanup in `otelgin`: after middleware execution, defer a check for `c.Request.MultipartForm` and call `RemoveAll()` to delete its temporary files. The SIG direction favors this over the less-aggressive “reattach the form to the original request” approach; cloning or merely reattaching does not reliably address the `WithContext`/lazy form-parsing lifecycle problem. The scope is intentionally limited to `otelgin`, though similar `*http.Request` middleware may need separate fixes. [SRC-PR-01](https://github.com/open-telemetry/opentelemetry-go-contrib/pull/6609)

Implementation is underway but not merged: PR [#6609](https://github.com/open-telemetry/opentelemetry-go-contrib/pull/6609) remains **open** (`fix/gin_multipartform` → `main`, +95/-0 across 3 files). Conflicts were resolved, package tests reportedly passed locally, and tests were expanded to cover upstream and downstream middleware behavior. A configurable cleanup option was discussed, but the decision was to defer configurability unless explicitly requested. [SRC-PR-01](https://github.com/open-telemetry/opentelemetry-go-contrib/pull/6609)

The related issue [#5946](https://github.com/open-telemetry/opentelemetry-go-contrib/issues/5946) is marked duplicate in the dataset; the PR is the active implementation vehicle.
