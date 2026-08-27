**Source ID**: SRC-SLACK-03

# Slack Thread: REST API Scaffolding and TempFile Policy
**Channel**: #cipherdoc
**Date**: 2026-06-14

---

**[2026-06-14 09:09] Bob**: Starting on the REST API scaffolding. Going with FastAPI for the layer. It's lightweight and the auto-generated OpenAPI docs will save us a ton of time.

**[2026-06-14 09:39] Diana**: +1 for FastAPI. Can we ensure we have request validation schemas for the upload endpoint? We don't want malformed JSON crashing the engine.

**[2026-06-14 09:43] Bob**: Already on it. Using Pydantic for the `RedactionRequest` model. Scaffold is up and running in the `api-scaffold` branch.

**[2026-06-14 10:50] Bob**: Quick update on the file handling. I'm implementing a strict temp-file cleanup policy.

**[2026-06-14 10:56] Diana**: How are we handling cleanup? If a request fails mid-stream, do we leave orphaned files on the container?

**[2026-06-14 11:15] Bob**: No, I'm using a `try...finally` block with a context manager. Files are wiped immediately after the redaction job completes or errors out. No PII should ever persist in `/tmp`.

**[2026-06-14 11:16] Diana**: What about memory-mapped files for larger uploads?

**[2026-06-14 11:33] Bob**: For now, everything is streamed. We might need `mmap` later, but for the MVP, the context manager approach is safer.

**[2026-06-14 11:47] Diana**: I'll start the security audit once you merge the policy. We need to be 100% sure about that cleanup logic.
