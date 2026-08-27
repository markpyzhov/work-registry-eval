# Why was `opentelemetry-go-contrib` pull request `#8014` (otelgin context save/restore) closed?

<!-- RESPONSE_START -->

PR #8014 was closed because the SIG concluded that removing the deferred context restoration was semantically incorrect, even though it eliminated the reproduced race.

The defer intentionally removes the otelgin span from the request context after the middleware returns. That preserves the established behavior: middleware that resumes after `c.Next()` should not create spans that are children of a span which has already finished. Removing it would change that behavior—and would be a breaking change from the long-standing pattern also used by other instrumentation such as `otelecho`.

After discussing it in the SIG meeting, maintainers decided the existing behavior was the correct one and closed the PR rather than merge it. [SRC-PR-07: PR #8014](https://github.com/open-telemetry/opentelemetry-go-contrib/pull/8014)
