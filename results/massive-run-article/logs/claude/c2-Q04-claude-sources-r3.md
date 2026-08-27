# What is the status of the otelgin MultipartForm temporary-file cleanup work tracked by `opentelemetry-go-contrib` issue `#5946` and pull request `#6609`?

<!-- RESPONSE_START -->

## Status: both still open and unresolved as of the dataset snapshot (collected 2026‑07‑14)

**Issue #5946** — "Using otelgin.Middleware will cause temporary MultipartForm files not to be destroyed" (author zacklpx, opened 2024‑07‑25)
- **State: open**, labels `bug`, `area: instrumentation`, `instrumentation: otelgin`, no milestone. Issue body last updated 2025‑07‑03.
- Timeline shows it was **marked as duplicate by dmathieu on 2025‑07‑02** (cross-referenced to #7541), and cross-referenced repeatedly: #4588 (flc1125, 2024‑11), PR #6609 (2025‑01), golang/go#74455 (2025‑07), opentelemetry-go#6648 (2025‑11), #8419 (MrAlias, 2026‑01‑16), PR #8851 (SAY‑5, 2026‑04‑21), referenced again by SAY‑5 2026‑05‑31. Despite the duplicate marking, the record still reads `State: open`.

**PR #6609** — "fix(otelgin): remove multipartform temporary file" (author Yiling‑J, opened 2025‑01‑13, branch `fix/gin_multipartform` → `main`)
- **State: open / not merged**, +95/−0 across 3 files, no labels, no milestone, last updated 2025‑11‑13T01:26:12Z. Description is just "Fix #5946".
- **Approved by akats7 on 2025‑11‑10T16:20:02Z**, but review discussion reopened afterward and it was never merged.
- CI/coverage: Codecov patch coverage 75% (3 lines missing); `otelgin/gintrace.go` 87.8% `<75.0%>` (−2.1%); the report notes it is **731 commits behind head on main**.

### Root cause (agreed by participants)
otelgin does `c.Request = c.Request.WithContext(ctx)`. The `MultipartForm` field is lazily initialized, so at middleware time it is nil; when the handler later parses the form, the temp files land on the *new* request, while `net/http`'s `finishRequest` only calls `RemoveAll()` on the *original* request it holds. flc1125 demonstrated with a framework-free `http.Server` repro that this happens for any middleware doing `WithContext` before `ParseMultipartForm`, so it is not gin-specific. `Request.Clone` was proposed by dmathieu and rejected by Yiling‑J (deep copy copies the form; shallow shares a nil field).

### Decision history
1. Jan 2025: options debated — `RemoveAll()` in a defer, deep `Clone`, parsing the form inside the middleware, or "reattach" the `MultipartForm` back to the original request. akats7 asked to take it to the SIG; Yiling‑J also filed golang/go#71382 and got no guidance from the Go team, and came to prefer the reattach approach. PR then stalled ~9 months.
2. Jul 2025: zihuyishi/akats7/flc1125 converged on the defer + `RemoveAll()` workaround since golang/go#74455 produced no official solution.
3. Nov 2025: flc1125 reported the SIG recommends middleware remove temporary resources; Yiling‑J accepted `RemoveAll()`, resolved conflicts (2025‑11‑10), and added tests with an upstream and a downstream middleware. akats7 raised making it configurable via an `Option` (default = clean up); flc1125 said the SIG preferred only adding configurability if users explicitly ask, and akats7 agreed to hold off. akats7 approved.
4. **Where it stopped (11–13 Nov 2025):** flc1125 objected to the test's `require.ErrorIs(t, err, fs.ErrNotExist)` behavior — arguing a middleware should still be able to retrieve the file — and posted a competing prototype, **PR #8161** (clone-the-request approach). Yiling‑J pushed back ("I thought we had already agreed on the `RemoveAll` approach"), and akats7 said he could not tell which result flc1125 considered wrong and doubted #8161 would work, since cloning still doesn't make the http server aware of the unparsed form. **No resolution of that disagreement appears after 2025‑11‑12**, and the PR remains open.

### Also of note
- A related otelgin PR, **#8014** ("remove unneeded context save/restore to avoid data race", nicksherron), which touched the same `savedCtx`/`WithContext` code and referenced the 2-year-old data-race issue #4588, was **closed by dmathieu on 2025‑10‑17**.
- flc1125 stated the fix should stay scoped to otelgin for minimality, but that other `*http.Request`-based middlewares (otelmux, otelecho) have the same defect and need their own minimal PRs. No such PRs are recorded in this dataset.

### Sources
- `opentelemetry/issues/opentelemetry-go-contrib-5946.md` [SRC-ISSUE-01]
- `opentelemetry/pulls/opentelemetry-go-contrib-6609.md` [SRC-PR-01]
- `opentelemetry/pulls/opentelemetry-go-contrib-8014.md` [SRC-PR-07] (related otelgin context save/restore PR)

Caveat: the dataset contains no records for PR #8161, issue #8419, or PR #8851, so their content and any post‑2025‑11‑13 outcome cannot be confirmed from these sources.
