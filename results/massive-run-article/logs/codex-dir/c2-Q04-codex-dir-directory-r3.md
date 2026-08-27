# What is the status of the otelgin MultipartForm temporary-file cleanup work tracked by `opentelemetry-go-contrib` issue `#5946` and pull request `#6609`?

<!-- RESPONSE_START -->

The cleanup work is complete locally but not yet published.

- The adopted solution is for `otelgin` to call `MultipartForm.RemoveAll()` automatically; reattaching the form or making users responsible was superseded. [WS-05](file:///Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md)  
- Conflict resolution and tests for PR [#6609](file:///Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-contrib-6609.md) were completed locally. Damien Mathieu recorded the task as done internally on 2026-03-08. [CMT-2026-03-002](file:///Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/comments/2026-03.md)  
- The remaining action is publication: the final commits have not been pushed and neither issue [#5946](file:///Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/issues/opentelemetry-go-contrib-5946.md) nor PR #6609 has been updated, merged, or closed on GitHub. Both records remain open. [WS-05](file:///Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md)  

The underlying bug is that `otelgin` replaces the request via `WithContext`; multipart parsing then populates the replacement request instead of the server-held original, so normal request-finalization cleanup misses the temporary files. [#5946](file:///Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/issues/opentelemetry-go-contrib-5946.md)
