# Why was `opentelemetry-go-contrib` pull request `#8014` (otelgin context save/restore) closed?

<!-- RESPONSE_START -->

PR #8014 was closed because the OpenTelemetry Go SIG decided that removing the deferred context restoration would be semantically incorrect.

The restoration intentionally removes the otelgin span once the middleware returns, so a parent middleware’s post-`c.Next()` work does not create spans as children of a trace that has already finished. Maintainers considered that established behavior—also present in other instrumentations—correct. They concluded that callers launching goroutines should explicitly pass the needed context/span instead. Damien Mathieu closed the PR after the SIG discussion on October 16. [SRC-PR-07] [SRC-NOTE-04]
