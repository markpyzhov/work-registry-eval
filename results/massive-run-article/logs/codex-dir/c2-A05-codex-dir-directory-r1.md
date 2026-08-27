# Why was `opentelemetry-go-contrib` pull request `#8014` (otelgin context save/restore) closed?

<!-- RESPONSE_START -->

PR #8014 was closed because the SIG concluded that deleting the deferred context restoration was semantically incorrect, despite the reported race.

The restoration is intentional: when `otelgin` finishes, it removes its server span from `c.Request.Context()` so an outer middleware resuming after `c.Next()` does not create spans as children of an already-finished `otelgin` span. That established behavior has existed for years and is shared by other instrumentations such as `otelecho`; removing it would be a breaking behavioral change. After the SIG discussion, maintainer `dmathieu` closed the PR, stating that “this fix is incorrect and the current behavior is the proper one.” The PR was closed on 2025-10-17. [SRC-PR-07: opentelemetry-go-contrib-8014.md](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-contrib-8014.md:533)
