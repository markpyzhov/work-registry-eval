# Which MultipartForm cleanup approach is being pursued for otelgin (`#5946` / `#6609`), and what is its current implementation status?

<!-- RESPONSE_START -->

## Answer

**The approach being pursued: unconditional `MultipartForm.RemoveAll()` inside the otelgin middleware's deferred cleanup — no config option, no form pre-parsing, no request cloning.**

### The problem
`otelgin.Middleware` replaces the request via `c.Request = c.Request.WithContext(ctx)`. Because `Request.MultipartForm` is lazily initialized (nil at middleware time) and `WithContext` is only a shallow copy, the form later parsed on the *new* request is invisible to the original one. `net/http`'s `finishRequest` then finds `req.MultipartForm == nil` on the original request and never calls `RemoveAll()`, so `multipart-*` temp files leak. This is not gin-specific — it affects any `*http.Request`-based middleware that does `WithContext` (SRC-ISSUE-01, SRC-PR-01).

### Alternatives considered and rejected
- **`c.Request.Clone(ctx)`** (dmathieu) — deep copy also copies MultipartForm, and the field is nil at that point anyway, so it doesn't help.
- **Parse the form in the middleware** (akats7's early preference) — rejected by Yiling-J: parsing is the user's call, and `ParseMultipartForm`'s `maxMemory` shouldn't be decided by instrumentation.
- **"Reattach" approach** (Yiling-J's own preference as late as 2025-11-03): save the original request, then in the defer copy `MultipartForm` back onto it so `net/http` cleans up naturally. Less aggressive and portable to other middlewares, but depends on every other middleware behaving correctly. He conceded to `RemoveAll` on 2025-11-04.
- **Configurable Option with cleanup as default** (akats7, 2025-11-10) — explicitly deferred. The SIG position (per flc1125, backed by Damien's meeting comment) was to start with unconditional removal and add configuration only if users ask; akats7 agreed to hold off. Adding an option later stays backward compatible.
- An upstream fix was sought from the Go team (golang/go#71382, golang/go#74455) but never materialized, which is why a workaround was adopted.

### SIG decision (meeting 2025-10-16, posted 2025-11-03)
Damien Mathieu raised it; three options were tabled (`RemoveAll`, leave to user, configurable option). Damien recommended starting with automatic deletion and no option; Tyler Yahn confirmed the instrumentation is responsible for cleanup. Component owners were empowered to decide. Scope was kept to otelgin only for a minimal PR; other middlewares (otelmux, otelecho, etc.) are acknowledged as similarly affected and left to separate follow-up PRs.

### Current implementation status: still open, unmerged, blocked on a test-behavior disagreement
- **Issue #5946** — open (bug / area: instrumentation / instrumentation: otelgin), opened 2024-07-25 by zacklpx, no milestone. Marked as duplicate target by dmathieu on 2025-07-02.
- **PR #6609** ("fix(otelgin): remove multipartform temporary file", Yiling-J, branch `fix/gin_multipartform` → `main`) — **open**, +95/−0 across 3 files, no labels, no milestone. Created 2025-01-13, last updated 2025-11-13. 15 discussion comments, 28 review comments.

Progress as of the last activity in the corpus:
1. 2025-11-10 — conflicts resolved, otelgin package tests passing locally; akats7 said "we're good to... close this out".
2. 2025-11-10 — flc1125 requested unit tests for the upstream-middleware-access scenario plus a CHANGELOG entry ("Fix issue in `go.opentelemetry.io/contrib/instrumentation/github.com/gin-gonic/gin/otelgin` middleware where temporary files for multipart/form-data were not being removed. (#6609)").
3. 2025-11-10 — Yiling-J added a test with one upstream and one downstream middleware demonstrating `RemoveAll` behavior.
4. 2025-11-11→12 — **the current sticking point**: flc1125 objects that the test's outcome (`require.ErrorIs(t, err, fs.ErrNotExist)` — an upstream middleware can no longer reopen the file) is wrong, and floated a competing clone-based prototype, PR #8161. Yiling-J and akats7 both pushed back: this is the natural consequence of the already-agreed `RemoveAll`, and akats7 argues #8161 doesn't fix the root cause since cloning still leaves the server unaware of the form. flc1125 asked for further investigation; the thread ends unresolved.

An open side concern noted in #5946: with `m1(m2(otel-middleware(m3(fn))))`, if outer middlewares call `ParseMultipartForm` themselves, the middleware's `RemoveAll` may cause them to recreate the form, adding memory allocations.

### Sources
- `opentelemetry/issues/opentelemetry-go-contrib-5946.md` — [SRC-ISSUE-01]
- `opentelemetry/pulls/opentelemetry-go-contrib-6609.md` — [SRC-PR-01]
- `opentelemetry/meeting-notes/entry-3479584781.md` — [SRC-NOTE-04], OpenTelemetry Go SIG meeting 2025-10-16
