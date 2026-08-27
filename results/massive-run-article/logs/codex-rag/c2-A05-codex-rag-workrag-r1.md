# Why was `opentelemetry-go-contrib` pull request `#8014` (otelgin context save/restore) closed?

<!-- RESPONSE_START -->

PR #8014 was closed without merging because the Go SIG decided the existing context save/restore behavior was intentional and correct: it prevents parent middleware from accessing otelgin’s span after the middleware returns.

For asynchronous work, the SIG’s position was that users should explicitly pass the needed context/span to spawned goroutines (and use span links where appropriate), rather than change otelgin’s middleware behavior. The decision was made on October 16, and the PR was closed on October 17, 2025. (`SRC-NOTE-04`; `SRC-PR-07`; authoritative work state `WS-05 / T007`)
