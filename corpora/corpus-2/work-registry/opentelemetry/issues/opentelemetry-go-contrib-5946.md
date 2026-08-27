**Source ID**: [SRC-ISSUE-01]

# Issue: Using otelgin.Middleware will cause temporary MultipartForm files not to be destroyed. (open-telemetry/opentelemetry-go-contrib#5946)

**Canonical URL**: https://github.com/open-telemetry/opentelemetry-go-contrib/issues/5946  
**Author**: zacklpx  
**Created**: 2024-07-25T03:50:39Z · **Updated**: 2025-07-03T13:28:05Z  
**Collected**: 2026-07-14T14:35:41Z  
**State**: open  
**Labels**: bug, area: instrumentation, instrumentation: otelgin  
**Milestone**: —

---

## Description

### Description

 Using otelgin.Middleware will cause temporary MultipartForm files not to be destroyed.

### Environment

- OS: MacOS
- Architecture: x86
- Go Version: 1.22
- `otelgin` version: 0.53.0

### Steps To Reproduce

1. Using this code start up gin http server
```
package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"go.opentelemetry.io/contrib/instrumentation/github.com/gin-gonic/gin/otelgin"
)

func main() {
	engine := gin.Default()
	engine.MaxMultipartMemory = 1024 * 1024
	engine.Use(otelgin.Middleware("my-server"))

	engine.POST("/upload", func(c *gin.Context) {
		ff, err := c.FormFile("file")
		if err != nil {
			_ = c.AbortWithError(http.StatusInternalServerError, err)
			return
		}
		_ = ff
		c.JSON(http.StatusOK, map[string]interface{}{"c": 0})
	})

	engine.Run(":8624")
}
```
2. Upload a file to the http api
```
curl --request POST \
  --url http://127.0.0.1:8624/upload \
  --header 'Content-Type: multipart/form-data' \
  --header 'User-Agent: insomnia/9.3.2' \
  --form 'file=@xxx.mp4'
```

### Expected behavior

Upload a file larger than MaxMultipartMemory, and the HTTP server will generate multipart-xxxx temporary files in the system temporary directory. These files will be automatically destroyed when the request ends. However, if the otelgin.Middleware is used, the temporary files will not be destroyed.  

the HTTP server holds the original request, and using otelgin.Middleware replaces the request with [c.request = c.request.WithContext(ctx)](https://github.com/open-telemetry/opentelemetry-go-contrib/blob/cb45b36c145ff13e4ba76fd9e02ef39297c906b5/instrumentation/github.com/gin-gonic/gin/otelgin/gintrace.go#L79), causing subsequent c.FormFile reads to fall on the new request. As a result, the original request held by the HTTP server does not have the MultipartForm, preventing it from being destroyed.


## Discussion (11)

**Yiling-J** — 2025-01-11T11:28:03Z

@akats7 Is there any plan to address this issue? For reference, a similar problem was resolved in Echo with this fix: [Echo-contrib PR #90](https://github.com/labstack/echo-contrib/pull/90/files#diff-86bf6c8ade26d5c58be942ac6765d89c8855c8713ba9a4d61249e16e3fa9c0fc).  If you're busy, I'd be happy to help by creating a PR to address it. Let me know!  


---

**dmathieu** — 2025-01-12T13:54:25Z

cc @akats7 as code owner.

---

**akats7** — 2025-01-13T02:11:01Z

Hi @Yiling-J,

Feel free to open a PR, I'll gladly review

---

**flc1125** — 2025-07-02T08:35:01Z

> Regarding this issue, my proposal is to adopt the following approach. If you have any better suggestions, please let me know:
> 
> We only need to replace this section with the content below:
> 
> - Before:
> 
> https://github.com/open-telemetry/opentelemetry-go-contrib/blob/46effa2b8f0be4ead4f4f3c2bd1cc8bf8ec32253/instrumentation/github.com/gin-gonic/gin/otelgin/gin.go#L82-L86 
> 
> - After:
> 
> ```go
> ctx := cfg.Propagators.Extract(c.Request.Context(), propagation.HeaderCarrier(c.Request.Header))
> c.Request.WithContext(ctx)
> ```

There still seems to be a problem, please ignore~😂

---

**akats7** — 2025-07-02T08:58:39Z

> Regarding this issue, my proposal is to adopt the following approach. If you have any better suggestions, please let me know:
> 
> We only need to replace this section with the content below:
> 
> * Before:
> 
> [opentelemetry-go-contrib/instrumentation/github.com/gin-gonic/gin/otelgin/gin.go](https://github.com/open-telemetry/opentelemetry-go-contrib/blob/46effa2b8f0be4ead4f4f3c2bd1cc8bf8ec32253/instrumentation/github.com/gin-gonic/gin/otelgin/gin.go#L82-L86)
> 
> Lines 82 to 86 in [46effa2](/open-telemetry/opentelemetry-go-contrib/commit/46effa2b8f0be4ead4f4f3c2bd1cc8bf8ec32253)
> 
>  savedCtx := c.Request.Context() 
>  defer func() { 
>  	c.Request = c.Request.WithContext(savedCtx) 
>  }() 
>  ctx := cfg.Propagators.Extract(savedCtx, propagation.HeaderCarrier(c.Request.Header)) 
> * After:
> 
> ctx := cfg.Propagators.Extract(c.Request.Context(), propagation.HeaderCarrier(c.Request.Header))
> c.Request.WithContext(ctx)
> PS: After adjusting according to this plan, I have already tested it locally and can solve this problem.

I don’t believe this will work, c.Request.WithContext will return a new request with the updated context, it won’t update the existing request.

---

**zihuyishi** — 2025-07-02T09:37:44Z

I think we should manual remove it. Who create new request should cleanup.
```golang
		defer func() {
			if c.Request.MultipartForm != nil {
				c.Request.MultipartForm.RemoveAll()
			}
		}()
```

---

**akats7** — 2025-07-02T09:40:40Z

> I think we should manual remove it. Who create new request should cleanup.
> 
> 		defer func() {
> 			if c.Request.MultipartForm != nil {
> 				c.Request.MultipartForm.RemoveAll()
> 			}
> 		}()

I’m fine with this, I think this is just the path of least resistance. Then we’d also have to explicitly parse the form in the middleware it seems.

---

**flc1125** — 2025-07-02T10:01:01Z

> I’m fine with this, I think this is just the path of least resistance. Then we’d also have to explicitly parse the form in the middleware it seems.

Yes, this solution is feasible. I'm just trying to understand why this issue occurs at the underlying level.

In addition, it is necessary to evaluate whether increasing it will have any impact when wrapping this middleware with an outer layer.

---

**akats7** — 2025-07-02T10:06:33Z

> > I’m fine with this, I think this is just the path of least resistance. Then we’d also have to explicitly parse the form in the middleware it seems.
> 
> Yes, this solution is feasible. I'm just trying to understand why this issue occurs at the underlying level.
> 
> In addition, it is necessary to evaluate whether increasing it will have any impact when wrapping this middleware with an outer layer.

I think the cause of the issue is when we replace the request we stop the form from being fully initialised on the original request, so at the end of the (original) request lifecycle, there’s nothing for the server to cleanup.

---

**flc1125** — 2025-07-02T15:23:47Z

I don't think this issue exists only in the Gin framework, but rather in all `http.Server` implementations.

The following is a simplified version of the experimental results:

```go
func TestHTTPRequest(t *testing.T) {
	req := &http.Request{}

	req2 := req.WithContext(context.WithValue(req.Context(), "key", "value"))

	// When using gin.Context to execute c.FormFile("file"), its underlying effect is similar to the following, performing assignment.
	// Actually executes c.Request.ParseMultipartForm(...)
	req2.MultipartForm = &multipart.Form{
		Value: map[string][]string{
			"key1": {"value1"},
		},
		File: map[string][]*multipart.FileHeader{
			"file1": {
				{
					Filename: "file1.txt",
				},
			},
		},
	}

	// Then, at the end of the request, it performs cleanup operations at the underlying level.
	// However, at this point, req.MultipartForm is nil, so the following does not actually execute.
	if req.MultipartForm != nil {
		// Pseudocode, the actual execution is: req.MultipartForm.RemoveAll()
		delete(req.MultipartForm.File, "file1")
	}

	// Therefore, the MultipartForm in the real req2 does not actually have a RemoveAll method.
	spew.Dump(req.MultipartForm, req2.MultipartForm)
}
```

output:

```
=== RUN   TestHTTPRequest
(*multipart.Form)(<nil>)
(*multipart.Form)(0x14000192ef0)({
 Value: (map[string][]string) (len=1) {
  (string) (len=4) "key1": ([]string) (len=1 cap=1) {
   (string) (len=6) "value1"
  }
 },
 File: (map[string][]*multipart.FileHeader) (len=1) {
  (string) (len=5) "file1": ([]*multipart.FileHeader) (len=1 cap=1) {
   (*multipart.FileHeader)(0x14000216d80)({
    Filename: (string) (len=9) "file1.txt",
    Header: (textproto.MIMEHeader) <nil>,
    Size: (int64) 0,
    content: ([]uint8) <nil>,
    tmpfile: (string) "",
    tmpoff: (int64) 0,
    tmpshared: (bool) false
   })
  }
 }
})
--- PASS: TestHTTPRequest (0.00s)
PASS
```

In the comments, there is an explanation of why the file was not cleaned up. It might be related to [this](https://github.com/golang/go/blob/b3251514531123d7fd007682389bce7428d159a0/src/net/http/h2_bundle.go#L6366-L6368).

**The conclusion of the experiment is: As long as we perform the following operations, this issue will definitely occur:**

```go
c.Request = c.Request.WithContext(
	context.WithValue(c.Request.Context(), "foo", "bar"),
)
```

-----

Attach an example that is detached from any framework, implemented solely using the underlying `http.Server`.

```go
package gin

import (
	"context"
	"fmt"
	"net/http"
	"testing"

	"github.com/fsnotify/fsnotify"
	"github.com/stretchr/testify/require"
)

func TestHTTP(t *testing.T) {
	watcher, err := fsnotify.NewWatcher()
	require.NoError(t, err)
	defer watcher.Close()

	tempDir := t.TempDir()
	t.Setenv("TMPDIR", tempDir)
	t.Logf("Temporary directory created: %s", tempDir)

	go func() {
		for {
			select {
			case event, ok := <-watcher.Events:
				if !ok {
					return
				}
				if event.Op&fsnotify.Create == fsnotify.Create {
					t.Logf("File created: %s", event.Name)
				}
				if event.Op&fsnotify.Write == fsnotify.Write {
					t.Logf("File modified: %s", event.Name)
				}
				if event.Op&fsnotify.Remove == fsnotify.Remove {
					t.Logf("File removed: %s", event.Name)
				}
			case err, ok := <-watcher.Errors:
				if !ok {
					return
				}
				t.Logf("Error: %s", err)
			}
		}
	}()

	require.NoError(t, watcher.Add(tempDir))

	srv := http.NewServeMux()
	srv.HandleFunc("/upload", func(w http.ResponseWriter, r *http.Request) {
		r = r.WithContext(context.WithValue(r.Context(), "foo", "bar"))

		if r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		err := r.ParseMultipartForm(1)
		if err != nil {
			http.Error(w, fmt.Sprintf("Error parsing form: %s", err.Error()), http.StatusBadRequest)
			return
		}

		file, _, err := r.FormFile("file")
		if err != nil {
			http.Error(w, fmt.Sprintf("Error retrieving file: %s", err.Error()), http.StatusBadRequest)
			return
		}
		defer file.Close()

		w.WriteHeader(http.StatusOK)
		w.Write([]byte("File uploaded successfully"))
	})

	server := &http.Server{
		Addr:    ":9999",
		Handler: srv,
	}

	server.ListenAndServe()
}
```

Initiate request:

```shell
curl --location 'http://localhost:9999/upload' \
--form 'file=@"/example/file.jpg"'
```

output:

```
RUN   TestHTTP
    gin_test.go:128: Temporary directory created: /var/folders/9q/lfpvvb251dv7bj4tqlq8bgpm0000gn/T/TestHTTP1269004834/001
    gin_test.go:138: File created: /var/folders/9q/lfpvvb251dv7bj4tqlq8bgpm0000gn/T/TestHTTP1269004834/001/multipart-2265161000
    gin_test.go:141: File modified: /var/folders/9q/lfpvvb251dv7bj4tqlq8bgpm0000gn/T/TestHTTP1269004834/001/multipart-2265161000
    gin_test.go:141: File modified: /var/folders/9q/lfpvvb251dv7bj4tqlq8bgpm0000gn/T/TestHTTP1269004834/001/multipart-2265161000
```

We did not see any record of "removed" here. To solve this problem, we only need to execute `r.MultipartForm.RemoveAll()`.

```go
err := r.ParseMultipartForm(1)
if err != nil {
	http.Error(w, fmt.Sprintf("Error parsing form: %s", err.Error()), http.StatusBadRequest)
	return
}
defer r.MultipartForm.RemoveAll() // <---- Add new code

file, _, err := r.FormFile("file")
```

output:

```
=== RUN   TestHTTP
    gin2_test.go:20: Temporary directory created: /var/folders/9q/lfpvvb251dv7bj4tqlq8bgpm0000gn/T/TestHTTP124433030/001
    gin2_test.go:30: File created: /var/folders/9q/lfpvvb251dv7bj4tqlq8bgpm0000gn/T/TestHTTP124433030/001/multipart-643567324
    gin2_test.go:33: File modified: /var/folders/9q/lfpvvb251dv7bj4tqlq8bgpm0000gn/T/TestHTTP124433030/001/multipart-643567324
    gin2_test.go:33: File modified: /var/folders/9q/lfpvvb251dv7bj4tqlq8bgpm0000gn/T/TestHTTP124433030/001/multipart-643567324
    gin2_test.go:33: File modified: /var/folders/9q/lfpvvb251dv7bj4tqlq8bgpm0000gn/T/TestHTTP124433030/001/multipart-643567324
    gin2_test.go:33: File modified: /var/folders/9q/lfpvvb251dv7bj4tqlq8bgpm0000gn/T/TestHTTP124433030/001/multipart-643567324
    gin2_test.go:36: File removed: /var/folders/9q/lfpvvb251dv7bj4tqlq8bgpm0000gn/T/TestHTTP124433030/001/multipart-643567324
```

----

Currently, I cannot determine whether this is a flaw in Go itself or if users are required to manually execute `RemoveAll()`. I have tried submitting [this issue](https://github.com/golang/go/issues/74455) to the official Go team to see if there will be any updates.

The following situations exist (tested and confirmed):

1. We executed `request.WithContext()` before executing `request.ParseMultipartForm`, but did not manually call `RemoveAll` on the new Request—it will be unable to delete the files;
2. We executed `request.WithContext()` before executing `request.ParseMultipartForm`, and manually called `RemoveAll` on the new Request—it will delete the files;
3. We executed `request.WithContext()` after executing `request.ParseMultipartForm,` and did not manually call `RemoveAll` on the new Request—it will delete the files.

---

**flc1125** — 2025-07-03T13:24:52Z

Given that this [issue](https://github.com/open-telemetry/opentelemetry-go-contrib/issues/5946#issuecomment-3028290240) currently lacks an official solution from the [Go team](https://github.com/golang/go/issues/74455), we need to find an appropriate workaround ourselves.

My suggestion is to proceed with the solution proposed in this [PR](https://github.com/open-telemetry/opentelemetry-go-contrib/pull/6609) (also the consistent approach suggested by @zihuyishi and @akats7).  

However, this approach will also introduce additional side effects, for which there is currently no better solution.  

**Impact:**  

Assuming our middleware is wrapped in the following manner: `m1(m2(otel-middleware(m3(fn))))`,  

where `m1` and `m2` internally implement operations such as `request.ParseMultipartForm(1)`. Due to the effect of `RemoveAll` in `otel-middleware`,  

there may be cases where they repeatedly create `request.MultipartForm` resources, resulting in additional memory allocations.

Of course, we can also choose not to handle it, but we need to remind users to process `c.Request.MultipartForm.RemoveAll()`.

----

I'd like to hear your opinions: @akats7 @open-telemetry/go-approvers 



## Timeline

- 2024-07-25T03:50:39Z · **labeled** by zacklpx `area: instrumentation`
- 2024-07-25T03:50:39Z · **labeled** by zacklpx `bug`
- 2024-07-25T03:50:39Z · **labeled** by zacklpx `instrumentation: otelgin`
- 2024-11-21T12:21:58Z · **cross-referenced** by flc1125 ← https://github.com/open-telemetry/opentelemetry-go-contrib/issues/4588
- 2025-01-13T13:45:45Z · **cross-referenced** by Yiling-J ← https://github.com/open-telemetry/opentelemetry-go-contrib/pull/6609
- 2025-07-02T08:06:05Z · **marked_as_duplicate** by dmathieu
- 2025-07-02T08:06:06Z · **cross-referenced** by dmathieu ← https://github.com/open-telemetry/opentelemetry-go-contrib/issues/7541
- 2025-07-02T15:30:57Z · **cross-referenced** by flc1125 ← https://github.com/golang/go/issues/74455
- 2025-11-03T09:18:09Z · **cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/issues/6648
- 2026-01-16T17:41:03Z · **cross-referenced** by MrAlias ← https://github.com/open-telemetry/opentelemetry-go-contrib/issues/8419
- 2026-04-21T06:02:25Z · **cross-referenced** by SAY-5 ← https://github.com/open-telemetry/opentelemetry-go-contrib/pull/8851
- 2026-05-31T02:40:32Z · **referenced** by SAY-5

