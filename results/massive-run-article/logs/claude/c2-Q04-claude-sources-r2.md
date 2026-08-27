# What is the status of the otelgin MultipartForm temporary-file cleanup work tracked by `opentelemetry-go-contrib` issue `#5946` and pull request `#6609`?

<!-- RESPONSE_START -->

## Status: both still open and unresolved (as of the corpus snapshot)

**Issue #5946** — "Using otelgin.Middleware will cause temporary MultipartForm files not to be destroyed" (author `zacklpx`, opened 2024-07-25) is **open**, labeled `bug` / `area: instrumentation` / `instrumentation: otelgin`, no milestone, last updated 2025-07-03.

**PR #6609** — "fix(otelgin): remove multipartform temporary file" (author `Yiling-J`, opened 2025-01-13, `fix/gin_multipartform` → `main`, +95/−0 across 3 files) is **open**, no labels or milestone, last updated 2025-11-13T01:26:12Z. It has been approved once (`akats7`, 2025-11-10T16:20:02Z) but was never merged — discussion continued past the approval and stalled.

### Root cause
otelgin does `c.Request = c.Request.WithContext(ctx)`. `WithContext` is a shallow copy and `MultipartForm` is lazily initialized (nil at middleware time), so when the handler later parses the form the temp files land on the *new* request. The `net/http` server's `finishRequest` only calls `RemoveAll()` on the *original* request, which still has `MultipartForm == nil` — so `multipart-xxxx` files leak. `flc1125` demonstrated this is not gin-specific: any `http.Server` middleware doing `r = r.WithContext(...)` before `ParseMultipartForm` reproduces it. Upstream Go issues golang/go#71382 and golang/go#74455 were filed and produced no official guidance.

### Approaches debated
- `Clone(ctx)` instead of `WithContext` (dmathieu) — rejected; deep copy also copies the (nil) form.
- Parse the form inside the middleware (dmathieu/akats7) — rejected by Yiling-J; `maxMemory` should be the user's call.
- **Reattach**: copy `MultipartForm` back to the original request before returning (Yiling-J's preference) — less aggressive, works only if every middleware behaves.
- **`RemoveAll()` in a defer** (zihuyishi, flc1125, the PR as written) — the option that carried.
- `flc1125` later posted an alternative prototype, PR #8161.

### SIG decision (Go SIG meeting 2025-10-16, notes published 2025-11-03)
Damien Mathieu raised it; the group considered (1) `RemoveAll()`, (2) leave cleanup to users, (3) a configurable option. Decision: **start with automatic removal, no config option; add configurability only if users explicitly ask.** Tyler Yahn agreed the instrumentation owns cleanup. `akats7` floated an `Option` on 2025-11-10 and then dropped it, consistent with the SIG.

### Why it stalled
After the approval, `flc1125` objected on the test (`gin_test.go` line 512) that the form should still be retrievable after the middleware returns, and pointed at his #8161 prototype. `Yiling-J` (2025-11-12) responded that `RemoveAll` deleting the files is the whole point and that they had already agreed. `akats7` (2025-11-12, the last recorded activity) said he still couldn't identify the behavior flc1125 considered wrong, and doubted #8161 would work since cloning does not address the unparsed-form-at-`WithContext` core problem. Nothing recorded after 2025-11-13 — roughly nine months of inactivity relative to today.

### Loose ends
- Scope: flc1125 noted all `*http.Request`-based middlewares (otelecho, otelmux, …) share the bug; the team chose to keep #6609 minimal to otelgin and handle others via separate PRs. That follow-up work is not tracked in this corpus.
- Issue #5946's timeline records a `marked_as_duplicate` event by `dmathieu` on 2025-07-02, alongside a cross-reference from contrib issue #7541 at the same moment.
- Later cross-references on #5946 — #8419 (MrAlias, 2026-01-16), PR #8851 (SAY-5, 2026-04-21), and a reference by SAY-5 on 2026-05-31 — suggest continued activity, but no source records for those items exist in this dataset, so I can't say what they did.

### Sources
- `opentelemetry/issues/opentelemetry-go-contrib-5946.md` [SRC-ISSUE-01]
- `opentelemetry/pulls/opentelemetry-go-contrib-6609.md` [SRC-PR-01]
- `opentelemetry/meeting-notes/entry-3479584781.md` [SRC-NOTE-04] — Go SIG, meeting of 2025-10-16
- `opentelemetry/pulls/opentelemetry-go-contrib-8014.md` [SRC-PR-07] — adjacent otelgin context save/restore discussion
