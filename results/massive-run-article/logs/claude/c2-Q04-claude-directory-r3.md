# What is the status of the otelgin MultipartForm temporary-file cleanup work tracked by `opentelemetry-go-contrib` issue `#5946` and pull request `#6609`?

<!-- RESPONSE_START -->

Status of the otelgin MultipartForm temporary-file cleanup (`opentelemetry-go-contrib#5946` / PR `#6609`):

## Current status (authoritative)
Per the Work State `WS-05` (`T001`), the work is **done internally but not published**: the fix approach is settled, conflict resolution and tests are complete locally, but final commits have not been pushed, so issue `#5946` and PR `#6609` remain **open / unmerged on GitHub**. `T001` is checked off in the task list, with "publication follow-up" listed as active work.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md` (lines 29, 38, 46, 52, 62)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md` (WS-05 overall: `in_progress`)

## Adopted approach
Automatic `MultipartForm.RemoveAll()` in the otelgin middleware — not the "reattach" alternative, and not leaving cleanup to users. This supersedes the earlier unresolved three-way choice (RemoveAll / reattach / user cleanup). Damien Mathieu and Tyler Yahn settled this over DM, effective 2026-03-08.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/comments/2026-03.md` (`CMT-2026-03-002`, lines 21-28) — evidence is that comment only; no supporting `SRC-*`, and the GitHub post is still outstanding.

## Underlying problem
`otelgin.Middleware` does `c.Request = c.Request.WithContext(ctx)`, a shallow clone. Because `MultipartForm` is lazily initialized, the parsed form lands on the *new* request while the original request the HTTP server holds still has `MultipartForm == nil` — so `net/http`'s end-of-request cleanup never fires and `multipart-*` temp files leak.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/issues/opentelemetry-go-contrib-5946.md` (opened 2024-07-25 by `zacklpx`; labels: bug, area: instrumentation, instrumentation: otelgin; no milestone; state `open`)

## History / chronology
- 2025-01-13 — `Yiling-J` opens PR `#6609` (`fix/gin_multipartform`, +95/-0 across 3 files), fixing `#5946`.
- Jan 2025 — long review debate: `dmathieu` proposes `Request.Clone` or parsing the form in the middleware; `Yiling-J` argues for the reattach approach and calls it a Go design issue; `akats7` suggests taking it to the SIG. PR stalls.
- 2025-07-02/03 — `flc1125` reproduces the leak with plain `http.Server`, files `golang/go#74455`, gets no official Go fix, and recommends proceeding with `#6609`; notes a side effect (upstream middleware that re-parses the form may reallocate).
- 2025-10-16 SIG meeting (published 2025-11-03) — Damien raises it; options weighed (RemoveAll / user responsibility / configurable option); consensus to start with automatic removal, add configuration only on demonstrated user need. Tyler agrees instrumentation owns cleanup.
- 2025-11-03/04 — `flc1125` revives the PR; `Yiling-J` accepts `RemoveAll()`.
- 2025-11-10 — `akats7` raises a concern about outer middleware still needing form data, then agrees to defer configurability; **approves the PR**. `Yiling-J` resolves conflicts and adds tests with an upstream and downstream middleware.
- 2025-11-11/12 — `flc1125` disputes the test expectation (`require.ErrorIs(t, err, fs.ErrNotExist)`) and posts an alternative prototype, PR `#8161`; `akats7` and `Yiling-J` push back, saying the result matches the agreed `RemoveAll` semantics. PR last updated 2025-11-13.
- Sources: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-contrib-6609.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/issues/opentelemetry-go-contrib-5946.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3479584781.md`

## People
Reporter `zacklpx`; PR author `Yiling-J`; code owner/approver `akats7`; main driver `flc1125`; SIG/maintainer input `dmathieu` (Damien Mathieu, WS-05 owner) and Tyler Yahn.

## What's outstanding
Publication of the completed `#6609` work — push the final commits and update `#5946` / `#6609` on GitHub. Not established anywhere in this package: a merge event, a release containing the fix, resolution of the `#8161` prototype disagreement, or whether sibling middlewares (otelmux, otelecho, etc., which have the same defect) get parallel fixes.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md` (Next Update Needed, line 62)

One caveat worth flagging: the "complete locally" status rests entirely on `CMT-2026-03-002`, which self-describes as having no supporting source record — the public GitHub state in this package still shows both the issue and the PR open as of the 2026-07-14 collection date.
