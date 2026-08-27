# What is the status of the otelgin MultipartForm temporary-file cleanup work tracked by `opentelemetry-go-contrib` issue `#5946` and pull request `#6609`?

<!-- RESPONSE_START -->

**Status: done internally, not yet published — issue `#5946` and PR `#6609` are still open/unmerged on GitHub.**

## Current state (authoritative)

Per the Work State `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md` (task `T001`, last updated 2026-03-08) and the index `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md`:

- The adopted fix is **automatic `MultipartForm.RemoveAll()`** in the otelgin middleware — not the reattach approach, and not leaving cleanup to users.
- Conflict resolution and tests are **complete locally**; the work is treated as done internally (`T001` is checked off).
- **Final commits have not been pushed**, so both `#5946` and PR `#6609` remain open/unmerged on GitHub. This is the one outstanding action: publication plus a GitHub status update.

The correction that established this is `CMT-2026-03-002` (author: Damien Mathieu, effective 2026-03-08) in `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/comments/2026-03.md`: he and Tyler settled the `RemoveAll()` decision over DM, finished the work locally, and had not yet pushed or updated the GitHub records. That comment is self-evidencing — there is no `SRC-*` backing it, which is why the public GitHub artifacts still show "open".

## Background and how the decision was reached

**The bug** (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/issues/opentelemetry-go-contrib-5946.md`, opened 2024-07-25 by `zacklpx`, labels: bug / area: instrumentation / instrumentation: otelgin; collected state `open`): `otelgin.Middleware` does `c.Request = c.Request.WithContext(ctx)`, so a later `c.FormFile` parses the form onto the *new* request. The original request the HTTP server holds still has a nil `MultipartForm`, so `net/http`'s end-of-request cleanup finds nothing to remove and `multipart-*` temp files leak. `flc1125` demonstrated this is not gin-specific — it reproduces on any bare `http.Server` handler that calls `WithContext` before `ParseMultipartForm` — and filed `golang/go#74455` upstream, which produced no official Go-team answer.

**The PR** (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-contrib-6609.md`, "fix(otelgin): remove multipartform temporary file", author `Yiling-J`, opened 2025-01-13, +95/-0 across 3 files, state `open`, last updated 2025-11-13): options debated were `RemoveAll()`, deep `Clone()`, parsing the form inside the middleware, and reattaching the form to the original request. `Yiling-J` initially preferred reattach; `dmathieu` and `akats7` pushed on clone/parse variants. `akats7` **approved** the PR on 2025-11-10. `flc1125` then objected on 2025-11-11 that the test showing files unreadable afterward (`require.ErrorIs(t, err, fs.ErrNotExist)`) was not the expected result and floated a prototype, PR `#8161`; `akats7` replied on 2025-11-12 that the result matched the agreed behavior and that cloning would not address the root cause. That thread is the last recorded PR activity.

**The SIG decision** (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3479584781.md`, Go SIG 2025-10-16): Damien proposed starting with automatic deletion and no configuration option, adding one only if strong user demand appeared; Tyler agreed instrumentation is responsible for cleanup. On the PR, `akats7` had floated a config Option but agreed on 2025-11-10 to hold off until explicitly requested.

## Known caveats

- Side effect flagged by `flc1125` on the issue: with middleware nested as `m1(m2(otel-middleware(m3(fn))))`, where outer layers also parse the form, `RemoveAll()` in the otel middleware can cause them to re-create `MultipartForm` resources and incur extra allocations. No better solution was identified.
- The same defect affects other `*http.Request`-based middleware (otelmux, otelecho, etc.). The team scoped `#6609` to otelgin only, to keep it minimal.

## Next update needed

Publication of the completed `#6609` work and the corresponding GitHub update to `#5946` (`WS-05-contrib.md`, "Next Update Needed").
