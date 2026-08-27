# What is the status of the otelgin MultipartForm temporary-file cleanup work tracked by `opentelemetry-go-contrib` issue `#5946` and pull request `#6609`?

<!-- RESPONSE_START -->

## Status: Complete internally, not yet published on GitHub

The authoritative Work State is **`WS-05: Contrib Modules`** (`work-states/WS-05-contrib.md`, Owner: Damien Mathieu, Status `in_progress`, Last Updated 2026-03-08). This work is task **`T001`**, mapped to issue `#5946` / PR `#6609`.

**Current state — `T001` is marked done (`[x]`), with publication pending:**
- The adopted fix is **automatic `MultipartForm.RemoveAll()`** in the otelgin middleware — not the "reattach" alternative, and not leaving cleanup to users.
- Conflict resolution and tests for `#6609` are **complete locally**.
- **Final commits have not been pushed**, so on GitHub issue `#5946` remains **open** and PR `#6609` remains **open/unmerged**.
- The one open follow-up under "Next Update Needed" is: publication of the completed `#6609` work and a GitHub issue update.

**Provenance for the state change:** `CMT-2026-03-002` (`work-states/comments/2026-03.md`), authored as a human correction effective 2026-03: Tyler and the commenter settled over DM that otelgin will call `MultipartForm.RemoveAll()` automatically; the work is treated as done, but nothing was pushed or posted to GitHub. This Comment is its own evidence — no supporting `SRC-*` record confirms it. It superseded the earlier stale Work State entry, which had `T001` open with the cleanup option unresolved.

## Background from Sources

**Issue `#5946`** (`SRC-ISSUE-01`) — "Using otelgin.Middleware will cause temporary MultipartForm files not to be destroyed", opened 2024-07-25 by `zacklpx`. Labels: `bug`, `area: instrumentation`, `instrumentation: otelgin`. State in the frozen Sources: **open**, last updated 2025-07-03. Root cause: otelgin replaces the request via `c.Request = c.Request.WithContext(ctx)`, so the original request held by the HTTP server never gets the lazily-initialized `MultipartForm`, and its automatic `RemoveAll()` on request completion never cleans up the temp files. Timeline includes a cross-reference from `#4588` (2024-11-21), the cross-reference from PR `#6609` (2025-01-13), and a **`marked_as_duplicate` event by `dmathieu` on 2025-07-02**.

**PR `#6609`** (`SRC-PR-01`) — "fix(otelgin): remove multipartform temporary file", by `Yiling-J`, opened 2025-01-13, branch `fix/gin_multipartform` → `main`, +95/-0 across 3 files, no labels or milestone. State: **open**, last updated 2025-11-13. Codecov reported 75% patch coverage (3 lines missing) and the head was 731 commits behind main.

**Design debate captured in the PR (28 review comments, 15 discussion comments):**
- `dmathieu` proposed `Clone(ctx)` instead of `WithContext(ctx)`; `Yiling-J` explained a deep clone doesn't help because `MultipartForm` is lazily initialized and is `nil` at middleware time. He linked golang/go#58809 and labstack/echo#2413, and noted otelmux and otelecho likely share the bug.
- `Yiling-J` initially preferred the less-aggressive "reattach" approach (2025-01-27), and said he could get no guidance from the Go team; he characterized it as a Go design problem around implicit `WithContext`/`ParseMultipartForm` behavior.
- The known trade-off with `RemoveAll`: if outer middleware calls `ParseMultipartForm` again, resources get recreated, causing extra memory allocation.
- On 2025-11-10 `akats7` said "we're good to resolve the conflicts and close this out"; `Yiling-J` resolved conflicts and added upstream/downstream middleware test cases. The SIG position was to defer configurability until users explicitly request it.
- As of 2025-11-11/12 the thread was **still unsettled**: `flc1125` objected that files should remain retrievable and offered a competing prototype, **PR `#8161`**; `akats7` replied twice that he couldn't identify the incorrect behavior being cited and that cloning the request doesn't address the core issue; `Yiling-J` said he thought `RemoveAll` had already been agreed and asked whether its implications were confirmed in the SIG meeting. The `CMT-2026-03-002` DM decision is what resolved this.

**SIG meeting note `SRC-NOTE-04`** (2025-10-16 meeting, attendees Tyler Yahn, Damien Mathieu, Bryan Boreham, David Ashpole, Robert Pająk): Damien raised the multipart-form cleanup problem, describing it as historical, surfacing in otelgin but potentially affecting virtually all HTTP-related middleware, and referenced both `#5946` and `#6609`.

## Caveat

The Sources are frozen (collected 2026-07-14, as-of 2026-02-27). The "done" designation rests solely on the human Comment `CMT-2026-03-002`, which explicitly records that nothing was pushed. So if you check GitHub, both `#5946` and `#6609` should be expected to still show as open — that is consistent with, not contradictory to, the Work State.

**Records cited:** `work-states/WS-05-contrib.md` (`WS-05/T001`); `work-states/comments/2026-03.md` (`CMT-2026-03-002`); `opentelemetry/issues/opentelemetry-go-contrib-5946.md` (`SRC-ISSUE-01`); `opentelemetry/pulls/opentelemetry-go-contrib-6609.md` (`SRC-PR-01`); `opentelemetry/meeting-notes/entry-3479584781.md` (`SRC-NOTE-04`).
