# Which MultipartForm cleanup approach is being pursued for otelgin (`#5946` / `#6609`), and what is its current implementation status?

<!-- RESPONSE_START -->

I don't have reliable knowledge of these two issues, and I'm not going to guess at their content.

What I can say honestly:

- **I can't identify `#5946` / `#6609`.** The numbering is consistent with `open-telemetry/opentelemetry-go-contrib` (which is where `otelgin` lives, under `instrumentation/github.com/gin-gonic/gin/otelgin`), and that repo was in the ~5000–7000 issue range across 2024–2025. But I have no specific recall of either issue's title, discussion, or proposed design, and no recall of a "MultipartForm cleanup" workstream in otelgin at all.
- **I can't state an implementation status.** Whether a PR exists, which approach won, or whether anything merged — I'd be fabricating.

For context on why the premise is plausible but I still can't confirm it: `MultipartForm` cleanup in Go is normally handled by `net/http`, which calls `Request.MultipartForm.RemoveAll()` after the handler returns to delete spooled temp files. Instrumentation middleware can interact badly with that if it wraps or retains the `*http.Request` / response writer past the handler's lifetime, or if it buffers the body. That's the general shape a bug like this would take, but I'm describing a category, not the actual issue you're asking about — treat it as background, not an answer.

If you want a real answer, the issues would need to be fetched from GitHub directly, which this task explicitly ruled out.
