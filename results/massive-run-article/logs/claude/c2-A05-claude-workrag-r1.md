# Why was `opentelemetry-go-contrib` pull request `#8014` (otelgin context save/restore) closed?

<!-- RESPONSE_START -->

I have complete evidence. Here is the answer.

## Why PR #8014 was closed

**Bottom line:** It was closed without merge by **dmathieu (Damien Mathieu) on 2025-10-17T10:41:58Z**, after the OpenTelemetry Go SIG meeting of 2025-10-16 decided the proposed fix was **incorrect** and that otelgin's existing context save/restore behavior is the **intended, correct** behavior.

dmathieu's closing comment: "We have been discussing this in yesterday's SIG meeting, and have decided this fix is incorrect and the current behavior is the proper one," pointing to `opentelemetry-go-contrib/issues/4588#issuecomment-3414917592`.

### What the PR proposed
nicksherron opened it 2025-10-14 (branch `fix/otelgin-data-race`, +83/-10 across 2 files) to delete the deferred `c.Request = c.Request.WithContext(savedCtx)` in `otelgin.Middleware()`, arguing the deferred write races with goroutines spawned by downstream handlers that read `c.Request.Context()` (the 2-year-old issue #4588), and that the restore has no benefit since Gin gives each request its own `*gin.Context`.

### The substantive objection that killed it
dmathieu explained the defer is **not** dead code: its purpose is to remove the span from the context so that spans created by *parent* middleware after their `c.Next()` returns are not children of the (already-finished) otelgin span. Dropping it would silently change span parentage — a behavior change, not just a race fix. He added that this has been the default for years and the same behavior exists in other instrumentations such as otelecho, and disagreed that users should have to handle it themselves.

### The SIG resolution (meeting note SRC-NOTE-04, meeting dated 2025-10-16)
- Damien Mathieu held that the current behavior is correct and that **users should explicitly pass the needed context/span into goroutines they spawn**, citing the Collector's pattern of passing context directly outside HTTP requests.
- Tyler Yahn agreed, adding that OpenTelemetry's pattern for asynchronous operations is to **link** spans rather than make them child references.

### Notable nuance
The PR was not rejected for lack of support: **akats7 APPROVED it** on 2025-10-14, and **flc1125** — who initially objected on concurrency/performance grounds ("I prefer to leave the decision of whether to ensure concurrency safety to the users themselves") — later reversed and approved, framing the value as removing unnecessary code with unintended side effects rather than as a race fix. nicksherron had also added the CI race-reproduction test dmathieu requested (`TestMiddleware_MinimalRaceRepro`), and Codecov was green. The maintainer-level semantics decision at the SIG overrode all of that. nicksherron's last comment before closure said he'd try to find something preserving existing semantics while fixing the race; no such follow-up appears in the dataset.

### Work Registry status
`WS-05/T007` records PR #8014 as **`closed_without_merge`** and unchecked (not done), noting it was closed after the SIG treated context-restore as intentional. WS-05 also flags as needing manual triage: **whether any in-tree follow-up replaced #8014**. The PR was later cross-referenced by pellared on 2025-11-03 from `opentelemetry-go/issues/6648`.

### Dataset records used
- `opentelemetry/pulls/opentelemetry-go-contrib-8014.md` (SRC-PR-07) — description, discussion, reviews, timeline
- `opentelemetry/meeting-notes/entry-3479584781.md` (SRC-NOTE-04) — SIG meeting 2025-10-16
- `work-states/WS-05-contrib.md` — T007 task status and Decisions section
