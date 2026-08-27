# Why was `opentelemetry-go-contrib` pull request `#8014` (otelgin context save/restore) closed?

<!-- RESPONSE_START -->

It was closed because the SIG concluded that the proposed removal was **semantically incorrect**: restoring the parent context after a middleware returns is the intended middleware behavior, not dead code.

Maintainers emphasized that this had been the established behavior for years and is shared by other instrumentation (for example, `otelecho`), so removing it would be a breaking change. After the SIG meeting, `dmathieu` stated that the current behavior was the proper one and the fix was incorrect. [SRC-PR-07, `opentelemetry-go-contrib#8014`]
