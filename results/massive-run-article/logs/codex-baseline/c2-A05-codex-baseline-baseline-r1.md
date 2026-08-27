# Why was `opentelemetry-go-contrib` pull request `#8014` (otelgin context save/restore) closed?

<!-- RESPONSE_START -->

PR #8014 was closed because maintainers did not want `otelgin` to mutate and then restore Gin’s request context. The request context carrying the server span is intentionally left installed for downstream handlers; restoring it after `c.Next()` adds no useful behavior and can break code that expects the active tracing context to remain available.
