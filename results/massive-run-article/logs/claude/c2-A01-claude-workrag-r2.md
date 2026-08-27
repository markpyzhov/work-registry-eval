# Which MultipartForm cleanup approach is being pursued for otelgin (`#5946` / `#6609`), and what is its current implementation status?

<!-- RESPONSE_START -->

## Approach: automatic `MultipartForm.RemoveAll()` in the otelgin middleware

**The adopted approach** is for otelgin to call `c.Request.MultipartForm.RemoveAll()` automatically in the middleware's deferred/return phase. The Work State (`WS-05: Contrib Modules`, task `T001`) records this explicitly under Decisions and Superseded Directions: *"The earlier unresolved choice among `RemoveAll()`, reattach, and user cleanup is superseded. Automatic `MultipartForm.RemoveAll()` is adopted."* `(SRC-PR-01, SRC-NOTE-04, CMT-2026-03-002)`

The alternatives that were considered and rejected:
- **Reattach** — save the original `c.Request` before `WithContext(ctx)` and reattach the `MultipartForm` in a defer, letting `net/http`'s `finishRequest` do the cleanup (proposed by Yiling-J; he initially favored it as "less aggressive")
- **Leave cleanup to users** — document that users must call `RemoveAll()` themselves
- **Parse the form in the middleware** (akats7's suggestion) — rejected by Yiling-J as an operation that should be explicit and user-controlled because of the `maxMemory` parameter and resource cost
- **`c.Request.Clone(ctx)` deep copy** (dmathieu's suggestion) — shown not to work, since `MultipartForm` is lazily initialized and is `nil` at middleware time

The decision was settled by Damien Mathieu and Tyler Yahn over DM: otelgin will call `RemoveAll()` automatically — not reattach, not leave cleanup to users (`CMT-2026-03-002`, effective 2026-03-08).

## Current status: complete locally, publication pending

`T001` is marked done in the Work State, with the caveat that completion is internal only:

- Conflict resolution and tests for PR `#6609` are **finished locally** and the MultipartForm cleanup work is treated as done.
- **Final commits have not been pushed**, and `#5946` / `#6609` have not been updated on GitHub — so both the issue and the PR **remain open/unmerged** publicly. Source snapshots confirm issue `#5946` state `open` and PR `#6609` state `open` (branch `fix/gin_multipartform` → `main`, +95/−0 across 3 files, last updated 2025-11-13).
- The Work State Index classifies this as **"Active / open"** under key blockers, specifically as "publication of the completed local otelgin cleanup," and separately as "Completed internally, external record pending."
- **Next update needed**: publication of the completed `#6609` work and the GitHub issue update.

## Supporting background

The root cause (per the 2025-10-16 Go SIG note, `SRC-NOTE-04`): the instrumentation replaces the request via `c.Request = c.Request.WithContext(ctx)`, so temporary multipart files land on a new request object that `net/http` never calls `RemoveAll()` on. Damien flagged it as a historical issue manifesting in otelgin but potentially affecting virtually all HTTP-related middleware.

Known trade-off accepted with `RemoveAll()`: if an upstream middleware (e.g. `m1(m2(otel-middleware(m3(fn))))`) later expects access to the form, the files are already gone, and middlewares calling `ParseMultipartForm` again may re-create resources and cause extra allocations. Yiling-J added test cases with one upstream and one downstream middleware to demonstrate the behavior; akats7 confirmed the result aligned with what was discussed. Configurability on top of `RemoveAll()` was deliberately deferred until users explicitly request it.

Note that a related but distinct otelgin item, PR `#8014` (context save/restore data race), is `closed_without_merge` and is **not** the MultipartForm work. A prototype alternative, `#8161` from flc1125, was floated in review but akats7 doubted it addressed the core issue; it is not the adopted path.

**Records cited**: `work-states/WS-05-contrib.md` (Task List, Active Work, Decisions, Done/Evidence, Next Update Needed), `work-states/index.md`, `work-states/comments/2026-03.md` (`CMT-2026-03-002`), `opentelemetry/issues/opentelemetry-go-contrib-5946.md` (`SRC-ISSUE-01`), `opentelemetry/pulls/opentelemetry-go-contrib-6609.md` (`SRC-PR-01`), `opentelemetry/meeting-notes/entry-3479584781.md` (`SRC-NOTE-04`).
