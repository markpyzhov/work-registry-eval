# What is the status of the otelgin MultipartForm temporary-file cleanup work tracked by `opentelemetry-go-contrib` issue `#5946` and pull request `#6609`?

<!-- RESPONSE_START -->

I have enough evidence to answer.

## Status: internally done, publicly unpublished

**Authoritative state** (`work-states/WS-05-contrib.md`, task `T001`, Last Updated 2026-03-08, owner Damien Mathieu, WS-05 overall `in_progress`, P0):

- `T001` (mapped to `#5946` / PR `#6609`) is marked **done (checked)**: automatic `MultipartForm.RemoveAll()` is the adopted approach, and conflict resolution plus tests are **complete locally**.
- **Publication is pending.** Final commits have not been pushed, so on GitHub issue `#5946` remains **open** and PR `#6609` remains **open / unmerged**.
- Next update needed: publication of the completed `#6609` work and the GitHub issue update.

## Decision history and provenance

**Design decision** — the earlier unresolved three-way choice (automatic `RemoveAll()` vs. reattach-to-original-request vs. leaving cleanup to users) is **superseded**; automatic `MultipartForm.RemoveAll()` is adopted. `(SRC-PR-01, SRC-NOTE-04, CMT-2026-03-002)`

**Root cause** (from the PR discussion and the 2025-10-16 SIG note): otelgin does `c.Request = c.Request.WithContext(ctx)`, creating a new request. Go's `net/http` calls `MultipartForm.RemoveAll()` on the *original* request at `finishRequest`, but the lazily-initialized `MultipartForm` ends up on the *new* request, so nothing cleans it up. `dmathieu`'s suggested `Request.Clone(ctx)` does not fix it (deep copy copies the form; at middleware time the field is still nil). Damien noted this is historical and potentially affects virtually all HTTP middleware, not just otelgin. `(SRC-PR-01, SRC-NOTE-04)`

**Chronology:**
- 2024-07-25 — issue `#5946` opened by `zacklpx`; labels bug / area: instrumentation / instrumentation: otelgin. `(SRC-ISSUE-01)`
- 2025-01-13 — PR `#6609` opened by `Yiling-J` (branch `fix/gin_multipartform` → `main`, +95/−0 across 3 files, no labels/milestone). Long review by `flc1125`, `dmathieu`, `akats7`. `(SRC-PR-01)`
- 2025-01-22 — cross-referenced to `golang/go#71382`; Yiling-J reported getting no guidance from the Go team and briefly favored the reattach approach.
- 2025-07-02 — `#5946` **marked as duplicate** by `dmathieu`. `(SRC-ISSUE-01)`
- 2025-10-16 SIG (published 2025-11-03) — Damien proposed starting with automatic deletion, adding a config option only if strong demand appears; Tyler Yahn agreed instrumentation owns cleanup. `(SRC-NOTE-04)`
- 2025-11-10 — `akats7`: "we're good to resolve the conflicts and close this out"; Yiling-J resolved conflicts and reported otelgin tests passing, then added upstream/downstream middleware test cases at `flc1125`'s request. `(SRC-PR-01)`
- 2025-11-11/12 — residual disagreement: `flc1125` filed a prototype alternative, PR `#8161`, and questioned the `require.ErrorIs(t, err, fs.ErrNotExist)` expectation; `akats7` responded the prototype's request-cloning doesn't address the core `WithContext` problem. PR last updated 2025-11-13. `(SRC-PR-01)`
- 2026-03-08 — `CMT-2026-03-002` (Damien Mathieu): he and Tyler settled over DM on automatic `RemoveAll()`; work finished offline and treated as done, but final commits not pushed and `#5946` / `#6609` not updated on GitHub. This comment is its own evidence — no supporting source record.

## Known trade-offs left open

Configurability is deliberately deferred until users explicitly request it. Acknowledged side effect: in a chain like `m1(m2(otel-middleware(m3(fn))))`, if `m1`/`m2` call `ParseMultipartForm` after the otel middleware's `RemoveAll()`, they may re-create `MultipartForm` resources and incur extra allocations. `(SRC-ISSUE-01, SRC-PR-01, SRC-NOTE-04)`

**Records used:** `work-states/WS-05-contrib.md` (path `work-state`); `work-states/comments/2026-03.md` → `CMT-2026-03-002` (path `comments`); `opentelemetry/issues/opentelemetry-go-contrib-5946.md` (`SRC-ISSUE-01`), `opentelemetry/pulls/opentelemetry-go-contrib-6609.md` (`SRC-PR-01`), `opentelemetry/meeting-notes/entry-3479584781.md` (`SRC-NOTE-04`) (path `sources`).
