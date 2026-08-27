# Why was `opentelemetry-go-contrib` pull request `#8014` (otelgin context save/restore) closed?

<!-- RESPONSE_START -->

PR **#8014 was closed without merging** because the Go SIG decided the existing context-restoration behavior was intentional and correct.

On 2025-10-16, Damien Mathieu and Tyler Yahn concluded that code starting goroutines should explicitly pass the needed context/span into them, rather than rely on `otelgin` leaving its derived context attached after middleware returns. Tyler also favored linked spans for asynchronous work over making those goroutines children of the request span. The PR was then closed on 2025-10-17. `(WS-05/T007; SRC-NOTE-04; SRC-PR-07)`

So, although the PR author presented the deferred restore as a reproducible data-race source, the maintainers’ decision was a semantic/design one: retain context reversal and require explicit context propagation for asynchronous work.
