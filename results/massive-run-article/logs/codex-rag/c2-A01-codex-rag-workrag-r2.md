# Which MultipartForm cleanup approach is being pursued for otelgin (`#5946` / `#6609`), and what is its current implementation status?

<!-- RESPONSE_START -->

The pursued approach is for `otelgin` to automatically call `MultipartForm.RemoveAll()`—rather than reattaching the form to the original request or leaving cleanup to application users. Those alternatives have been superseded. [WS-05: Contrib Modules, T001 / CMT-2026-03-002]

Implementation is complete locally: conflicts were resolved and tests completed. However, the final commits have not been pushed, so issue `#5946` and PR `#6609` are still open and unmerged on GitHub; the remaining work is publication/update, not implementation. [WS-05: Contrib Modules, Active Work and Done / Evidence]
