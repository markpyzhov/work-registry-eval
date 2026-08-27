# Which MultipartForm cleanup approach is being pursued for otelgin (`#5946` / `#6609`), and what is its current implementation status?

<!-- RESPONSE_START -->

The pursued design is end-of-request cleanup: let the handlers finish, then best-effort call `Request.MultipartForm.RemoveAll()` when a multipart form was parsed. It avoids cleanup while application code may still use uploaded files.

It is not yet a shipped otelgin behavior. `#6609` is the implementation/proposal work for `#5946`; current otelgin does not automatically remove multipart temporary files.
