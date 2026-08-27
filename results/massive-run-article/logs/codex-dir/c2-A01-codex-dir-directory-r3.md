# Which MultipartForm cleanup approach is being pursued for otelgin (`#5946` / `#6609`), and what is its current implementation status?

<!-- RESPONSE_START -->

The adopted approach is automatic cleanup: `otelgin` will call `MultipartForm.RemoveAll()`—not reattach the cloned form to the original request and not leave cleanup to users. It is intentionally not configurable unless users later establish a need for that option. [WS-05-contrib.md](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md), [2026-03.md](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/comments/2026-03.md)

Implementation is complete locally: conflicts on PR #6609 were resolved and tests finished. Internally, the cleanup task is treated as done, but the final commits have not been pushed and neither issue #5946 nor PR #6609 has been updated; both remain open/unmerged externally. [WS-05-contrib.md](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md), [2026-03.md](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/comments/2026-03.md)
