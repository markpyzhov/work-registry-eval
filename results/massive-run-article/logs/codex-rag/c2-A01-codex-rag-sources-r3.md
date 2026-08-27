# Which MultipartForm cleanup approach is being pursued for otelgin (`#5946` / `#6609`), and what is its current implementation status?

<!-- RESPONSE_START -->

The pursued fix is explicit cleanup: have otelgin call `c.Request.MultipartForm.RemoveAll()` as middleware unwinds, rather than forcing form parsing or reattaching the form to the original request. This intentionally deletes temporary multipart files; optional configurability is deferred unless users explicitly request it. [SRC-PR-01](https://github.com/open-telemetry/opentelemetry-go-contrib/pull/6609)

Implementation is present in PR #6609: conflicts were resolved, local otelgin tests passed, and tests were expanded to cover upstream/downstream middleware behavior. But it is **not merged**—the PR remains open (+95/−0 across 3 files), and the expected post-`RemoveAll` access behavior was still being confirmed. Issue #5946 is open and marked duplicate. [SRC-PR-01](https://github.com/open-telemetry/opentelemetry-go-contrib/pull/6609) [SRC-ISSUE-01](https://github.com/open-telemetry/opentelemetry-go-contrib/issues/5946)
