# Which MultipartForm cleanup approach is being pursued for otelgin (`#5946` / `#6609`), and what is its current implementation status?

<!-- RESPONSE_START -->

## Answer

**Approach being pursued: explicit cleanup inside the otelgin middleware — a deferred `c.Request.MultipartForm.RemoveAll()`.**

### Why this approach

The bug (issue #5946, opened 2024-07-25 by zacklpx, still `open`, labels: bug / area: instrumentation / instrumentation: otelgin): otelgin does `c.Request = c.Request.WithContext(ctx)`, creating a new request. `MultipartForm` is lazily initialized, so it is still `nil` at middleware time and never gets shared back. When the form is later parsed, the temp files land on the *new* request, and `net/http`'s `finishRequest` calls `RemoveAll()` on the *original* request, where `MultipartForm` is nil — so `multipart-xxxx` temp files are never deleted.

Alternatives that were considered and set aside:
- **`c.Request.Clone(ctx)`** (dmathieu, 2025-01-14) — rejected: deep copy also copies MultipartForm, and the field is nil at that point anyway.
- **Parse the form in the middleware** (akats7) — rejected by Yiling-J: parsing should be the user's explicit choice, and `ParseMultipartForm`'s `maxMemory` belongs to the user.
- **"Reattach" approach** (Yiling-J's own preference: save the original request, then copy `MultipartForm` back to it in the defer) — less aggressive and portable to other middlewares, but relies on every other middleware also behaving correctly. Yiling-J re-proposed it on 2025-11-03; the group instead converged on `RemoveAll()`.
- **Make it configurable via an `Option`** (akats7, 2025-11-10) — deliberately deferred; flc1125 argued for the SIG's position of adding configurability only if users explicitly request it (it stays backward-compatible to add later), and akats7 agreed to hold off.

The Go team gave no guidance — Yiling-J filed golang/go#71382 and flc1125 filed golang/go#74455, neither produced an official solution, so contrib decided on a workaround of its own. The Go Go SIG (meeting 2025-10-16, minutes posted 2025-11-03) discussed it and recommended that middleware remove temporary resources; it also noted this is a historical issue affecting essentially all `*http.Request`-based middleware (otelmux, otelecho, etc.), but the group agreed to keep #6609 minimal and fix otelgin only, with separate per-component PRs for the rest.

### Implementation status (PR #6609, "fix(otelgin): remove multipartform temporary file", author Yiling-J)

**Open, approved but not merged — stalled on an unresolved review disagreement.**

- Created 2025-01-13, branch `fix/gin_multipartform` → `main`, **+95 / −0 across 3 files**, no labels, no milestone. Last updated 2025-11-13 (data collected 2026-07-14).
- The change is a deferred `if c.Request.MultipartForm != nil { RemoveAll() }`, with the error routed to `otel.Handle()` per dmathieu's suggestion rather than ignored. Windows test is skipped, matching Go's own form-cleanup tests.
- 2025-11-04: consensus reached on `RemoveAll()` (flc1125 proposed, Yiling-J accepted).
- 2025-11-10: akats7 said "we're good to resolve the conflicts and close this out"; Yiling-J resolved conflicts, tests pass; **akats7 APPROVED at 16:20 UTC**. flc1125 asked for and got extra test coverage with one upstream and one downstream middleware, plus a suggested CHANGELOG line: "Fix issue in `go.opentelemetry.io/contrib/instrumentation/github.com/gin-gonic/gin/otelgin` middleware where temporary files for multipart/form-data were not being removed. (#6609)".
- 2025-11-11 to 11-12: **blocked again.** flc1125 objected to the new test's expectation (`require.ErrorIs(t, err, fs.ErrNotExist)` — i.e. an upstream middleware can no longer read the file after `RemoveAll`), saying the file should still be retrievable, and posted an alternative prototype, **PR #8161**, based on cloning the request. Yiling-J pushed back ("I thought we had already agreed on the `RemoveAll` approach") and asked whether the implications of `RemoveAll` were actually covered in the SIG. akats7 said the result matches his understanding and doubted the prototype works, since cloning does not address the core problem of the unparsed form on the swapped request. No resolution appears after 2025-11-12.

So: agreed design (`RemoveAll` in a defer), code written, conflicts resolved, tests passing, one approval in hand — held up by an open thread over whether deleting the temp files out from under an upstream middleware is the correct expected behavior, with #8161 floated as a competing fix. Issue #5946 remains open.

### Sources

- `[SRC-ISSUE-01]` — opentelemetry/issues/opentelemetry-go-contrib-5946.md (issue #5946)
- `[SRC-PR-01]` — opentelemetry/pulls/opentelemetry-go-contrib-6609.md (PR #6609, discussion + 28 review comments + 25 reviews)
- `[SRC-NOTE-04]` — opentelemetry/meeting-notes/entry-3479584781.md (Go SIG meeting 2025-10-16, posted by pellared 2025-11-03)
