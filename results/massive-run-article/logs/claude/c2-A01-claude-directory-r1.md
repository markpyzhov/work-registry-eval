# Which MultipartForm cleanup approach is being pursued for otelgin (`#5946` / `#6609`), and what is its current implementation status?

<!-- RESPONSE_START -->

## Approach adopted

**Automatic `MultipartForm.RemoveAll()` inside the otelgin middleware** — not the "reattach" alternative, and not leaving cleanup to users.

The middleware defers a call that removes the temporary multipart files it would otherwise orphan:

```go
defer func() {
    if c.Request.MultipartForm != nil {
        c.Request.MultipartForm.RemoveAll()
    }
}()
```

**Why the problem exists:** otelgin does `c.Request = c.Request.WithContext(ctx)`. Because `MultipartForm` is lazily initialized, the parsed form lands on the *new* request, while `net/http`'s end-of-request cleanup only checks the *original* one — so the `multipart-xxxx` temp files are never deleted (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/issues/opentelemetry-go-contrib-5946.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3479584781.md`).

**Rejected/superseded alternatives** (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-contrib-6609.md`):
- **Reattach** — copy the cloned request's `MultipartForm` back onto the original before returning. Yiling-J's long-standing preference (less aggressive, portable to other middlewares), superseded.
- **Leave cleanup to the user** — documented workaround only.
- **`Request.Clone(ctx)`** (dmathieu) and **parsing the form in the middleware** (dmathieu/akats7) — rejected; deep clone doesn't help, and forcing `ParseMultipartForm` takes the `maxMemory` decision away from the user.
- **A config Option to disable cleanup** (akats7, 2025-11-10) — deferred; per SIG guidance, add configurability only if users explicitly ask. Removal stays the default.
- flc1125's clone-based prototype PR `#8161` (2025-11-11) — akats7 doubted it addresses the root cause.

## Current implementation status

The Work State (`WS-05-contrib.md`, task `T001`, last updated 2026-03-08) marks this **done internally but not yet published**:

- Conflict resolution and tests for PR `#6609` are **complete locally**.
- **Final commits have not been pushed**, so issue `#5946` and PR `#6609` **remain open / unmerged on GitHub**.
- The decision itself was settled between Damien Mathieu and Tyler Yahn **over DM**, effective 2026-03-08, with no supporting public `SRC-*` record (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/comments/2026-03.md`, `CMT-2026-03-002`).
- Listed under "Next Update Needed": publication of the completed `#6609` work and the GitHub issue update.

Supporting history on the PR itself: opened 2025-01-13 by Yiling-J (+95/-0 across 3 files), **approved by akats7 on 2025-11-10**, tests extended on 2025-11-10 with an upstream and a downstream middleware to demonstrate `RemoveAll` behavior; the PR record's own state field still reads `open` as of collection (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-contrib-6609.md`).

**Known side effect, accepted:** in a chain like `m1(m2(otel-middleware(m3(fn))))`, if `m1`/`m2` also parse the form, `RemoveAll` in the otel middleware can force them to re-create `MultipartForm` resources, causing extra allocations. No better solution was identified (`opentelemetry-go-contrib-5946.md`).

**Scope:** the fix is deliberately kept minimal to otelgin, though the same defect affects any `*http.Request`-based middleware that calls `WithContext` (otelmux, otelecho, etc.); those would be separate minimal PRs.
