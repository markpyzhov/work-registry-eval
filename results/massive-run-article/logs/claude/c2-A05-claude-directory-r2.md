# Why was `opentelemetry-go-contrib` pull request `#8014` (otelgin context save/restore) closed?

<!-- RESPONSE_START -->

I have what I need. No comment record modifies the PR #8014 outcome (the one otelgin-adjacent comment concerns a different task, T001/MultipartForm).

## Answer

**PR #8014 was closed without merge on 2025-10-17 by Damien Mathieu (dmathieu), because the OpenTelemetry Go SIG decided at its 2025-10-16 meeting that the fix was incorrect and the existing context save/restore behavior is the intended, correct one.**

### What the PR proposed
Author `nicksherron` opened it on 2025-10-14 (`fix/otelgin-data-race`, +83/-10 across 2 files). It removed the deferred `c.Request = c.Request.WithContext(savedCtx)` restore in the otelgin middleware, arguing that the deferred write races with goroutines spawned by downstream handlers that read `c.Request.Context()` — reproducible with `go test -race`, and matching the long-open issue #4588. He also argued the defer costs an extra allocation and a redundant `WithContext` call.
(`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-contrib-8014.md`)

### How it initially went well, then turned
- `flc1125` first objected, then after the discussion **approved and agreed** with the change (framing its value as removing unnecessary code with side effects rather than "fixing a data race").
- `akats7` **formally approved** the PR on 2025-10-14.
- `dmathieu` asked for the reproducer gist to be turned into a CI test, which the author added.

### The blocking objection
`dmathieu` then identified the actual purpose of the defer: it removes the span from the context so that **spans created in parent middleware after `c.Next()` don't become children of the already-finished otelgin span**. Dropping the defer would change that long-standing semantics (also shared with otelecho), making it a behavior break, not dead-code removal. The author conceded this was a strong argument and said he'd try to preserve the semantics while fixing the race. `dmathieu` invited him to discuss it at the SIG meeting.
(`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-contrib-8014.md`)

### The SIG decision (2025-10-16)
At the OpenTelemetry Go SIG (attendees: Tyler Yahn, Damien Mathieu, Bryan Boreham, David Ashpole, Robert Pająk):
- Damien held that the current context-reversion behavior is correct, and that **users should explicitly pass the current context into goroutines they spawn**, citing the collector's pattern of passing context directly outside HTTP requests.
- Tyler Yahn agreed, adding that OpenTelemetry's pattern for asynchronous operations is to **link** spans rather than make them child references.
- An action item was recorded for Damien to respond on PR #8014 accordingly.
(`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3479584781.md`)

Damien posted the outcome on 2025-10-17 at 10:41:58Z — "this fix is incorrect and the current behavior is the proper one," pointing to a comment on issue #4588 — and closed the PR in the same minute. The timeline shows **`closed` by dmathieu, with no merge event**.

### Registry status
The Work State records this as task `T007`, status **`closed_without_merge`** — explicitly *not done* under the PR done convention, and it remains unchecked. An open follow-up question is noted: whether any in-tree work later replaced #8014.
(`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md`, lines 15, 35, 40, 48, 59)

Note the irony worth flagging: the PR carried an approving review from `akats7` and agreement from `flc1125` at the time it was closed — approval was overtaken by the SIG's semantic objection, not withdrawn.
