# Why was `opentelemetry-go-contrib` pull request `#8014` (otelgin context save/restore) closed?

<!-- RESPONSE_START -->

I don't have reliable knowledge of that specific pull request, so I can't tell you why it was closed.

What I can say honestly:

- I have no recollection of `open-telemetry/opentelemetry-go-contrib#8014` specifically, nor of a PR in that repo described as "otelgin context save/restore." PR numbers and their close reasons are exactly the kind of fine-grained, high-churn detail that I don't retain reliably, and guessing would risk inventing a plausible-sounding rationale (e.g. "superseded by another PR" or "stale/inactive") that I have no actual basis for.
- I can't verify it either, since you've asked me not to use web, retrieval, or local files.

General context that may or may not apply: `otelgin` (the Gin instrumentation under `instrumentation/github.com/gin-gonic/gin/otelgin`) has a long-standing known issue where the span context is placed on `*gin.Context`'s request via `c.Request = c.Request.WithContext(...)`, which interacts awkwardly with Gin's context pooling and with `c.Copy()` in goroutines. PRs touching that area have historically run into concerns about breaking changes to the middleware's context propagation semantics and about Gin's own `ContextWithFallback` setting. But I want to be clear that this is background on the problem space, not knowledge of what happened to #8014.

If you want a real answer, checking `https://github.com/open-telemetry/opentelemetry-go-contrib/pull/8014` directly (or letting me fetch it) is the only dependable route.
