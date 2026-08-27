# Which MultipartForm cleanup approach is being pursued for otelgin (`#5946` / `#6609`), and what is its current implementation status?

<!-- RESPONSE_START -->

## Approach: automatic `MultipartForm.RemoveAll()` in the otelgin middleware

**The adopted approach** is for the otelgin middleware itself to call `c.Request.MultipartForm.RemoveAll()` automatically (in a deferred cleanup after the handler chain), with **no configuration option** — cleanup is unconditional by default. This is recorded as a settled decision in `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md` (task `T001`, "Decisions and Superseded Directions").

**Root cause it addresses:** the middleware replaces the request via `c.Request = c.Request.WithContext(ctx)`, so when a handler later parses the form, `MultipartForm` is populated on the *new* request while `net/http`'s end-of-request cleanup only looks at the *original* request — leaving `multipart-*` temp files on disk (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/issues/opentelemetry-go-contrib-5946.md`).

**Alternatives that were considered and are now superseded** (`.../work-states/WS-05-contrib.md`, `.../opentelemetry/pulls/opentelemetry-go-contrib-6609.md`, `.../opentelemetry/meeting-notes/entry-3479584781.md`):
- **Reattach** — copy the cloned request's `MultipartForm` back onto the original request before returning (Yiling-J's preference; also floated as prototype PR `#8161` by flc1125).
- **Leave cleanup to users** — document that callers must call `RemoveAll()` themselves.
- **Deep `Request.Clone(ctx)`** (dmathieu) and **parsing the form inside the middleware** (akats7) — both rejected as not fixing the core problem / imposing `maxMemory` policy on users.
- **A configurable Option** (akats7, 2025-11-10) — deferred; the SIG position is to add configurability only if users explicitly request it, since `RemoveAll()`-by-default can be made configurable later without breaking compatibility.

The 2025-10-16 Go SIG (notes at `.../meeting-notes/entry-3479584781.md`) enumerated exactly these three options and Damien recommended starting with automatic deletion, no option; Tyler agreed instrumentation owns the cleanup.

## Current implementation status: done locally, not yet published

Per the authoritative Work State (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md`) and the human correction `CMT-2026-03-002` (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/comments/2026-03.md`, effective 2026-03-08, author Damien Mathieu):

- `T001` is marked **complete**: merge-conflict resolution and tests for PR `#6609` are finished **locally**.
- The final commits **have not been pushed**, and `#5946` / `#6609` **have not been updated on GitHub** — so both the issue and the PR still show as **open / unmerged** in the collected sources (issue `#5946` state: open; PR `#6609` state: open, +95/−0 across 3 files, branch `fix/gin_multipartform`).
- The decision itself was settled **over DM between Damien Mathieu and Tyler Yahn**, not in a public thread — `CMT-2026-03-002` is its only evidence (no supporting `SRC-*`).
- No release is established for this fix in the sources.
- The outstanding next action is **publication**: push the commits and update the GitHub issue/PR (`.../work-states/WS-05-contrib.md`, "Active Work" and "Next Update Needed"; also summarized in `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md`).

**Last public state before that correction** (PR `#6609`, `.../pulls/opentelemetry-go-contrib-6609.md`): akats7 approved on 2025-11-10; Yiling-J resolved conflicts and expanded tests with an upstream and a downstream middleware on 2025-11-10; flc1125 pushed back on 2025-11-11 that the test asserting `fs.ErrNotExist` for a later middleware isn't the expected result and proposed prototype PR `#8161`; akats7 replied 2025-11-12 that the result matches the agreed behavior and doubted the clone-based prototype fixes the core issue. Last PR update recorded: 2025-11-13.

Note: the related otelgin PR `#8014` (context save/restore data race) is a *separate* task (`T007`) and was **closed without merge** on 2025-10-17 — not part of the MultipartForm fix.
