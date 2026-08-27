# Which MultipartForm cleanup approach is being pursued for otelgin (`#5946` / `#6609`), and what is its current implementation status?

<!-- RESPONSE_START -->

The adopted approach is automatic `c.Request.MultipartForm.RemoveAll()` in `otelgin`—not reattaching the form and not leaving cleanup to callers. It is intentionally non-configurable for now; an option can be added if users later need it. [WS-05-contrib.md](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md:46)

Implementation is complete locally: conflicts resolved and tests finished. However, the final commits have not been pushed, so GitHub issue [#5946](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/issues/opentelemetry-go-contrib-5946.md:1) and PR [#6609](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-contrib-6609.md:1) remain open and unmerged. The pending action is publication of the completed work. [2026-03.md](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/comments/2026-03.md:18)
