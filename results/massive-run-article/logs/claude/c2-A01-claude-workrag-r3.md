# Which MultipartForm cleanup approach is being pursued for otelgin (`#5946` / `#6609`), and what is its current implementation status?

<!-- RESPONSE_START -->

## Approach adopted

**Automatic `MultipartForm.RemoveAll()`** — the otelgin middleware calls `RemoveAll()` itself, in the middleware's deferred/return phase.

The earlier three-way choice is explicitly **superseded**. The alternatives that were considered and rejected:
- **Reattach** — saving `c.Request` before `WithContext(ctx)` and reattaching `MultipartForm` to the original request in a defer (proposed by Yiling-J).
- **Leave cleanup to users** — documenting that users must call `c.Request.MultipartForm.RemoveAll()` themselves.
- Parsing the form in the middleware / cloning the request (akats7 argued cloning does not address the core issue: setting `c.Request = c.Request.WithContext(ctx)` with an unparsed form means the http server never learns to clean it up).

The decision was settled between Tyler Yahn and Robert Pająk over DM, per `CMT-2026-03-002`.

## Implementation status (as of Work State `WS-05`, last updated 2026-03-08)

Task `T001` is marked **complete internally, but not published**:

- Conflict resolution and tests for PR `#6609` are **finished locally**, and the MultipartForm cleanup work is treated as done.
- **Final commits have not been pushed.** Issue `#5946` and PR `#6609` therefore **remain open/unmerged on GitHub**, and neither has been updated with the outcome.
- The parent workstream `WS-05: Contrib Modules` is still `in_progress` (P0, owner Damien Mathieu in contrib SIG context); this item sits under **Active Work** as a "publication follow-up".

## Next action

Push the final commits and update `#5946` / `#6609` on GitHub. The Work State index summarizes it as: `RemoveAll()` adopted and local work complete; final commits unpushed; GitHub issue/PR open. Publication of the completed local otelgin cleanup is listed among the registry's key active/open items.

## Known side effect of the chosen approach

Raised on `#5946` and unresolved in the record: with middleware nested as `m1(m2(otel-middleware(m3(fn))))`, where outer middlewares call `request.ParseMultipartForm(...)`, the `RemoveAll()` in otel-middleware can cause them to repeatedly recreate `request.MultipartForm` resources, adding memory allocations. Yiling-J's position was that since removal happens during the middleware's return phase, most middlewares would not read the multipart form at that point anyway.

## Records cited

Dataset `b5f5be0e8a9b11f197db2303d7337e37`:
- `work-states/WS-05-contrib.md` (Task List `T001`, Active Work, Decisions and Superseded Directions, Done / Evidence, Next Update Needed) — authoritative Work State
- `work-states/comments/2026-03.md` — `CMT-2026-03-002` (the DM decision and unpublished status)
- `work-states/index.md` — item-coverage row for `opentelemetry-go-contrib#5946` / `#6609`
- `opentelemetry/issues/opentelemetry-go-contrib-5946.md` — `SRC-ISSUE-01`
- `opentelemetry/pulls/opentelemetry-go-contrib-6609.md` — `SRC-PR-01`
- `opentelemetry/meeting-notes/entry-3479584781.md` — `SRC-NOTE-04` (2025-10-16 SIG discussion)

One caveat on freshness: the source cutoff is 2026-02-27 and the final Work State runs through 2026-03-11, so anything that happened on GitHub after that is not covered by this dataset.
