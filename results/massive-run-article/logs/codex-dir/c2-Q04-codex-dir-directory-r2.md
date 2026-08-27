# What is the status of the otelgin MultipartForm temporary-file cleanup work tracked by `opentelemetry-go-contrib` issue `#5946` and pull request `#6609`?

<!-- RESPONSE_START -->

Status: internally complete, externally pending publication.

- The adopted fix is for `otelgin` to call `MultipartForm.RemoveAll()` automatically. Conflict resolution and tests for PR #6609 are complete locally. [WS-05](file:///Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md)
- Damien Mathieu recorded that the final commits have not been pushed and neither GitHub record has been updated; therefore issue #5946 and PR #6609 remain open and unmerged. Publishing #6609 and updating the issue are the outstanding actions. [2026-03 correction](file:///Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/comments/2026-03.md)
- The defect is caused by `otelgin` replacing the request with a context-bearing clone before multipart parsing; the form then lives on the new request, while the server cleans up the original request. [Issue #5946](file:///Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/issues/opentelemetry-go-contrib-5946.md)
- Earlier alternatives—reattaching the form, leaving cleanup to users, or adding configuration—were superseded by automatic deletion, with configuration deferred unless users show a need. [PR #6609](file:///Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-contrib-6609.md)
