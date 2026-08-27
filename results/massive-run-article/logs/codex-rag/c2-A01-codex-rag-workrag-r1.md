# Which MultipartForm cleanup approach is being pursued for otelgin (`#5946` / `#6609`), and what is its current implementation status?

<!-- RESPONSE_START -->

The adopted approach is automatic `MultipartForm.RemoveAll()`—superseding the alternatives of reattaching the form or requiring user-managed cleanup.

Implementation is complete locally: conflicts resolved and tests passed. However, the final commits have not been pushed, so issue **#5946** and PR **#6609** are still open and unmerged. (WS-05 work-state records `b4176e256b279eb7`, `305e6a3ed457d989`; updated 2026-03-08)
