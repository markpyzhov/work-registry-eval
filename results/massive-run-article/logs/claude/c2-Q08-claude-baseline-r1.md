# What is the status of `opentelemetry-go-contrib` issue `#7254` (otelhttp error recording under the new semantic conventions)?

<!-- RESPONSE_START -->

I don't have reliable knowledge of that specific issue. I can't recall the contents, title, or state of `open-telemetry/opentelemetry-go-contrib#7254`, and I'm not going to guess at a status (open/closed/merged), assignee, or linked PR — issue numbers in the 7000s for that repo fall in a range where I'd be reconstructing plausible-sounding detail rather than recalling it.

What I can offer is general background that may or may not match the issue:

- `otelhttp` (in `instrumentation/net/http/otelhttp`) went through a semantic-convention migration gated by the `OTEL_SEMCONV_STABILITY_OPT_IN` environment variable (`http/dup`, etc.), moving from the old `http.method`/`http.status_code` style attributes to the stable HTTP conventions (`http.request.method`, `http.response.status_code`, `error.type`, `url.*`, `server.*`).
- Under the stable conventions, error signaling shifted toward the `error.type` attribute on spans and metrics, and span status is set to `Error` for 5xx on the server side and 4xx/5xx on the client side. A recurring class of complaints in that area concerns whether transport-level errors and non-2xx responses get `span.RecordError` called, whether `error.type` is populated consistently between spans and the `http.server.request.duration` metric, and handler panics/`http.ErrAbortHandler` handling.

If you need the actual status, the authoritative check is the issue page itself or `gh issue view 7254 --repo open-telemetry/opentelemetry-go-contrib` — I just can't do that under the no-tools constraint you set.
