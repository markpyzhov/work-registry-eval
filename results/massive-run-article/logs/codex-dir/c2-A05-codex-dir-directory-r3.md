# Why was `opentelemetry-go-contrib` pull request `#8014` (otelgin context save/restore) closed?

<!-- RESPONSE_START -->

PR #8014 was closed without merging because the Go SIG decided that removing otelgin’s deferred context restoration was incorrect.

The restoration is intentional: after middleware execution, it removes the otelgin span from the request context so parent middleware does not create spans as children of an already-finished request span. Maintainers also noted this is longstanding behavior shared by other instrumentations. For asynchronous work, the SIG’s guidance was to explicitly pass the needed context/span into spawned goroutines (and use links for asynchronous spans), rather than retain the request span through the restore boundary. Damien closed it on 2025-10-17 following that SIG decision. [PR #8014 record](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-contrib-8014.md) [Go SIG meeting note](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3479584781.md)

The authoritative work state records it as `closed_without_merge`, not completed. [WS-05](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md)
