**Source ID**: [SRC-PR-01]

# Pull Request: fix(otelgin): remove multipartform temporary file (open-telemetry/opentelemetry-go-contrib#6609)

**Canonical URL**: https://github.com/open-telemetry/opentelemetry-go-contrib/pull/6609  
**Author**: Yiling-J  
**Created**: 2025-01-13T13:45:43Z · **Updated**: 2025-11-13T01:26:12Z  
**Collected**: 2026-07-14T14:35:41Z  
**State**: open  
**Branch**: `fix/gin_multipartform` → `main`  
**Changes**: +95 / -0 across 3 files  
**Labels**: —  
**Milestone**: —

---

## Description

Fix #5946 

## Discussion (15)

**linux-foundation-easycla[bot]** — 2025-01-13T13:45:52Z

<a href="https://easycla.lfx.linuxfoundation.org/#/?version=2"><img src="https://s3.amazonaws.com/cla-project-logo-prod/cla-signed.svg?v=2" alt="CLA Signed" align="left" height="28" width="328" ></a><br/><br />The committers listed above are authorized under a signed CLA.<ul><li>:white_check_mark: login: Yiling-J / name: Yiling-J  (b432f868ba452eb7a928e0b655fd1a2652b86ceb)</li></ul>

---

**codecov[bot]** — 2025-01-13T14:15:46Z

## [Codecov](https://app.codecov.io/gh/open-telemetry/opentelemetry-go-contrib/pull/6609?dropdown=coverage&src=pr&el=h1&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry) Report
Attention: Patch coverage is `75.00000%` with `3 lines` in your changes missing coverage. Please review.
> Project coverage is 68.6%. Comparing base [(`9640704`)](https://app.codecov.io/gh/open-telemetry/opentelemetry-go-contrib/commit/96407041d21127e91171493abffd457dcc24815d?dropdown=coverage&el=desc&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry) to head [(`65ce788`)](https://app.codecov.io/gh/open-telemetry/opentelemetry-go-contrib/commit/65ce788198c015ebbab7dda62837781e16f8ea1f?dropdown=coverage&el=desc&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry).
> Report is 731 commits behind head on main.

| [Files with missing lines](https://app.codecov.io/gh/open-telemetry/opentelemetry-go-contrib/pull/6609?dropdown=coverage&src=pr&el=tree&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry) | Patch % | Lines |
|---|---|---|
| [...ation/github.com/gin-gonic/gin/otelgin/gintrace.go](https://app.codecov.io/gh/open-telemetry/opentelemetry-go-contrib/pull/6609?src=pr&el=tree&filepath=instrumentation%2Fgithub.com%2Fgin-gonic%2Fgin%2Fotelgin%2Fgintrace.go&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry#diff-aW5zdHJ1bWVudGF0aW9uL2dpdGh1Yi5jb20vZ2luLWdvbmljL2dpbi9vdGVsZ2luL2dpbnRyYWNlLmdv) | 75.0% | [2 Missing and 1 partial :warning: ](https://app.codecov.io/gh/open-telemetry/opentelemetry-go-contrib/pull/6609?src=pr&el=tree&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry) |

<details><summary>Additional details and impacted files</summary>


[![Impacted file tree graph](https://app.codecov.io/gh/open-telemetry/opentelemetry-go-contrib/pull/6609/graphs/tree.svg?width=650&height=150&src=pr&token=P6F3W9WA7Q&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry)](https://app.codecov.io/gh/open-telemetry/opentelemetry-go-contrib/pull/6609?src=pr&el=tree&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry)

```diff
@@           Coverage Diff           @@
##            main   #6609     +/-   ##
=======================================
+ Coverage   68.5%   68.6%   +0.1%     
=======================================
  Files        200     200             
  Lines      16781   16882    +101     
=======================================
+ Hits       11500   11589     +89     
- Misses      4935    4943      +8     
- Partials     346     350      +4     
```

| [Files with missing lines](https://app.codecov.io/gh/open-telemetry/opentelemetry-go-contrib/pull/6609?dropdown=coverage&src=pr&el=tree&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry) | Coverage Δ | |
|---|---|---|
| [...ation/github.com/gin-gonic/gin/otelgin/gintrace.go](https://app.codecov.io/gh/open-telemetry/opentelemetry-go-contrib/pull/6609?src=pr&el=tree&filepath=instrumentation%2Fgithub.com%2Fgin-gonic%2Fgin%2Fotelgin%2Fgintrace.go&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry#diff-aW5zdHJ1bWVudGF0aW9uL2dpdGh1Yi5jb20vZ2luLWdvbmljL2dpbi9vdGVsZ2luL2dpbnRyYWNlLmdv) | `87.8% <75.0%> (-2.1%)` | :arrow_down: |

... and [2 files with indirect coverage changes](https://app.codecov.io/gh/open-telemetry/opentelemetry-go-contrib/pull/6609/indirect-changes?src=pr&el=tree-more&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry)

</details>
<details><summary> :rocket: New features to boost your workflow: </summary>

- :snowflake: [Test Analytics](https://docs.codecov.com/docs/test-analytics): Detect flaky tests, report on failures, and find test suite problems.
</details>

---

**flc1125** — 2025-01-13T16:19:36Z

I have written 2 examples to facilitate the analysis of this issue.

I believe that gin falls into the first category, so I think the main logic of the modifications in this PR should be fine.

> Here I am using a `URL` to simulate the behavior of `MultipartForm`, and I believe their logic should be consistent.

---

- The first example:

```go
package gin

import (
	"context"
	"net/http"
	"net/url"
	"testing"

	"github.com/stretchr/testify/assert"
)

type handler func(t *testing.T, req *http.Request)

var test1Handler handler = func(t *testing.T, req *http.Request) {
	t.Logf("req1.0: %p, req.URL: %p", req, req.URL)
}

var test2Handler handler = func(t *testing.T, req *http.Request) {
	t.Logf("req2.0: %p, req.URL: %p", req, req.URL)

	saveCtx := req.Context()
	defer func() {
		t.Logf("req2.3: %p, req.URL: %p", req, req.URL)
		req = req.WithContext(saveCtx)
		t.Logf("req2.4: %p, req.URL: %p", req, req.URL)
	}()

	defer func() {
		t.Logf("req2.1: %p, req.URL: %p", req, req.URL)
		req.URL = &url.URL{
			Scheme: "https",
		}
		t.Logf("req2.2: %p, req.URL: %p", req, req.URL)
	}()

	req = req.WithContext(context.WithValue(req.Context(), "key", "value"))
}

var test3Handler handler = func(t *testing.T, req *http.Request) {
	t.Logf("req3.0: %p, req.URL: %p", req, req.URL)
	t.Logf("req3.1: %v", req.Context().Value("key"))
}

func TestIssue_Middleware(t *testing.T) {
	req, err := http.NewRequest("POST", "/upload", nil)
	assert.NoError(t, err)
	req.URL = &url.URL{
		Scheme: "http",
	}

	t.Logf("req0.0: %p, req.URL: %p", req, req.URL)

	handlers := []handler{
		test1Handler,
		test2Handler,
		test3Handler,
	}
	for _, h := range handlers {
		h(t, req)
	}
}
```

output:

```
=== RUN   TestIssue_Middleware
    issue_test.go:51: req0.0: 0x1400049ba40, req.URL: 0x1400016ca20
    issue_test.go:15: req1.0: 0x1400049ba40, req.URL: 0x1400016ca20
    issue_test.go:19: req2.0: 0x1400049ba40, req.URL: 0x1400016ca20
    issue_test.go:29: req2.1: 0x1400049bb80, req.URL: 0x1400016ca20
    issue_test.go:33: req2.2: 0x1400049bb80, req.URL: 0x1400016cab0
    issue_test.go:23: req2.3: 0x1400049bb80, req.URL: 0x1400016cab0
    issue_test.go:25: req2.4: 0x1400049bcc0, req.URL: 0x1400016cab0
    issue_test.go:40: req3.0: 0x1400049ba40, req.URL: 0x1400016ca20
    issue_test.go:41: req3.1: <nil>
--- PASS: TestIssue_Middleware (0.00s)
```

- The secend example:

```go
package gin

import (
	"context"
	"net/http"
	"net/url"
	"testing"

	"github.com/stretchr/testify/assert"
)

type handler func(t *testing.T, req *http.Request) *http.Request

var test1Handler handler = func(t *testing.T, req *http.Request) *http.Request {
	t.Logf("req1.0: %p, req.URL: %p", req, req.URL)
	return req
}

var test2Handler handler = func(t *testing.T, req *http.Request) *http.Request {
	t.Logf("req2.0: %p, req.URL: %p", req, req.URL)

	saveCtx := req.Context()
	defer func() {
		t.Logf("req2.3: %p, req.URL: %p", req, req.URL)
		req = req.WithContext(saveCtx)
		t.Logf("req2.4: %p, req.URL: %p", req, req.URL)
	}()

	defer func() {
		t.Logf("req2.1: %p, req.URL: %p", req, req.URL)
		req.URL = &url.URL{
			Scheme: "https",
		}
		t.Logf("req2.2: %p, req.URL: %p", req, req.URL)
	}()

	req = req.WithContext(context.WithValue(req.Context(), "key", "value"))

	return req
}

var test3Handler handler = func(t *testing.T, req *http.Request) *http.Request {
	t.Logf("req3.0: %p, req.URL: %p", req, req.URL)
	t.Logf("req3.1: %v", req.Context().Value("key"))
	return req
}

func TestIssue_Middleware(t *testing.T) {
	req, err := http.NewRequest("POST", "/upload", nil)
	assert.NoError(t, err)
	req.URL = &url.URL{
		Scheme: "http",
	}

	t.Logf("req0.0: %p, req.URL: %p", req, req.URL)

	handlers := []handler{
		test1Handler,
		test2Handler,
		test3Handler,
	}
	for _, h := range handlers {
		req = h(t, req)
	}
}
```

output:

```
=== RUN   TestIssue_Middleware
    issue_test.go:55: req0.0: 0x140001b6500, req.URL: 0x14000130360
    issue_test.go:15: req1.0: 0x140001b6500, req.URL: 0x14000130360
    issue_test.go:20: req2.0: 0x140001b6500, req.URL: 0x14000130360
    issue_test.go:30: req2.1: 0x140001b6640, req.URL: 0x14000130360
    issue_test.go:34: req2.2: 0x140001b6640, req.URL: 0x140001303f0
    issue_test.go:24: req2.3: 0x140001b6640, req.URL: 0x140001303f0
    issue_test.go:26: req2.4: 0x140001b6780, req.URL: 0x140001303f0
    issue_test.go:43: req3.0: 0x140001b6640, req.URL: 0x140001303f0
    issue_test.go:44: req3.1: value
--- PASS: TestIssue_Middleware (0.00s)
PASS
```

---

**Yiling-J** — 2025-01-14T15:29:23Z

I skipped the failed test on the Windows platform. This is consistent with how Go handles form cleanup tests (https://github.com/golang/go/blob/6da16013ba4444e0d71540f68279f0283a92d05d/src/net/http/serve_test.go#L7028), so I think it’s fine.

---

**flc1125** — 2025-11-03T13:01:49Z

@Yiling-J Hi, are you still willing to handle this issue?

According to the SIG discussion, it is recommended that middleware remove temporary resources.

cc @akats7 

---

**Yiling-J** — 2025-11-03T15:41:21Z

> are you still willing to handle this issue

@flc1125 Yes. But first, let’s reach an agreement on how we should fix it. As I proposed a while ago, I prefer the reattach approach: “copy the cloned `Request.MultipartForm` value back to the original request before returning,” as mentioned in https://github.com/golang/go/issues/74455#issuecomment-3099652232.

We should also decide whether to fix this in otelgin only, or to review other middlewares and address the issue there as well if it exists.

---

**flc1125** — 2025-11-04T00:35:28Z

> let’s reach an agreement on how we should fix it

We tend to only need to add the following on the basis of the original main branch:

```go
c.Request.MultipartForm.RemoveAll()
```

> We should also decide whether to fix this in otelgin only, or to review other middlewares and address the issue there as well if it exists.

In fact, all middleware based on `*http.Request` has issues whenever a situation like `c.Request.WithContext(c.Request.Context())` occurs, so other components also need to be fixed.

However, for this current PR, we only need to fix otelgin to keep the PR as minimal as possible. For other middleware, if you are interested, you can also submit fixes in the form of minimal PRs for individual components.


---

**Yiling-J** — 2025-11-04T01:19:00Z

@flc1125 `RemoveAll()` works for me. I think my original PR already aligns well with the goal, it looks like I just need to resolve the conflicts and make sure the tests pass. Let me confirm agin that we’re all in agreement on this approach. @dmathieu @akats7


---

**akats7** — 2025-11-10T01:45:42Z

Sorry just got caught up on this thread. My only concern with RemoveAll is on the off chance that a middleware further up the chain still expect access to the form data. 

What about making it configurable with an Option, with the default behavior being to clean it up. That way the user can have more control over which middleware cleans up the form data.

I don't want to stall this issue further but just a thought.

cc. @flc1125 @dmathieu  

---

**flc1125** — 2025-11-10T01:53:34Z

> Sorry just got caught up on this thread. My only concern with RemoveAll is on the off chance that a middleware further up the chain still expect access to the form data.

Agree.

> What about making it configurable with an Option, with the default behavior being to clean it up. That way the user can have more control over which middleware cleans up the form data.

I would lean towards the solution proposed by the SIG: only support configurability when users explicitly request it. After all, enabling configurability after `RemoveAll()` is an operation that ensures both extensibility compatibility and backward compatibility.

@akats7 @dmathieu 

---

**akats7** — 2025-11-10T02:01:52Z

Ah gotcha, didn't see that that was mentioned. I'm good on holding off until it's explicitly requested.

---

**akats7** — 2025-11-10T04:27:26Z

@Yiling-J I think we're good to resolve the conflicts and close this out, thanks!

---

**Yiling-J** — 2025-11-10T11:58:48Z

I’ve resolved the conflicts, and the otelgin package tests passed on my machine @flc1125 @dmathieu @akats7 

---

**flc1125** — 2025-11-10T14:02:53Z

Could you add the corresponding unit tests for this scenario?

> My only concern with RemoveAll is on the off chance that a middleware further up the chain still expect access to the form data.

---

**Yiling-J** — 2025-11-10T15:21:14Z

> Could you add the corresponding unit tests for this scenario?
> 
> > My only concern with RemoveAll is on the off chance that a middleware further up the chain still expect access to the form data.

I’ve added more details to the test case, it now includes two extra middlewares, one upstream and one downstream, to demonstrate what happens when `RemoveAll` is called in the otel middleware. The behavior is correct to me, but let’s confirm that we all agree it’s the expected one.

## Reviews (25)

**flc1125** — COMMENTED — 2025-01-13T15:02:41Z

**Yiling-J** — COMMENTED — 2025-01-13T15:27:41Z

**Yiling-J** — COMMENTED — 2025-01-13T15:31:16Z

**Yiling-J** — COMMENTED — 2025-01-13T15:35:45Z

**flc1125** — COMMENTED — 2025-01-13T16:20:13Z

**dmathieu** — COMMENTED — 2025-01-14T08:21:37Z

**Yiling-J** — COMMENTED — 2025-01-14T14:39:53Z

**dmathieu** — COMMENTED — 2025-01-14T14:55:45Z

**Yiling-J** — COMMENTED — 2025-01-14T15:31:10Z

**dmathieu** — COMMENTED — 2025-01-14T16:18:27Z

**akats7** — COMMENTED — 2025-01-14T17:44:13Z

**akats7** — COMMENTED — 2025-01-14T17:49:48Z

**dmathieu** — COMMENTED — 2025-01-14T17:50:46Z

**akats7** — COMMENTED — 2025-01-19T18:17:46Z

**Yiling-J** — COMMENTED — 2025-01-20T01:52:04Z

**Yiling-J** — COMMENTED — 2025-01-27T12:14:50Z

**flc1125** — COMMENTED — 2025-11-10T14:02:13Z

**flc1125** — COMMENTED — 2025-11-10T14:03:40Z

**flc1125** — COMMENTED — 2025-11-10T14:03:54Z

**akats7** — APPROVED — 2025-11-10T16:20:02Z

**flc1125** — COMMENTED — 2025-11-11T13:20:30Z

**flc1125** — COMMENTED — 2025-11-11T13:59:33Z

**akats7** — COMMENTED — 2025-11-11T15:42:57Z

**Yiling-J** — COMMENTED — 2025-11-12T01:28:14Z

**akats7** — COMMENTED — 2025-11-12T10:24:52Z

## Review Comments (28)

**flc1125** on `instrumentation/github.com/gin-gonic/gin/otelgin/test/gintrace_test.go` — 2025-01-13T14:56:36Z

I believe the content of `ff` can be detected here.

**flc1125** on `instrumentation/github.com/gin-gonic/gin/otelgin/test/gintrace_test.go` — 2025-01-13T14:59:10Z

assert.NoError?

**flc1125** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 117) — 2025-01-13T15:02:32Z

I'm wondering, if there's another middleware layer outside this one, would it be removed because of this?

**Yiling-J** on `instrumentation/github.com/gin-gonic/gin/otelgin/test/gintrace_test.go` — 2025-01-13T15:27:41Z

The goal of the test is to ensure that temporary files are automatically removed, not to test multipart file parsing. The sole purpose of using `c.FormFile` is to trigger multipart parsing, which creates temporary files. I added a `fileHeader.Open()` test in this function to confirm that the temporary file is available. However, I think checking the value of `ff` is unnecessary.

**Yiling-J** on `instrumentation/github.com/gin-gonic/gin/otelgin/test/gintrace_test.go` — 2025-01-13T15:31:16Z

I prefer using `require.NoError` because it ensures that no additional information distracts me when a test has already failed. I also searched the codebase and seems that both `require` and `assert` are used, and `require.NoError` appears more.

**Yiling-J** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 117) — 2025-01-13T15:35:44Z

It's hard to say, but in all cases, regardless of how many middlewares are chained, temporary files should be removed. I didn't check the return error of `RemoveAll` here, which aligns with the behavior in both Go's [`http` package](https://github.com/golang/go/blob/44a6f817ea0fbeb3ba4aa398794c4e80dba13b1e/src/net/http/server.go#L1727) and [echo-contrib](https://github.com/labstack/echo-contrib/pull/90). I believe each middleware should independently attempt to remove temporary files.

**flc1125** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 117) — 2025-01-13T16:20:13Z

see: https://github.com/open-telemetry/opentelemetry-go-contrib/pull/6609#issuecomment-2587572600

**dmathieu** on `instrumentation/github.com/gin-gonic/gin/otelgin/gintrace.go` — 2025-01-14T08:12:17Z

Rather than ignoring an error here, how about passing it to the otel error handler?

```suggestion
				err := c.Request.MultipartForm.RemoveAll()
				if err != nil {
					otel.Handle(err)
				}
```

**dmathieu** on `instrumentation/github.com/gin-gonic/gin/otelgin/test/gintrace_test.go` — 2025-01-14T08:13:50Z

I think what @flc1125 meant here is that you don't necessarily need to use `AbortWithError` (which also can return an error but ignores it), but instead call `require.NoError` here.

```suggestion
		require.NoError(err)
```

**dmathieu** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 109) — 2025-01-14T08:21:31Z

Wouldn't we be fixing this rather more easily with the following:

```suggestion
		c.Request = c.Request.Clone(ctx)
```

[WithContext](https://pkg.go.dev/net/http#Request.WithContext) performs a shallow clone, and therefore doesn't clone the multipart form.
However, [Clone](https://pkg.go.dev/net/http#Request.Clone) performs a deep copy, and makes an explicit clone of [MultipartForm](https://cs.opensource.google/go/go/+/refs/tags/go1.23.4:src/net/http/request.go;l=406).

**Yiling-J** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 109) — 2025-01-14T14:39:53Z

The problem here is, go http request will call MultipartForm.RemoveAll() automatically when request finishes. However, the otelgin middleware creates a new request, and temporary files will be stored in this new request's MultipartForm field. Unfortunately, no one is calling MultipartForm.RemoveAll() on this new request.

A deep clone wouldn’t resolve the problem because the MultipartForm is also copied. A shallow clone might seem like it should work since the MultipartForm field is shared, but it doesn’t. This is because the MultipartForm field is lazily initialized—it’s only assigned a value when you [parse the form](https://github.com/golang/go/blob/6da16013ba4444e0d71540f68279f0283a92d05d/src/net/http/request.go#L1403). As a result, in the middleware, the field is nil.

Related issues: https://github.com/golang/go/issues/58809, https://github.com/labstack/echo/issues/2413

I think other OpenTelemetry middlewares, such as otelmux and otelehco, might also have the same issue.

**dmathieu** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 109) — 2025-01-14T14:55:45Z

What if we parse the form before making the new request?
Wouldn't we share the object then?

**Yiling-J** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 109) — 2025-01-14T15:31:10Z

I think this approach could work, but it feels a bit unusual to enforce form parsing in the middleware.

**dmathieu** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 109) — 2025-01-14T16:18:27Z

Having to force remove multipart files is a bit unusual too.

**akats7** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 109) — 2025-01-14T17:44:13Z

I'm probably more in favor of doing the initialization on the original request as well, explicitly handling clean up logic does seem a bit strange

**akats7** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 109) — 2025-01-14T17:49:47Z

@dmathieu maybe we should discuss this in the SIG since it might have implications in the other instrumentation modules

**dmathieu** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 109) — 2025-01-14T17:50:46Z

I won't be able to attend this week's meeting (it's the week where it's late for EU). But yes, feel free to bring it there.

**akats7** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 109) — 2025-01-19T18:17:34Z

@Yiling-J what are you thoughts on parsing the form in the middleware, the more I think about it, the more that seems to be the better approach, for example what about certain edge cases where down the chain middlewares might want to access the files

**Yiling-J** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 109) — 2025-01-20T01:52:04Z

@akats7 Another option is to save `c.Request` to a variable before calling `c.Request.WithContext(ctx)`. Then, in the defer function, if `c.Request.MultipartForm != nil`, we can reattach the `MultipartForm` to the original request. This way, there won’t be any automatic removing or parsing. If other middlewares handle the form correctly, this approach should work. 
In [http/server.go](https://github.com/golang/go/blob/40b3c0e58a0ae8dec4684a009bf3806769e0fc41/src/net/http/server.go#L2102), the `ServeHTTP` method is called first, which invokes the Gin handlers/middlewares, and then `finishRequest` is called, which removes the temporary files.

I haven’t tested yet, but I think it should work. However, I’m considering opening an issue in Go to get their suggestions. Since it’s closely related to the `http` package and the `WithContext` method is widely used by middlewares and frameworks, I think they might be able to suggest best practice for this situation.

**Yiling-J** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 109) — 2025-01-27T12:14:50Z

@akats7 It seems I can’t get any help from the Go team. I’m not in favor of parsing the form in the middleware, as this step should be explicitly done by the user. Parsing large forms can consume resources, and the `ParseMultipartForm` function has a `maxMemory` parameter that should also be decided by the user.

After giving this more thought over the past few days, I believe this is more of a Go design issue. The `WithContext` and `ParseMultipartForm` behavior is implicit, hard to notice, poorly documented, and lacks a clear best practice solution. I think the reattach approach might be better because it’s less aggressive and can likely be safely applied to other OpenTelemetry middlewares facing the same issue. The only downside, compared to `RemoveAll`, is that it relies on other middlewares to also handle `WithContext` and `ParseMultipartForm` correctly. If all middlewares do the right thing, `net/http` should eventually clean up the temporary files automatically.

**flc1125** on `CHANGELOG.md` — 2025-11-10T14:01:14Z

```suggestion
- Fix issue in `go.opentelemetry.io/contrib/instrumentation/github.com/gin-gonic/gin/otelgin` middleware where temporary files for multipart/form-data were not being removed. (#6609)
```

**flc1125** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 109) — 2025-11-10T14:03:40Z

Close to reduce distractions.

**flc1125** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 117) — 2025-11-10T14:03:54Z

Close to reduce distractions.

**flc1125** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin_test.go` (line 512) — 2025-11-11T13:20:30Z

I don’t think this is the expected result; in any case—whether it’s middleware or something else—it should be able to retrieve the file again.

I think we may need to investigate this issue further.

**flc1125** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin_test.go` (line 512) — 2025-11-11T13:59:33Z

Based on this PR, I’ve provided a prototype reference: https://github.com/open-telemetry/opentelemetry-go-contrib/pull/8161

@dmathieu @akats7, take a look and see how it works if we adjust it according to the prototype.

**akats7** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin_test.go` (line 512) — 2025-11-11T15:42:57Z

@flc1125 can you clarify which behavior you’re referring to as incorrect, are you referring to 

```
require.ErrorIs(t, err, fs.ErrNotExist)
```

**Yiling-J** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin_test.go` (line 512) — 2025-11-12T01:28:14Z

I thought we had already agreed on the `RemoveAll` approach? Naturally, if you call RemoveAll, the temporary files are deleted and can’t be accessed afterward. Since this happens during the middleware’s return phase, I’d expect that most middlewares wouldn’t read the multipart form at that point anyway. I’m not sure if the implications of RemoveAll were discussed in the SIG meeting, but it might be worth confirming.

**akats7** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin_test.go` (line 512) — 2025-11-12T10:24:52Z

@flc1125 I’m still not clear on the result you’re referring to, the result aligns to my understanding of what we’ve discussed.

Also I’m not sure if your prototype fix would work, I think it still doesn’t address the core issue which is that when we originally set c.Request = c.Request.WithContext(ctx) with an unparsed form the http server won’t know to clean it up. I don’t think Cloning the request solves that.

## Timeline

- 2025-01-13T13:45:44Z · **review_requested** by Yiling-J
- 2025-01-13T13:45:57Z · **review_requested** by github-actions[bot]
- 2025-01-22T15:54:04Z · **cross-referenced** by Yiling-J ← https://github.com/golang/go/issues/71382
- 2025-07-03T13:24:53Z · **cross-referenced** by flc1125 ← https://github.com/open-telemetry/opentelemetry-go-contrib/issues/5946
- 2025-11-03T09:18:09Z · **cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/issues/6648
- 2025-11-11T14:00:20Z · **cross-referenced** by flc1125 ← https://github.com/open-telemetry/opentelemetry-go-contrib/pull/8161

