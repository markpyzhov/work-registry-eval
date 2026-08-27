# What is the status of the otelgin MultipartForm temporary-file cleanup work tracked by `opentelemetry-go-contrib` issue `#5946` and pull request `#6609`?

<!-- RESPONSE_START -->

## Status summary (as of the dataset snapshot, collected 2026-07-14)

**Both the issue and the PR are still open — the fix has not landed.**

### Issue #5946 — "Using otelgin.Middleware will cause temporary MultipartForm files not to be destroyed"
- Author zacklpx, opened 2024-07-25, **State: open**, last updated 2025-07-03. Labels: `bug`, `area: instrumentation`, `instrumentation: otelgin`. No milestone.
- Root cause: otelgin replaces the request via `c.Request = c.Request.WithContext(ctx)`. Because `MultipartForm` is lazily initialized (nil at middleware time), the parsed form ends up on the *new* request, while `net/http`'s `finishRequest` calls `RemoveAll()` on the *original* one — so nothing cleans up the `multipart-*` temp files.
- Timeline notes: cross-referenced from #4588 (2024-11-21) and from PR #6609 (2025-01-13); **marked as duplicate by dmathieu on 2025-07-02** (the issue nonetheless remains in `open` state in the record).
- flc1125 confirmed the problem is not Gin-specific — it affects any `http.Server` middleware doing `WithContext` before `ParseMultipartForm` — and filed golang/go#74455 upstream, which got no official Go-team answer. On 2025-07-03 he concluded the project needs its own workaround and endorsed PR #6609's approach (also favored by zihuyishi and akats7).

### PR #6609 — "fix(otelgin): remove multipartform temporary file" (Yiling-J)
- Opened 2025-01-13, **State: open**, branch `fix/gin_multipartform` → `main`, **+95 / −0 across 3 files**, no labels/milestone. Last updated 2025-11-13. Codecov: patch coverage 75% (3 lines uncovered); the branch was ~731 commits behind main at that report.
- Approach debated at length in early 2025: `Request.Clone` (dmathieu) was rejected as ineffective; parsing the form inside the middleware (akats7) was rejected by the author as the user's decision (`maxMemory`); Yiling-J initially preferred a "reattach the MultipartForm to the original request" approach.
- **Resolution of the design question:** discussed at the OpenTelemetry Go SIG on 2025-10-16 (notes posted 2025-11-03). Damien Mathieu presented it as affecting virtually all HTTP middleware; options weighed were `RemoveAll()`, leaving it to users, or a configurable option. The SIG direction: **default to automatic removal, add configurability only if users explicitly ask**, and let component owners decide. Tyler Yahn agreed the instrumentation is responsible for cleanup.
- Post-SIG (Nov 2025): flc1125 and Yiling-J converged on plain `c.Request.MultipartForm.RemoveAll()`, scoped to otelgin only to keep the PR minimal (other middlewares to be fixed in separate minimal PRs). akats7 raised the "upstream middleware may still need the form" concern, then agreed to hold off on an Option. Yiling-J resolved merge conflicts on 2025-11-10 and added a test with one upstream and one downstream middleware. **akats7 APPROVED on 2025-11-10T16:20:02Z.**
- **Why it is still not merged:** flc1125 reopened the behavioral question on 2025-11-11, arguing the test result (`require.ErrorIs(t, err, fs.ErrNotExist)` — file gone for other middleware) is not the expected outcome, and offered an alternative prototype, **PR #8161**. akats7 (2025-11-11 and 2025-11-12) asked for clarification and said he doubts the prototype works, since cloning the request still does not make the HTTP server aware of the unparsed form. Yiling-J (2025-11-12) noted `RemoveAll` deleting the files is the natural consequence of the already-agreed approach and suggested confirming the SIG's view. The thread ends there — **the disagreement between flc1125 and akats7/Yiling-J over the expected post-cleanup behavior is the open blocker**, despite the existing approval.

### Related context in the same dataset
- PR #8014 (nicksherron, otelgin context save/restore data race, issue #4588) is **closed**; it touched the same `savedCtx`/`WithContext` code region and was discussed at the same 2025-10-16 SIG meeting.
- A CHANGELOG entry was suggested by flc1125 for #6609: fix for otelgin where multipart/form-data temporary files were not removed.

### Sources cited
- `opentelemetry/issues/opentelemetry-go-contrib-5946.md` [SRC-ISSUE-01]
- `opentelemetry/pulls/opentelemetry-go-contrib-6609.md` [SRC-PR-01]
- `opentelemetry/meeting-notes/entry-3479584781.md` [SRC-NOTE-04] (Go SIG 2025-10-16, published 2025-11-03)
- `opentelemetry/pulls/opentelemetry-go-contrib-8014.md` [SRC-PR-07] (related otelgin data-race PR)

Note: PR #8161 is referenced only inside #6609's review thread; the dataset contains no source record for #8161 itself, so its own state is unknown.
