# Which MultipartForm cleanup approach is being pursued for otelgin (`#5946` / `#6609`), and what is its current implementation status?

<!-- RESPONSE_START -->

## Answer

**Approach pursued: automatic `MultipartForm.RemoveAll()` in the otelgin middleware** — not reattaching the form to the original request, and not leaving cleanup to users.

### Why this problem exists
otelgin replaces the request via `c.Request = c.Request.WithContext(ctx)`. Go's `net/http` calls `MultipartForm.RemoveAll()` on the *original* request when the request finishes, but the temp files end up attached to the new request's lazily-initialized `MultipartForm` field, which nothing cleans up. `Request.Clone` doesn't help (it deep-copies the form), and a shallow copy doesn't help either because the field is `nil` at middleware time. Damien Mathieu raised it at the 2025-10-16 Go SIG as a historical issue that potentially affects virtually all HTTP-related middleware (`otelmux`, `otelecho`, etc.), not just otelgin. (SRC-ISSUE-01, SRC-PR-01, SRC-NOTE-04)

### Alternatives considered and superseded
- **Parse the form in the middleware** — rejected; Yiling-J argued parsing is the user's call (`maxMemory` is user-controlled, large forms are costly).
- **Reattach the form to the saved original request in a `defer`** — Yiling-J's preferred option at one point (less aggressive, portable to other OTel middlewares), but it depends on every other middleware handling `WithContext`/`ParseMultipartForm` correctly.
- **Do nothing and document that users must call `RemoveAll()`** — also rejected.
- **`flc1125`'s clone-based prototype (`#8161`)** — akats7 pushed back that cloning does not address the core issue.
- **Making the behavior configurable** — agreed to hold off until users explicitly request it (backward-compatible to add later on top of `RemoveAll()`).

The Work State records this explicitly: the earlier unresolved three-way choice among `RemoveAll()`, reattach, and user cleanup is **superseded**; automatic `RemoveAll()` is adopted. (WS-05 Decisions; SRC-PR-01, SRC-NOTE-04, CMT-2026-03-002)

### Current implementation status (authoritative, WS-05 as of 2026-03-08)

**Complete locally / internally done, but unpublished.** Task `T001` (mapped to `#5946` / PR `#6609`) is marked done: conflict resolution and tests are finished locally using automatic `RemoveAll()`, including tests with an added upstream and downstream middleware to demonstrate the `RemoveAll()` behavior. However:

- Final commits **have not been pushed**.
- Issue `#5946` and PR `#6609` **remain open / unmerged on GitHub** and have not been updated.

This state comes from `CMT-2026-03-002` (author Damien Mathieu, effective 2026-03-08), which records that he and Tyler settled the `RemoveAll()` decision over DM. The comment is its own evidence — there is no supporting `SRC-*` for the decision or the completion.

The item sits under **Active Work** in WS-05 as a "publication follow-up," and appears in the Work State Index's key-blockers list as both "Active / open: publication of the completed local otelgin cleanup" and "Completed internally, external record pending." The **Next Update Needed** is publication of the completed `#6609` work plus the GitHub issue update.

### Notes on adjacent items
- The known downside of `RemoveAll()` is acknowledged in `#5946`: if outer middlewares (`m1(m2(otel-middleware(m3(fn))))`) call `ParseMultipartForm` themselves, they may repeatedly re-create `MultipartForm` resources, causing extra allocations. Temp files are also unreadable after the otel middleware's return phase, which the team accepted as expected behavior.
- Do not confuse this with `T007` / PR `#8014`, the separate otelgin **context save/restore data-race** work, which was closed without merge on 2025-10-17.

### Dataset records used
- `work-states/WS-05-contrib.md` (`path = work-state`) — Task List `T001`, Active Work, Decisions and Superseded Directions, Done / Evidence, Next Update Needed, Applied Comments
- `work-states/comments/2026-03.md` (`path = comments`) — `CMT-2026-03-002`
- `work-states/index.md` (`path = work-state-index`) — navigation only
- `opentelemetry/issues/opentelemetry-go-contrib-5946.md` (`SRC-ISSUE-01`)
- `opentelemetry/pulls/opentelemetry-go-contrib-6609.md` (`SRC-PR-01`)
- `opentelemetry/meeting-notes/entry-3479584781.md` (`SRC-NOTE-04`, 2025-10-16 Go SIG)
