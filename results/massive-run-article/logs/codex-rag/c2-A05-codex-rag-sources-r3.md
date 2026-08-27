# Why was `opentelemetry-go-contrib` pull request `#8014` (otelgin context save/restore) closed?

<!-- RESPONSE_START -->

PR #8014 was closed because maintainers decided the existing context restoration was intentional middleware scoping: after a middleware returns, its context changes should not leak back to parent middleware. They considered the reported race a consequence of application code reading `c.Request.Context()` from a spawned goroutine after the request/middleware had completed.

Their prescribed solution was for users to explicitly capture and pass the current context (or needed span) into spawned goroutines. Damien Mathieu and Tyler Yahn agreed with that approach, so the proposal to remove the restore was not accepted. The PR was closed by dmathieu on October 17, 2025. [SRC-PR-07](https://github.com/open-telemetry/opentelemetry-go-contrib/pull/8014); [SRC-NOTE-04](https://github.com/open-telemetry/opentelemetry-go/issues/6648#issuecomment-3479584781)
