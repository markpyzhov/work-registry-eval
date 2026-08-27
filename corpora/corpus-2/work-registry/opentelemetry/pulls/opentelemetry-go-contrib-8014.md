**Source ID**: [SRC-PR-07]

# Pull Request: otelgin: remove unneeded context save/restore to avoid data race (open-telemetry/opentelemetry-go-contrib#8014)

**Canonical URL**: https://github.com/open-telemetry/opentelemetry-go-contrib/pull/8014  
**Author**: nicksherron  
**Created**: 2025-10-14T04:01:24Z · **Updated**: 2025-10-17T10:42:07Z  
**Collected**: 2026-07-14T14:35:41Z  
**State**: closed  
**Branch**: `fix/otelgin-data-race` → `main`  
**Changes**: +83 / -10 across 2 files  
**Labels**: —  
**Milestone**: —

---

## Description

There seems to be absolutely no reason to save and restore the request context in a deferred function. The way it was done before could (and did) lead to a race condition because when c.Next() is called, the request context could be changed by another goroutine, and then the deferred function would modify the request while another goroutine is using it. 

I can't for the life of me figure out what benefit the previous code was trying to achieve, other than maybe trying to minimize the context size in memory, but that seems unnecessary and not worth the risk of a data race. Furthermore, I'm not even sure that said memory savings would pay off because when running `go build -gcflags="-m"` against the current implementation you can see that context and request escapes to heap:
```
./gin.go:84:37: "nil context" escapes to heap
./gin.go:84:37: new(http.Request) escapes to heap
```
This is likely negligible but I figured I'd add it for more context, no pun intended 😉

Perhaps the goal was not that of performance/memory savings but instead to "restore" the context. If so, this is also incorrect because in Gin, there's no need to restore the context - each request gets its own *gin.Context .

Finally, this change actually more closely matches the [code cited](https://github.com/DataDog/dd-trace-go/blob/8fb554ff7cf694267f9077ae35e27ce4689ed8b6/contrib/gin-gonic/gin/gintrace.go) as the "inspiration" for the otelgin package. 

Without this change, we unfortunately cannot run our tests with the race detector enabled and is not production ready due to not being goroutine safe.

## Discussion (27)

**linux-foundation-easycla[bot]** — 2025-10-14T04:01:31Z

<a href="https://easycla.lfx.linuxfoundation.org/#/?version=2"><img src="https://s3.amazonaws.com/cla-project-logo-prod/cla-signed.svg?v=2" alt="CLA Signed" align="left" height="28" width="328" ></a><br/><br />The committers listed above are authorized under a signed CLA.<ul><li>:white_check_mark: login: nicksherron / name: Nick Sherron  (43d6c1b5f0c27c73a83543d0f681e2dc766d86dc, 6c560fe0a618c400f5961126b3daf71074a98113, ebe29b975966edee33e7c0e2fdcca7c89710fd63)</li></ul>

---

**flc1125** — 2025-10-14T04:35:20Z

The current changes do not guarantee thread safety.

Additionally, I lean towards the view that for infrastructure-level components or frameworks, there is no need to consider the concurrency safety of `req.WithContext` and `req.Context()`.

Once these components introduce certain mechanisms for concurrency safety, it may lead to performance degradation.

For users pursuing high performance, such performance degradation is unacceptable. Moreover, once implemented, users have no choice but to use these mechanisms.

Therefore, I prefer to leave the decision of whether to ensure concurrency safety to the users themselves, and let them implement these mechanisms on their own.

---

**nicksherron** — 2025-10-14T04:43:31Z

Just found an open 2 year old issue this would fix #4588 

---

**nicksherron** — 2025-10-14T04:56:41Z

Thanks for the quick response @flc1125 , but I would like to offer a rebuttal. 

## This PR Fixes an Existing Bug, Not Introducing New Safety Mechanisms

I respectfully disagree with the characterization that this PR "introduces mechanisms for concurrency safety." The opposite is true: this PR removes problematic code that causes a data race.

The current code has a real, reproducible race condition reported in issue #4588 (open for 2 years). The race detector fails consistently. This is not theoretical—it violates Go's memory model.

## The Defer Provides No Benefit

Let's analyze what the current code does:
```go
  savedCtx := c.Request.Context()
  defer func() {
      c.Request = c.Request.WithContext(savedCtx)  // ← Restores AFTER request completes
  }()
  ctx := cfg.Propagators.Extract(savedCtx, propagation.HeaderCarrier(c.Request.Header))
  // ...
  c.Request = c.Request.WithContext(ctx)  // ← Sets new context
  c.Next()  // ← Processes request
  // When we return, defer runs and "restores" the old context
```
  Question: Why restore the context after the request is complete?

  - After c.Next() returns, the request has been fully processed
  - Gin doesn't reuse *gin.Context instances across requests
  - Downstream handlers may spawn goroutines that read c.Request.Context()
  - The deferred write to c.Request races with those goroutine reads
  - There is no code that benefits from this restoration

## The Performance Argument is Backwards

The current code with the defer is slower than the fix:

  Current code overhead:
  - Allocates closure for defer
  - Saves context reference
  - Executes deferred function on return
  - Calls WithContext() twice (once to set, once to "restore")

  Fixed code:
  - No defer
  - No closure allocation
  - One fewer WithContext() call
  - No unnecessary context copy

 Benchmark comparison (removing defer should show improvement):
  -  Current: ~3 allocations per request
  -  Fixed:   ~2 allocations per request

## Users Cannot Fix This Themselves

 This is middleware code that users cannot work around without forking the library. The race happens inside otelgin.Middleware(). A user who wants to use otelgin AND pass race detection has no choice but to:

  1. Fork this library
  2. Apply this exact fix
  3. Maintain their fork indefinitely

  This is not "leaving the decision to users"—it's forcing users to fork or live with failing race detection.

## Precedent: This Project Has Fixed Similar Races Before

  From the git history:
  - #4577: "otelgrpc: Fix data race in stats handlers" (merged)
  - #881: "otelsarama: Fix WrapAsyncProducer race condition" (merged)

  These fixes were accepted because data races are bugs, not "concurrency mechanisms left to users."

## The Race Is Real and Reproducible

  From issue #4588:
  WARNING: DATA RACE
  Write at 0x... by goroutine X:
    [defer in Middleware]
  Read at 0x... by goroutine Y:
    [user handler accessing context]

  This is undefined behavior. The Go memory model states: "Programs that modify data being simultaneously accessed by multiple goroutines must serialize such access."

## The Fix is Correct

  The fix simply removes dead code:
```go
  // Before: Save and restore (unnecessary)
  savedCtx := c.Request.Context()
  defer func() { c.Request = c.Request.WithContext(savedCtx) }()
  ctx := cfg.Propagators.Extract(savedCtx, ...)

  // After: Use context directly (correct)
  reqCtx := c.Request.Context()
  ctx := cfg.Propagators.Extract(reqCtx, ...)
```
  The behavior is identical except:
  -  No race condition
  -  Better performance
  -  Simpler code
  -  Tests pass with -race

  Conclusion

  This is a straightforward bug fix that:
  1. Removes unnecessary code that causes a race
  2. Improves performance (fewer allocations, no defer overhead)
  3. Fixes a 2-year-old issue (#4588)
  4. Follows precedent from previous race fixes in this project
  5. Enables CI to enforce race-free code

  There is no downside to this change, and significant benefits. I respectfully request approval to merge.


---

**akats7** — 2025-10-14T04:58:07Z

Hi @nicksherron, 

It's a fair question, I also don't really see the benefit of it, I'm going to assume it was added for hygiene to avoid leaking the modifications out of the intended request's middleware chain.

@flc1125 what are your thoughts, even if it doesn't provide thread safety it does seem valid

---

**flc1125** — 2025-10-14T05:01:16Z

> I'm going to assume it was added for hygiene to avoid leaking the modifications out of the intended request's middleware chain.

I agree with this situation.

---

**nicksherron** — 2025-10-14T05:06:09Z

I'm confused about this "doesn't provide thread safety" claim. I'm starring at a test failure due to data race when running `go test -race`  in one of my projects that clearly points the finger to the code I removed as being the culprit. When I do a `go mod -replace` using my change in this PR the race goes away. 


---

**flc1125** — 2025-10-14T05:09:52Z

> I'm confused about this "doesn't provide thread safety" claim. I'm starring at a test failure due to data race when running `go test -race` in one of my projects that clearly points the finger to the code I removed as being the culprit. When I do a `go mod -replace` using my change in this PR the race goes away.

I'm not quite sure about your specific case, so this is for reference only: Since `*http.Request` is often passed to subsequent logic, if there are concurrent modifications to it, it can lead to thread safety issues.

---

**akats7** — 2025-10-14T05:13:28Z

> > I'm confused about this "doesn't provide thread safety" claim. I'm starring at a test failure due to data race when running `go test -race` in one of my projects that clearly points the finger to the code I removed as being the culprit. When I do a `go mod -replace` using my change in this PR the race goes away.
> 
> I'm not quite sure about your specific case, so this is for reference only: Since `*http.Request` is often passed to subsequent logic, if there are concurrent modifications to it, it can lead to thread safety issues.

 That’s essentially what’s happening here, this would be an example of subsequent logic that’s creating a data race. We can’t guarantee that others middleware’s won’t do something similar but I think this is a valid fix.

---

**nicksherron** — 2025-10-14T05:13:48Z

  The "hygiene to avoid leaking modifications" argument is backwards. The defer causes the race, it doesn't prevent leaking:

  1. There's nothing to leak - Gin doesn't reuse *gin.Context across requests. Each request gets a fresh context.
  2. The defer IS the race - When a handler spawns a goroutine that reads c.Request.Context(), the defer writes to c.Request while that goroutine reads from it. That's the data race.
  3. Proof:
  ```go
  router.POST("/test", func(c *gin.Context) {
      ctx := c.Request.Context()
      go func() {
          time.Sleep(1ms)
          _ = ctx.Value("key")  // READ
      }()
      c.JSON(200, "ok")
      // defer runs here and WRITES to c.Request ← RACE!
  })
  ```

The "concurrent modifications" concern is the problem we're fixing - The defer itself is the concurrent modification! It writes to c.Request after the handler returns while background goroutines may still be using it.


---

**nicksherron** — 2025-10-14T05:19:18Z

 Here's a test you can run to test this for yourself. It proves the current implementation is the culprit for data races.

https://gist.github.com/nicksherron/08dfbc599e0de0532cd4dc0d30f9f4a4 (moved to a gist to save the thread from a giant comment)

By the way I'm really blown away by your quick responses. I never see this kind of quick back and forth on a new PR in other oss projects. I'm really impressed and it's much appreciated. 

---

**nicksherron** — 2025-10-14T05:23:38Z

I can also provide a benchmark to prove the performance impact is actually net positive if you'd like @flc1125 

---

**flc1125** — 2025-10-14T06:05:25Z

> https://gist.github.com/nicksherron/08dfbc599e0de0532cd4dc0d30f9f4a4

<details>
<summary>This is a minimal case to examine the issue of data races:</summary>

```go
package otelgin

import (
	"context"
	"net/http/httptest"
	"sync"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
)

func TestConcurrency(t *testing.T) {
	t.Run("no defer", func(t *testing.T) {
		runConcurrency(t, noDeferMiddleware())
	})

	t.Run("have defer", func(t *testing.T) {
		runConcurrency(t, haveDeferMiddleware())
	})

	t.Run("no middleware", func(t *testing.T) {
		runConcurrency(t, nil)
	})
}

func runConcurrency(t *testing.T, middleware gin.HandlerFunc) {
	router := gin.New()
	if middleware != nil {
		router.Use(middleware)
	}
	router.POST("/test", func(c *gin.Context) {
		go func() {
			_ = c.Request.Context()
		}()
		c.String(200, "ok")
	})

	wg := sync.WaitGroup{}
	for i := 0; i < 1000; i++ {
		wg.Go(func() {
			req := httptest.NewRequest("POST", "/test", nil)
			w := httptest.NewRecorder()
			router.ServeHTTP(w, req)

			assert.Equal(t, 200, w.Code)
		})
	}
	wg.Wait()
}

func noDeferMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Request.WithContext(
			context.WithValue(c.Request.Context(), "key1", "value1"),
		)
		c.Next()
	}
}

func haveDeferMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		origCtx := c.Request.Context()
		defer func() {
			c.Request = c.Request.WithContext(origCtx)
		}()
		c.Request.WithContext(
			context.WithValue(origCtx, "key1", "value1"),
		)
		c.Next()
	}
}
```
</details>



Whether `defer` is present or not, data races have always existed. My understanding of this is that the reason lies in the fact that `*http.Request` itself cannot guarantee thread safety, and this applies to any framework, including the native one as well.

Therefore, I'm not quite clear about what issue you are trying to verify.

[As mentioned before](https://github.com/open-telemetry/opentelemetry-go-contrib/issues/4588#issuecomment-2490995125), I was wondering what this piece of code is intended to handle—it doesn't seem to serve any purpose and appears to be removable.

```go
defer func() {
	c.Request = c.Request.WithContext(savedCtx)
}()
```


---

**nicksherron** — 2025-10-14T06:52:09Z

> Whether `defer` is present or not, data races have always existed. My understanding of this is that the reason lies in the fact that `*http.Request` itself cannot guarantee thread safety, and this applies to any framework, including the native one as well.
> 
> Therefore, I'm not quite clear about what issue you are trying to verify.
> 
> [As mentioned before](https://github.com/open-telemetry/opentelemetry-go-contrib/issues/4588#issuecomment-2490995125), I was wondering what this piece of code is intended to handle—it doesn't seem to serve any purpose and appears to be removable.
> 
> ```go
> defer func() {
> 	c.Request = c.Request.WithContext(savedCtx)
> }()
> ```

I feel like we're talking in circles a little here and I don't know if I can explain it any better, but I'll try. 
I'm not claiming this change will make `*http.Request` impervious to data races. The disconnect seems to be thinking we're adding concurrency safety. **We're removing the code that breaks it**. 
I think there's a misunderstanding about when the defer runs. Let me clarify:

Timeline with OLD code (defer pattern):
```go
func Middleware() {
    savedCtx := c.Request.Context()
    defer func() {
        c.Request = c.Request.WithContext(savedCtx)  // ← Step 5: WRITE
    }()

    c.Request = c.Request.WithContext(ctx)  // Step 1
    c.Next()                                 // Step 2: All handlers/middleware run
    // Step 3: Handler spawned goroutine that reads c.Request.Context()
    // Step 4: Handler returns
    // Step 5: defer runs and WRITES to c.Request
    // Step 6: Background goroutine READS c.Request ← **RACE**!
}
```

The defer IS the concurrent modification. It writes to c.Request after handlers complete, while
background goroutines spawned by those handlers may still be reading it.

The fix removes this write:
```go
func Middleware() {
    reqCtx := c.Request.Context()
    ctx := cfg.Propagators.Extract(reqCtx, ...)

    c.Request = c.Request.WithContext(ctx)  // Step 1: Set once
    c.Next()                                 // Step 2: Handlers run
    // Step 3: Handler spawns goroutine
    // Step 4: Handler returns
    // Step 5: No defer, no write ← NO RACE
}
```
Proof: TestMiddleware_MinimalRaceRepro demonstrates exactly this:
- Handler spawns goroutine that accesses c.Request.Context()
- Handler returns
- Old code: defer writes → DATA RACE
- Fixed code: no write → PASS

Furthermore this isn't my "specific case" - this is how Go middleware is supposed to work. The defer breaks standard Go patterns that every Go developer uses.


Go's own documentation recommends this pattern

From https://pkg.go.dev/context:

>   "Incoming requests to a server should create a Context, and outgoing calls to servers should accept a Context. The chain of function calls between them must propagate the Context,
>   optionally replacing it with a derived Context..."
> 

Passing c.Request.Context() to goroutines is the recommended approach for:
  - Timeouts
  - Cancellation
  - Tracing (which is what otelgin does!)

Other popular Gin middleware use this exact pattern!

Example using an extremely common pattern in production:
```go

 func main() {
      router := gin.New()

      // Setup OpenTelemetry tracing (standard pattern)
      router.Use(otelgin.Middleware("my-service"))

      // Add async logging middleware (also standard pattern)
      router.Use(asyncLoggingMiddleware())

      router.POST("/api/orders", createOrder)
      router.Run(":8080")
  }

  // Async logging middleware - BREAKS with otelgin's defer pattern
  func asyncLoggingMiddleware() gin.HandlerFunc {
      logger := zap.NewProduction()

      return func(c *gin.Context) {
          start := time.Now()
          path := c.Request.URL.Path
          method := c.Request.Method

          // Process request
          c.Next()

          // Log asynchronously to avoid blocking response
          // This is THE standard pattern for production logging
          go func(ctx context.Context, statusCode int, duration time.Duration) {
              // Extract trace context for correlation
              span := trace.SpanFromContext(ctx)
              traceID := span.SpanContext().TraceID().String()
              spanID := span.SpanContext().SpanID().String()

              // Write structured log with trace correlation
              logger.Info("http_request",
                  zap.String("method", method),
                  zap.String("path", path),
                  zap.Int("status", statusCode),
                  zap.Duration("duration", duration),
                  zap.String("trace_id", traceID),    // ← Links logs to traces
                  zap.String("span_id", spanID),
              )

              // Could also send to external logging service here
              // sendToDatadog(ctx, logEntry)
              // sendToCloudWatch(ctx, logEntry)
          }(c.Request.Context(), c.Writer.Status(), time.Since(start))
          //  ^^^^^^^^^^^^^^^^^^^^
          //  THIS RACES WITH otelgin's defer!
      }
  }

  func createOrder(c *gin.Context) {
      var order Order
      if err := c.BindJSON(&order); err != nil {
          c.JSON(400, gin.H{"error": err.Error()})
          return
      }

      // Process order...
      c.JSON(201, order)
  }

  ```


---

**nicksherron** — 2025-10-14T06:58:23Z

Hopefully that provides enough evidence to support my claim which is that **the spurious defer code is prone to data races when used in a project with typical gin server patterns** and this PR fixes it.

---

**dmathieu** — 2025-10-14T07:26:23Z

Could you turn your gist into a test that can run on CI, and add it to this PR?

---

**nicksherron** — 2025-10-14T07:27:58Z

> Could you turn your gist into a test that can run on CI, and add it to this PR?

Sure, I'd be happy to.

---

**flc1125** — 2025-10-14T07:42:26Z

> ```go
> }(c.Request.Context(), c.Writer.Status(), time.Since(start))
>           //  ^^^^^^^^^^^^^^^^^^^^
>           //  THIS RACES WITH otelgin's defer!
> ```

I believe my understanding aligns with yours. I approve this PR and agree with the changes.

I'd like to clarify that the primary value isn't about "fixing data race". Rather, it removes unnecessary code that has unintended side effects.

e.g., The defer restoration discards any context modifications made within the `otelgin` middleware chain (including downstream handlers).

---

**nicksherron** — 2025-10-14T07:47:23Z

> > ```go
> > }(c.Request.Context(), c.Writer.Status(), time.Since(start))
> >           //  ^^^^^^^^^^^^^^^^^^^^
> >           //  THIS RACES WITH otelgin's defer!
> > ```
> 
> I believe my understanding aligns with yours. I approve this PR and agree with the changes.
> 
> I'd like to clarify that the primary value isn't about "fixing data race". Rather, it removes unnecessary code that has unintended side effects.
> 
> e.g., The defer restoration discards any context modifications made within the `otelgin` middleware chain (including downstream handlers).

Sounds good, thank you for your time on this. I also added the test @dmathieu requested. If you want me to make any changes to it just let me know.

---

**codecov[bot]** — 2025-10-14T07:50:11Z

## [Codecov](https://app.codecov.io/gh/open-telemetry/opentelemetry-go-contrib/pull/8014?dropdown=coverage&src=pr&el=h1&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry) Report
:white_check_mark: All modified and coverable lines are covered by tests.
:white_check_mark: Project coverage is 78.6%. Comparing base ([`bf97050`](https://app.codecov.io/gh/open-telemetry/opentelemetry-go-contrib/commit/bf9705049e4b884480c156a704acbdb6bfad9167?dropdown=coverage&el=desc&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry)) to head ([`6c560fe`](https://app.codecov.io/gh/open-telemetry/opentelemetry-go-contrib/commit/6c560fe0a618c400f5961126b3daf71074a98113?dropdown=coverage&el=desc&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry)).
:warning: Report is 10 commits behind head on main.

<details><summary>Additional details and impacted files</summary>



[![Impacted file tree graph](https://app.codecov.io/gh/open-telemetry/opentelemetry-go-contrib/pull/8014/graphs/tree.svg?width=650&height=150&src=pr&token=P6F3W9WA7Q&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry)](https://app.codecov.io/gh/open-telemetry/opentelemetry-go-contrib/pull/8014?src=pr&el=tree&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry)

```diff
@@          Coverage Diff          @@
##            main   #8014   +/-   ##
=====================================
  Coverage   78.5%   78.6%           
=====================================
  Files        185     185           
  Lines      14760   14754    -6     
=====================================
+ Hits       11598   11605    +7     
+ Misses      2808    2795   -13     
  Partials     354     354           
```

| [Files with missing lines](https://app.codecov.io/gh/open-telemetry/opentelemetry-go-contrib/pull/8014?dropdown=coverage&src=pr&el=tree&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry) | Coverage Δ | |
|---|---|---|
| [...umentation/github.com/gin-gonic/gin/otelgin/gin.go](https://app.codecov.io/gh/open-telemetry/opentelemetry-go-contrib/pull/8014?src=pr&el=tree&filepath=instrumentation%2Fgithub.com%2Fgin-gonic%2Fgin%2Fotelgin%2Fgin.go&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry#diff-aW5zdHJ1bWVudGF0aW9uL2dpdGh1Yi5jb20vZ2luLWdvbmljL2dpbi9vdGVsZ2luL2dpbi5nbw==) | `92.9% <100.0%> (-0.4%)` | :arrow_down: |

... and [1 file with indirect coverage changes](https://app.codecov.io/gh/open-telemetry/opentelemetry-go-contrib/pull/8014/indirect-changes?src=pr&el=tree-more&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry)
</details>
<details><summary> :rocket: New features to boost your workflow: </summary>

- :snowflake: [Test Analytics](https://docs.codecov.com/docs/test-analytics): Detect flaky tests, report on failures, and find test suite problems.
</details>

---

**dmathieu** — 2025-10-14T07:54:22Z

The intent of the defer is to remove the span from the context, so spans using the same context aren't childs of the created span once the middleware has finished running.

Imaging the following setup:

```golang
r := gin.New()
r.Use(myCustomMiddleware)
r.Use(otelgin.Middleware("my-server"))
	
r.GET("/", func(c *gin.Context) {
	c.HTML(http.StatusOK, "index.tmpl", gin.H{})
})
```

When `myCustomMiddleware` runs, the span has either not started yet, or is already finished.
If it's already finished, the context shouldn't have the span within it, as we're not within the trace anymore.

Right now, if you create a span within `myCustomMiddleware`, after the call to `c.Next()`, it won't be a child of the otelgin span.
After your change it is one.

This is what the defer prevents.
While I agree to fixing this race condition, the defer does have a use and I don't think we can just drop it.

(ideally, we should add a test for this too)

---

**akats7** — 2025-10-14T08:01:45Z

> The intent of the defer is to remove the span from the context, so spans using the same context aren't childs of the created span once the middleware has finished running.
> 
> Imaging the following setup:
> 
> ```go
> r := gin.New()
> r.Use(myCustomMiddleware)
> r.Use(otelgin.Middleware("my-server"))
> 	
> r.GET("/", func(c *gin.Context) {
> 	c.HTML(http.StatusOK, "index.tmpl", gin.H{})
> })
> ```
> 
> When `myCustomMiddleware` runs, the span has either not started yet, or is already finished. If it's already finished, the context shouldn't have the span within it, as we're not within the trace anymore.
> 
> Right now, if you create a span within `myCustomMiddleware`, after the call to `c.Next()`, it won't be a child of the otelgin span. After your change it is one.
> 
> This is what the defer prevents. While I agree to fixing this race condition, the defer does have a use and I don't think we can just drop it.
> 
> (ideally, we should add a test for this too)

Ah that’s a really good observation

---

**nicksherron** — 2025-10-14T08:34:20Z

> The intent of the defer is to remove the span from the context, so spans using the same context aren't childs of the created span once the middleware has finished running.
> 
> Imaging the following setup:
> 
> ```go
> r := gin.New()
> r.Use(myCustomMiddleware)
> r.Use(otelgin.Middleware("my-server"))
> 	
> r.GET("/", func(c *gin.Context) {
> 	c.HTML(http.StatusOK, "index.tmpl", gin.H{})
> })
> ```
> 
> When `myCustomMiddleware` runs, the span has either not started yet, or is already finished. If it's already finished, the context shouldn't have the span within it, as we're not within the trace anymore.
> 
> Right now, if you create a span within `myCustomMiddleware`, after the call to `c.Next()`, it won't be a child of the otelgin span. After your change it is one.
> 
> This is what the defer prevents. While I agree to fixing this race condition, the defer does have a use and I don't think we can just drop it.
> 
> (ideally, we should add a test for this too)

That's a really good theory about what the original code was intending to do and you made a really good point. However, I think there are some fundamental issues with this approach:

1. This is an anti-pattern for context.Context

The defer modifies c.Request.Context() after passing it forward, which violates Go's context conventions. From the https://pkg.go.dev/context:

> "Contexts form a tree... Successive calls to WithValue, WithCancel, WithDeadline, or WithTimeout derive new contexts."


Contexts are meant to flow forward, not be "restored" backward. The library shouldn't enforce this opinion.

2. Most users want otelgin early in the chain

I (and I assume most users) place otelgin as one of the first middleware specifically so child spans can be created from it:

r.Use(otelgin.Middleware("my-service"))  // ← First - creates root span
r.Use(loggingMiddleware)                  // ← Creates child spans
r.Use(authMiddleware)                     // ← Creates child spans
r.GET("/", handler)                       // ← Handler creates child spans

Common use cases that need the parent span:
- Database transactions with tracing
- Inter-service HTTP calls with trace propagation
- Structured logging with trace IDs
- Background jobs that need trace context

Your example breaks all of these - they'd have no parent span.

3. Users can control span isolation themselves 

If a user doesn't want their spans to be children of otelgin's span, they can do exactly what the defer does - but explicitly:
```go
var tracer = otel.Tracer(instrumentationName)

func myCustomMiddleware(c *gin.Context) {
    ctx, span := tracer.Start(c.Request.Context(), "myCustomMiddleware")
    defer span.End()

    c.Next() // runs otelgin and other middleware

    // Explicitly restore context if the user doesn't want child spans and since the user is in control of goroutines the onus is on them to do so safely (as it should be)  
    c.Request = c.Request.WithContext(ctx)
}
```
This gives users control without the library making opinionated (and race-prone) decisions.

Even if we agreed on the semantics, I'm not sure of a safe way of doing it from a library implementation.

Bottom line: The defer enforces an anti-pattern, breaks the common use case (otelgin as root span), prevents valid patterns (goroutines with trace context), and causes data races.
Users who need span isolation can manage it themselves without the library making unsafe assumptions.

What do you think? I'm happy to add documentation showing how users can achieve span isolation if they need it. 


---

**dmathieu** — 2025-10-14T08:42:01Z

I disagree with this being a violation of Go's conventions (in the context of the middleware pattern, we don't flow forward. At the end of a middleware, we go back to its parent).
I also disagree that folks should do this themselves. Especially since this has been the default behavior for many years now (and the same behavior exists for other instrumentations, such as otelecho).

I think this discussion would be better synchronously though. If you're able to, I'd recommend you to join our next SIG meeting (tomorrow at 4pm UTC).
https://github.com/open-telemetry/community/?tab=readme-ov-file#implementation-sigs

---

**nicksherron** — 2025-10-14T08:48:08Z

> I disagree with this being a violation of Go's conventions (in the context of the middleware pattern, we don't flow forward. At the end of a middleware, we go back to its parent). I also disagree that folks should do this themselves. Especially since this has been the default behavior for many years now (and the same behavior exists for other instrumentations, such as otelecho).
> 
> I think this discussion would be better synchronously though. If you're able to, I'd recommend you to join our next SIG meeting (tomorrow at 4pm UTC). https://github.com/open-telemetry/community/?tab=readme-ov-file#implementation-sigs

Ok well one thing is for certain, you all have a much better understanding of the existing patterns and user expectations for this project than I do. It's getting quite late for me so I'll sleep on this and give your points their time to marinate. As far as the SIG meeting goes that's a great idea (and sounds fun too) - unfortunately that's a fairly busy time for me but I'll do my best to make it.

---

**nicksherron** — 2025-10-14T08:59:49Z

> Especially since this has been the default behavior for many years now (and the same behavior exists for other instrumentations, such as otelecho).

This is a strong argument, I didn’t realize that was the case.  I wasn’t looking to add a breaking change and I’m glad you pointed it out. I’ll see what I can do to come up with something that maintains the existing semantics while also fixing the race.

---

**dmathieu** — 2025-10-17T10:41:58Z

We have been discussing this in yesterday's SIG meeting, and have decided this fix is incorrect and the current behavior is the proper one.
See https://github.com/open-telemetry/opentelemetry-go-contrib/issues/4588#issuecomment-3414917592

## Reviews (1)

**akats7** — APPROVED — 2025-10-14T07:52:18Z

## Review Comments (0)

_No inline review comments._

## Timeline

- 2025-10-14T04:05:44Z · **ready_for_review** by nicksherron
- 2025-10-14T04:05:44Z · **review_requested** by nicksherron
- 2025-10-14T04:05:44Z · **review_requested** by nicksherron
- 2025-10-14T04:05:53Z · **review_requested** by github-actions[bot]
- 2025-10-17T10:41:58Z · **closed** by dmathieu
- 2025-11-03T09:18:09Z · **cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/issues/6648

