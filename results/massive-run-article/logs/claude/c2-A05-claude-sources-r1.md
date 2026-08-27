# Why was `opentelemetry-go-contrib` pull request `#8014` (otelgin context save/restore) closed?

<!-- RESPONSE_START -->

## Answer

PR #8014 was **closed by maintainer dmathieu on 2025-10-17T10:41:58Z**, after the OpenTelemetry Go SIG discussed it at its 2025-10-16 meeting and concluded the proposed change was the wrong fix.

His closing comment:

> "We have been discussing this in yesterday's SIG meeting, and have decided this fix is incorrect and the current behavior is the proper one."

(pointing to https://github.com/open-telemetry/opentelemetry-go-contrib/issues/4588#issuecomment-3414917592)

### Why the SIG rejected it

The PR (by nicksherron, branch `fix/otelgin-data-race`, +83/-10 across 2 files) proposed deleting the `defer func() { c.Request = c.Request.WithContext(savedCtx) }()` in `otelgin.Middleware()`, arguing the deferred write races with goroutines spawned by downstream handlers that read `c.Request.Context()` (the 2-year-old issue #4588), and that removing it is also faster and simpler.

Maintainers held that the defer is deliberate and load-bearing:

1. **The restore is intentional semantics, not dead code.** dmathieu (2025-10-14T07:54:22Z): the defer removes the span from the context so that spans created by *parent* middleware after `c.Next()` returns do not become children of the already-finished otelgin span. Removing it would silently change that parenting behavior.
2. **It would be a behavior/breaking change.** This has been the default for years and the same behavior exists in other instrumentations such as otelecho.
3. **The correct fix belongs on the user side.** Per the SIG notes (2025-10-16, attendees Tyler Yahn, Damien Mathieu, Bryan Boreham, David Ashpole, Robert Pająk): Damien argued the current behavior is correct and users should explicitly pass the current context to goroutines they spawn, citing the Collector's pattern of passing context directly outside HTTP requests. Tyler Yahn agreed, adding that OpenTelemetry's pattern for asynchronous operations is to *link* spans rather than make them child references.

Notably the PR had momentum before that: akats7 approved it on 2025-10-14, and flc1125 — who initially objected on thread-safety/performance grounds — later agreed with the change (while reframing its value as "removes unnecessary code that has unintended side effects" rather than a race fix). The author himself conceded on 2025-10-14T08:59:49Z that he had not intended a breaking change and would look for something preserving existing semantics; the SIG then closed it three days later.

### Sources

- `opentelemetry/pulls/opentelemetry-go-contrib-8014.md` — [SRC-PR-07], PR #8014 body, discussion (27 comments), reviews, and timeline (`2025-10-17T10:41:58Z · closed by dmathieu`)
- `opentelemetry/meeting-notes/entry-3479584781.md` — [SRC-NOTE-04], OpenTelemetry Go SIG meeting note for 2025-10-16, item 1 "otelgin Context Reversal in DataRace"
