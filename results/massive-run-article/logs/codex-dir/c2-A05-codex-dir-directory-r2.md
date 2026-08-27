# Why was `opentelemetry-go-contrib` pull request `#8014` (otelgin context save/restore) closed?

<!-- RESPONSE_START -->

PR #8014 was closed without merging because the SIG concluded that removing the deferred context restoration would break intentional, long-standing middleware semantics.

The defer removes the otelgin span from the request context after the middleware returns, so parent middleware does not create spans that remain children of an already-finished request span. Maintainers considered that behavior deliberate and consistent with other instrumentation such as `otelecho`. [PR discussion](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-contrib-8014.md:615) [maintainer rationale](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-contrib-8014.md:736)

At the 2025-10-16 SIG meeting, Damien Mathieu and Tyler Yahn agreed the existing behavior was correct: code launching goroutines should explicitly pass the needed context or span, with linked spans appropriate for asynchronous work. [meeting note](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3479584781.md:23)

Damien then closed the PR on 2025-10-17, stating that the proposed fix was incorrect and the current behavior proper. It remains `closed_without_merge`. [closure record](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-contrib-8014.md:783) [work state](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md:40)
