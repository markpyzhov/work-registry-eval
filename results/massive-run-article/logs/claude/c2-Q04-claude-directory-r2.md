# What is the status of the otelgin MultipartForm temporary-file cleanup work tracked by `opentelemetry-go-contrib` issue `#5946` and pull request `#6609`?

<!-- RESPONSE_START -->

I have everything needed.

## Status: work is complete internally, but not yet published to GitHub

**Bottom line (as of the authoritative Work State, last updated 2026-03-08):** The otelgin MultipartForm temporary-file cleanup task (`T001`) is **done internally but unpublished**. Automatic `MultipartForm.RemoveAll()` is the adopted approach, conflict resolution and tests are complete locally, but the final commits have not been pushed — so issue `#5946` and PR `#6609` both remain **open/unmerged on GitHub**.

Source: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md` (lines 29, 38, 46, 52), corroborated by the registry index at `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md`.

### The problem
`otelgin.Middleware` replaces the request via `c.Request = c.Request.WithContext(ctx)`. Because `MultipartForm` is lazily initialized, it lands on the *new* request while the HTTP server still holds the original — so `net/http`'s end-of-request cleanup finds `MultipartForm == nil` and never deletes the `multipart-*` temp files. Filed 2024-07-25 by `zacklpx` against otelgin 0.53.0; labeled `bug`, `area: instrumentation`, `instrumentation: otelgin`. `flc1125` demonstrated the same failure with plain `http.Server`, meaning it affects essentially all `*http.Request`-based middleware, and escalated it to the Go team as `golang/go#74455` without an official resolution.
Source: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/issues/opentelemetry-go-contrib-5946.md`

### The decision path
Three options were weighed — `RemoveAll()`, reattach the form to the original request, and leaving cleanup to users. The Go SIG discussed it on 2025-10-16 (Damien Mathieu, Tyler Yahn, Bryan Boreham, David Ashpole, Robert Pająk): start with automatic deletion, no config option until users ask for one, and let component owners decide. Tyler confirmed the instrumentation owns the cleanup responsibility.
Source: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3479584781.md`

The earlier contest between `RemoveAll()`, reattach, and user cleanup is **superseded** — automatic `RemoveAll()` is settled.

### PR #6609 history
Opened 2025-01-13 by `Yiling-J` (+95/-0 across 3 files, branch `fix/gin_multipartform`). Long review debate: `dmathieu` proposed `Clone()` and pre-parsing the form; `Yiling-J` favored reattach for a stretch; `akats7` floated a configurable Option, then withdrew it in favor of waiting for explicit user demand. `akats7` **approved on 2025-11-10**. `Yiling-J` resolved conflicts and expanded tests with upstream and downstream middlewares on 2025-11-10. Last activity in Sources: `flc1125` questioning a test expectation (files unreadable after `RemoveAll`) and floating an alternative prototype in PR `#8161` on 2025-11-11; `akats7` pushed back on 2025-11-12, saying cloning does not fix the core issue.
Source: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-contrib-6609.md`

### What closed it out
A correction from Damien Mathieu, effective 2026-03-08: he and Tyler settled over DM that otelgin will call `MultipartForm.RemoveAll()` automatically — not reattach, not user cleanup. He finished conflict resolution and tests for `#6609` locally and treats the work as done, but has not pushed the final commits or updated `#5946`/`#6609` on GitHub. This comment is its own only evidence — no supporting `SRC-*` record.
Source: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/comments/2026-03.md` (`CMT-2026-03-002`)

### Known side effect
With `RemoveAll()` in the otel middleware, an outer middleware chain like `m1(m2(otel-middleware(m3(fn))))` where `m1`/`m2` also call `ParseMultipartForm` may re-create form resources, causing extra memory allocations. No better solution was identified.

### Next update needed
Publication of the completed `#6609` work and the corresponding GitHub issue update. Note the Sources were collected 2026-07-14 and still show both records as open — but per the registry's convention, the Work State (dated 2026-03-08) is the authoritative status and the GitHub state simply reflects the unpushed publication.
