# Why was `opentelemetry-go-contrib` pull request `#8014` (otelgin context save/restore) closed?

<!-- RESPONSE_START -->

I have everything needed.

## Why PR #8014 was closed

**Bottom line:** It was closed without merge on **2025-10-17 by Damien Mathieu (`dmathieu`)** because the OpenTelemetry Go SIG decided at its **2025-10-16 meeting** that the proposed fix was incorrect — the existing context save/restore behavior in otelgin is intentional and correct.

### The PR
`otelgin: remove unneeded context save/restore to avoid data race` (open-telemetry/opentelemetry-go-contrib#8014), opened 2025-10-14 by **nicksherron**, branch `fix/otelgin-data-race`, +83/-10 across 2 files. It proposed dropping the deferred restore of `c.Request`'s context, arguing the deferred mutation races with goroutines that read `c.Request.Context()` after `c.Next()`.
(`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-contrib-8014.md`)

### The chain of events
1. The PR gained early support — `flc1125` and `akats7` agreed, and `akats7` **approved** it on 2025-10-14T07:52:18Z. Codecov was clean. `dmathieu` even asked nicksherron to turn his reproducer gist into a CI test, which he did.
2. **The objection (2025-10-14T07:54:22Z, `dmathieu`):** the defer is not spurious — its purpose is to *remove the span from the context* so that parent middleware running after `c.Next()` does not create spans that become children of the finished otelgin span. Removing the defer would silently change that parenting behavior.
3. `dmathieu` added (08:42) that this has been the default behavior for years and is shared with other instrumentations such as `otelecho`, so changing it would be a breaking change; he invited the author to the SIG meeting. nicksherron conceded this was "a strong argument" and said he'd look for a fix preserving existing semantics.
4. **SIG discussion 2025-10-16** (recorded in `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3479584781.md`): Damien Mathieu stated the current behavior is correct and that **users should explicitly pass the current context into spawned goroutines**, citing the collector's pattern of passing context directly outside HTTP requests. **Tyler Yahn agreed**, adding that OpenTelemetry's pattern for asynchronous operations is to *link* spans rather than make them children. An action item was recorded for Damien to respond on the PR accordingly.
5. **Closing comment (2025-10-17T10:41:58Z, `dmathieu`):** "We have been discussing this in yesterday's SIG meeting, and have decided this fix is incorrect and the current behavior is the proper one," referencing `opentelemetry-go-contrib` issue #4588's comment thread. The timeline records `2025-10-17T10:41:58Z · closed by dmathieu` — a **close event with no merge event**.

### Registry status
The work state tracks this as task `T007`, **`closed_without_merge`** — explicitly not done — and flags as needing manual triage whether any in-tree follow-up replaced #8014.
(`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md`)

Note the underlying data race was never disputed as unreal — the rejection was of *this fix*, because dropping the defer would change long-standing span-parenting semantics across gin/echo instrumentation. The registry sources contain no record of a replacement fix.
