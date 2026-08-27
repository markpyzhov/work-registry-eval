# Why was `opentelemetry-go-contrib` pull request `#8014` (otelgin context save/restore) closed?

<!-- RESPONSE_START -->

I have everything needed to answer.

## Why PR #8014 was closed

**Closed by dmathieu on 2025-10-17T10:41:58Z**, after the OpenTelemetry Go SIG decided the change was wrong:

> "We have been discussing this in yesterday's SIG meeting, and have decided this fix is incorrect and the current behavior is the proper one."
> — dmathieu, referencing `opentelemetry-go-contrib/issues/4588#issuecomment-3414917592`

### What the PR proposed
nicksherron ("otelgin: remove unneeded context save/restore to avoid data race", branch `fix/otelgin-data-race`, +83/-10 across 2 files) wanted to delete the deferred `c.Request = c.Request.WithContext(savedCtx)` in the otelgin middleware, arguing it caused a reproducible data race (issue #4588, open ~2 years): the defer writes to `c.Request` after `c.Next()` returns, while goroutines spawned by downstream handlers may still be reading `c.Request.Context()` — a common pattern in async logging middleware.

### Why the SIG rejected it
From the SIG meeting notes of 2025-10-16 (attendees: Tyler Yahn, Damien Mathieu, Bryan Boreham, David Ashpole, Robert Pająk), which discussed PR #8014 directly:

- The context reversal is **intentional**: it prevents parent middlewares from accessing the span after otelgin's middleware finishes.
- **Damien Mathieu** held that the current behavior is correct and that users should **explicitly pass the current context** into goroutines they spawn, citing the Collector's pattern of passing context directly outside HTTP requests for processors/exporters.
- **Tyler Yahn** agreed — passing needed values (like the span) into spawned goroutines is the right solution — and noted OpenTelemetry's pattern of **linking** spans for asynchronous operations rather than making them child references.

Earlier in the PR thread, dmathieu also argued the middleware pattern does not "flow forward" (at the end of a middleware you return to its parent), and that this had been the default behavior for years, shared with other instrumentations such as otelecho. nicksherron accepted that point ("I wasn't looking to add a breaking change") and said he'd try to find an approach preserving existing semantics — but the PR was closed before that happened.

### Notable wrinkle
The PR had momentum before the SIG overruled it: **akats7 APPROVED** it on 2025-10-14, and **flc1125**, who initially opposed it, later wrote "I approve this PR and agree with the changes" — though framing its value as removing unnecessary code with unintended side effects rather than as a data-race fix. A CI test requested by dmathieu was added, and Codecov reported full coverage of modified lines. The SIG decision reversed all of that.

### Sources cited
- `opentelemetry/pulls/opentelemetry-go-contrib-8014.md` — [SRC-PR-07], PR body, discussion (27 comments), reviews, and timeline (`2025-10-17T10:41:58Z · closed by dmathieu`)
- `opentelemetry/meeting-notes/entry-3479584781.md` — [SRC-NOTE-04], OpenTelemetry Go SIG meeting notes dated 2025-10-16, section "otelgin Context Reversal in DataRace"
