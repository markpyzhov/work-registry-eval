# Which MultipartForm cleanup approach is being pursued for otelgin (`#5946` / `#6609`), and what is its current implementation status?

<!-- RESPONSE_START -->

I have enough evidence to answer.

## Answer

**Approach being pursued: explicit `RemoveAll()` cleanup inside the otelgin middleware.**

The middleware calls `c.Request.MultipartForm.RemoveAll()` in a deferred function (guarded by a nil check) when the middleware returns, so the otelgin-created request's temporary multipart files are deleted by whoever created that request.

### Why this issue exists
otelgin replaces the request via `c.Request = c.Request.WithContext(ctx)`. `WithContext` is a shallow clone, and `MultipartForm` is lazily initialized (nil at middleware time), so when the form is later parsed the temp files land on the *new* request. `net/http`'s `finishRequest` only calls `RemoveAll()` on the *original* request, whose `MultipartForm` is still nil — so nothing cleans up. Damien Mathieu flagged in the 2025-10-16 Go SIG that this is a historical issue affecting virtually all HTTP-related middleware, not just otelgin.

### Alternatives considered and rejected
- **`c.Request.Clone(ctx)`** (dmathieu, Jan 2025) — rejected: a deep copy also copies `MultipartForm`, so it doesn't help.
- **Parse the form in the middleware** (akats7) — rejected by Yiling-J: parsing is the user's decision, `maxMemory` should not be chosen by instrumentation.
- **"Reattach" approach** (Yiling-J's preference: save the original `c.Request`, and in the defer copy `MultipartForm` back to it so `net/http` cleans up naturally) — argued as less aggressive and portable to other middlewares, but not adopted; it depends on every other middleware behaving correctly.
- **Configurable `Option` to control cleanup** (akats7, 2025-11-10) — deferred. flc1125 and akats7 agreed to hold off and only add configurability if users explicitly request it, since adding it after `RemoveAll()` remains backward compatible.
- **PR #8161** (flc1125, 2025-11-11) — a clone-based prototype offered as an alternative; akats7 pushed back that it doesn't address the root cause.

The Go team was asked for guidance (golang/go#74455, also #71382) and did not provide an official solution, so contrib chose its own workaround.

### Current implementation status
- **PR #6609** ("fix(otelgin): remove multipartform temporary file", Yiling-J, branch `fix/gin_multipartform` → `main`): **still open**, +95/−0 across 3 files, no labels, no milestone. Created 2025-01-13, last updated 2025-11-13.
- **Approved by akats7 on 2025-11-10.** Merge conflicts were resolved 2025-11-10 and otelgin package tests pass locally. A CHANGELOG entry was suggested by flc1125.
- **Not merged — open review thread as of the latest activity.** Tests were expanded on 2025-11-10 to include one upstream and one downstream middleware demonstrating `RemoveAll` behavior. flc1125 then objected (2025-11-11) that the resulting behavior (file no longer retrievable, `require.ErrorIs(t, err, fs.ErrNotExist)`) is not what he expects and proposed prototype #8161. Yiling-J and akats7 both maintained the result matches the agreed `RemoveAll` design; the disagreement was unresolved at the last recorded comment (akats7, 2025-11-12).
- **Scope decision:** fix otelgin only in this PR to keep it minimal; other affected middlewares (otelmux, otelecho, etc.) to be fixed in separate minimal PRs.
- **Issue #5946** remains **open** (labels: bug, area: instrumentation, instrumentation: otelgin), last updated 2025-07-03.

### Sources
- `opentelemetry/pulls/opentelemetry-go-contrib-6609.md` [SRC-PR-01] — PR state, reviews, approval, and the full design debate
- `opentelemetry/issues/opentelemetry-go-contrib-5946.md` [SRC-ISSUE-01] — original bug report, root-cause experiments, `RemoveAll` proposal and its side-effect analysis
- `opentelemetry/meeting-notes/entry-3479584781.md` [SRC-NOTE-04] — Go SIG 2025-10-16 discussion framing the issue as affecting all HTTP middleware
- `opentelemetry/pulls/opentelemetry-go-contrib-8014.md` — related otelgin context/data-race PR referenced in the same SIG discussion
