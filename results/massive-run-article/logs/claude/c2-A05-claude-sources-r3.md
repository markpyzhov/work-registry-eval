# Why was `opentelemetry-go-contrib` pull request `#8014` (otelgin context save/restore) closed?

<!-- RESPONSE_START -->

I have the closure reason directly from the source.

## Answer

**PR #8014 was closed by maintainer dmathieu on 2025-10-17 because the OpenTelemetry Go SIG decided the proposed fix was incorrect and that the existing context save/restore behavior is the correct one.**

His closing comment (2025-10-17T10:41:58Z):

> "We have been discussing this in yesterday's SIG meeting, and have decided this fix is incorrect and the current behavior is the proper one." — pointing to `opentelemetry-go-contrib` issue #4588, comment 3414917592.

### How it got there

- **The PR** (author: nicksherron, branch `fix/otelgin-data-race`, +83/-10 across 2 files) proposed deleting the `savedCtx := c.Request.Context()` / `defer func() { c.Request = c.Request.WithContext(savedCtx) }()` pattern in otelgin's `Middleware()`, arguing the deferred write races with goroutines that downstream handlers spawn while holding `c.Request.Context()` — a reproducible `go test -race` failure and the cause of the 2-year-old issue #4588.
- **Early reception was mixed but leaning positive**: flc1125 initially objected (concurrency safety should be left to users), then reversed and approved, framing the value as removing unnecessary code with unintended side effects. akats7 formally APPROVED on 2025-10-14. dmathieu asked for the race repro to be turned into a CI test, which the author added.
- **The blocking objection** came from dmathieu (2025-10-14T07:54:22Z): the defer is not dead code — it removes the span from the request context so that middleware registered *before* otelgin, running after `c.Next()`, does not create spans that become children of the already-finished otelgin span. Removing it would change span parentage, a behavior that has been the default for years and is shared with other instrumentations such as otelecho. He called it a behavior change, not just a race fix.
- The author conceded this was a strong point ("I wasn't looking to add a breaking change"), said he'd try to find something that preserved semantics while fixing the race, and dmathieu moved the discussion to the SIG meeting. The SIG's verdict three days later closed the PR.

Note that the race itself was never disputed — dmathieu explicitly said "While I agree to fixing this race condition, the defer does have a use and I don't think we can just drop it." The PR was rejected on approach (dropping the restore changes span-parenting semantics), not on whether the bug exists. A later cross-reference from `open-telemetry/opentelemetry-go` issue #6648 (2025-11-03, by pellared) suggests the topic stayed live.

### Source

`[SRC-PR-07]` — `opentelemetry/pulls/opentelemetry-go-contrib-8014.md`, canonical URL https://github.com/open-telemetry/opentelemetry-go-contrib/pull/8014 (state: closed; discussion of 27 comments plus timeline entry "2025-10-17T10:41:58Z · closed by dmathieu").
