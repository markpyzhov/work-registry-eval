# Why was `opentelemetry-go-contrib` pull request `#8014` (otelgin context save/restore) closed?

<!-- RESPONSE_START -->

## Why PR #8014 was closed

**Bottom line:** it was **closed without merge by `dmathieu` on 2025-10-17T10:41:58Z** because the OpenTelemetry Go SIG concluded that the context save/restore (`defer`) in `otelgin.Middleware` is **intentional behavior, not a bug** — and that users who spawn goroutines should explicitly pass the context into them rather than have the library drop the restore.

### What the PR proposed
`nicksherron` opened it 2025-10-14 ("otelgin: remove unneeded context save/restore to avoid data race", branch `fix/otelgin-data-race` → `main`, +83/−10 across 2 files). The argument: the deferred `c.Request = c.Request.WithContext(savedCtx)` writes to `c.Request` *after* `c.Next()` returns, racing with reads from goroutines spawned by downstream handlers — the race reported in the two-year-old issue #4588. He added a reproducer test (`TestMiddleware_MinimalRaceRepro`) at `dmathieu`'s request, and argued the restore also serves no purpose since Gin does not reuse `*gin.Context` across requests.

### The counter-argument that carried
- **`flc1125` (2025-10-14T04:35Z)** initially objected that the change doesn't guarantee thread safety, and that concurrency safety of `req.WithContext`/`req.Context()` should be left to users rather than baked into infrastructure components (performance concern). He later reversed and approved, but reframed the value as "removes unnecessary code with unintended side effects," not "fixes a data race."
- **`dmathieu` (2025-10-14T07:54Z)** gave the decisive objection: the defer exists **to remove the span from the context** so that spans created after `c.Next()` in an outer middleware are not children of the (already-finished) otelgin span. With the PR's change, a span created in an outer `myCustomMiddleware` after `c.Next()` *would* become a child of the otelgin span. His words: "the defer does have a use and I don't think we can just drop it."
- **`dmathieu` (2025-10-14T08:42Z)** rejected the "violates Go conventions" framing: in the middleware pattern, control returns to the parent at the end of a middleware, so context does not simply flow forward.
- `akats7` had APPROVED the PR (2025-10-14T07:52Z), so the closure was not for lack of any approval — it was overridden by the design decision.

### Where the decision was made
The **2025-10-16 OpenTelemetry Go SIG meeting** (Tyler Yahn, Damien Mathieu, Bryan Boreham, David Ashpole, Robert Pająk) recorded an action item for Damien: respond to the "otelgin Context Reversal in DataRace" issue/PR, **suggesting passing context to spawned goroutines**. He closed the PR the next day.

### Current registry state
`WS-05` (Contrib Modules) tracks this as task `T007`, status **`closed_without_merge` — not done**, and unchecked; the SIG treated the current context-restore behavior as correct. The PR was later cross-referenced on 2025-11-03 by `pellared` from opentelemetry-go issue #6648 (the SIG meeting-notes thread).

### Dataset records used
- `opentelemetry/pulls/opentelemetry-go-contrib-8014.md` (SRC-PR-07) — description, discussion, review, timeline (`closed` by `dmathieu` 2025-10-17T10:41:58Z)
- `opentelemetry/meeting-notes/entry-3479584781.md` (SRC-NOTE-04) — 2025-10-16 SIG action item
- `work-states/WS-05-contrib.md` — `T007` status and "Decisions and Superseded Directions"
- `work-states/index.md` — "#8014 closed without merge (not done)"
- Related context: `opentelemetry/issues/opentelemetry-go-contrib-5946.md` (earlier proposal to drop the same `savedCtx` defer, with `akats7` noting `c.Request.WithContext` returns a new request rather than mutating the existing one)
