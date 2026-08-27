# Which MultipartForm cleanup approach is being pursued for otelgin (`#5946` / `#6609`), and what is its current implementation status?

<!-- RESPONSE_START -->

The adopted approach is to have otelgin automatically call `MultipartForm.RemoveAll()`. This supersedes both reattaching the form to the original request and leaving cleanup to users.

Implementation is complete locally: conflicts were resolved and tests passed. It is treated as done internally, but the final commits have not been pushed, so `#5946` and PR `#6609` remain open/unmerged; publication is the outstanding step. (Work State `WS-05`, last updated 2026-03-08; records `b4176e256b279eb7`, `e327f56400e3daee`, `305e6a3ed457d989`)
