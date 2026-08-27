# Which MultipartForm cleanup approach is being pursued for otelgin (`#5946` / `#6609`), and what is its current implementation status?

<!-- RESPONSE_START -->

## Approach: automatic `MultipartForm.RemoveAll()` in the otelgin middleware

**The adopted approach** is for otelgin's middleware to call `c.Request.MultipartForm.RemoveAll()` automatically in a deferred cleanup — not the "reattach" alternative, and not leaving cleanup to users. It is unconditional by default; a configuration Option would only be added if users explicitly request one.

### Why this one won

- **Root cause**: otelgin does `c.Request = c.Request.WithContext(ctx)`, a shallow clone. The multipart form is lazily initialized, so it lands on the *new* request while `net/http`'s end-of-request cleanup only inspects the *original* request — which still has `MultipartForm == nil`. Nothing removes the temp files. (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/issues/opentelemetry-go-contrib-5946.md`)
- **Rejected alternatives** debated on PR #6609: `Request.Clone()` (deep copy also copies the form — doesn't help), parsing the form inside the middleware (imposes `maxMemory` decisions on users), and Yiling-J's preferred "reattach the `MultipartForm` back to the original request before returning" (less aggressive but depends on every other middleware behaving correctly). (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-contrib-6609.md`)
- **SIG decision, 2025-10-16**: Damien Mathieu raised the three options (RemoveAll / leave to user / configurable option) and proposed starting with automatic deletion, adding configuration only on demonstrated need. Tyler Yahn agreed the instrumentation owns the cleanup. (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3479584781.md`)
- **Agreement on the PR, Nov 2025**: flc1125 and Yiling-J converged on `RemoveAll()`; akats7 floated an Option for middlewares upstream that still want form data, then accepted holding off until explicitly requested, and approved the PR on 2025-11-10. (`.../opentelemetry-go-contrib-6609.md`)

### Current status: done locally, not published

The implementation work is **complete but unpublished**. Per the authoritative Work State (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md`, task `T001`), conflict resolution and tests are finished locally, and the task is treated as done internally — but final commits have not been pushed, so issue **#5946 and PR #6609 remain open/unmerged on GitHub**.

This comes from a correction by Damien Mathieu effective 2026-03-08: he and Tyler settled over DM on automatic `RemoveAll()`, he finished the `#6609` conflict resolution and tests locally, and had not yet pushed or updated the GitHub issue/PR. Note the provenance caveat recorded there — this rests on the comment alone, with no supporting `SRC-*` evidence. (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/comments/2026-03.md`, `CMT-2026-03-002`)

Both source records still show `State: open` as collected (issue #5946 updated 2025-07-03; PR #6609 updated 2025-11-13), consistent with the unpublished status.

### Loose end

One unresolved review thread: flc1125 objected on 2025-11-11 that a file should still be retrievable by other middleware after cleanup, and offered a competing prototype in PR #8161. Both akats7 and Yiling-J pushed back — akats7 doubted the prototype's cloning approach addresses the root cause. The Work State records no reversal of the `RemoveAll()` decision. The next update needed is publication of the completed #6609 work and the corresponding GitHub issue update.
